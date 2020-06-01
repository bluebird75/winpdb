#! /usr/bin/env python

"""
    Functional tests for rpdb2

    Copyright (C) 2013-2017 Philippe Fremy

    This program is free software; you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation; either version 2 of the License, or any later
    version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02111-1307 USA
"""


# Python
import unittest, subprocess, threading
import os, time, sys, re, signal

# RPDB2
import rpdb2
import src.const

src.const.STARTUP_TIMEOUT = 10.0 # necessary because sometimes subprocess debugger is really slow to start

# Compatibility support
IS_PYTHON_LESS_THAN_26 = sys.version_info[:2] < (2,6)
if IS_PYTHON_LESS_THAN_26:
    from StringIO import StringIO
else:
    from io import StringIO

DEBUGLEVEL='DEBUG'
def dbg( t ):
    if DEBUGLEVEL != 'INFO':
        print( '>>>>>> %s <<<<<<' % t )

if sys.platform != 'win32' or sys.version_info[:2] < (2,7) or ((3,0) <= sys.version_info[:2] <= (3,1)):
    CREATE_NEW_PROCESS_GROUP=0x200
else:
    CREATE_NEW_PROCESS_GROUP=subprocess.CREATE_NEW_PROCESS_GROUP

HAS_PSKILL=False
if sys.platform == 'win32':
    try:
        rpdb2.FindFile('pskill.exe')
        HAS_PSKILL=True
    except IOError:
        pass

PYTHON=sys.executable
DEBUGME=rpdb2.as_unicode('debugme.py')
RPDB2 = 'rpdb2.py'
PWD=rpdb2.as_unicode('toto')

STEPS = [ 'tests/%s' % f for f in ('start', 'f1', 'f2', 'f3', 'done') ]

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

class ReNonMatcher:
    '''Class that behaves like a non-matching RegExp:
    - it returns None if the re matches
    - it returns True if the re does not match.
    '''
    def __init__( self, re ):
        self.re = re

    def match( self, t ):
        ret = self.re.match( t )
        if ret:
            return None
        return True

class Rpdb2Stdout(StringIO):
    reAttached = re.compile(r'\*\*\* Successfully attached to.*')
    reDetached = re.compile(r'\*\*\* Detached from script.*' )
    reBreakonexitOn  = re.compile( r'.*break-on-exit mode.*True.*' )
    reBreakonexitOff = re.compile( r'.*break-on-exit mode.*False.*' )
    reWaitingOnBp    = re.compile( r'\*\*\* Debuggee is waiting at break point.*' )
    reNotWaitingOnBp = ReNonMatcher( re.compile( r'\*\*\* Debuggee is waiting at break point.*' ) )
    reNotRunning = re.compile( r'\*\*\* Debuggee has terminated.*' )

    def __init__(self, *args, **kwargs):
        if 'dispStdout' in kwargs:
            self.dispStdout = kwargs['dispStdout']
            del kwargs['dispStdout']
        else:
            self.dispStdout = True
        StringIO.__init__(self, *args, **kwargs)

        self.matcher = (
            ( self.reAttached,      'attached',     True ),
            # ( self.reAttached,      'running',      True ),
            # ( self.reNotRunning,    'running',      False),
            ( self.reDetached,      'attached',     False),
            ( self.reBreakonexitOn, 'breakonexit',  True ),
            ( self.reBreakonexitOff,'breakonexit',  False),
            ( self.reWaitingOnBp,   'waitingOnBp',  True ),
            ( self.reNotWaitingOnBp,'waitingOnBp',  False),
        )

        for m in self.matcher:
            setattr( self, m[1], False )

        self.lineCount = 0

    def write(self,t):
        if len(t) == 0 or (len(t) == 1 and t == "\n"):
            return

        for retomatch, attr, assignment in self.matcher:
            if retomatch.match( t ):
                dbg('Auto-setting %s to %s' % (attr, assignment) )
                setattr( self, attr, assignment )

        dbg('stdout %d="%s"' % (self.lineCount, t) )
        if self.dispStdout:
            sys.stdout.write( 'RPDB2: %s' % t )

        self.lineCount += 1


