
# Python
import unittest, subprocess, threading, platform
import os, time, socket, sys, re, signal

# RPDB2
import rpdb2

# Compatibility support
IS_PYTHON_LESS_THAN_26 = sys.version_info[:2] < (2,6)
if IS_PYTHON_LESS_THAN_26:
    from StringIO import StringIO
else:
    from io import StringIO

if sys.platform != 'win32' or sys.version_info[:2] < (2,7) or ((3,0) <= sys.version_info[:2] <= (3,1)):
    CREATE_NEW_PROCESS_GROUP=0x200
else:
    CREATE_NEW_PROCESS_GROUP=subprocess.CREATE_NEW_PROCESS_GROUP

if sys.version_info[:2] < (3,0):
    def u(s): return unicode(s)
else:
    def u(s): return s

HAS_PSKILL=False
try:
    subprocess.call('pskill')
    HAS_PSKILL=True
except OSError:
    pass

PYTHON='C:/Python27/python.exe'
DEBUGME=u('debugme.py')
RPDB2 = 'rpdb2.py'
PWD=u('toto')

STEPS = [ 'start', 'f1', 'f2', 'f3', 'done' ]
LINE_IN_F2=16

class FakeStdin:
    def __init__(self):
        self.please_stop = False
        self.lines = []
        self.dispStdin = True

    def appendCmd( self, l ):
        cmd = l if (l[-1] == '\n') else (l + '\n')
        self.lines.append( cmd )

    def readline(self):
        while not self.please_stop:
           if len(self.lines):
                p = self.lines.pop(0)
                if self.dispStdin:
                    sys.stdout.write( 'stdin: %s\n' % p[:-1] )
                return p
        time.sleep(0.1)

def dbg( t ):
    print( '>>>>>> %s <<<<<<' % t )

class Rpdb2Stdout(StringIO):
    def __init__(self, *args):
        StringIO.__init__(self, *args)
        self.attached = False

    reAttached = re.compile(r'\*\*\* Successfully attached to.*')
    reDetached = re.compile(r'\*\*\* Detached from script.*' )

    def write(self,t):
        if self.reAttached.match( t ):
            self.attached = True
        elif self.reDetached.match(t):
            self.attached = False

        sys.stdout.write( '%s' % t )


class TestRpdb2Stdout( unittest.TestCase ):
    def testReAttached( self ):
        self.assertNotEqual( Rpdb2Stdout.reAttached.match( '*** Successfully attached to\n' ), None )

