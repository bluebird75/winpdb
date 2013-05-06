
import unittest, subprocess, io, threading
import os, time, socket, sys, re

import rpdb2

PYTHON='C:/Python27/python.exe'
DEBUGME=u'debugme.py'
RPDB2 = 'rpdb2.py'
PWD=u'toto'

class MyStdin:
    def __init__(self):
        self.please_stop = False
        self.lines = []

    def readline(self):
        while not self.please_stop:
           if len(self.lines):
            p = self.lines.pop(0)
            print 'stdin:', p
            return p
        time.sleep(0.1)

def dbg( t ):
    print '>>>>>>', t, '<<<<<<'

class CopyStdout(io.StringIO):
    def __init__(self, *args):
        io.StringIO.__init__(self, *args)
        self.attached = False

    reAttached = re.compile(r'\*\*\* Successfully attached to.*')
    reDetached = re.compile(r'\*\*\* Detached from script.*' )

    def write(self,t):
        if self.reAttached.match( t ):
            self.attached = True
        elif self.reDetached.match(t):
            self.attached = False

        sys.stdout.write( '%s' % t )


class TestCopyStdout( unittest.TestCase ):
    def testReAttached( self ):
        self.assertNotEquals( CopyStdout.reAttached.match( '*** Successfully attached to\n' ), None )


class TestRpdb2( unittest.TestCase ):

    def setUp(self):
        self.console = None
        self.sm = None
        self.myStdin = MyStdin()
        self.script = subprocess.Popen( [ PYTHON, RPDB2, '-d', '--pwd=%s' % PWD, os.path.join( 'tests', DEBUGME ) ], 
                        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP ) # stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
        # script.wait()
        # scriptStdout = script.stdout.read()
        # print scriptStdout

    def tearDown(self):

        dbg( 'Teardown' )
        if self.console:
            dbg( 'Running script until the end' )
            self.myStdin.lines.append('go\n')
            time.sleep(1.0)
            dbg( 'Detaching...' )
            self.myStdin.lines.append('detach\n')
            time.sleep(1.0)
            dbg( 'Exiting...' )
            self.myStdin.lines.append('exit\n')
            time.sleep(1.0)
            dbg( 'console exit ok' )
            self.console.join( 1.0 )
            dbg( 'console join ok' )
            self.sm.shutdown()
            dbg( 'sm shutdown ok' )
            time.sleep(1.0)
            dbg( 'console done' )


        print 'tearDown: attempt1'
        if self.script.poll() != None: return

        time.sleep(1.0)
        print 'tearDown: attempt2'
        if self.script.poll() != None: return

        print 'tearDown: attempt3'
        self.script.terminate()
        if self.script.poll() != None: return

        # script not terminated yet
        time.sleep(1.0)
        print 'tearDown: attempt4'
        if self.script.poll() != None: return

        self.script.kill()
        print 'tearDown: attempt5'
        if self.script.poll() != None: return

        time.sleep(1.0)
        print 'tearDown: attempt6'
        if self.script.poll() != None: return

        raise ValueError( 'Error, script not terminated: pid=%d' % self.script.pid )


    def testGo( self ):
        fAttach=True
        fchdir=False,
        _rpdb2_pwd=PWD
        fAllowUnencrypted=True
        fAllowRemote=False
        host='localhost'
        command_line=DEBUGME
        fSplit=True

        copyStdout = CopyStdout()

        self.sm = rpdb2.CSessionManager(_rpdb2_pwd, fAllowUnencrypted, fAllowRemote, host)
        self.console = rpdb2.CConsoleInternal(self.sm, stdout=copyStdout, stdin=self.myStdin, fSplit=fSplit )
        self.console.start()

        time.sleep(1.0)

        self.myStdin.lines.append( "attach %s\n" % DEBUGME )
        startCountDown = time.time()
        while time.time() - startCountDown < 10.0:
            time.sleep(1.0)
            if copyStdout.attached: 
                break
        self.assertEquals( copyStdout.attached, True )


if __name__ == '__main__':
    unittest.main()