class TestRpdb2Stdout( unittest.TestCase ):
    def testReAttached( self ):
        self.assertNotEqual( Rpdb2Stdout.reAttached.match( '*** Successfully attached to\n' ), None )

    def testreWaitingOnBp( self ):
        self.assertTrue( Rpdb2Stdout.reWaitingOnBp.match('*** Debuggee is waiting at break point for further commands.') != None )
        self.assertTrue( Rpdb2Stdout.reNotWaitingOnBp.match('*** Debuggee is waiting at break point for further commands.') == None )

        self.assertTrue( Rpdb2Stdout.reWaitingOnBp.match('*** Totoro .') == None )
        self.assertTrue( Rpdb2Stdout.reNotWaitingOnBp.match('*** Totoro .') != None )

def findBpHint( fname ):
    content = open(fname).readlines()
    return _findBpHintWithContent( content )

reBpHint = re.compile( '# (BP\w+)' )

def _findBpHintWithContent( content ):
    d = {}
    i = 0
    for l in content:
        i += 1
        mo = reBpHint.search( l )
        if mo:
            d[ mo.group(1) ] = i
    return d

class StdoutDisplayer:
    def __init__(self, process ):
        self.process = process
        self.t = threading.Thread( target=self.displayStdout )
        self.shouldStop = False
        self.t.start()

    def stop( self ):
        self.shouldStop = True

    def displayStdout( self ):
        # Wait until stdout exists
        while self.process.stdout == None and self.shouldStop == False:
            print( 'OUT: ... waiting for process to start ...' )
            time.sleep(1.1)

        while True: # not self.shouldStop:
            l = self.process.stdout.readline()
            if not l:
                break
            if l[-1] == '\n':
                l = l[:-1]
            print( 'OUT: %s' % l )