class TestRpdb2( unittest.TestCase ):

    def setUp(self):
        self.cleanBpFiles()
        self.cleanStepFiles()
        self.console = None
        self.sm = None
        self.fakeStdin = FakeStdin()
        self.rpdb2Stdout = Rpdb2Stdout()
        self.script = subprocess.Popen( [ PYTHON, RPDB2, '-d', '--pwd=%s' % PWD, os.path.join( 'tests', DEBUGME ) ], 
                        creationflags=CREATE_NEW_PROCESS_GROUP, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )

    def cleanStepFiles(self):
        for fname in STEPS:
            if os.path.exists( fname ):
                os.unlink( fname )

    def cleanBpFiles(self):
        bpldir = os.path.dirname( rpdb2.calc_bpl_filename( '' ) )
        for fname in os.listdir( bpldir ):
            os.unlink( os.path.join( bpldir, fname ) )

    def terminateScript( self ):
        dbg( 'Teardown.Script: check if finished')
        if self.script.poll() != None: return

        dbg( 'Teardown.Script: check if finished after 1 sec')
        time.sleep(1.0)
        if self.script.poll() != None: return

        if not IS_PYTHON_LESS_THAN_26:
            dbg( 'Teardown.Script: terminate()')
            self.script.terminate()
            if self.script.poll() != None: return
            time.sleep(1.0)
            if self.script.poll() != None: return

            dbg( 'Teardown.Script: kill()')
            self.script.kill()
            if self.script.poll() != None: return
            time.sleep(1.0)
            if self.script.poll() != None: return
        elif sys.platform == 'win32':
            # windows, Python < 2.6
            dbg( 'Teardown.Script: pskill')
            subprocess.call( ['pskill', '%s' % self.script.pid] )
            if self.script.poll() != None: return
            time.sleep(1.0)
            if self.script.poll() != None: return

        else:
            # unix, Python < 2.6
            dbg( 'Teardown.Script: SIGTERM')
            os.kill( self.script.pid, signal.SIGTERM )
            if self.script.poll() != None: return
            time.sleep(1.0)
            if self.script.poll() != None: return

            dbg( 'Teardown.Script: SIGKILL')
            os.kill( self.script.pid, signal.SIGKILL )
            if self.script.poll() != None: return
            time.sleep(1.0)
            if self.script.poll() != None: return

        raise OSError( 'Error, can not terminate or kill a python process. Process is still running  with pid: %d' % self.script.pid )

    def tearDown(self):
        dbg( 'Teardown' )
        self.cleanStepFiles()
        if self.console:
            if self.rpdb2Stdout.attached:
                dbg( 'Teardown: Stopping...' )
                self.fakeStdin.appendCmd('stop\n')
                time.sleep(1.0)

                #dbg( 'Teardown: Detaching...' )
                #self.fakeStdin.appendCmd('detach\n')
                #time.sleep(1.0)

            dbg( 'Teardown: Exiting...' )
            self.fakeStdin.appendCmd('exit\n')
            time.sleep(1.0)

            # dbg( 'console exit ok' )
            self.console.join( 1.0 )
            # dbg( 'console join ok' )
            self.sm.shutdown()
            # dbg( 'sm shutdown ok' )
            time.sleep(1.0)
            dbg( 'Teardown: Console and SM done' )

        self.terminateScript()


    #############[ debugger control ]##################

    def startPdb2(self):
        dbg('Start pdb2')
        self.sm = rpdb2.CSessionManager(PWD,True,False,'localhost')
        self.console = rpdb2.CConsoleInternal(self.sm, stdout=self.rpdb2Stdout, stdin=self.fakeStdin, fSplit=True )
        self.console.start()
        time.sleep(1.0)


    def attach( self ):
        self.fakeStdin.appendCmd( "attach %s\n" % DEBUGME )
        startCountDown = time.time()
        while time.time() - startCountDown < 10.0:
            time.sleep(1.0)
            if self.rpdb2Stdout.attached: 
                break
        self.assertEqual( self.rpdb2Stdout.attached, True )

    def go( self ):
        self.fakeStdin.appendCmd( "go" )
        time.sleep(1.0)

    def breakp( self, arg ):
        self.fakeStdin.appendCmd( "bp %s" % arg)

    def failIfCanNotKillTheProcess( self ):
        if sys.platform == 'win32' and IS_PYTHON_LESS_THAN_26 and not HAS_PSKILL:
            self.fail("On Python 2.4 and 2.5 on Windows this work only if you have pstools installed: http://technet.microsoft.com/fr-fr/sysinternals/bb896649.aspx" )

    #############[ tests ]##################

    def testGo( self ):
        self.failIfCanNotKillTheProcess()
        self.startPdb2()
        self.attach()
        self.go()

        assert os.path.exists( 'f1' )
        assert os.path.exists( 'done' )

    def testBp( self ):
        self.failIfCanNotKillTheProcess()
        self.startPdb2()
        self.attach()
        self.breakp( 'f1' )
        self.breakp( LINE_IN_F2 )
        self.go() # break during definition of f1
        self.go() # break during call of f1
        assert os.path.exists( 'start' )
        assert not os.path.exists( 'f1' )
        self.go() # break after call of f2
        assert os.path.exists( 'f1' )
        assert os.path.exists( 'f2' )
        self.go() # run until the end
        assert os.path.exists('done')



if __name__ == '__main__':
    unittest.main()
