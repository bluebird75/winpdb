
# Python
import unittest, subprocess, threading
import os, time, sys, re, signal
from io import StringIO

# RPDB2
import rpdb2
import rpdb.const
import rpdb.session_manager
import rpdb.utils

rpdb.const.STARTUP_TIMEOUT = 10.0 # necessary because sometimes subprocess debugger is really slow to start

PREFIX_OUT = ' '*40 + 'OUT: '
PREFIX_RPDB2 = ' '*0 + 'RPDB2: '
PREFIX_STDOUT = ' '*20 + 'STDOUT: '
PREFIX_STDIN = ' '*20 + 'IN: '

DEBUGLEVEL='DEBUG'
def dbg( t ):
    if DEBUGLEVEL != 'INFO':
        print( '>> %s' % t )

if sys.platform != 'win32':
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
                    sys.stdout.write( PREFIX_STDIN  + ' %s\n' % p[:-1] )
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
        nb_written = super().write(t)
        if len(t) == 0 or (len(t) == 1 and t == "\n"):
            return

        lines = t.split('\n')

        for l in lines:
            if not l: continue
            print(PREFIX_STDOUT + ':%d: %s' % (self.lineCount, l) )
            if self.dispStdout:
                sys.stdout.write( PREFIX_RPDB2 + l )

            for retomatch, attr, assignment in self.matcher:
                if retomatch.match( l ) and getattr(self, attr) != assignment:
                    # dbg('Auto-setting %s to %s' % (attr, assignment) )
                    setattr( self, attr, assignment )

            self.lineCount += 1
        return nb_written


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
        print(PREFIX_OUT + 'Debugee output' )
        print(PREFIX_OUT + '--------------' )
        self.t.start()

    def stop( self ):
        self.shouldStop = True

    def displayStdout( self ):
        # Wait until stdout exists
        while self.process.stdout == None and self.shouldStop == False:
            print( PREFIX_OUT + ' ... waiting for process to start ...' )
            time.sleep(1.1)

        while True: # not self.shouldStop:
            l = self.process.stdout.readline()
            if not l:
                break
            if l[-1] == '\n':
                l = l[:-1]
            print( PREFIX_OUT + l.decode( sys.stdout.encoding, errors='replace'), end='' )



class BaseTestRpdb2( unittest.TestCase ):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        rpdb2.create_rpdb_settings_folder()
        self.bp1Line = findBpHint( 'tests/debugme.py' )['BP1']
        self.rpdb2Args = []

    def setUp(self):
        self.cleanBpFiles()
        self.cleanStepFiles()
        self.console = None
        self.sm = None
        self.fakeStdin = FakeStdin()
        self.rpdb2Stdout = Rpdb2Stdout( dispStdout=False )
        kwargs = {}
        pythonCmdLine = [ PYTHON, '-u', RPDB2, '-d'] + self.rpdb2Args
        rid = rpdb.utils.generate_rid()
        rpdb.session_manager.create_pwd_file( rid, PWD )
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
        bpldir = os.path.dirname( rpdb.session_manager.calc_bpl_filename( '' ) )
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

        # python more than 2.6
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

    def command( self, cmd, syncLines=0, timeout=3):
        '''Send the command cmd to the debuggee and wait until syncLines lines have been outputted
        by the debuggee or until the timeout expires'''
        value_before = self.rpdb2Stdout.getvalue()
        endLineCount = self.rpdb2Stdout.lineCount + syncLines
        endTime = time.time() + timeout
        self.fakeStdin.appendCmd( "%s\n" % cmd )
        while ( (syncLines != 0 and self.rpdb2Stdout.lineCount < endLineCount)
                and time.time() < endTime):
            time.sleep(0.2)
        value_delta = self.rpdb2Stdout.getvalue()[len(value_before):]
        return value_delta

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

    def stack( self, sync_lines=3 ):
        return self.command( "stack", sync_lines )