class TestRpdb2( unittest.TestCase ):

    def __init__(self, *args, **kwargs):
        super( TestRpdb2, self ).__init__(*args, **kwargs)
        rpdb2.create_rpdb_settings_folder()
        self.bp1Line = findBpHint( 'tests/debugme.py' )['BP1']
        self.rpdb2Args = []

    def setUp(self):
        self.cleanBpFiles()
        self.cleanStepFiles()
        self.console = None
        self.sm = None
        self.fakeStdin = FakeStdin()
        self.rpdb2Stdout = Rpdb2Stdout( dispStdout=True )
        kwargs = {}
        pythonCmdLine = [ PYTHON, '-u', RPDB2, '-d'] + self.rpdb2Args
        rid = rpdb2.generate_rid()
        rpdb2.create_pwd_file( rid, PWD )
        if sys.platform == 'win32':
            kwargs['creationflags'] = CREATE_NEW_PROCESS_GROUP
            pythonCmdLine.append( '--pwd=%s' % PWD )
        else:
            pythonCmdLine.append( '--rid=%s' % rid )
        # pythonCmdLine.append ( '--debug' )
        pythonCmdLine.append( os.path.join( 'tests', DEBUGME ) ) 
        self.script = subprocess.Popen( pythonCmdLine, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **kwargs )
        self.stdoutDisp = StdoutDisplayer( self.script )

    def cleanStepFiles(self):
        for fname in STEPS:
            if os.path.exists( fname ):
                os.unlink( fname )

    def cleanBpFiles(self):
        bpldir = os.path.dirname( rpdb2.calc_bpl_filename( '' ) )
        try:
            files = os.listdir( bpldir )
        except OSError:
            return

        for fname in files:
            os.unlink( os.path.join( bpldir, fname ) )

    def terminateScript( self ):
        dbg( 'Teardown.Script: check if finished')
        self.stdoutDisp.stop()

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
            self.failIfCanNotKillTheProcess()
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
                self.stop()

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
        # rpdb2.g_fDebug = True
        self.sm = rpdb2.CSessionManager(PWD,True,False,'localhost')
        self.sm.wait_for_debuggee()
        self.console = rpdb2.CConsoleInternal(self.sm, stdout=self.rpdb2Stdout, stdin=self.fakeStdin, fSplit=True )
        self.console.start()
        time.sleep(1.0)

    def command( self, cmd, syncLines, timeout=3):
        '''Send the command cmd to the debuggee and wait until syncLines lines have been outputted
        by the debuggee or until the timeout expires'''
        endLineCount = self.rpdb2Stdout.lineCount + syncLines
        endTime = time.time() + timeout
        self.fakeStdin.appendCmd( "%s\n" % cmd )
        while ( (syncLines == 0 or self.rpdb2Stdout.lineCount < endLineCount)
                and time.time() < endTime):
            time.sleep(0.2)

    def attach( self ):
        self.command("attach %s\n" % DEBUGME, 4, 20 )
        self.assertEqual( self.rpdb2Stdout.attached, True )

    def stop( self ):
        self.command( "stop", 3 )

    def setBreakonexit( self, fbreakonexit ):
        self.command( "breakonexit  %s\n" % str(fbreakonexit), 1 )

    def getBreakonexit( self ):
        self.command( "breakonexit\n", 1 )

    def goAndWaitOnBp( self, syncLines=1, timeout=20):
        self.rpdb2Stdout.waitingOnBp = False
        self.command( "go", syncLines, timeout )
        self.assertEqual( self.rpdb2Stdout.waitingOnBp, True )

    def goAndExit( self, syncLines=3, timeout=20 ):
        dbg( "Starting goAndExit" )
        self.rpdb2Stdout.waitingOnBp = False
        self.command( "go", syncLines, timeout )
        dbg( "go sync done" )
        # self.assertEqual( self.rpdb2Stdout.running,  False )
        self.assertEqual( self.rpdb2Stdout.attached, False )

    def breakp( self, arg ):
        self.fakeStdin.appendCmd( "bp %s" % arg)

    def failIfCanNotKillTheProcess( self ):
        if sys.platform == 'win32' and IS_PYTHON_LESS_THAN_26 and not HAS_PSKILL:
            self.fail("On Python 2.4 and 2.5 on Windows this work only if you have pstools installed: http://technet.microsoft.com/fr-fr/sysinternals/bb896649.aspx" )

    #############[ tests ]##################

    def testGo( self ):
        self.startPdb2()
        self.attach()
        self.goAndExit()

        assert os.path.exists( 'tests/f1' )
        assert os.path.exists( 'tests/done' )
        assert os.path.exists( 'tests/atexit' )

    def testBp( self ):
        self.startPdb2()
        self.attach()
        self.breakp( 'f1' )
        self.breakp( self.bp1Line )
        self.goAndWaitOnBp() # break during definition of f1
        self.goAndWaitOnBp() # break during call of f1
        assert os.path.exists( 'tests/start' )
        assert not os.path.exists( 'tests/f1' )
        self.goAndWaitOnBp() # break after call of f2
        assert os.path.exists( 'tests/f1' )
        assert os.path.exists( 'tests/f2' )
        self.goAndExit() # run until the end
        assert os.path.exists('tests/done')
        assert os.path.exists('tests/atexit')

    def testChangingBreakonexit( self ):
        self.startPdb2()
        self.attach()
        self.getBreakonexit()
        self.assertEqual( self.rpdb2Stdout.breakonexit, False )
        self.setBreakonexit( True )
        self.assertEqual( self.rpdb2Stdout.breakonexit, True )
        self.setBreakonexit( False )
        self.assertEqual( self.rpdb2Stdout.breakonexit, False )

    def testRunWithBreakonexit( self ):
        self.startPdb2()
        self.assertEqual( self.rpdb2Stdout.waitingOnBp, False )
        self.attach()
        self.setBreakonexit( True )
        self.goAndWaitOnBp()
        self.assertEqual( self.rpdb2Stdout.attached, True )
        self.assertEqual( self.rpdb2Stdout.waitingOnBp, True )
        self.goAndExit()

    def testRunWithoutBreakonexit( self ):
        self.startPdb2()
        self.attach()
        self.setBreakonexit( False )
        self.goAndExit()
        self.assertEqual( self.rpdb2Stdout.attached, False )

if __name__ == '__main__':
    # unittest.main( argv=[sys.argv[0] + '-v'] + sys.argv[1:] )
    unittest.main()
