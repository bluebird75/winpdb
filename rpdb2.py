#! /usr/bin/env python

"""
    rpdb2.py

    A remote Python debugger for CPython

    Copyright (C) 2013-2017 Philippe Fremy
    Copyright (C) 2005-2009 Nir Aides

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
import src.globals
import src.source_provider
from src.breakinfo import CScopeBreakInfo, CalcValidLines
from src.breakpoint import CBreakPointsManager
from src.compat import sets, unicode, str8
from src.const import *
from src.const import get_version, get_interface_compatibility_version, NT_DEBUG, SCREEN, MAC, DARWIN, POSIX, \
    STR_STATE_BROKEN, STATE_BROKEN, STATE_RUNNING, STATE_ANALYZE, STATE_DETACHED, DEBUGGER_FILENAME, THREADING_FILENAME, \
    DEFAULT_NUMBER_OF_LINES, DICT_KEY_TID, DICT_KEY_STACK, \
    DICT_KEY_CODE_LIST, DICT_KEY_CURRENT_TID, DICT_KEY_BROKEN, DICT_KEY_BREAKPOINTS, DICT_KEY_LINES, DICT_KEY_FILENAME, \
    DICT_KEY_FIRST_LINENO, DICT_KEY_FRAME_LINENO, DICT_KEY_EVENT, DICT_KEY_EXPR, DICT_KEY_NAME, DICT_KEY_REPR, \
    DICT_KEY_IS_VALID, DICT_KEY_TYPE, DICT_KEY_SUBNODES, DICT_KEY_N_SUBNODES, DICT_KEY_ERROR, BREAKPOINTS_FILE_EXT, \
    PYTHON_FILE_EXTENSION, PYTHONW_FILE_EXTENSION, PYTHON_EXT_LIST
from src.events import CEventNull, CEventEmbeddedSync, CEventClearSourceCache, CEventSignalIntercepted, \
    CEventSignalException, CEventPsycoWarning, CEventConflictingModules, CEventSyncReceivers, \
    CEventForkSwitch, CEventExecSwitch, CEventExit, CEventState, CEventSynchronicity, CEventBreakOnExit, CEventTrap, \
    CEventForkMode, CEventUnhandledException, CEventNamespace, CEventNoThreads, CEventThreads, CEventThreadBroken, \
    CEventStack, CEventStackDepth, CEventBreakpoint, CEventSync, breakpoint_copy, CEventDispatcher
from src.exceptions import InvalidScopeName, CException, NotPythonSource, BadArgument, ThreadNotFound, \
    NoThreads, ThreadDone, DebuggerNotBroken, InvalidFrame, NoExceptionFound, CConnectionException, BadVersion, \
    NotAttached, SpawnUnsupported, EncryptionNotSupported, EncryptionExpected, DecryptionFailure, AuthenticationBadData, AuthenticationFailure, \
    AuthenticationBadIndex
from src.globals import g_fDebug, g_traceback_lock, g_builtins_module
from src.repr import class_name, clip_filename, safe_str, safe_repr, parse_type, repr_ltd, calc_suffix
from src.session_manager import CSessionManager, is_valid_pwd, calc_pwd_file_path
from src.state_manager import CStateManager, lock_notify_all, g_alertable_waiters
from src.utils import is_unicode, as_unicode, as_string, as_bytes, print_debug, print_debug_exception, winlower, _print, \
    thread_set_daemon, thread_is_alive, thread_set_name, thread_get_name, current_thread, \
    detect_encoding, detect_locale, get_python_executable, ENCODING_AUTO, ENCODING_RAW, ENCODING_RAW_I, generate_rid, \
    safe_wait, my_os_path_join, FindFile, my_abspath, CalcScriptName, getcwd, getcwdu
from src.source_provider import MODULE_SCOPE, MODULE_SCOPE2, lines_cache, g_lines_cache, get_source_line, \
    is_provider_filesystem, g_found_unicode_files, myisfile

if '.' in __name__:
    raise ImportError('rpdb2 must not be imported as part of a package!')

import threading
import traceback
import tempfile
import platform
import operator
import weakref
import os.path
import pickle
import socket
import getopt
import random
import base64
import atexit
import codecs
import signal
import errno
import time
import copy
import hmac
import stat
import zlib
import sys
import cmd
import imp
import os

# TODO py3k
import hashlib
_md5 = hashlib.md5

if sys.version_info[:2] < (3,2):
    print(STR_BAD_PYTHON_VERSION)
    sys.exit(-1)

try:
    from Crypto.Cipher import DES
except ImportError:
    pass

import xmlrpc.server as SimpleXMLRPCServer
import xmlrpc.client as xmlrpclib
import socketserver as SocketServer
import subprocess as commands
import copyreg as copy_reg
import http.client as httplib
import _thread as thread
import numbers


#
#-------------------------------- Design Notes -------------------------------
#

"""
  Design:

    RPDB2 divides the world into two main parts: debugger and debuggee.
    The debuggee is the script that needs to be debugged.
    The debugger is another script that attaches to the debuggee for the
    purpose of debugging.

    Thus RPDB2 includes two main components: The debuggee-server that runs
    in the debuggee and the session-manager that runs in the debugger.

    The session manager and the debuggee-server communicate via XML-RPC.

    The main classes are: CSessionManager and CDebuggeeServer
"""



#
#--------------------------------- Export functions ------------------------
#


def start_embedded_debugger(
            _rpdb2_pwd,
            fAllowUnencrypted = True,
            fAllowRemote = False,
            timeout =TIMEOUT_FIVE_MINUTES,
            source_provider = None,
            fDebug = False,
            depth = 0
            ):

    """
    Use 'start_embedded_debugger' to invoke the debugger engine in embedded
    scripts. put the following line as the first line in your script:

    import rpdb2; rpdb2.start_embedded_debugger(<some-password-string>)

    This will cause the script to freeze until a debugger console attaches.

    _rpdb2_pwd - The password that governs security of client/server communication.

    fAllowUnencrypted - Allow unencrypted communications. Communication will
        be authenticated but encrypted only if possible.

    fAllowRemote - Allow debugger consoles from remote machines to connect.

    timeout - Seconds to wait for attachment before giving up. Once the
        timeout period expires, the debuggee will resume execution.
        If None, never give up. If 0, do not wait at all.

    source_provider - When script source is not available on file system it is
        possible to specify a function that receives a "filename" and returns
        its source. If filename specifies a file that does not fall under
        the jurisdiction of this function it should raise IOError. If this
        function is responsible for the specified file but the source is
        not available it should raise IOError(SOURCE_NOT_AVAILABLE). You can
        study the way source_provider_blender() works. Note that a misbehaving
        function can break the debugger.

    fDebug - debug output.

    depth - Depth of the frame in which the debugger should be started. This
        defaults to '0' so the top of stack will be in the code where
        start_embedded_debugger is called.

    IMPORTNAT SECURITY NOTE:
    USING A HARDCODED PASSWORD MAY BE UNSECURE SINCE ANYONE WITH READ
    PERMISSION TO THE SCRIPT WILL BE ABLE TO READ THE PASSWORD AND CONNECT TO
    THE DEBUGGER AND DO WHATEVER THEY WISH VIA THE 'EXEC' DEBUGGER COMMAND.

    It is safer to use: start_embedded_debugger_interactive_password()
    """

    return __start_embedded_debugger(
                        _rpdb2_pwd,
                        fAllowUnencrypted,
                        fAllowRemote,
                        timeout,
                        source_provider,
                        fDebug,
                        depth + 2
                        )



def start_embedded_debugger_interactive_password(
                fAllowUnencrypted = True,
                fAllowRemote = False,
                timeout =TIMEOUT_FIVE_MINUTES,
                source_provider = None,
                fDebug = False,
                stdin = sys.stdin,
                stdout = sys.stdout,
                depth = 0
                ):

    if g_server is not None:
        return

    while True:
        if stdout is not None:
            stdout.write('Please type password:')

        _rpdb2_pwd = stdin.readline().rstrip('\n')
        _rpdb2_pwd = as_unicode(_rpdb2_pwd, detect_encoding(stdin), fstrict = True)

        try:
            return __start_embedded_debugger(
                                _rpdb2_pwd,
                                fAllowUnencrypted,
                                fAllowRemote,
                                timeout,
                                source_provider,
                                fDebug,
                                depth + 2
                                )

        except BadArgument:
            stdout.write(STR_PASSWORD_BAD)



def settrace():
    """
    Trace threads that were created with thread.start_new_thread()
    To trace, call this function from the thread target function.

    NOTE: The main thread and any threads created with the threading module
    are automatically traced, and there is no need to invoke this function
    for them.

    Note: This call does not pause the script.
    """

    return __settrace()



def setbreak(depth = 0):
    """
    Pause the script for inspection at next script statement.
    """

    return __setbreak(depth + 2)



def set_temp_breakpoint(path, scopename = '', lineno = 1):
    """
    Set a temporary breakpoint in a file. path must be an absolute path.
    scopename can either be an empty string or a fully qualified scope name
    (For example u'g_debugger.m_bp_manager.set_temp_breakpoint'). lineno is
    either relative to file start or to scope start.

    To set a temporary breakpoint to hit when a file is first
    imported or exec-uted call set_temp_breakpoint(path)

    This function may throw a varaiety of exceptions.
    """

    path = as_unicode(path, fstrict = True)
    scopename = as_unicode(scopename, fstrict = True)

    return __set_temp_breakpoint(path, scopename, lineno)



#
#----------------------------------- Interfaces ------------------------------
#


class CConsole:
    """
    Interface to a debugger console.
    """

    def __init__(
            self,
            session_manager,
            stdin = None,
            stdout = None,
            fSplit = False
            ):

        """
        Constructor of CConsole

        session_manager - session manager object.
        stdin, stdout - redirection for IO.
        fsplit - Set flag to True when Input and Ouput belong to different
                 panes. For example take a look at Winpdb.
        """

        self.m_ci = CConsoleInternal(
                        session_manager,
                        stdin,
                        stdout,
                        fSplit
                        )


    def start(self):
        return self.m_ci.start()


    def join(self):
        """
        Wait until the console ends.
        """

        return self.m_ci.join()


    def set_filename(self, filename):
        """
        Set current filename for the console. The current filename can change
        from outside the console when the console is embeded in other
        components, for example take a look at Winpdb.
        """

        filename = as_unicode(filename)

        return self.m_ci.set_filename(filename)


    def complete(self, text, state):
        """
        Return the next possible completion for 'text'.
        If a command has not been entered, then complete against command list.
        Otherwise try to call complete_<command> to get list of completions.
        """

        text = as_unicode(text)

        return self.m_ci.complete(text, state)


    def printer(self, text):
        text = as_unicode(text)

        return self.m_ci.printer(text)



#
# ---------------------------- Exceptions ----------------------------------
#


#
#----------------- unicode handling for compatibility with py3k ----------------
#



def is_py3k():
    return sys.version_info[0] >= 3


#
#----------------------- Infinite List of Globals ---------------------------
#



#
# According to PEP-8: "Use 4 spaces per indentation level."
#

GNOME_DEFAULT_TERM = 'gnome-terminal'
GNOME_DEFAULT_TERM_BEFORE_3_8 = 'gnome-terminal --disable-factory'
GNOME_DEFAULT_TERM_BEFORE_3_8_CHECK_FILE = "/../share/gnome-terminal/profile-manager.ui" #this glade-related file present for only gnome terminal versions 2.24-3.6

#
# Map between OS type and relevant command to initiate a new OS console.
# entries for other OSs can be added here.
# '%s' serves as a place holder.
#
# Currently there is no difference between 'nt' and NT_DEBUG, since now
# both of them leave the terminal open after termination of debuggee to
# accommodate scenarios of scripts with child processes.
#
osSpawn = {
    'nt': 'start "rpdb2 - Version ' + get_version() + ' - Debuggee Console" cmd.exe /K ""%(exec)s" %(options)s"',
    NT_DEBUG: 'start "rpdb2 - Version ' + get_version() + ' - Debuggee Console" cmd.exe /K ""%(exec)s" %(options)s"',
    POSIX: "%(term)s -e %(shell)s -c '%(exec)s %(options)s; %(shell)s' &",
    'Terminal': "Terminal --disable-server -x %(shell)s -c '%(exec)s %(options)s; %(shell)s' &",
    GNOME_DEFAULT_TERM_BEFORE_3_8: "gnome-terminal --disable-factory -x %(shell)s -c '%(exec)s %(options)s; %(shell)s' &",
    GNOME_DEFAULT_TERM: "gnome-terminal -x %(shell)s -c '%(exec)s %(options)s; %(shell)s' &",
    MAC: '%(exec)s %(options)s',
    DARWIN: '%(exec)s %(options)s',
    SCREEN: 'screen -t debuggee_console %(exec)s %(options)s'
}

RPDBTERM = 'RPDBTERM'
COLORTERM = 'COLORTERM'
TERM = 'TERM'
KDE_PREFIX = 'KDE'
GNOME_PREFIX = 'GNOME'

KDE_DEFAULT_TERM_QUERY = "kreadconfig --file kdeglobals --group General --key TerminalApplication --default konsole"
XTERM = 'xterm'
RXVT = 'rxvt'

FORK_CHILD = 'child'
FORK_PARENT = 'parent'
FORK_MANUAL = 'manual'
FORK_AUTO = 'auto'

ENCRYPTION_ENABLED = 'encrypted'
ENCRYPTION_DISABLED = 'plain-text'

STATE_ENABLED = 'enabled'
STATE_DISABLED = 'disabled'

BP_FILENAME_SEP = ':'
BP_EVAL_SEP = ','

RPDB_EXEC_INFO = as_unicode('rpdb_exception_info')

MODE_ON = 'ON'
MODE_OFF = 'OFF'

MAX_EVALUATE_LENGTH = 256 * 1024
MAX_NAMESPACE_ITEMS = 1024
MAX_SORTABLE_LENGTH = 256 * 1024
REPR_ID_LENGTH = 4096

MAX_NAMESPACE_WARNING = {
    DICT_KEY_EXPR: STR_MAX_NAMESPACE_WARNING_TITLE,
    DICT_KEY_NAME: STR_MAX_NAMESPACE_WARNING_TITLE,
    DICT_KEY_REPR: STR_MAX_NAMESPACE_WARNING_MSG,
    DICT_KEY_IS_VALID: False,
    DICT_KEY_TYPE: STR_MAX_NAMESPACE_WARNING_TYPE,
    DICT_KEY_N_SUBNODES: 0
    }

MAX_EVENT_LIST_LENGTH = 1000

INDEX_TABLE_SIZE = 100

DISPACHER_METHOD = 'dispatcher_method'

CONFLICTING_MODULES = ['psyco', 'pdb', 'bdb', 'doctest']

XML_DATA = """<?xml version='1.0'?>
<methodCall>
<methodName>dispatcher_method</methodName>
<params>
<param>
<value><string>%s</string></value>
</param>
</params>
</methodCall>""" % RPDB_COMPATIBILITY_VERSION

N_WORK_QUEUE_THREADS = 8

ERROR_NO_ATTRIBUTE = 'Error: No attribute.'


g_server_lock = threading.RLock()
g_server = None
g_debugger = None

g_fScreen = False
g_fDefaultStd = True

#
# These globals are related to handling the os.fork() os._exit() and exec
# pattern.
#
g_forkpid = None
g_forktid = None
g_fignorefork = False

g_exectid = None
g_execpid = None

g_fos_exit = False


#
# To hold a reference to __main__ to prevent its release if an unhandled
# exception is raised.
#
g_module_main = None

g_found_conflicting_modules = []

g_fignore_atexit = False
g_ignore_broken_pipe = 0



g_frames_path = {}

g_signal_handlers = {}
g_signals_pending = []

#g_profile = None

g_fbreakonexit = False



g_safe_base64_to = bytes.maketrans(as_bytes('/+='), as_bytes('_-#'))
g_safe_base64_from = bytes.maketrans(as_bytes('_-#'), as_bytes('/+='))



#
# ---------------------------- General Utils ------------------------------
#

def parse_console_launch( arg ):
    '''Split a the console command launch into chdir option, interprter option and real commandline

    Returns: (fchdir, intrepreter, arg)
    '''
    (fchdir, interpreter) = (True, get_python_executable())
    if arg == '':
        return (fchdir, interpreter, arg)

    idx = 0
    while idx < len(arg):
        if arg[:2] == '-k':
            fchdir = False
            arg = arg[2:].strip()
        elif arg[:2] == '-i':
            arg = arg[2:].strip()
            if arg[0] in ('"', "'"):
                st = 1
                end = arg.find(arg[0],1 )
                interpreter = '"%s"' % arg[st:end]
            else:
                st = 0
                end = arg.find(' ', 1 )
                interpreter = arg[st:end]
            arg = arg[end+1:].strip()
        else:
            # no more arguments for us
            break


    return (fchdir, interpreter, arg)


def job_wrapper(event, foo, *args, **kwargs):
    try:
        #print_debug('Thread %d doing job %s' % (thread.get_ident(), foo.__name__))
        foo(*args, **kwargs)
    finally:
        event.set()



def send_job(tid, timeout, foo, *args, **kwargs):
    #
    # Attempt to send job to thread tid.
    # Will throw KeyError if thread tid is not available for jobs.
    #

    (lock, jobs) = g_alertable_waiters[tid]

    event = threading.Event()
    f = lambda: job_wrapper(event, foo, *args, **kwargs)
    jobs.append(f)

    try:
        lock.acquire()
        lock_notify_all(lock)
    finally:
        lock.release()

    safe_wait(event, timeout)


def event_is_set(event):
    return event.is_set()

# TODO: adjust
def _raw_input(s):
    return input(s)



def calc_frame_path(frame):
    globals_filename = frame.f_globals.get('__file__', None)
    filename = frame.f_code.co_filename

    if filename.startswith('<'):
        if globals_filename == None:
            return filename
        else:
            filename = CalcScriptName(os.path.basename(globals_filename))

    if filename in g_frames_path:
        return g_frames_path[filename]

    if globals_filename != None:
        dirname = os.path.dirname(globals_filename)
        basename = os.path.basename(filename)
        path = my_os_path_join(dirname, basename)

        if os.path.isabs(path):
            abspath = my_abspath(path)
            lowered = winlower(abspath)
            g_frames_path[filename] = lowered
            return lowered

        try:
            abspath = FindFile(path, fModules = True)
            lowered = winlower(abspath)
            g_frames_path[filename] = lowered
            return lowered

        except IOError:
            pass

    if os.path.isabs(filename):
        abspath = my_abspath(filename)
        lowered = winlower(abspath)
        g_frames_path[filename] = lowered
        return lowered

    try:
        abspath = FindFile(filename, fModules = True)
        lowered = winlower(abspath)
        g_frames_path[filename] = lowered
        return lowered

    except IOError:
        lowered = winlower(filename)
        return lowered


if is_py3k() and sys.version_info[:2] > (3,0):
    base64_encodestring = base64.encodebytes
    base64_decodestring = base64.decodebytes
else:
    base64_encodestring = base64.encodestring
    base64_decodestring = base64.decodestring


#
# MOD
#


def IsPythonSourceFile(path):
    if path.endswith(PYTHON_FILE_EXTENSION):
        return True

    if path.endswith(PYTHONW_FILE_EXTENSION):
        return True

    path = g_found_unicode_files.get(path, path)

    for lineno in range(1, 10):
        line = get_source_line(path, lineno)

        if line.startswith('#!') and 'python' in line:
            return True

    # In doubt, return True
    # in the past, we would try to parse the file successfully but
    # this is too complicated in Python 3


def CalcModuleName(filename):
    _basename = os.path.basename(filename)
    (modulename, ext) = os.path.splitext(_basename)

    if ext in PYTHON_EXT_LIST:
        return modulename

    return  _basename


def FindModuleDir(module_name):
    if module_name == '':
        raise IOError

    dot_index = module_name.rfind('.')
    if dot_index != -1:
        parent = module_name[: dot_index]
        child = module_name[dot_index + 1:]
    else:
        parent = ''
        child = module_name

    m = sys.modules[module_name]

    if not hasattr(m, '__file__') or m.__file__ == None:
        parent_dir = FindModuleDir(parent)
        module_dir = my_os_path_join(parent_dir, winlower(child))
        return module_dir

    if not os.path.isabs(m.__file__):
        parent_dir = FindModuleDir(parent)
        module_dir = my_os_path_join(parent_dir, winlower(child))
        return module_dir

    (root, ext) = os.path.splitext(m.__file__)
    if root.endswith('__init__'):
        root = os.path.dirname(root)

    abspath = my_abspath(root)
    lowered = winlower(abspath)

    return lowered


def IsFileInPath(filename):
    if filename == '':
        return False

    try:
        FindFile(filename)
        return True

    except IOError:
        return False



def IsPrefixInEnviron(_str):
    for e in os.environ.keys():
        if e.startswith(_str):
            return True

    return False



def CalcTerminalCommand():
    """
    Calc the unix command to start a new terminal, for example: xterm
    """

    if RPDBTERM in os.environ:
        term = os.environ[RPDBTERM]
        if IsFileInPath(term):
            return term

    if COLORTERM in os.environ:
        term = os.environ[COLORTERM]
        if term != 'yes' and IsFileInPath(term):
            return term

    if IsPrefixInEnviron(KDE_PREFIX):
        (s, term) = commands.getstatusoutput(KDE_DEFAULT_TERM_QUERY)
        if (s == 0) and IsFileInPath(term):
            return term

    elif IsPrefixInEnviron(GNOME_PREFIX):
        try:
            gnome_terminal_path = FindFile(GNOME_DEFAULT_TERM)
            if gnome_terminal_path:
                if myisfile(os.path.dirname(gnome_terminal_path) + GNOME_DEFAULT_TERM_BEFORE_3_8_CHECK_FILE):
                    return GNOME_DEFAULT_TERM_BEFORE_3_8
                return GNOME_DEFAULT_TERM
        except IOError:
            pass

    if IsFileInPath(XTERM):
        return XTERM

    if IsFileInPath(RXVT):
        return RXVT

    raise SpawnUnsupported



def CalcMacTerminalCommand(command):
    """
    Calculate what to put in popen to start a given script.
    Starts a tiny Applescript that performs the script action.
    """

    #
    # Quoting is a bit tricky; we do it step by step.
    # Make Applescript string: put backslashes before double quotes and
    # backslashes.
    #
    command = command.replace('\\', '\\\\').replace('"', '\\"')

    #
    # Make complete Applescript command.
    #
    command = 'tell application "Terminal" to do script "%s"' % command

    #
    # Make a shell single quoted string (put backslashed single quotes
    # outside string).
    #
    command = command.replace("'", "'\\''")

    #
    # Make complete shell command.
    #
    return "osascript -e '%s'" % command


def get_file_encoding(filename):
    (lines, encoding, ffilesystem) = lines_cache(filename)
    return encoding






def _getpid():
    try:
        return os.getpid()
    except:
        return -1



def calcURL(host, port):
    """
    Form HTTP URL from 'host' and 'port' arguments.
    """

    url = "http://" + str(host) + ":" + str(port)
    return url



def GetSocketError(e):
    if (not isinstance(e.args, tuple)) or (len(e.args) == 0):
        return -1

    return e.args[0]



def ControlRate(t_last_call, max_rate):
    """
    Limits rate at which this function is called by sleeping.
    Returns the time of invocation.
    """

    p = 1.0 / max_rate
    t_current = time.time()
    dt = t_current - t_last_call

    if dt < p:
        time.sleep(p - dt)

    return t_current


def generate_random_char(_str):
    """
    Return a random character from string argument.
    """

    if _str == '':
        return ''

    i = random.randint(0, len(_str) - 1)
    return _str[i]



def generate_random_password():
    """
    Generate an 8 characters long password.
    """

    s = 'abdefghijmnqrt' + 'ABDEFGHJLMNQRTY'
    ds = '23456789_' + s

    _rpdb2_pwd = generate_random_char(s)

    for i in range(0, 7):
        _rpdb2_pwd += generate_random_char(ds)

    _rpdb2_pwd = as_unicode(_rpdb2_pwd)

    return _rpdb2_pwd


def is_encryption_supported():
    """
    Is the Crypto module imported/available.
    """

    return 'DES' in globals()


def calc_prefix(_str, n):
    """
    Return an n charaters prefix of the argument string of the form
    'prefix...'.
    """

    if len(_str) <= n:
        return _str

    return _str[: (n - 3)] + '...'



def create_rpdb_settings_folder():
    """
    Create the settings folder on Posix systems:
    '~/.rpdb2_settings' with mode 700.
    """

    if os.name != POSIX:
        return

    home = os.path.expanduser('~')

    rsf = os.path.join(home, RPDB_SETTINGS_FOLDER)
    if not os.path.exists(rsf):
        os.mkdir(rsf, int('0700', 8))

    pwds = os.path.join(home, RPDB_PWD_FOLDER)
    if not os.path.exists(pwds):
        os.mkdir(pwds, int('0700', 8))

    bpl = os.path.join(home, RPDB_BPL_FOLDER)
    if not os.path.exists(bpl):
        os.mkdir(bpl, int('0700', 8))



def cleanup_bpl_folder(path):
    if random.randint(0, 10) > 0:
        return

    l = os.listdir(path)
    if len(l) < MAX_BPL_FILES:
        return

    try:
        ll = [(os.stat(os.path.join(path, f))[stat.ST_ATIME], f) for f in l]
    except:
        return

    ll.sort()

    for (t, f) in ll[: -MAX_BPL_FILES]:
        try:
            os.remove(os.path.join(path, f))
        except:
            pass



def calc_bpl_filename(filename):
    key = as_bytes(filename)
    tmp_filename = hmac.new(key, digestmod=_md5).hexdigest()[:10]

    if os.name == POSIX:
        home = os.path.expanduser('~')
        bpldir = os.path.join(home, RPDB_BPL_FOLDER)
        cleanup_bpl_folder(bpldir)
        path = os.path.join(bpldir, tmp_filename) + BREAKPOINTS_FILE_EXT
        return path

    #
    # gettempdir() is used since it works with unicode user names on
    # Windows.
    #

    tmpdir = tempfile.gettempdir()
    bpldir = os.path.join(tmpdir, RPDB_BPL_FOLDER_NT)

    if not os.path.exists(bpldir):
        #
        # Folder creation is done here since this is a temp folder.
        #
        try:
            os.mkdir(bpldir, int('0700', 8))
        except:
            print_debug_exception()
            raise CException

    else:
        cleanup_bpl_folder(bpldir)

    path = os.path.join(bpldir, tmp_filename) + BREAKPOINTS_FILE_EXT
    return path


def read_pwd_file(rid):
    """
    Read password from password file for Posix systems.
    """

    assert(os.name == POSIX)

    path = calc_pwd_file_path(rid)

    p = open(path, 'r')
    _rpdb2_pwd = p.read()
    p.close()

    _rpdb2_pwd = as_unicode(_rpdb2_pwd, fstrict = True)

    return _rpdb2_pwd



def delete_pwd_file(rid):
    """
    Delete password file for Posix systems.
    """

    if os.name != POSIX:
        return

    path = calc_pwd_file_path(rid)

    try:
        os.remove(path)
    except:
        pass



def CalcUserShell():
    try:
        s = os.getenv('SHELL')
        if s != None:
            return s

        import getpass
        username = getpass.getuser()

        f = open('/etc/passwd', 'r')
        l = f.read()
        f.close()

        ll = l.split('\n')
        d = dict([(e.split(':', 1)[0], e.split(':')[-1]) for e in ll])

        return d[username]

    except:
        return 'sh'



def IsFilteredAttribute(a):
    if not (a.startswith('__') and a.endswith('__')):
        return False

    if a in ['__class__', '__bases__', '__file__', '__doc__', '__name__', '__all__', '__builtins__']:
        return False

    return True



def IsFilteredAttribute2(r, a):
    try:
        o = getattr(r, a)
        r = parse_type(type(o))

        if 'function' in r or 'method' in r or r == 'type':
            return True

        return False

    except:
        return False



def CalcFilteredDir(r, filter_level):
    d = dir(r)

    if 'finfo' in d and parse_type(type(r)) == 'mp_request':
        #
        # Workaround mod_python segfault in type(req.finfo) by
        # removing this attribute from the namespace viewer.
        #
        d.remove('finfo')

    if filter_level == 0:
        return d

    fd = [a for a in d if not IsFilteredAttribute(a)]

    return fd



def CalcIdentity(r, filter_level):
    if filter_level == 0:
        return r

    if not hasattr(r, 'im_func'):
        return r

    return r.im_func



def getattr_nothrow(o, a):
    try:
        return getattr(o, a)

    except AttributeError:
        return ERROR_NO_ATTRIBUTE

    except:
        print_debug_exception()
        return ERROR_NO_ATTRIBUTE



def calc_attribute_list(r, filter_level):
    d = CalcFilteredDir(r, filter_level)
    rs = set(d)

    c = getattr_nothrow(r, '__class__')
    if not c is ERROR_NO_ATTRIBUTE:
        d = CalcFilteredDir(c, False)
        cs = set(d)
        s = rs & cs

        for e in s:
            o1 = getattr_nothrow(r, e)
            o2 = getattr_nothrow(c, e)

            if o1 is ERROR_NO_ATTRIBUTE or CalcIdentity(o1, filter_level) is CalcIdentity(o2, filter_level):
                rs.discard(e)

            try:
                if filter_level == 1 and getattr(o1, '__self__') is getattr(o2, '__self__'):
                    rs.discard(e)
            except:
                pass

    bl = getattr_nothrow(r, '__bases__')
    if type(bl) == tuple:
        for b in bl:
            d = CalcFilteredDir(b, False)
            bs = set(d)
            s = rs & bs

            for e in s:
                o1 = getattr_nothrow(r, e)
                o2 = getattr_nothrow(b, e)

                if o1 is ERROR_NO_ATTRIBUTE or CalcIdentity(o1, filter_level) is CalcIdentity(o2, filter_level):
                    rs.discard(e)

                try:
                    if filter_level == 1 and getattr(o1, '__self__') is getattr(o2, '__self__'):
                        rs.discard(e)
                except:
                    pass

    l = [a for a in rs if (filter_level < 2 or not IsFilteredAttribute2(r, a))]

    if hasattr(r, '__class__') and not '__class__' in l:
        l = ['__class__'] + l

    if hasattr(r, '__bases__') and not '__bases__' in l:
        l = ['__bases__'] + l

    al = [a for a in l if hasattr(r, a)]

    return al



class _RPDB2_FindRepr:
    def __init__(self, o, repr_limit):
        self.m_object = o
        self.m_repr_limit = repr_limit


    def __getitem__(self, key):
        index = 0
        for i in self.m_object:
            if repr_ltd(i, self.m_repr_limit, encoding =ENCODING_RAW_I).replace('"', '&quot') == key:
                if isinstance(self.m_object, dict):
                    return self.m_object[i]

                return i

            index += 1
            if index > MAX_SORTABLE_LENGTH:
                return None


    def __setitem__(self, key, value):
        if not isinstance(self.m_object, dict):
            return

        index = 0
        for i in self.m_object:
            if repr_ltd(i, self.m_repr_limit, encoding =ENCODING_RAW_I).replace('"', '&quot') == key:
                self.m_object[i] = value
                return

            index += 1
            if index > MAX_SORTABLE_LENGTH:
                return



#
# Since on Python 3000 the comparison of different types raises exceptions and
# the __cmp__ method was removed, sorting of namespace items is based on
# lexicographic order except for numbers which are sorted normally and appear
# before all other types.
#
def sort(s):
    if sys.version_info[:2] == (2, 3):
        #
        # On Python 2.3 the key parameter is not supported.
        #
        s.sort(sort_cmp)
        return

    s.sort(key = sort_key)



def sort_key(e):
    if is_py3k() and isinstance(e, numbers.Number):
        return (0, e)

    if not is_py3k() and operator.isNumberType(e):
        return (0, e)

    return (1, repr_ltd(e, 256, encoding =ENCODING_RAW_I))



def sort_cmp(x, y):
    skx = sort_key(x)
    sky = sort_key(y)

    return cmp(skx, sky)



def recalc_sys_path(old_pythonpath):
    opl = old_pythonpath.split(os.path.pathsep)
    del sys.path[1: 1 + len(opl)]

    pythonpath = os.environ.get('PYTHONPATH', '')
    ppl = pythonpath.split(os.path.pathsep)

    for i, p in enumerate(ppl):
        abspath = my_abspath(p)
        lowered = winlower(abspath)

        sys.path.insert(1 + i, lowered)


#
# Similar to traceback.extract_stack() but fixes path with calc_frame_path()
#
def my_extract_stack(f):
    '''
    :param f: frame object
    :return: similar to traceback.extract_stack()
        - list of : (filename, line number, function name, text of source code)
    '''
    if f == None:
        return []

    try:
        g_traceback_lock.acquire()
        _s = traceback.extract_stack(f)

    finally:
        g_traceback_lock.release()

    _s.reverse()

    s = []
    for (p, ln, fn, text) in _s:
        path = as_unicode(calc_frame_path(f), sys.getfilesystemencoding())
        if text == None:
            text = ''

        s.append((path, ln, as_unicode(fn), as_unicode(text)))

        f = f.f_back
        if f == None:
            break

    s.reverse()
    return s




#
# Similar to traceback.extract_tb() but fixes path with calc_frame_path()
#
def my_extract_tb(tb):
    '''
    :param tb: traceback object
    :return: similar to traceback.extract_tb()
        - list of : (filename, line number, function name, text of source code)
    '''
    try:
        g_traceback_lock.acquire()
        _s = traceback.extract_tb(tb)

    finally:
        g_traceback_lock.release()

    s = []
    for (p, ln, fn, text) in _s:
        path = as_unicode(calc_frame_path(tb.tb_frame), sys.getfilesystemencoding())
        if text == None:
            text = ''

        s.append((path, ln, as_unicode(fn), as_unicode(text)))

        tb = tb.tb_next
        if tb == None:
            break

    return s



def get_traceback(frame, ctx):
    if is_py3k():
        if ctx.get_exc_info() != None:
            return ctx.get_exc_info()[2]
    else:
        if frame.f_exc_traceback != None:
            return frame.f_exc_traceback

    locals = copy.copy(frame.f_locals)
    if not 'traceback' in locals:
        return None

    tb = locals['traceback']
    if dir(tb) == ['tb_frame', 'tb_lasti', 'tb_lineno', 'tb_next']:
        return tb


#
# ---------------------------------- CThread ---------------------------------------
#



class CThread (threading.Thread):
    m_fstop = False
    m_threads = {}

    m_lock = threading.RLock()
    m_id = 0


    def __init__(self, name = None, target = None, args = (), shutdown = None):
        threading.Thread.__init__(self, name = name, target = target, args = args)

        self.m_fstarted = False
        self.m_shutdown_callback = shutdown

        self.m_id = self.__getId()


    def __del__(self):
        #print_debug('Destructor called for ' + thread_get_name(self))

        #threading.Thread.__del__(self)

        if self.m_fstarted:
            try:
                del CThread.m_threads[self.m_id]
            except KeyError:
                pass


    def start(self):
        if CThread.m_fstop:
            return

        CThread.m_threads[self.m_id] = weakref.ref(self)

        if CThread.m_fstop:
            del CThread.m_threads[self.m_id]
            return

        self.m_fstarted = True

        threading.Thread.start(self)


    def run(self):
        sys.settrace(None)
        sys.setprofile(None)

        threading.Thread.run(self)


    def join(self, timeout = None):
        try:
            threading.Thread.join(self, timeout)
        except AssertionError:
            pass


    def shutdown(self):
        if self.m_shutdown_callback:
            self.m_shutdown_callback()


    def joinAll(cls):
        print_debug('Shutting down debugger threads...')

        CThread.m_fstop = True

        for tid, w in list(CThread.m_threads.items()):
            t = w()
            if not t:
                continue

            try:
                #print_debug('Calling shutdown of thread %s.' % thread_get_name(t))
                t.shutdown()
            except:
                pass

            t = None

        t0 = time.time()

        while len(CThread.m_threads) > 0:
            if time.time() - t0 > SHUTDOWN_TIMEOUT:
                print_debug('Shut down of debugger threads has TIMED OUT!')
                return

            #print_debug(repr(CThread.m_threads))
            time.sleep(0.1)

        print_debug('Shut down debugger threads, done.')

    joinAll = classmethod(joinAll)


    def clearJoin(cls):
        CThread.m_fstop = False

    clearJoin = classmethod(clearJoin)


    def __getId(self):
        CThread.m_lock.acquire()
        id = CThread.m_id
        CThread.m_id += 1
        CThread.m_lock.release()

        return id



#
#--------------------------------------- Crypto ---------------------------------------
#



class CCrypto:
    """
    Handle authentication and encryption of data, using password protection.
    """

    m_keys = {}

    def __init__(self, _rpdb2_pwd, fAllowUnencrypted, rid):
        assert(is_unicode(_rpdb2_pwd))
        assert(is_unicode(rid))

        self.m_rpdb2_pwd = _rpdb2_pwd
        self.m_key = self.__calc_key(_rpdb2_pwd)

        self.m_fAllowUnencrypted = fAllowUnencrypted
        self.m_rid = rid

        self.m_failure_lock = threading.RLock()

        self.m_lock = threading.RLock()

        self.m_index_anchor_in = random.randint(0, 1000000000)
        self.m_index_anchor_ex = 0

        self.m_index = 0
        self.m_index_table = {}
        self.m_index_table_size = INDEX_TABLE_SIZE
        self.m_max_index = 0


    def __calc_key(self, _rpdb2_pwd):
        """
        Create and return a key from a password.
        A Weak password means a weak key.
        """

        if _rpdb2_pwd in CCrypto.m_keys:
            return CCrypto.m_keys[_rpdb2_pwd]

        key = as_bytes(_rpdb2_pwd)
        suffix = key[:16]

        d = hmac.new(key, digestmod = _md5)

        #
        # The following loop takes around a second to complete
        # and should strengthen the password by ~12 bits.
        # a good password is ~30 bits strong so we are looking
        # at ~42 bits strong key
        #
        for i in range(2 ** 12):
            d.update((key + suffix) * 16)
            key = d.digest()

        CCrypto.m_keys[_rpdb2_pwd] = key

        return key


    def set_index(self, i, anchor):
        try:
            self.m_lock.acquire()

            self.m_index = i
            self.m_index_anchor_ex = anchor

        finally:
            self.m_lock.release()


    def get_max_index(self):
        return self.m_max_index


    def do_crypto(self, args, fencrypt):
        """
        Sign args and possibly encrypt.
        Return signed/encrypted string.
        """

        if not fencrypt and not self.m_fAllowUnencrypted:
            raise EncryptionExpected

        if fencrypt and not is_encryption_supported():
            raise EncryptionNotSupported

        (digest, s) = self.__sign(args)

        fcompress = False

        if len(s) > 50000:
            _s = zlib.compress(s)

            if len(_s) < len(s) * 0.4:
                s = _s
                fcompress = True

        if fencrypt:
            s = self.__encrypt(s)

        s = base64_encodestring(s)
        u = as_unicode(s)

        return (fcompress, digest, u)


    def undo_crypto(self, fencrypt, fcompress, digest, msg, fVerifyIndex = True):
        """
        Take crypto string, verify its signature and decrypt it, if
        needed.
        """

        if not fencrypt and not self.m_fAllowUnencrypted:
            raise EncryptionExpected

        if fencrypt and not is_encryption_supported():
            raise EncryptionNotSupported

        s = as_bytes(msg)
        s = base64_decodestring(s)

        if fencrypt:
            s = self.__decrypt(s)

        if fcompress:
            s = zlib.decompress(s)

        args, id = self.__verify_signature(digest, s, fVerifyIndex)

        return (args, id)


    def __encrypt(self, s):
        s_padded = s + as_bytes('\x00') * (DES.block_size - (len(s) % DES.block_size))

        key_padded = (self.m_key + as_bytes('0') * (DES.key_size - (len(self.m_key) % DES.key_size)))[:DES.key_size]
        iv = as_bytes('0') * DES.block_size

        d = DES.new(key_padded, DES.MODE_CBC, iv)
        r = d.encrypt(s_padded)

        return r


    def __decrypt(self, s):
        try:
            key_padded = (self.m_key + as_bytes('0') * (DES.key_size - (len(self.m_key) % DES.key_size)))[:DES.key_size]
            iv = as_bytes('0') * DES.block_size

            d = DES.new(key_padded, DES.MODE_CBC, iv)
            _s = d.decrypt(s).strip(as_bytes('\x00'))

            return _s

        except:
            self.__wait_a_little()
            raise DecryptionFailure


    def __sign(self, args):
        i = self.__get_next_index()
        pack = (self.m_index_anchor_ex, i, self.m_rid, args)

        #print_debug('***** 1' + repr(args)[:50])
        s = pickle.dumps(pack, 2)
        #print_debug('***** 2' + repr(args)[:50])

        h = hmac.new(self.m_key, s, digestmod = _md5)
        d = h.hexdigest()

        #if 'coding:' in s:
        #    print_debug('%s, %s, %s\n\n==========\n\n%s' % (len(s), d, repr(args), repr(s)))

        return (d, s)


    def __get_next_index(self):
        try:
            self.m_lock.acquire()

            self.m_index += 1
            return self.m_index

        finally:
            self.m_lock.release()


    def __verify_signature(self, digest, s, fVerifyIndex):
        try:
            h = hmac.new(self.m_key, s, digestmod = _md5)
            d = h.hexdigest()

            #if 'coding:' in s:
            #    print_debug('%s, %s, %s, %s' % (len(s), digest, d, repr(s)))

            if d != digest:
                self.__wait_a_little()
                raise AuthenticationFailure

            pack = pickle.loads(s)
            (anchor, i, id, args) = pack

        except AuthenticationFailure:
            raise

        except:
            print_debug_exception()
            self.__wait_a_little()
            raise AuthenticationBadData

        if fVerifyIndex:
            self.__verify_index(anchor, i, id)

        return args, id


    def __verify_index(self, anchor, i, id):
        """
        Manage messages ids to prevent replay of old messages.
        """

        try:
            try:
                self.m_lock.acquire()

                if anchor != self.m_index_anchor_in:
                    raise AuthenticationBadIndex(self.m_max_index, self.m_index_anchor_in)

                if i > self.m_max_index + INDEX_TABLE_SIZE // 2:
                    raise AuthenticationBadIndex(self.m_max_index, self.m_index_anchor_in)

                i_mod = i % INDEX_TABLE_SIZE
                (iv, idl) = self.m_index_table.get(i_mod, (None, None))

                #print >> sys.__stderr__, i, i_mod, iv, self.m_max_index

                if (iv is None) or (i > iv):
                    idl = [id]
                elif (iv == i) and (not id in idl):
                    idl.append(id)
                else:
                    raise AuthenticationBadIndex(self.m_max_index, self.m_index_anchor_in)

                self.m_index_table[i_mod] = (i, idl)

                if i > self.m_max_index:
                    self.m_max_index = i

                return self.m_index

            finally:
                self.m_lock.release()

        except:
            self.__wait_a_little()
            raise


    def __wait_a_little(self):
        self.m_failure_lock.acquire()
        time.sleep((1.0 + random.random()) / 2)
        self.m_failure_lock.release()



#
# --------------------------------- Events List --------------------------
#


#
# --------------------------------- Event Manager --------------------------
#


class CEventQueue:
    """
    Add queue semantics above an event dispatcher.
    Instead of firing event callbacks, new events are returned in a list
    upon request.

    Events are stored in a FIFO of size MAX_EVENT_LIST_LENGTH (defaults to 1000)

    """

    def __init__(self, event_dispatcher, max_event_list_length = MAX_EVENT_LIST_LENGTH):
        self.m_event_dispatcher = event_dispatcher

        self.m_event_lock = threading.Condition()
        self.m_max_event_list_length = max_event_list_length
        self.m_event_list = []
        self.m_event_index = 0

        self.m_n_waiters = []


    def shutdown(self):
        self.m_event_dispatcher.remove_callback(self.event_handler)


    def register_event_types(self, event_type_dict):
        self.m_event_dispatcher.register_callback(self.event_handler, event_type_dict, fSingleUse = False)


    def event_handler(self, event):
        try:
            self.m_event_lock.acquire()

            if isinstance(event, CEventSyncReceivers):
                t0 = time.time()
                while len(self.m_n_waiters) < event.m_sync_n and time.time() < t0 + HEARTBEAT_TIMEOUT:
                    time.sleep(0.1)

            self.m_event_list.append(event)
            if len(self.m_event_list) > self.m_max_event_list_length:
                self.m_event_list.pop(0)

            self.m_event_index += 1
            lock_notify_all(self.m_event_lock)

        finally:
            self.m_event_lock.release()


    def get_event_index(self):
        return self.m_event_index


    def wait_for_event(self, timeout, event_index):
        """
        Return the events above index event_index which were fired.
        """

        try:
            self.m_n_waiters.append(0)

            self.m_event_lock.acquire()
            if event_index >= self.m_event_index:
                safe_wait(self.m_event_lock, timeout)

            if event_index >= self.m_event_index:
                return (self.m_event_index, [])

            sub_event_list = self.m_event_list[event_index - self.m_event_index:]
            return (self.m_event_index, sub_event_list)

        finally:
            self.m_n_waiters.pop()

            self.m_event_lock.release()


#
# -------------------------------------- Break Info manager ---------------------------------------
#



#
# -------------------------------- Break Point Manager -----------------------------
#


#
# ----------------------------------- Core Debugger ------------------------------------
#



class CCodeContext:
    """
    Class represents info related to code objects.
    """

    def __init__(self, frame, bp_manager):
        self.m_code = frame.f_code
        self.m_filename = calc_frame_path(frame)
        self.m_basename = os.path.basename(self.m_filename)

        self.m_file_breakpoints = bp_manager.get_active_break_points_by_file(self.m_filename)

        self.m_fExceptionTrap = False


    def is_untraced(self):
        """
        Return True if this code object should not be traced.
        """

        return self.m_basename in [THREADING_FILENAME, DEBUGGER_FILENAME]


    def is_exception_trap_frame(self):
        """
        Return True if this frame should be a trap for unhandled
        exceptions.
        """

        if self.m_basename == THREADING_FILENAME:
            return True

        if self.m_basename == DEBUGGER_FILENAME and self.m_code.co_name in ['__execv', '__execve', '__function_wrapper']:
            return True

        return False



class CDebuggerCoreThread:
    """
    Class represents a debugged thread.
    This is a core structure of the debugger. It includes most of the
    optimization tricks and hacks, and includes a good amount of
    subtle bug fixes, be carefull not to mess it up...
    """

    def __init__(self, name, core_debugger, frame, event):
        self.m_thread_id = thread.get_ident()
        self.m_thread_name = name
        self.m_fBroken = False
        self.m_fUnhandledException = False

        self.m_frame = frame
        self.m_event = event
        self.m_ue_lineno = None
        self.m_uef_lineno = None

        self.m_code_context = core_debugger.get_code_context(frame)

        self.m_locals_copy = {}

        self.m_core = core_debugger
        self.m_bp_manager = core_debugger.m_bp_manager

        self.m_frame_lock = threading.Condition()
        self.m_frame_external_references = 0

        self.m_exc_info = None

        self.m_depth = 0
        self.set_depth(frame)


    def set_depth(self, frame):
        self.m_depth = 0
        while frame is not None:
            self.m_depth += 1
            frame = frame.f_back


    def profile_recursion(self, frame, event, arg):
        if event == 'call':
            if self.m_depth > g_recursionlimit:
                print_debug('Exceeded recursion limit and caught in profile function.')

                try:
                    #
                    # The allowed recursion limit was exceeded.
                    # To view the offending script frame, go two frames
                    # down the stack with the 'down' console command.
                    #
                    raise RuntimeError('maximum recursion depth exceeded')

                except:
                    #
                    # Schedule the debugger to re-enable the profile hook.
                    #
                    self.set_tracers(fsignal_exception = True)
                    raise

        elif event == 'return':
            return self.profile(frame, event, arg)



    def profile(self, frame, event, arg):
        """
        Profiler method.
        The Python profiling mechanism is used by the debugger
        mainly to handle synchronization issues related to the
        life time of the frame structure.
        """
        #print_debug('profile: %s, %s, %s, %s, %s' % (repr(frame), event, frame.f_code.co_name, frame.f_code.co_filename, repr(arg)[:40]))

        if event == 'return':
            self.m_depth -= 1

            if sys.excepthook != g_excepthook:
                set_excepthook()

            self.m_frame = frame.f_back

            try:
                self.m_code_context = self.m_core.m_code_contexts[self.m_frame.f_code]
            except AttributeError:
                if self.m_event != 'return' and self.m_core.m_ftrap:
                    #
                    # An exception is raised from the outer-most frame.
                    # This means an unhandled exception.
                    #

                    self.m_frame = frame
                    self.m_event = 'exception'

                    self.m_uef_lineno = self.m_ue_lineno

                    self.m_fUnhandledException = True
                    self.m_core._break(self, frame, event, arg)

                    self.m_uef_lineno = None

                    if frame in self.m_locals_copy:
                        self.update_locals()

                    self.m_frame = None

                self.m_core.remove_thread(self.m_thread_id)
                sys.setprofile(None)
                sys.settrace(self.m_core.trace_dispatch_init)

            if self.m_frame_external_references == 0:
                return

            #
            # Wait until no one references the frame object
            #

            try:
                self.m_frame_lock.acquire()

                while self.m_frame_external_references != 0:
                    safe_wait(self.m_frame_lock, 1.0)

            finally:
                self.m_frame_lock.release()


    def frame_acquire(self):
        """
        Aquire a reference to the frame.
        """

        try:
            self.m_frame_lock.acquire()

            self.m_frame_external_references += 1
            f = self.m_frame
            if f is None:
                raise ThreadDone

            return f

        finally:
            self.m_frame_lock.release()


    def frame_release(self):
        """
        Release a reference to the frame.
        """

        try:
            self.m_frame_lock.acquire()

            self.m_frame_external_references -= 1
            if self.m_frame_external_references == 0:
                self.m_frame_lock.notify()

        finally:
            self.m_frame_lock.release()


    def get_frame(self, base_frame, index, fException = False):
        """
        Get frame at index depth down the stack.
        Starting from base_frame return the index depth frame
        down the stack. If fException is True use the exception
        stack (traceback).

        Arguments:
            - base_frame: frame
            - index: positive number, index of the targetted frame
            - fException: boolean, look for frame of the current xception if True

        Returns: (f, lineno)
        - f: current frame object
        - lineno: line number of the current code
        """

        if fException:
            tb = get_traceback(base_frame, self)
            if tb is None:
                raise NoExceptionFound

            while tb.tb_next is not None:
                tb = tb.tb_next

            f = tb.tb_frame
        else:
            f = base_frame

        while f is not None:
            if is_func_hidden( f.f_code.co_name ):
                f = f.f_back
                continue

            if index <= 0:
                break

            f = f.f_back
            index -= 1

        if (index < 0) or (f is None):
            raise InvalidFrame

        if (self.m_uef_lineno is not None) and (f.f_back is None):
            lineno = self.m_uef_lineno
        else:
            lineno = f.f_lineno

        if fException:
            tb = get_traceback(base_frame, self)
            while tb is not None:
                if tb.tb_frame == f:
                    lineno = tb.tb_lineno
                    break
                tb = tb.tb_next

        return (f, lineno)


    def get_locals_copy(self, frame_index, fException, fReadOnly):
        """
        Get globals and locals of frame.
        A copy scheme is used for locals to work around a bug in
        Python 2.3 and 2.4 that prevents modifying the local dictionary.

        Returns: (gc, lc, olc):
        - gc: copy of global ...
        - lc: copy of local ...
        - olc: copy of local ...
        """

        try:
            base_frame = self.frame_acquire()

            (f, lineno) = self.get_frame(base_frame, frame_index, fException)

            if fReadOnly:
                gc = copy.copy(f.f_globals)
            else:
                gc = f.f_globals

            try:
                (lc, olc) = self.m_locals_copy[f]

            except KeyError:
                if f.f_code.co_name in [MODULE_SCOPE, MODULE_SCOPE2]:
                    lc = gc
                    olc = gc

                else:
                    lc = copy.copy(f.f_locals)
                    olc = copy.copy(lc)

                    if not fReadOnly:
                        self.m_locals_copy[f] = (lc, olc)
                        self.set_local_trace(f)

            return (gc, lc, olc)

        finally:
            f = None
            base_frame = None

            self.frame_release()


    def update_locals_copy(self):
        """
        Update copy of locals with changes in locals.
        """

        lct = self.m_locals_copy.get(self.m_frame, None)
        if lct is None:
            return

        (lc, base) = lct
        cr = copy.copy(self.m_frame.f_locals)

        for k in cr:
            if not k in base:
                lc[k] = cr[k]
                continue

            if not cr[k] is base[k]:
                lc[k] = cr[k]


    def update_locals(self):
        """
        Update locals with changes from copy of locals.
        """

        lct = self.m_locals_copy.pop(self.m_frame, None)
        if lct is None:
            return

        self.m_frame.f_locals.update(lct[0])


    def __eval_breakpoint(self, frame, bp):
        """
        Return True if the breakpoint is hit.
        """

        if not bp.m_fEnabled:
            return False

        if bp.m_expr == '':
            return True

        try:
            if frame in self.m_locals_copy:
                l = self.m_locals_copy[frame][0]
                v = eval(bp.m_code, frame.f_globals, l)
            else:
                v = eval(bp.m_code, frame.f_globals, frame.f_locals)

            return (v != False)

        except:
            return False


    def set_local_trace(self, frame, fsignal_exception = False):
        """
        Set trace callback of frame.
        Specialized trace methods are selected here to save switching time
        during actual tracing.
        """

        if not self.m_core.m_ftrace:
            frame.f_trace = self.trace_dispatch_stop
            return

        if fsignal_exception:
            frame.f_trace = self.trace_dispatch_signal
            return

        code_context = self.m_core.get_code_context(frame)

        if self.m_core.is_break(self, frame):
            frame.f_trace = self.trace_dispatch_break

        elif code_context.m_fExceptionTrap or (frame.f_back is None):
            frame.f_trace = self.trace_dispatch_trap

        elif frame.f_code.co_name in self.m_bp_manager.m_break_points_by_function:
            frame.f_trace = self.trace_dispatch

        elif frame in self.m_locals_copy:
            frame.f_trace = self.trace_dispatch

        elif frame == self.m_core.m_return_frame:
            frame.f_trace = self.trace_dispatch

        else:
            del frame.f_trace


    def set_tracers(self, fsignal_exception = False):
        """
        Set trace callbacks for all frames in stack.
        """

        try:
            try:
                f = self.frame_acquire()
                while f is not None:
                    self.set_local_trace(f, fsignal_exception)
                    f = f.f_back

            except ThreadDone:
                f = None

        finally:
            f = None
            self.frame_release()


    def trace_dispatch_stop(self, frame, event, arg):
        """
        Disable tracing for this thread.
        """

        if frame in self.m_locals_copy:
            self.update_locals()

        sys.settrace(None)
        sys.setprofile(None)
        return None


    def trace_dispatch_break(self, frame, event, arg):
        """
        Trace method for breaking a thread.
        """

        if event not in ['line', 'return', 'exception']:
            return frame.f_trace

        if event == 'exception':
            self.set_exc_info(arg)

        self.m_event = event

        if frame in self.m_locals_copy:
            self.update_locals_copy()

        self.m_core._break(self, frame, event, arg)

        if frame in self.m_locals_copy:
            self.update_locals()
            self.set_local_trace(frame)

        return frame.f_trace


    def trace_dispatch_call(self, frame, event, arg):
        """
        Initial trace method for thread.
        """

        if not self.m_core.m_ftrace:
            return self.trace_dispatch_stop(frame, event, arg)

        self.m_depth += 1
        if self.m_depth > g_recursionlimit:
            sys.setprofile(self.profile_recursion)

        self.m_frame = frame

        try:
            self.m_code_context = self.m_core.m_code_contexts[frame.f_code]
        except KeyError:
            self.m_code_context = self.m_core.get_code_context(frame)

        if self.m_core.m_fBreak or (self.m_core.m_step_tid == self.m_thread_id):
            self.m_event = event
            self.m_core._break(self, frame, event, arg)
            if frame in self.m_locals_copy:
                self.update_locals()
                self.set_local_trace(frame)
            return frame.f_trace

        if not frame.f_code.co_name in self.m_bp_manager.m_break_points_by_function:
            return None

        bp = self.m_code_context.m_file_breakpoints.get(frame.f_lineno, None)
        if bp is not None and self.__eval_breakpoint(frame, bp):
            self.m_event = event
            self.m_core._break(self, frame, event, arg)
            if frame in self.m_locals_copy:
                self.update_locals()
                self.set_local_trace(frame)
            return frame.f_trace

        return self.trace_dispatch


    def trace_dispatch(self, frame, event, arg):
        """
        General trace method for thread.
        """

        if (event == 'line'):
            if frame in self.m_locals_copy:
                self.update_locals_copy()

            bp = self.m_code_context.m_file_breakpoints.get(frame.f_lineno, None)

            if bp is not None and self.__eval_breakpoint(frame, bp):
                self.m_event = event
                self.m_core._break(self, frame, event, arg)

            if frame in self.m_locals_copy:
                self.update_locals()
                self.set_local_trace(frame)

            return frame.f_trace

        if event == 'return':
            if frame in self.m_locals_copy:
                self.update_locals_copy()

            if frame == self.m_core.m_return_frame:
                self.m_event = event
                self.m_core._break(self, frame, event, arg)

            if frame in self.m_locals_copy:
                self.update_locals()

            return None

        if event == 'exception':
            if frame in self.m_locals_copy:
                self.update_locals()
                self.set_local_trace(frame)

            if not is_py3k() and not frame.f_exc_traceback is arg[2]:
                (frame.f_exc_type, frame.f_exc_value, frame.f_exc_traceback) = arg

            return frame.f_trace

        return frame.f_trace


    def trace_dispatch_trap(self, frame, event, arg):
        """
        Trace method used for frames in which unhandled exceptions
        should be caught.
        """

        if (event == 'line'):
            self.m_event = event

            if frame in self.m_locals_copy:
                self.update_locals_copy()

            bp = self.m_code_context.m_file_breakpoints.get(frame.f_lineno, None)
            if bp is not None and self.__eval_breakpoint(frame, bp):
                self.m_core._break(self, frame, event, arg)

            if frame in self.m_locals_copy:
                self.update_locals()
                self.set_local_trace(frame)

            return frame.f_trace

        if event == 'return':
            last_event = self.m_event
            self.m_event = event

            if frame in self.m_locals_copy:
                self.update_locals_copy()

            if frame == self.m_core.m_return_frame:
                self.m_core._break(self, frame, event, arg)

            if frame in self.m_locals_copy:
                self.update_locals()

            if last_event == 'exception':
                self.m_event = last_event

            return None

        if event == 'exception':
            self.m_event = event

            if self.m_code_context.m_fExceptionTrap and self.m_core.m_ftrap:
                self.set_exc_info(arg)

                self.m_fUnhandledException = True
                self.m_core._break(self, frame, event, arg)

                if frame in self.m_locals_copy:
                    self.update_locals()

                return frame.f_trace

            self.m_ue_lineno = frame.f_lineno

            if frame in self.m_locals_copy:
                self.update_locals()
                self.set_local_trace(frame)

            if is_py3k():
                self.set_exc_info(arg)
            elif not frame.f_exc_traceback is arg[2]:
                (frame.f_exc_type, frame.f_exc_value, frame.f_exc_traceback) = arg

            return frame.f_trace

        return frame.f_trace


    def trace_dispatch_signal(self, frame, event, arg):
        #print_debug('*** trace_dispatch_signal %s, %s, %s' % (frame.f_lineno, event, repr(arg)))
        self.set_exc_info(arg)
        self.set_tracers()
        self.set_depth(frame)
        sys.setprofile(self.profile)

        return self.trace_dispatch_trap(frame, event, arg)


    def set_exc_info(self, arg):
        """
        Set exception information.
        """

        if arg == None:
            return

        if is_py3k():
            self.m_exc_info = arg
            return

        (t, v, tb) = arg

        while tb is not None:
            f = tb.tb_frame
            f.f_exc_type = t
            f.f_exc_value = v
            f.f_exc_traceback = tb

            tb = tb.tb_next


    def get_exc_info(self):
        return self.m_exc_info


    def reset_exc_info(self):
        self.m_exc_info = None


    def is_breakpoint(self):
        """
        Calc if current line is hit by breakpoint.
        """

        bp = self.m_code_context.m_file_breakpoints.get(self.m_frame.f_lineno, None)
        if bp is not None and self.__eval_breakpoint(self.m_frame, bp):
            return True

        return False


    def get_breakpoint(self):
        """
        Return current line breakpoint if any.
        """

        return self.m_code_context.m_file_breakpoints.get(self.m_frame.f_lineno, None)



class CDebuggerCore:
    """
    Base class for the debugger.
    Handles basic debugger functionality.
    """

    def __init__(self, fembedded = False):
        self.m_ftrace = True

        self.m_current_ctx = None
        self.m_f_first_to_break = True
        self.m_f_break_on_init = False

        self.m_builtins_hack = None

        self.m_timer_embedded_giveup = None

        self.m_threads_lock = threading.Condition()

        self.m_threads = {}

        self.m_event_dispatcher = CEventDispatcher()
        self.m_state_manager = CStateManager(STATE_RUNNING, self.m_event_dispatcher)

        self.m_ffork_into_child = False
        self.m_ffork_auto = False

        self.m_fsynchronicity = True
        self.m_ftrap = True
        self.m_fUnhandledException = False
        self.m_fBreak = False

        self.m_lastest_event = None
        self.m_step_tid = None
        self.m_next_frame = None
        self.m_return_frame = None
        self.m_saved_step = (None, None, None)
        self.m_saved_next = None

        self.m_bp_manager = CBreakPointsManager()

        self.m_code_contexts = {None: None}

        self.m_fembedded = fembedded
        self.m_embedded_event = threading.Event()
        self.m_embedded_sync_t0 = 0
        self.m_embedded_sync_t1 = 0

        self.m_heartbeats = {0: time.time() + 3600}


    def shutdown(self):
        self.m_event_dispatcher.shutdown()
        self.m_state_manager.shutdown()


    def is_embedded(self):
        return self.m_fembedded


    def send_fork_switch(self, sync_n):
        """
        Notify client that debuggee is forking and that it should
        try to reconnect to the child.
        """

        print_debug('Sending fork switch event')

        event = CEventForkSwitch(sync_n)
        self.m_event_dispatcher.fire_event(event)


    def send_exec_switch(self, sync_n):
        """
        Notify client that debuggee is doing an exec and that it should
        try to reconnect (in case the exec failed).
        """

        print_debug('Sending exec switch event')

        event = CEventExecSwitch(sync_n)
        self.m_event_dispatcher.fire_event(event)


    def send_event_exit(self):
        """
        Notify client that the debuggee is shutting down.
        """

        event = CEventExit()
        self.m_event_dispatcher.fire_event(event)


    def send_events(self, event):
        pass


    def set_request_go_timer(self, timeout):
        """
        Set timeout thread to release debugger from waiting for a client
        to attach.
        """

        self.cancel_request_go_timer()

        if timeout is None:
            return

        _timeout = max(1.0, timeout)

        f = lambda: (
            self.record_client_heartbeat(0, False, True),
            self.request_go()
            )

        self.m_timer_embedded_giveup = threading.Timer(_timeout, f)
        self.m_timer_embedded_giveup.start()

        #
        # sleep() releases control and allow timer thread to actually start
        # before this scope returns.
        #
        time.sleep(0.1)


    def cancel_request_go_timer(self):
        t = self.m_timer_embedded_giveup
        if t is not None:
            self.m_timer_embedded_giveup = None
            t.cancel()


    def setbreak(self, f):
        """
        Set thread to break on next statement.
        """

        if not self.m_ftrace:
            return

        tid = thread.get_ident()

        if not tid in self.m_threads:
            return self.settrace(f)

        ctx = self.m_threads[tid]
        f.f_trace = ctx.trace_dispatch_break
        self.m_saved_next = self.m_next_frame
        self.m_next_frame = f


    def settrace(self, f = None, f_break_on_init = True, timeout = None, builtins_hack = None):
        """
        Start tracing mechanism for thread.
        """

        if not self.m_ftrace:
            return

        tid = thread.get_ident()
        if tid in self.m_threads:
            return

        self.set_request_go_timer(timeout)

        self.m_f_break_on_init = f_break_on_init
        self.m_builtins_hack = builtins_hack

        threading.settrace(self.trace_dispatch_init)
        sys.settrace(self.trace_dispatch_init)

        if f is not None:
            f.f_trace = self.trace_dispatch_init


    def stoptrace(self):
        """
        Stop tracing mechanism.
        """

        global g_fignore_atexit

        g_fignore_atexit = True

        threading.settrace(None)
        sys.settrace(None)
        sys.setprofile(None)

        self.m_ftrace = False
        self.set_all_tracers()

        try:
            self.request_go()
        except DebuggerNotBroken:
            pass

        #self.m_threads = {}


    def get_code_context(self, frame):
        try:
            return self.m_code_contexts[frame.f_code]
        except KeyError:
            if self.m_builtins_hack != None:
                if calc_frame_path(frame) == self.m_builtins_hack:
                    self.m_builtins_hack = None
                    frame.f_globals['__builtins__'] = g_builtins_module

            code_context = CCodeContext(frame, self.m_bp_manager)
            return self.m_code_contexts.setdefault(frame.f_code, code_context)


    def get_current_ctx(self):
        if len(self.m_threads) == 0:
            raise NoThreads

        return self.m_current_ctx


    def get_ctx(self, tid):
        ctx = self.m_threads.get(tid, None)
        if ctx == None:
            raise ThreadNotFound

        return ctx


    def wait_for_first_thread(self):
        """
        Wait until at least one debuggee thread is alive.
        Python can have 0 threads in some circumstances as
        embedded Python and the Python interpreter console.
        """

        if self.m_current_ctx is not None:
            return

        try:
            self.m_threads_lock.acquire()

            while self.m_current_ctx is None:
                safe_wait(self.m_threads_lock, 1.0)

        finally:
            self.m_threads_lock.release()


    def notify_first_thread(self):
        """
        Notify that first thread is available for tracing.
        """

        try:
            self.m_threads_lock.acquire()
            self.m_threads_lock.notify()
        finally:
            self.m_threads_lock.release()


    def set_exception_trap_frame(self, frame):
        """
        Set trap for unhandled exceptions in relevant frame.
        """

        while frame is not None:
            code_context = self.get_code_context(frame)
            if code_context.is_exception_trap_frame():
                code_context.m_fExceptionTrap = True
                return

            frame = frame.f_back


    def __set_signal_handler(self):
        """
        Set rpdb2 to wrap all signal handlers.
        """
        for key, value in list(vars(signal).items()):
            if not key.startswith('SIG') or key in ['SIG_IGN', 'SIG_DFL', 
                'SIGRTMIN', 'SIGRTMAX', 'SIG_BLOCK', 'SIG_UNBLOCK', 'SIG_SETMASK' ]:
                continue

            handler = signal.getsignal(value)
            if handler in [signal.SIG_IGN, signal.SIG_DFL]:
                continue

            try:
                signal.signal(value, handler)
            except:
                print_debug('Failed to set signal handler for signal %s(%d)' % (key, value))


    def clear_source_cache(self):
        g_lines_cache.clear()

        event = CEventClearSourceCache()
        self.m_event_dispatcher.fire_event(event)


    def trace_dispatch_init(self, frame, event, arg):
        """
        Initial tracing method.
        """

        if event not in ['call', 'line', 'return']:
            return None

        code_context = self.get_code_context(frame)
        if event == 'call' and code_context.is_untraced():
            return None

        self.set_exception_trap_frame(frame)

        try:
            t = current_thread()
            name = thread_get_name(t)
        except:
            name = ''

        if name == 'MainThread':
            self.__set_signal_handler()

        ctx = CDebuggerCoreThread(name, self, frame, event)
        ctx.set_tracers()

        try:
            self.m_threads_lock.acquire()

            self.m_threads[ctx.m_thread_id] = ctx
            nthreads = len(self.m_threads)

            if nthreads == 1:
                self.prepare_embedded_sync()

        finally:
            self.m_threads_lock.release()

        if nthreads == 1:
            self.clear_source_cache()

            self.m_current_ctx = ctx
            self.notify_first_thread()

            if self.m_f_break_on_init:
                self.m_f_break_on_init = False
                self.request_break()

        sys.settrace(ctx.trace_dispatch_call)
        sys.setprofile(ctx.profile)

        self.wait_embedded_sync(nthreads == 1)

        if event == 'call':
            return ctx.trace_dispatch_call(frame, event, arg)
        elif hasattr(frame, 'f_trace') and (frame.f_trace is not None):
            return frame.f_trace(frame, event, arg)
        else:
            return None


    def prepare_embedded_sync(self):
        if not self.m_fembedded:
            return

        t = time.time()
        t0 = self.m_embedded_sync_t0

        if t0 != 0:
            self.fix_heartbeats(t - t0)

        if self.get_clients_attached() == 0:
            return

        if t - t0 < EMBEDDED_SYNC_THRESHOLD:
            return

        self.m_embedded_sync_t1 = t
        self.m_embedded_event.clear()


    def wait_embedded_sync(self, ftrigger):
        if not self.m_fembedded:
            return

        t = time.time()
        t0 = self.m_embedded_sync_t0
        t1 = self.m_embedded_sync_t1

        if t - t0 < EMBEDDED_SYNC_THRESHOLD:
            return

        if t - t1 >= EMBEDDED_SYNC_TIMEOUT:
            return

        if ftrigger:
            event = CEventEmbeddedSync()
            self.m_event_dispatcher.fire_event(event)

        safe_wait(self.m_embedded_event, EMBEDDED_SYNC_TIMEOUT - (t - t1))

        if ftrigger:
            self.m_embedded_sync_t1 = 0


    def embedded_sync(self):
        self.m_embedded_event.set()


    def set_all_tracers(self):
        """
        Set trace methods for all frames of all threads.
        """

        for ctx in list(self.m_threads.values()):
            ctx.set_tracers()


    def remove_thread(self, thread_id):
        try:
            del self.m_threads[thread_id]

            if self.m_current_ctx.m_thread_id == thread_id:
                self.m_current_ctx = list(self.m_threads.values())[0]

        except (KeyError, IndexError):
            self.m_embedded_sync_t0 = time.time()


    def set_break_flag(self):
        self.m_fBreak = (self.m_state_manager.get_state() == STATE_BROKEN)


    def is_break(self, ctx, frame, event = None):
        if self.m_fBreak:
            return True

        if ctx.m_fUnhandledException:
            return True

        if self.m_step_tid == ctx.m_thread_id:
            return True

        if self.m_next_frame == frame:
            return True

        if (self.m_return_frame == frame) and (event == 'return'):
            return True

        return False


    def record_client_heartbeat(self, id, finit, fdetach):
        """
        Record that client id is still attached.
        """

        if finit:
            self.m_heartbeats.pop(0, None)

        if fdetach:
            self.m_heartbeats.pop(id, None)
            return

        if finit or id in self.m_heartbeats:
            self.m_heartbeats[id] = time.time()


    def fix_heartbeats(self, missing_pulse):
        for k, v in list(self.m_heartbeats.items()):
            self.m_heartbeats[k] = v + missing_pulse


    def get_clients_attached(self):
        n = 0
        t = time.time()

        for v in list(self.m_heartbeats.values()):
            if t < v + HEARTBEAT_TIMEOUT:
                n += 1

        return n


    def is_waiting_for_attach(self):
        if self.get_clients_attached() != 1:
            return False

        if list(self.m_heartbeats.keys()) != [0]:
            return False

        return True


    def _break(self, ctx, frame, event, arg):
        """
        Main break logic.
        """

        global g_fos_exit
        global g_module_main

        if not self.is_break(ctx, frame, event) and not ctx.is_breakpoint():
            ctx.set_tracers()
            return

        ctx.m_fBroken = True
        f_full_notification = False
        f_uhe_notification = False

        step_tid = self.m_step_tid

        try:
            self.m_state_manager.acquire()
            if self.m_state_manager.get_state() != STATE_BROKEN:
                self.set_break_dont_lock()

            if g_module_main == -1:
                try:
                    g_module_main = sys.modules['__main__']
                except:
                    g_module_main = None

            if not is_py3k() and not frame.f_exc_traceback is None:
                ctx.set_exc_info((frame.f_exc_type, frame.f_exc_value, frame.f_exc_traceback))

            if is_py3k() and ctx.get_exc_info() == None and sys.exc_info()[2] != None:
                ctx.set_exc_info(sys.exc_info())

            try:
                t = current_thread()
                ctx.m_thread_name = thread_get_name(t)
            except:
                pass

            if ctx.m_fUnhandledException and not self.m_fUnhandledException:
                self.m_fUnhandledException = True
                f_uhe_notification = True

            if self.is_auto_fork_first_stage(ctx.m_thread_id):
                self.m_saved_step = (self.m_step_tid, self.m_saved_next, self.m_return_frame)
                self.m_saved_next = None
                self.m_bp_manager.m_fhard_tbp = True

            if self.m_f_first_to_break or (self.m_current_ctx == ctx):
                self.m_current_ctx = ctx
                self.m_lastest_event = event

                self.m_step_tid = None
                self.m_next_frame = None
                self.m_return_frame = None
                self.m_saved_next = None

                self.m_bp_manager.del_temp_breakpoint(breakpoint = ctx.get_breakpoint())

                self.m_f_first_to_break = False
                f_full_notification = True

        finally:
            self.m_state_manager.release()

        ffork_second_stage = self.handle_fork(ctx)
        self.handle_exec(ctx)

        if self.is_auto_fork_first_stage(ctx.m_thread_id):
            self.request_go_quiet()

        elif self.m_ffork_auto and ffork_second_stage:
            (self.m_step_tid, self.m_next_frame, self.m_return_frame) = self.m_saved_step
            self.m_saved_step = (None, None, None)
            self.m_bp_manager.m_fhard_tbp = False
            self.request_go_quiet()

        elif self.get_clients_attached() == 0:
            #print_debug('state: %s' % self.m_state_manager.get_state())
            self.request_go_quiet()

        elif step_tid == ctx.m_thread_id and is_func_hidden( frame.f_code.co_name ):
            self.request_step_quiet()

        else:
            if f_full_notification:
                self.send_events(None)
            else:
                self.notify_thread_broken(ctx.m_thread_id, ctx.m_thread_name)
                self.notify_namespace()

            if f_uhe_notification:
                self.send_unhandled_exception_event()

            state = self.m_state_manager.wait_for_state([STATE_RUNNING])

        self.prepare_fork_step(ctx.m_thread_id)
        self.prepare_exec_step(ctx.m_thread_id)

        ctx.m_fUnhandledException = False
        ctx.m_fBroken = False
        ctx.set_tracers()
        ctx.reset_exc_info()

        if g_fos_exit:
            g_fos_exit = False
            self.send_event_exit()
            time.sleep(1.0)
            self.stoptrace()


    def is_auto_fork_first_stage(self, tid):
        if not self.m_ffork_auto:
            return False

        return tid == g_forktid and g_forkpid == None


    def prepare_fork_step(self, tid):
        global g_forkpid
        global g_ignore_broken_pipe

        if tid != g_forktid:
            return

        self.m_step_tid = tid
        g_forkpid = os.getpid()

        if not self.m_ffork_into_child:
            return

        n = self.get_clients_attached()
        self.send_fork_switch(n)
        time.sleep(0.5)
        g_server.shutdown()
        CThread.joinAll()

        g_ignore_broken_pipe = time.time()


    def handle_fork(self, ctx):
        global g_forktid
        global g_forkpid

        tid = ctx.m_thread_id

        if g_forkpid == None or tid != g_forktid:
            return False

        forkpid = g_forkpid
        g_forkpid = None
        g_forktid = None

        if os.getpid() == forkpid:
            #
            # Parent side of fork().
            #

            if not self.m_ffork_into_child:
                #CThread.clearJoin()
                #g_server.jumpstart()

                return True

            self.stoptrace()
            return False

        #
        # Child side of fork().
        #

        if not self.m_ffork_into_child:
            self.stoptrace()
            return False

        self.m_threads = {tid: ctx}

        CThread.clearJoin()
        g_server.jumpstart()

        return True


    def prepare_exec_step(self, tid):
        global g_execpid

        if tid != g_exectid:
            return

        self.m_step_tid = tid
        g_execpid = os.getpid()

        n = self.get_clients_attached()
        self.send_exec_switch(n)
        time.sleep(0.5)
        g_server.shutdown()
        CThread.joinAll()


    def handle_exec(self, ctx):
        global g_exectid
        global g_execpid

        tid = ctx.m_thread_id

        if g_execpid == None or tid != g_exectid:
            return False

        g_execpid = None
        g_exectid = None

        #
        # If we are here it means that the exec failed.
        # Jumpstart the debugger to allow debugging to continue.
        #

        CThread.clearJoin()
        g_server.jumpstart()

        return True


    def notify_thread_broken(self, tid, name):
        """
        Notify that thread (tid) has broken.
        This notification is sent for each thread that breaks after
        the first one.
        """

        _event = CEventThreadBroken(tid, name)
        self.m_event_dispatcher.fire_event(_event)


    def notify_namespace(self):
        """
        Notify that a namespace update query should be done.
        """

        _event = CEventNamespace()
        self.m_event_dispatcher.fire_event(_event)


    def get_state(self):
        return self.m_state_manager.get_state()


    def verify_broken(self):
        if self.m_state_manager.get_state() != STATE_BROKEN:
            raise DebuggerNotBroken


    def get_current_filename(self, frame_index, fException):
        """
        Return path of sources corresponding to the frame at depth
        'frame_index' down the stack of the current thread.
        """

        ctx = self.get_current_ctx()

        try:
            f = None
            base_frame = ctx.frame_acquire()

            (f, frame_lineno) = ctx.get_frame(base_frame, frame_index, fException)
            frame_filename = calc_frame_path(f)

            return frame_filename

        finally:
            f = None
            base_frame = None
            ctx.frame_release()


    def get_threads(self):
        return self.m_threads


    def set_break_dont_lock(self):
        self.m_f_first_to_break = True

        self.m_state_manager.set_state(STATE_BROKEN, fLock = False)

        self.set_break_flag()
        self.set_all_tracers()


    def request_break(self):
        """
        Ask debugger to break (pause debuggee).
        """

        if len(self.m_threads) == 0:
            self.wait_for_first_thread()

        try:
            self.m_state_manager.acquire()
            if self.m_state_manager.get_state() == STATE_BROKEN:
                return

            self.set_break_dont_lock()

        finally:
            self.m_state_manager.release()

        self.send_events(None)


    def request_go_quiet(self, fLock = True):
        try:
            self.request_go(fLock)

        except DebuggerNotBroken:
            pass


    def request_go(self, fLock = True):
        """
        Let debugger run.
        """

        try:
            if fLock:
                self.m_state_manager.acquire()

            self.verify_broken()

            self.m_fUnhandledException = False
            self.m_state_manager.set_state(STATE_RUNNING, fLock = False)

            if self.m_fembedded:
                time.sleep(0.33)

            self.set_break_flag()

        finally:
            if fLock:
                self.m_state_manager.release()


    def request_go_breakpoint(self, filename, scope, lineno, frame_index, fException):
        """
        Let debugger run until temp breakpoint as defined in the arguments.
        """

        assert(is_unicode(filename))
        assert(is_unicode(scope))

        try:
            self.m_state_manager.acquire()
            self.verify_broken()

            if filename in [None, '']:
                _filename = self.get_current_filename(frame_index, fException)
            elif not is_provider_filesystem(filename):
                _filename = as_string(filename, sys.getfilesystemencoding())
            else:
                _filename = FindFile(filename, fModules = True)

            self.m_bp_manager.set_temp_breakpoint(_filename, scope, lineno)
            self.set_all_tracers()
            self.request_go(fLock = False)

        finally:
            self.m_state_manager.release()


    def request_step_quiet(self, fLock = True):
        try:
            self.request_step(fLock)

        except DebuggerNotBroken:
            pass


    def request_step(self, fLock = True):
        """
        Let debugger run until next statement is reached or a breakpoint
        is hit in another thread.
        """

        try:
            if fLock:
                self.m_state_manager.acquire()

            self.verify_broken()

            try:
                ctx = self.get_current_ctx()
            except NoThreads:
                return

            self.m_step_tid = ctx.m_thread_id
            self.m_next_frame = None
            self.m_return_frame = None

            self.request_go(fLock = False)

        finally:
            if fLock:
                self.m_state_manager.release()


    def request_next(self):
        """
        Let debugger run until next statement in the same frame
        is reached or a breakpoint is hit in another thread.
        """

        try:
            self.m_state_manager.acquire()
            self.verify_broken()

            try:
                ctx = self.get_current_ctx()
            except NoThreads:
                return

            if self.m_lastest_event in ['return', 'exception']:
                return self.request_step(fLock = False)

            self.m_next_frame = ctx.m_frame
            self.m_return_frame = None

            self.request_go(fLock = False)

        finally:
            self.m_state_manager.release()


    def request_return(self):
        """
        Let debugger run until end of frame frame is reached
        or a breakpoint is hit in another thread.
        """

        try:
            self.m_state_manager.acquire()
            self.verify_broken()

            try:
                ctx = self.get_current_ctx()
            except NoThreads:
                return

            if self.m_lastest_event == 'return':
                return self.request_step(fLock = False)

            self.m_next_frame = None
            self.m_return_frame = ctx.m_frame

            self.request_go(fLock = False)

        finally:
            self.m_state_manager.release()


    def request_jump(self, lineno):
        """
        Jump to line number 'lineno'.
        """

        try:
            self.m_state_manager.acquire()
            self.verify_broken()

            try:
                ctx = self.get_current_ctx()
            except NoThreads:
                return

            frame = ctx.m_frame
            code = frame.f_code

            valid_lines = CalcValidLines(code)
            sbi = CScopeBreakInfo(as_unicode(''), valid_lines)
            l = sbi.CalcScopeLine(lineno)

            frame.f_lineno = l

        finally:
            frame = None
            self.m_state_manager.release()

        self.send_events(None)


    def set_thread(self, tid):
        """
        Switch focus to specified thread.
        """

        try:
            self.m_state_manager.acquire()
            self.verify_broken()

            try:
                if (tid >= 0) and (tid < 100):
                    _tid = list(self.m_threads.keys())[tid]
                else:
                    _tid = tid

                ctx = self.m_threads[_tid]
            except (IndexError, KeyError):
                raise ThreadNotFound

            self.m_current_ctx = ctx
            self.m_lastest_event = ctx.m_event

        finally:
            self.m_state_manager.release()

        self.send_events(None)



class CDebuggerEngine(CDebuggerCore):
    """
    Main class for the debugger.
    Adds functionality on top of CDebuggerCore.
    """

    def __init__(self, fembedded = False):
        CDebuggerCore.__init__(self, fembedded)

        event_type_dict = {
            CEventState: {},
            CEventStackDepth: {},
            CEventBreakpoint: {},
            CEventThreads: {},
            CEventNoThreads: {},
            CEventThreadBroken: {},
            CEventNamespace: {},
            CEventUnhandledException: {},
            CEventStack: {},
            CEventNull: {},
            CEventExit: {},
            CEventForkSwitch: {},
            CEventExecSwitch: {},
            CEventSynchronicity: {},
            CEventBreakOnExit: {},
            CEventTrap: {},
            CEventForkMode: {},
            CEventPsycoWarning: {},
            CEventConflictingModules: {},
            CEventSignalIntercepted: {},
            CEventSignalException: {},
            CEventClearSourceCache: {},
            CEventEmbeddedSync: {}
            }

        self.m_event_queue = CEventQueue(self.m_event_dispatcher)
        self.m_event_queue.register_event_types(event_type_dict)

        event_type_dict = {CEventSync: {}}
        self.m_event_dispatcher.register_callback(self.send_events, event_type_dict, fSingleUse = False)


    def shutdown(self):
        self.m_event_queue.shutdown()

        CDebuggerCore.shutdown(self)



    def sync_with_events(self, fException, fSendUnhandled):
        """
        Send debugger state to client.
        """

        if len(self.m_threads) == 0:
            self.wait_for_first_thread()

        index = self.m_event_queue.get_event_index()
        event = CEventSync(fException, fSendUnhandled)
        self.m_event_dispatcher.fire_event(event)
        return index


    def trap_conflicting_modules(self):
        modules_list = []

        for m in CONFLICTING_MODULES:
            if m in g_found_conflicting_modules:
                continue

            if not m in sys.modules:
                continue

            if m == 'psyco':
                #
                # Old event kept for compatibility.
                #
                event = CEventPsycoWarning()
                self.m_event_dispatcher.fire_event(event)

            g_found_conflicting_modules.append(m)
            modules_list.append(as_unicode(m))

        if modules_list == []:
            return False

        event = CEventConflictingModules(modules_list)
        self.m_event_dispatcher.fire_event(event)

        return True


    def wait_for_event(self, timeout, event_index):
        """
        Wait for new events and return them as list of events.
        """

        self.cancel_request_go_timer()
        self.trap_conflicting_modules()

        (new_event_index, sel) = self.m_event_queue.wait_for_event(timeout, event_index)

        if self.trap_conflicting_modules():
            (new_event_index, sel) = self.m_event_queue.wait_for_event(timeout, event_index)

        return (new_event_index, sel)


    def set_breakpoint(self, filename, scope, lineno, fEnabled, expr, frame_index, fException, encoding):
        print_debug('Setting breakpoint to: %s, %s, %d' % (repr(filename), scope, lineno))

        assert(is_unicode(filename))
        assert(is_unicode(scope))
        assert(is_unicode(expr))

        fLock = False

        try:
            if filename in [None, '']:
                self.m_state_manager.acquire()
                fLock = True
                self.verify_broken()

                _filename = self.get_current_filename(frame_index, fException)
            elif not is_provider_filesystem(filename):
                _filename = as_string(filename, sys.getfilesystemencoding())
            else:
                _filename = FindFile(filename, fModules = True)

            if expr != '':
                try:
                    encoding = self.__calc_encoding(encoding, filename = _filename)
                    _expr = as_bytes(ENCODING_SOURCE % encoding + expr, encoding)
                    compile(_expr, '<string>', 'eval')
                except:
                    raise SyntaxError

            encoding = as_unicode(encoding)

            bp = self.m_bp_manager.set_breakpoint(_filename, scope, lineno, fEnabled, expr, encoding)
            self.set_all_tracers()

            event = CEventBreakpoint(bp)
            #print_debug(repr(vars(bp)))
            self.m_event_dispatcher.fire_event(event)

        finally:
            if fLock:
                self.m_state_manager.release()


    def disable_breakpoint(self, id_list, fAll):
        self.m_bp_manager.disable_breakpoint(id_list, fAll)
        self.set_all_tracers()

        event = CEventBreakpoint(None, CEventBreakpoint.DISABLE, id_list, fAll)
        self.m_event_dispatcher.fire_event(event)


    def enable_breakpoint(self, id_list, fAll):
        self.m_bp_manager.enable_breakpoint(id_list, fAll)
        self.set_all_tracers()

        event = CEventBreakpoint(None, CEventBreakpoint.ENABLE, id_list, fAll)
        self.m_event_dispatcher.fire_event(event)


    def delete_breakpoint(self, id_list, fAll):
        self.m_bp_manager.delete_breakpoint(id_list, fAll)
        self.set_all_tracers()

        event = CEventBreakpoint(None, CEventBreakpoint.REMOVE, id_list, fAll)
        self.m_event_dispatcher.fire_event(event)


    def get_breakpoints(self):
        """
        return id->breakpoint dictionary.
        """

        bpl = self.m_bp_manager.get_breakpoints()
        _items = [(id, breakpoint_copy(bp)) for (id, bp) in bpl.items()]
        for (id, bp) in _items:
            bp.m_code = None

        _bpl = dict(_items)

        return _bpl


    def send_events(self, event):
        """
        Send series of events that define the debugger state.
        """

        if isinstance(event, CEventSync):
            fException = event.m_fException
            fSendUnhandled = event.m_fSendUnhandled
        else:
            fException = False
            fSendUnhandled = False

        try:
            if isinstance(event, CEventSync) and not fException:
                self.m_state_manager.set_state()

            self.send_stack_depth()
            self.send_threads_event(fException)
            self.send_stack_event(fException)
            self.send_namespace_event()

            if fSendUnhandled and self.m_fUnhandledException:
                self.send_unhandled_exception_event()

        except NoThreads:
            self.send_no_threads_event()

        except:
            print_debug_exception()
            raise


    def send_unhandled_exception_event(self):
        event = CEventUnhandledException()
        self.m_event_dispatcher.fire_event(event)


    def send_stack_depth(self):
        """
        Send event with stack depth and exception stack depth.
        """

        f = None
        tb = None
        ctx = self.get_current_ctx()

        try:
            try:
                f = ctx.frame_acquire()
            except ThreadDone:
                return

            s = my_extract_stack(f)
            s = [1 for (a, b, c, d) in s if not is_func_hidden( c ) ]

            stack_depth = len(s)

            tb = get_traceback(f, ctx)
            if tb == None:
                stack_depth_exception = None

            else:
                s = my_extract_stack(tb.tb_frame.f_back)
                s += my_extract_tb(tb)
                s = [1 for (a, b, c, d) in s if is_func_hidden( c ) ]

                stack_depth_exception = len(s)

            event = CEventStackDepth(stack_depth, stack_depth_exception)
            self.m_event_dispatcher.fire_event(event)

        finally:
            f = None
            tb = None
            ctx.frame_release()


    def send_threads_event(self, fException):
        """
        Send event with current thread list.
        In case of exception, send only the current thread.
        """

        tl = self.get_thread_list()

        if fException:
            ctid = tl[0]
            itl = tl[1]
            _itl = [a for a in itl if a[DICT_KEY_TID] == ctid]
            _tl = (ctid, _itl)
        else:
            _tl = tl

        event = CEventThreads(*_tl)
        self.m_event_dispatcher.fire_event(event)


    def send_stack_event(self, fException):
        sl = self.get_stack([], False, fException)

        if len(sl) == 0:
            return

        event = CEventStack(sl[0])
        self.m_event_dispatcher.fire_event(event)


    def send_namespace_event(self):
        """
        Send event notifying namespace should be queried again.
        """

        event = CEventNamespace()
        self.m_event_dispatcher.fire_event(event)


    def send_no_threads_event(self):
        _event = CEventNoThreads()
        self.m_event_dispatcher.fire_event(_event)


    def send_event_null(self):
        """
        Make the event waiter return.
        """

        event = CEventNull()
        self.m_event_dispatcher.fire_event(event)


    def __get_stack(self, ctx, ctid, fException):
        '''
        Arguments:
        :param ctx: a CDebuggerCoreThread of the current context
        :param ctid: id of the current thread, used to set DICT_KEY_CURRENT_TID
        :param fException: boolean, whether to get stack from exception frame or not

        :return: dictionary describing the thread state with the following keys
            - DICT_KEY_STACK: list of (filename, line number, function name, text of source code)
            - DICT_KEY_CODE_LIST: list of code object references represented as string containing hex value
            - DICT_KEY_TID: thread identifier
            - DICT_KEY_BROKEN: boolean, whether thread is currently in Break state or running
            - DICT_KEY_EVENT: name of the event providing the stack: exception, call, return, ...
            - DICT_KEY_CURRENT_TID: boolean, True if this is the current thread
        '''
        tid = ctx.m_thread_id

        f = None
        _f = None
        tb = None
        _tb = None

        try:
            try:
                f = ctx.frame_acquire()
            except ThreadDone:
                return None

            if fException:
                tb = get_traceback(f, ctx)
                if tb == None:
                    raise NoExceptionFound

                _tb = tb
                while _tb.tb_next is not None:
                    _tb = _tb.tb_next

                _f = _tb.tb_frame
                s = my_extract_stack(tb.tb_frame.f_back)
                s += my_extract_tb(tb)

            else:
                _f = f
                s = my_extract_stack(f)

            code_list = []
            while _f is not None:
                rc = repr(_f.f_code).split(',')[0].split()[-1]
                rc = as_unicode(rc)
                code_list.insert(0, rc)
                _f = _f.f_back

        finally:
            f = None
            _f = None
            tb = None
            _tb = None

            ctx.frame_release()

        #print code_list

        __s = [(a, b, c, d) for (a, b, c, d) in s if not is_func_hidden( c ) ]

        if (ctx.m_uef_lineno is not None) and (len(__s) > 0):
            (a, b, c, d) = __s[0]
            __s = [(a, ctx.m_uef_lineno, c, d)] + __s[1:]

        r = {}
        r[DICT_KEY_STACK] = __s
        r[DICT_KEY_CODE_LIST] = code_list
        r[DICT_KEY_TID] = tid
        r[DICT_KEY_BROKEN] = ctx.m_fBroken
        r[DICT_KEY_EVENT] = as_unicode([ctx.m_event, 'exception'][fException])

        if tid == ctid:
            r[DICT_KEY_CURRENT_TID] = True

        return r


    def get_stack(self, tid_list, fAll, fException):
        '''
        Return a list if dictionaries describing the stacks for each threads requested.

        :param tid_list: list of threads id for which we want the stack, or an empty list for 
                         the current thread or for other args to apply
        :param fAll: boolean, True requests stacks for all threads (tid_list must be an empty list then)
        :param fException: boolean, True request stack of current exception (tid_list must be [] and fAll must be False)

        :return: list of dictionaries containing thread information
            - DICT_KEY_STACK: list of (filename, line number, function name, text of source code)
            - DICT_KEY_CODE_LIST: list of code object references represented as string containing hex value
            - DICT_KEY_TID: thread identifier
            - DICT_KEY_BROKEN: boolean, whether thread is currently in Break state or running
            - DICT_KEY_EVENT: name of the event providing the stack: exception, call, return, ...
            - DICT_KEY_CURRENT_TID: boolean, True if this is the current thread
        '''
        if fException and (fAll or (len(tid_list) != 0)):
            raise BadArgument("You shall request either Exception, or list of tid, or all")

        ctx = self.get_current_ctx()
        ctid = ctx.m_thread_id

        if fAll:
            ctx_list = list(self.get_threads().values())
        elif fException or (len(tid_list) == 0):
            ctx_list = [ctx]
        else:
            ctx_list = [self.get_threads().get(t, None) for t in tid_list]

        _sl = [self.__get_stack(ctx, ctid, fException) for ctx in ctx_list if ctx is not None]
        sl = [s for s in _sl if s is not None]

        return sl


    def get_source_file(self, filename, lineno, nlines, frame_index, fException):
        assert(is_unicode(filename))

        if lineno < 1:
            lineno = 1
            nlines = -1

        _lineno = lineno
        r = {}
        frame_filename = None

        try:
            ctx = self.get_current_ctx()

            try:
                f = None
                base_frame = None

                base_frame = ctx.frame_acquire()
                (f, frame_lineno) = ctx.get_frame(base_frame, frame_index, fException)
                frame_filename = calc_frame_path(f)

            finally:
                f = None
                base_frame = None
                ctx.frame_release()

            frame_event = [[ctx.m_event, 'call'][frame_index > 0], 'exception'][fException]

        except NoThreads:
            if filename in [None, '']:
                raise

        if filename in [None, '']:
            __filename = frame_filename
            r[DICT_KEY_TID] = ctx.m_thread_id
        elif not is_provider_filesystem(filename):
            __filename = as_string(filename, sys.getfilesystemencoding())
        else:
            __filename = FindFile(filename, fModules = True)
            if not IsPythonSourceFile(__filename):
                raise NotPythonSource

        _filename = winlower(__filename)

        lines = []
        breakpoints = {}
        fhide_pwd_mode = False

        while nlines != 0:
            try:
                g_traceback_lock.acquire()
                line = get_source_line(_filename, _lineno)

            finally:
                g_traceback_lock.release()

            if line == '':
                break

            #
            # Remove any trace of session password from data structures that
            # go over the network.
            #

            if fhide_pwd_mode:
                if not ')' in line:
                    line = as_unicode('...\n')
                else:
                    line = '...""")' + line.split(')', 1)[1]
                    fhide_pwd_mode = False

            elif 'start_embedded_debugger(' in line:
                ls = line.split('start_embedded_debugger(', 1)
                line = ls[0] + 'start_embedded_debugger("""...Removed-password-from-output...'

                if ')' in ls[1]:
                    line += '""")' + ls[1].split(')', 1)[1]
                else:
                    line += '\n'
                    fhide_pwd_mode = True

            lines.append(line)

            try:
                bp = self.m_bp_manager.get_breakpoint(_filename, _lineno)
                breakpoints[_lineno] = as_unicode([STATE_DISABLED, STATE_ENABLED][bp.isEnabled()])
            except KeyError:
                pass

            _lineno += 1
            nlines -= 1

        if frame_filename == _filename:
            r[DICT_KEY_FRAME_LINENO] = frame_lineno
            r[DICT_KEY_EVENT] = as_unicode(frame_event)
            r[DICT_KEY_BROKEN] = ctx.m_fBroken

        r[DICT_KEY_LINES] = lines
        r[DICT_KEY_FILENAME] = as_unicode(_filename, sys.getfilesystemencoding())
        r[DICT_KEY_BREAKPOINTS] = breakpoints
        r[DICT_KEY_FIRST_LINENO] = lineno

        return r


    def __get_source(self, ctx, nlines, frame_index, fException):
        tid = ctx.m_thread_id
        _frame_index = [0, frame_index][tid == self.m_current_ctx.m_thread_id]

        try:
            try:
                f = None
                base_frame = None

                base_frame = ctx.frame_acquire()
                (f, frame_lineno)  = ctx.get_frame(base_frame, _frame_index, fException)
                frame_filename = calc_frame_path(f)

            except (ThreadDone, InvalidFrame):
                return None

        finally:
            f = None
            base_frame = None
            ctx.frame_release()

        frame_event = [[ctx.m_event, 'call'][frame_index > 0], 'exception'][fException]

        first_line = max(1, frame_lineno - nlines // 2)
        _lineno = first_line

        lines = []
        breakpoints = {}
        fhide_pwd_mode = False

        while nlines != 0:
            try:
                g_traceback_lock.acquire()
                line = get_source_line(frame_filename, _lineno)

            finally:
                g_traceback_lock.release()

            if line == '':
                break

            #
            # Remove any trace of session password from data structures that
            # go over the network.
            #

            if fhide_pwd_mode:
                if not ')' in line:
                    line = as_unicode('...\n')
                else:
                    line = '...""")' + line.split(')', 1)[1]
                    fhide_pwd_mode = False

            elif 'start_embedded_debugger(' in line:
                ls = line.split('start_embedded_debugger(', 1)
                line = ls[0] + 'start_embedded_debugger("""...Removed-password-from-output...'

                if ')' in ls[1]:
                    line += '""")' + ls[1].split(')', 1)[1]
                else:
                    line += '\n'
                    fhide_pwd_mode = True

            lines.append(line)

            try:
                bp = self.m_bp_manager.get_breakpoint(frame_filename, _lineno)
                breakpoints[_lineno] = as_unicode([STATE_DISABLED, STATE_ENABLED][bp.isEnabled()])
            except KeyError:
                pass

            _lineno += 1
            nlines -= 1

        r = {}

        r[DICT_KEY_FRAME_LINENO] = frame_lineno
        r[DICT_KEY_EVENT] = as_unicode(frame_event)
        r[DICT_KEY_BROKEN] = ctx.m_fBroken
        r[DICT_KEY_TID] = tid
        r[DICT_KEY_LINES] = lines
        r[DICT_KEY_FILENAME] = as_unicode(frame_filename, sys.getfilesystemencoding())
        r[DICT_KEY_BREAKPOINTS] = breakpoints
        r[DICT_KEY_FIRST_LINENO] = first_line

        return r


    def get_source_lines(self, nlines, fAll, frame_index, fException):
        if fException and fAll:
            raise BadArgument

        if fAll:
            ctx_list = list(self.get_threads().values())
        else:
            ctx = self.get_current_ctx()
            ctx_list = [ctx]

        _sl = [self.__get_source(ctx, nlines, frame_index, fException) for ctx in ctx_list]
        sl = [s for s in _sl if s is not None]

        return sl


    def __get_locals_globals(self, frame_index, fException, fReadOnly = False):
        ctx = self.get_current_ctx()
        (_globals, _locals, _original_locals_copy) = ctx.get_locals_copy(frame_index, fException, fReadOnly)

        return (_globals, _locals, _original_locals_copy)


    def __calc_number_of_subnodes(self, r):
        for t in [bytearray, bytes, str, str8, unicode, int, float, bool, type(None)]:
            if t is type(r):
                return 0

        try:
            try:
                if isinstance(r, frozenset) or isinstance(r, set):
                    return len(r)

            except NameError:
                pass

            if isinstance(r, sets.BaseSet):
                return len(r)

            if isinstance(r, dict):
                return len(r)

            if isinstance(r, list):
                return len(r)

            if isinstance(r, tuple):
                return len(r)

            return len(dir(r))

        except AttributeError:
            return 0

        return 0


    def __calc_subnodes(self, expr, r, fForceNames, filter_level, repr_limit, encoding):
        snl = []

        try:
            if isinstance(r, frozenset) or isinstance(r, set):
                if len(r) > MAX_SORTABLE_LENGTH:
                    g = r
                else:
                    g = [i for i in r]
                    sort(g)

                for i in g:
                    if len(snl) >= MAX_NAMESPACE_ITEMS:
                        snl.append(MAX_NAMESPACE_WARNING)
                        break

                    is_valid = [True]
                    rk = repr_ltd(i, REPR_ID_LENGTH, encoding =ENCODING_RAW_I)

                    e = {}
                    e[DICT_KEY_EXPR] = as_unicode('_RPDB2_FindRepr((%s), %d)["%s"]' % (expr, REPR_ID_LENGTH, rk.replace('"', '&quot')))
                    e[DICT_KEY_NAME] = repr_ltd(i, repr_limit, encoding)
                    e[DICT_KEY_REPR] = repr_ltd(i, repr_limit, encoding, is_valid)
                    e[DICT_KEY_IS_VALID] = is_valid[0]
                    e[DICT_KEY_TYPE] = as_unicode(parse_type(type(i)))
                    e[DICT_KEY_N_SUBNODES] = self.__calc_number_of_subnodes(i)

                    snl.append(e)

                return snl

        except NameError:
            pass

        if isinstance(r, sets.BaseSet):
            if len(r) > MAX_SORTABLE_LENGTH:
                g = r
            else:
                g = [i for i in r]
                sort(g)

            for i in g:
                if len(snl) >= MAX_NAMESPACE_ITEMS:
                    snl.append(MAX_NAMESPACE_WARNING)
                    break

                is_valid = [True]
                rk = repr_ltd(i, REPR_ID_LENGTH, encoding =ENCODING_RAW_I)

                e = {}
                e[DICT_KEY_EXPR] = as_unicode('_RPDB2_FindRepr((%s), %d)["%s"]' % (expr, REPR_ID_LENGTH, rk.replace('"', '&quot')))
                e[DICT_KEY_NAME] = repr_ltd(i, repr_limit, encoding)
                e[DICT_KEY_REPR] = repr_ltd(i, repr_limit, encoding, is_valid)
                e[DICT_KEY_IS_VALID] = is_valid[0]
                e[DICT_KEY_TYPE] = as_unicode(parse_type(type(i)))
                e[DICT_KEY_N_SUBNODES] = self.__calc_number_of_subnodes(i)

                snl.append(e)

            return snl

        if isinstance(r, list) or isinstance(r, tuple):
            for i, v in enumerate(r[0: MAX_NAMESPACE_ITEMS]):
                is_valid = [True]
                e = {}
                e[DICT_KEY_EXPR] = as_unicode('(%s)[%d]' % (expr, i))
                e[DICT_KEY_NAME] = as_unicode(repr(i))
                e[DICT_KEY_REPR] = repr_ltd(v, repr_limit, encoding, is_valid)
                e[DICT_KEY_IS_VALID] = is_valid[0]
                e[DICT_KEY_TYPE] = as_unicode(parse_type(type(v)))
                e[DICT_KEY_N_SUBNODES] = self.__calc_number_of_subnodes(v)

                snl.append(e)

            if len(r) > MAX_NAMESPACE_ITEMS:
                snl.append(MAX_NAMESPACE_WARNING)

            return snl

        if isinstance(r, dict):
            if filter_level == 2 and expr in ['locals()', 'globals()']:
                r = copy.copy(r)
                for k, v in list(r.items()):
                    if parse_type(type(v)) in ['function', 'classobj', 'type']:
                        del r[k]

            if len(r) > MAX_SORTABLE_LENGTH:
                kl = r
            else:
                kl = list(r.keys())
                sort(kl)

            for k in kl:
                #
                # Remove any trace of session password from data structures that
                # go over the network.
                #
                if k in ['_RPDB2_FindRepr', '_RPDB2_builtins', '_rpdb2_args', '_rpdb2_pwd', 'm_rpdb2_pwd']:
                    continue

                v = r[k]

                if len(snl) >= MAX_NAMESPACE_ITEMS:
                    snl.append(MAX_NAMESPACE_WARNING)
                    break

                is_valid = [True]
                e = {}

                if [True for t in [bool, int, float, bytes, str, unicode, type(None)] if t is type(k)]:
                    rk = repr(k)
                    if len(rk) < REPR_ID_LENGTH:
                        e[DICT_KEY_EXPR] = as_unicode('(%s)[%s]' % (expr, rk))

                if type(k) is str8:
                    rk = repr(k)
                    if len(rk) < REPR_ID_LENGTH:
                        e[DICT_KEY_EXPR] = as_unicode('(%s)[str8(%s)]' % (expr, rk[1:]))

                if not DICT_KEY_EXPR in e:
                    rk = repr_ltd(k, REPR_ID_LENGTH, encoding =ENCODING_RAW_I)
                    e[DICT_KEY_EXPR] = as_unicode('_RPDB2_FindRepr((%s), %d)["%s"]' % (expr, REPR_ID_LENGTH, rk.replace('"', '&quot')))

                e[DICT_KEY_NAME] = as_unicode([repr_ltd(k, repr_limit, encoding), k][fForceNames])
                e[DICT_KEY_REPR] = repr_ltd(v, repr_limit, encoding, is_valid)
                e[DICT_KEY_IS_VALID] = is_valid[0]
                e[DICT_KEY_TYPE] = as_unicode(parse_type(type(v)))
                e[DICT_KEY_N_SUBNODES] = self.__calc_number_of_subnodes(v)

                snl.append(e)

            return snl

        al = calc_attribute_list(r, filter_level)
        sort(al)

        for a in al:
            if a == 'm_rpdb2_pwd':
                continue

            try:
                v = getattr(r, a)
            except AttributeError:
                continue

            if len(snl) >= MAX_NAMESPACE_ITEMS:
                snl.append(MAX_NAMESPACE_WARNING)
                break

            is_valid = [True]
            e = {}
            e[DICT_KEY_EXPR] = as_unicode('(%s).%s' % (expr, a))
            e[DICT_KEY_NAME] = as_unicode(a)
            e[DICT_KEY_REPR] = repr_ltd(v, repr_limit, encoding, is_valid)
            e[DICT_KEY_IS_VALID] = is_valid[0]
            e[DICT_KEY_TYPE] = as_unicode(parse_type(type(v)))
            e[DICT_KEY_N_SUBNODES] = self.__calc_number_of_subnodes(v)

            snl.append(e)

        return snl


    def get_exception(self, frame_index, fException):
        ctx = self.get_current_ctx()

        if is_py3k():
            exc_info = ctx.get_exc_info()
            if exc_info == None:
                return {'type': None, 'value': None, 'traceback': None}

            type, value, traceback = exc_info
            e = {'type': type, 'value': value, 'traceback': traceback}

            return e

        try:
            f = None
            base_frame = None

            base_frame = ctx.frame_acquire()
            (f, frame_lineno) = ctx.get_frame(base_frame, frame_index, fException)

            e = {'type': f.f_exc_type, 'value': f.f_exc_value, 'traceback': f.f_exc_traceback}

            return e

        finally:
            f = None
            base_frame = None
            ctx.frame_release()


    def is_child_of_failure(self, failed_expr_list, expr):
        for failed_expr in failed_expr_list:
            if expr.startswith(failed_expr):
                return True

        return False


    def calc_expr(self, expr, fExpand, filter_level, frame_index, fException, _globals, _locals, lock, event, rl, index, repr_limit, encoding):
        e = {}

        try:
            __globals = _globals
            __locals = _locals

            if RPDB_EXEC_INFO in expr:
                rpdb_exception_info = self.get_exception(frame_index, fException)
                __globals = globals()
                __locals = locals()

            __locals['_RPDB2_FindRepr'] = _RPDB2_FindRepr

            is_valid = [True]
            r = eval(expr, __globals, __locals)

            e[DICT_KEY_EXPR] = as_unicode(expr)
            e[DICT_KEY_REPR] = repr_ltd(r, repr_limit, encoding, is_valid)
            e[DICT_KEY_IS_VALID] = is_valid[0]
            e[DICT_KEY_TYPE] = as_unicode(parse_type(type(r)))
            e[DICT_KEY_N_SUBNODES] = self.__calc_number_of_subnodes(r)

            if fExpand and (e[DICT_KEY_N_SUBNODES] > 0):
                fForceNames = (expr in ['globals()', 'locals()']) or (RPDB_EXEC_INFO in expr)
                e[DICT_KEY_SUBNODES] = self.__calc_subnodes(expr, r, fForceNames, filter_level, repr_limit, encoding)
                e[DICT_KEY_N_SUBNODES] = len(e[DICT_KEY_SUBNODES])

        except:
            print_debug_exception()
            e[DICT_KEY_ERROR] = as_unicode(safe_repr(sys.exc_info()))

        lock.acquire()
        if len(rl) == index:
            rl.append(e)
        lock.release()

        event.set()


    def __calc_encoding(self, encoding, fvalidate = False, filename = None):
        if encoding != ENCODING_AUTO and not fvalidate:
            return encoding

        if encoding != ENCODING_AUTO:
            try:
                codecs.lookup(encoding)
                return encoding

            except:
                pass

        if filename == None:
            ctx = self.get_current_ctx()
            filename = ctx.m_code_context.m_filename

        try:
            encoding = get_file_encoding(filename)
            return encoding

        except:
            return 'utf-8'



    def get_namespace(self, nl, filter_level, frame_index, fException, repr_limit, encoding, fraw):
        if fraw:
            encoding = ENCODING_RAW_I
        else:
            encoding = self.__calc_encoding(encoding, fvalidate = True)

        try:
            (_globals, _locals, x) = self.__get_locals_globals(frame_index, fException, fReadOnly = True)
        except:
            print_debug_exception()
            raise

        failed_expr_list = []
        rl = []
        index = 0
        lock = threading.Condition()

        for (expr, fExpand) in nl:
            if self.is_child_of_failure(failed_expr_list, expr):
                continue

            event = threading.Event()
            args = (expr, fExpand, filter_level, frame_index, fException, _globals, _locals, lock, event, rl, index, repr_limit, encoding)

            if self.m_fsynchronicity:
                g_server.m_work_queue.post_work_item(target = self.calc_expr, args = args, name = 'calc_expr %s' % expr)
            else:
                try:
                    ctx = self.get_current_ctx()
                    tid = ctx.m_thread_id
                    send_job(tid, 0, self.calc_expr, *args)
                except:
                    pass

            safe_wait(event, 2)

            lock.acquire()
            if len(rl) == index:
                rl.append('error')
                failed_expr_list.append(expr)
            index += 1
            lock.release()

            if len(failed_expr_list) > 3:
                break

        _rl = [r for r in rl if r != 'error']

        return _rl


    def evaluate(self, expr, frame_index, fException, encoding, fraw):
        """
        Evaluate expression in context of frame at depth 'frame-index'.
        """

        result = [(as_unicode(''), as_unicode(STR_SYNCHRONICITY_BAD), as_unicode(''))]

        if self.m_fsynchronicity:
            self._evaluate(result, expr, frame_index, fException, encoding, fraw)
        else:
            try:
                ctx = self.get_current_ctx()
                tid = ctx.m_thread_id
                send_job(tid, 1000, self._evaluate, result, expr, frame_index, fException, encoding, fraw)
            except:
                pass

        return result[-1]


    def _evaluate(self, result, expr, frame_index, fException, encoding, fraw):
        """
        Evaluate expression in context of frame at depth 'frame-index'.
        """

        encoding = self.__calc_encoding(encoding)

        (_globals, _locals, x) = self.__get_locals_globals(frame_index, fException)

        v = ''
        w = ''
        e = ''

        try:
            if '_rpdb2_pwd' in expr or '_rpdb2_args' in expr:
                r = '...Removed-password-from-output...'

            else:
                _expr = as_bytes(ENCODING_SOURCE % encoding + expr, encoding, fstrict = True)

                if '_RPDB2_builtins' in expr:
                    _locals['_RPDB2_builtins'] = vars(g_builtins_module)

                try:
                    redirect_exc_info = True
                    r = eval(_expr, _globals, _locals)

                finally:
                    del redirect_exc_info

                    if '_RPDB2_builtins' in expr:
                        del _locals['_RPDB2_builtins']


            if fraw:
                encoding = ENCODING_RAW_I

            v = repr_ltd(r, MAX_EVALUATE_LENGTH, encoding)

            if len(v) > MAX_EVALUATE_LENGTH:
                v += '... *** %s ***' % STR_MAX_EVALUATE_LENGTH_WARNING
                w = STR_MAX_EVALUATE_LENGTH_WARNING

        except:
            exc_info = sys.exc_info()
            e = "%s, %s" % (safe_str(exc_info[0]), safe_str(exc_info[1]))

        self.notify_namespace()

        result.append((as_unicode(v), as_unicode(w), as_unicode(e)))


    def execute(self, suite, frame_index, fException, encoding):
        """
        Execute suite (Python statement) in context of frame at
        depth 'frame-index'.
        """

        result = [(as_unicode(STR_SYNCHRONICITY_BAD), as_unicode(''))]

        if self.m_fsynchronicity:
            self._execute(result, suite, frame_index, fException, encoding)
        else:
            try:
                ctx = self.get_current_ctx()
                tid = ctx.m_thread_id
                send_job(tid, 1000, self._execute, result, suite, frame_index, fException, encoding)
            except:
                pass

        return result[-1]


    def _execute(self, result, suite, frame_index, fException, encoding):
        """
        Execute suite (Python statement) in context of frame at
        depth 'frame-index'.
        """

        print_debug('exec called with: ' + repr(suite))

        encoding = self.__calc_encoding(encoding)

        (_globals, _locals, _original_locals_copy) = self.__get_locals_globals(frame_index, fException)

        if frame_index > 0 and not _globals is _locals:
            _locals_copy = copy.copy(_locals)

        w = ''
        e = ''

        try:
            if '_RPDB2_FindRepr' in suite and not '_RPDB2_FindRepr' in _original_locals_copy:
                _locals['_RPDB2_FindRepr'] = _RPDB2_FindRepr

            try:
                _suite = as_bytes(ENCODING_SOURCE % encoding + suite, encoding, fstrict = True)
                #print_debug('suite is %s' % repr(_suite))

                _code = compile(_suite, '<string>', 'exec')

                try:
                    redirect_exc_info = True
                    exec(_code, _globals, _locals)

                finally:
                    del redirect_exc_info

            finally:
                if '_RPDB2_FindRepr' in suite and not '_RPDB2_FindRepr' in _original_locals_copy:
                    del _locals['_RPDB2_FindRepr']

        except:
            exc_info = sys.exc_info()
            e = "%s, %s" % (safe_str(exc_info[0]), safe_str(exc_info[1]))

        if frame_index > 0 and (not _globals is _locals) and _locals != _locals_copy:
            l = [(k, safe_repr(v)) for k, v in _locals.items()]
            sl = set(l)

            lc = [(k, safe_repr(v)) for k, v in _locals_copy.items()]
            slc = set(lc)

            nsc = [k for (k, v) in sl - slc if k in _original_locals_copy]
            if len(nsc) != 0:
                w = STR_LOCAL_NAMESPACE_WARNING

        self.notify_namespace()

        result.append((as_unicode(w), as_unicode(e)))


    def __decode_thread_name(self, name):
        name = as_unicode(name)
        return name


    def get_thread_list(self):
        """
        Return thread list with tid, state, and last event of each thread.
        """

        ctx = self.get_current_ctx()

        if ctx is None:
            current_thread_id = -1
        else:
            current_thread_id = ctx.m_thread_id

        ctx_list = list(self.get_threads().values())

        tl = []
        for c in ctx_list:
            d = {}
            d[DICT_KEY_TID] = c.m_thread_id
            d[DICT_KEY_NAME] = self.__decode_thread_name(c.m_thread_name)
            d[DICT_KEY_BROKEN] = c.m_fBroken
            d[DICT_KEY_EVENT] = as_unicode(c.m_event)
            tl.append(d)

        return (current_thread_id, tl)


    def stop_debuggee(self):
        """
        Notify the client and terminate this proccess.
        """

        g_server.m_work_queue.post_work_item(target = _atexit, args = (True, ), name = '_atexit')


    def set_synchronicity(self, fsynchronicity):
        self.m_fsynchronicity = fsynchronicity

        event = CEventSynchronicity(fsynchronicity)
        self.m_event_dispatcher.fire_event(event)

        if self.m_state_manager.get_state() == STATE_BROKEN:
            self.notify_namespace()

    def set_trap_unhandled_exceptions(self, ftrap):
        self.m_ftrap = ftrap

        event = CEventTrap(ftrap)
        self.m_event_dispatcher.fire_event(event)


    def is_unhandled_exception(self):
        return self.m_fUnhandledException


    def set_fork_mode(self, ffork_into_child, ffork_auto):
        self.m_ffork_into_child = ffork_into_child
        self.m_ffork_auto = ffork_auto

        event = CEventForkMode(ffork_into_child, ffork_auto)
        self.m_event_dispatcher.fire_event(event)


    def set_environ(self, envmap):
        global g_fignorefork

        print_debug('Entered set_environ() with envmap = %s' % repr(envmap))

        if len(envmap) == 0:
            return

        old_pythonpath = os.environ.get('PYTHONPATH', '')

        encoding = detect_locale()

        for k, v in envmap:
            try:
                k = as_string(k, encoding, fstrict = True)
                v = as_string(v, encoding, fstrict = True)
            except:
                continue

            command = 'echo %s' % v

            try:
                g_fignorefork = True
                f = platform.popen(command)

            finally:
                g_fignorefork = False

            value = f.read()
            f.close()

            if value[-1:] == '\n':
                value = value[:-1]

            os.environ[k] = value

        if 'PYTHONPATH' in [k for (k, v) in envmap]:
            recalc_sys_path(old_pythonpath)



#
# ------------------------------------- RPC Server --------------------------------------------
#



class CWorkQueue:
    """
    Worker threads pool mechanism for RPC server.
    """

    def __init__(self, size = N_WORK_QUEUE_THREADS):
        self.m_lock = threading.Condition()
        self.m_work_items = []
        self.m_f_shutdown = False

        self.m_size = size
        self.m_n_threads = 0
        self.m_n_available = 0

        self.__create_thread()


    def __create_thread(self):
        t = CThread(name = '__worker_target', target = self.__worker_target, shutdown = self.shutdown)
        #thread_set_daemon(t, True)
        t.start()


    def shutdown(self):
        """
        Signal worker threads to exit, and wait until they do.
        """

        if self.m_f_shutdown:
            return

        print_debug('Shutting down worker queue...')

        self.m_lock.acquire()
        self.m_f_shutdown = True
        lock_notify_all(self.m_lock)

        t0 = time.time()

        while self.m_n_threads > 0:
            if time.time() - t0 > SHUTDOWN_TIMEOUT:
                self.m_lock.release()
                print_debug('Shut down of worker queue has TIMED OUT!')
                return

            safe_wait(self.m_lock, 0.1)

        self.m_lock.release()
        print_debug('Shutting down worker queue, done.')


    def __worker_target(self):
        try:
            self.m_lock.acquire()

            self.m_n_threads += 1
            self.m_n_available += 1
            fcreate_thread = not self.m_f_shutdown and self.m_n_threads < self.m_size

            self.m_lock.release()

            if fcreate_thread:
                self.__create_thread()

            self.m_lock.acquire()

            while not self.m_f_shutdown:
                safe_wait(self.m_lock)

                if self.m_f_shutdown:
                    break

                if len(self.m_work_items) == 0:
                    continue

                fcreate_thread = self.m_n_available == 1

                (target, args, name) = self.m_work_items.pop()

                self.m_n_available -= 1
                self.m_lock.release()

                if fcreate_thread:
                    print_debug('Creating an extra worker thread.')
                    self.__create_thread()

                thread_set_name(current_thread(), '__worker_target-' + name)

                try:
                    target(*args)
                except:
                    print_debug_exception()

                thread_set_name(current_thread(), '__worker_target')

                self.m_lock.acquire()
                self.m_n_available += 1

                if self.m_n_available > self.m_size:
                    break

            self.m_n_threads -= 1
            self.m_n_available -= 1
            lock_notify_all(self.m_lock)

        finally:
            self.m_lock.release()


    def post_work_item(self, target, args, name ): 
        if self.m_f_shutdown:
            return

        try:
            self.m_lock.acquire()

            if self.m_f_shutdown:
                return

            self.m_work_items.append((target, args, name))

            self.m_lock.notify()

        finally:
            self.m_lock.release()



#
# MOD
#
class CUnTracedThreadingMixIn(SocketServer.ThreadingMixIn):
    """
    Modification of SocketServer.ThreadingMixIn that uses a worker thread
    queue instead of spawning threads to process requests.
    This mod was needed to resolve deadlocks that were generated in some
    circumstances.
    """

    def process_request(self, request, client_address):
        g_server.m_work_queue.post_work_item(target = SocketServer.ThreadingMixIn.process_request_thread, args = (self, request, client_address), name = 'process_request')



#
# MOD
#
def my_xmlrpclib_loads(data):
    """
    Modification of Python 2.3 xmlrpclib.loads() that does not do an
    import. Needed to prevent deadlocks.
    """

    p, u = xmlrpclib.getparser()
    p.feed(data)
    p.close()
    return u.close(), u.getmethodname()



#
# MOD
#
class CXMLRPCServer(CUnTracedThreadingMixIn, SimpleXMLRPCServer.SimpleXMLRPCServer):
    if os.name == POSIX:
        allow_reuse_address = True
    else:
        allow_reuse_address = False

    """
    Modification of Python 2.3 SimpleXMLRPCServer.SimpleXMLRPCDispatcher
    that uses my_xmlrpclib_loads(). Needed to prevent deadlocks.
    """

    def __marshaled_dispatch(self, data, dispatch_method = None):
        params, method = my_xmlrpclib_loads(data)

        # generate response
        try:
            if dispatch_method is not None:
                response = dispatch_method(method, params)
            else:
                response = self._dispatch(method, params)
            # wrap response in a singleton tuple
            response = (response,)
            response = xmlrpclib.dumps(response, methodresponse=1)
        except xmlrpclib.Fault:
            fault = sys.exc_info()[1]
            response = xmlrpclib.dumps(fault)
        except:
            # report exception back to server
            response = xmlrpclib.dumps(
                xmlrpclib.Fault(1, "%s:%s" % (sys.exc_type, sys.exc_value))
                )
            print_debug_exception()

        return response

    if sys.version_info[:2] <= (2, 3):
        _marshaled_dispatch = __marshaled_dispatch


    #def server_activate(self):
    #    self.socket.listen(1)


    def handle_error(self, request, client_address):
        print_debug("handle_error() in pid %d" % _getpid())

        if g_ignore_broken_pipe + 5 > time.time():
            return

        return SimpleXMLRPCServer.SimpleXMLRPCServer.handle_error(self, request, client_address)



class CPwdServerProxy:
    """
    Encrypted proxy to the debuggee.
    Works by wrapping a xmlrpclib.ServerProxy object.
    """

    def __init__(self, crypto, uri, transport = None, target_rid = 0):
        self.m_crypto = crypto
        self.m_proxy = xmlrpclib.ServerProxy(uri, transport)

        self.m_fEncryption = is_encryption_supported()
        self.m_target_rid = target_rid

        self.m_method = getattr(self.m_proxy, DISPACHER_METHOD)


    def __set_encryption(self, fEncryption):
        self.m_fEncryption = fEncryption


    def get_encryption(self):
        return self.m_fEncryption


    def __request(self, name, params):
        """
        Call debuggee method 'name' with parameters 'params'.
        """

        while True:
            try:
                #
                # Encrypt method and params.
                #
                fencrypt = self.get_encryption()
                args = (as_unicode(name), params, self.m_target_rid)
                (fcompress, digest, msg) = self.m_crypto.do_crypto(args, fencrypt)

                rpdb_version = as_unicode(get_interface_compatibility_version())

                r = self.m_method(rpdb_version, fencrypt, fcompress, digest, msg)
                (fencrypt, fcompress, digest, msg) = r

                #
                # Decrypt response.
                #
                ((max_index, _r, _e), id) = self.m_crypto.undo_crypto(fencrypt, fcompress, digest, msg, fVerifyIndex = False)

                if _e is not None:
                    raise _e

            except AuthenticationBadIndex:
                e = sys.exc_info()[1]
                self.m_crypto.set_index(e.m_max_index, e.m_anchor)
                continue

            except xmlrpclib.Fault:
                fault = sys.exc_info()[1]
                if class_name(BadVersion) in fault.faultString:
                    s = fault.faultString.split("'")
                    version = ['', s[1]][len(s) > 0]
                    raise BadVersion(version)

                if class_name(EncryptionExpected) in fault.faultString:
                    raise EncryptionExpected

                elif class_name(EncryptionNotSupported) in fault.faultString:
                    if self.m_crypto.m_fAllowUnencrypted:
                        self.__set_encryption(False)
                        continue

                    raise EncryptionNotSupported

                elif class_name(DecryptionFailure) in fault.faultString:
                    raise DecryptionFailure

                elif class_name(AuthenticationBadData) in fault.faultString:
                    raise AuthenticationBadData

                elif class_name(AuthenticationFailure) in fault.faultString:
                    raise AuthenticationFailure

                else:
                    print_debug_exception()
                    assert False

            except xmlrpclib.ProtocolError:
                print_debug("Caught ProtocolError for %s" % name)
                #print_debug_exception()
                raise CConnectionException

            return _r


    def __getattr__(self, name):
        return xmlrpclib._Method(self.__request, name)



class CIOServer:
    """
    Base class for debuggee server.
    """

    def __init__(self, _rpdb2_pwd, fAllowUnencrypted, fAllowRemote, rid):
        assert(is_unicode(_rpdb2_pwd))
        assert(is_unicode(rid))

        self.m_thread = None

        self.m_crypto = CCrypto(_rpdb2_pwd, fAllowUnencrypted, rid)

        self.m_fAllowRemote = fAllowRemote
        self.m_rid = rid

        self.m_port = None
        self.m_stop = False
        self.m_server = None

        self.m_work_queue = None


    def shutdown(self):
        self.stop()


    def start(self):
        self.m_thread = CThread(name = 'ioserver', target = self.run, shutdown = self.shutdown)
        thread_set_daemon(self.m_thread, True)
        self.m_thread.start()


    def jumpstart(self):
        self.m_stop = False
        self.start()


    def stop(self):
        if self.m_stop:
            return

        print_debug('Stopping IO server... (pid = %d)' % _getpid())

        self.m_stop = True

        while thread_is_alive(self.m_thread):
            try:
                proxy = CPwdServerProxy(self.m_crypto, calcURL(LOOPBACK, self.m_port), CLocalTimeoutTransport())
                proxy.null()
            except (socket.error, CException):
                pass

            self.m_thread.join(0.5)

        self.m_thread = None

        self.m_work_queue.shutdown()

        #try:
        #    self.m_server.socket.close()
        #except:
        #    pass

        print_debug('Stopping IO server, done.')


    def export_null(self):
        return 0


    def run(self):
        if self.m_server == None:
            (self.m_port, self.m_server) = self.__StartXMLRPCServer()

        self.m_work_queue = CWorkQueue()
        self.m_server.register_function(self.dispatcher_method)

        while not self.m_stop:
            self.m_server.handle_request()


    def dispatcher_method(self, rpdb_version, fencrypt, fcompress, digest, msg):
        """
        Process RPC call.
        """

        #print_debug('dispatcher_method() called with: %s, %s, %s, %s' % (rpdb_version, fencrypt, digest, msg[:100]))

        if rpdb_version != as_unicode(get_interface_compatibility_version()):
            raise BadVersion(as_unicode(get_version()))

        try:
            try:
                #
                # Decrypt parameters.
                #
                ((name, __params, target_rid), client_id) = self.m_crypto.undo_crypto(fencrypt, fcompress, digest, msg)

            except AuthenticationBadIndex:
                e = sys.exc_info()[1]
                #print_debug_exception()

                #
                # Notify the caller on the expected index.
                #
                max_index = self.m_crypto.get_max_index()
                args = (max_index, None, e)
                (fcompress, digest, msg) = self.m_crypto.do_crypto(args, fencrypt)
                return (fencrypt, fcompress, digest, msg)

            r = None
            e = None

            try:
                #
                # We are forcing the 'export_' prefix on methods that are
                # callable through XML-RPC to prevent potential security
                # problems
                #
                func = getattr(self, 'export_' + name)
            except AttributeError:
                raise Exception('method "%s" is not supported' % ('export_' + name))

            try:
                if (target_rid != 0) and (target_rid != self.m_rid):
                    raise NotAttached

                #
                # Record that client id is still attached.
                #
                self.record_client_heartbeat(client_id, name, __params)

                r = func(*__params)

            except Exception:
                _e = sys.exc_info()[1]
                print_debug_exception()
                e = _e

            #
            # Send the encrypted result.
            #
            max_index = self.m_crypto.get_max_index()
            args = (max_index, r, e)
            (fcompress, digest, msg) = self.m_crypto.do_crypto(args, fencrypt)
            return (fencrypt, fcompress, digest, msg)

        except:
            print_debug_exception()
            raise


    def __StartXMLRPCServer(self):
        """
        As the name says, start the XML RPC server.
        Looks for an available tcp port to listen on.
        """

        host = [LOOPBACK, ""][self.m_fAllowRemote]
        port = SERVER_PORT_RANGE_START

        while True:
            try:
                server = CXMLRPCServer((host, port), logRequests = 0)
                return (port, server)

            except socket.error:
                e = sys.exc_info()[1]
                if GetSocketError(e) != errno.EADDRINUSE:
                    raise

                if port >= SERVER_PORT_RANGE_START + SERVER_PORT_RANGE_LENGTH - 1:
                    raise

                port += 1
                continue


    def record_client_heartbeat(self, id, name, params):
        pass



class CServerInfo(object):
    def __init__(self, age, port, pid, filename, rid, state, fembedded):
        assert(is_unicode(rid))

        self.m_age = age
        self.m_port = port
        self.m_pid = pid
        self.m_filename = as_unicode(filename, sys.getfilesystemencoding())
        self.m_module_name = as_unicode(CalcModuleName(filename), sys.getfilesystemencoding())
        self.m_rid = rid
        self.m_state = as_unicode(state)
        self.m_fembedded = fembedded


    def __reduce__(self):
        rv = (copy_reg.__newobj__, (type(self), ), vars(self), None, None)
        return rv


    def __str__(self):
        return 'age: %d, port: %d, pid: %d, filename: %s, rid: %s' % (self.m_age, self.m_port, self.m_pid, self.m_filename, self.m_rid)



class CDebuggeeServer(CIOServer):
    """
    The debuggee XML RPC server class.
    """

    def __init__(self, filename, debugger, _rpdb2_pwd, fAllowUnencrypted, fAllowRemote, rid = None):
        if rid is None:
            rid = generate_rid()

        assert(is_unicode(_rpdb2_pwd))
        assert(is_unicode(rid))

        CIOServer.__init__(self, _rpdb2_pwd, fAllowUnencrypted, fAllowRemote, rid)

        self.m_filename = filename
        self.m_pid = _getpid()
        self.m_time = time.time()
        self.m_debugger = debugger
        self.m_rid = rid


    def shutdown(self):
        CIOServer.shutdown(self)


    def record_client_heartbeat(self, id, name, params):
        finit = (name == 'request_break')
        fdetach = (name == 'request_go' and True in params)

        self.m_debugger.record_client_heartbeat(id, finit, fdetach)


    def export_null(self):
        return self.m_debugger.send_event_null()


    def export_server_info(self):
        age = time.time() - self.m_time
        state = self.m_debugger.get_state()
        fembedded = self.m_debugger.is_embedded()

        si = CServerInfo(age, self.m_port, self.m_pid, self.m_filename, self.m_rid, state, fembedded)
        return si


    def export_sync_with_events(self, fException, fSendUnhandled):
        ei = self.m_debugger.sync_with_events(fException, fSendUnhandled)
        return ei


    def export_wait_for_event(self, timeout, event_index):
        (new_event_index, s) = self.m_debugger.wait_for_event(timeout, event_index)
        return (new_event_index, s)


    def export_set_breakpoint(self, filename, scope, lineno, fEnabled, expr, frame_index, fException, encoding):
        self.m_debugger.set_breakpoint(filename, scope, lineno, fEnabled, expr, frame_index, fException, encoding)
        return 0


    def export_disable_breakpoint(self, id_list, fAll):
        self.m_debugger.disable_breakpoint(id_list, fAll)
        return 0


    def export_enable_breakpoint(self, id_list, fAll):
        self.m_debugger.enable_breakpoint(id_list, fAll)
        return 0


    def export_delete_breakpoint(self, id_list, fAll):
        self.m_debugger.delete_breakpoint(id_list, fAll)
        return 0


    def export_get_breakpoints(self):
        bpl = self.m_debugger.get_breakpoints()
        return bpl


    def export_request_break(self):
        self.m_debugger.request_break()
        return 0


    def export_request_go(self, fdetach = False):
        self.m_debugger.request_go()
        return 0


    def export_request_go_breakpoint(self, filename, scope, lineno, frame_index, fException):
        self.m_debugger.request_go_breakpoint(filename, scope, lineno, frame_index, fException)
        return 0


    def export_request_step(self):
        self.m_debugger.request_step()
        return 0


    def export_request_next(self):
        self.m_debugger.request_next()
        return 0


    def export_request_return(self):
        self.m_debugger.request_return()
        return 0


    def export_request_jump(self, lineno):
        self.m_debugger.request_jump(lineno)
        return 0


    def export_get_stack(self, tid_list, fAll, fException):
        r = self.m_debugger.get_stack(tid_list, fAll, fException)
        return r


    def export_get_source_file(self, filename, lineno, nlines, frame_index, fException):
        r = self.m_debugger.get_source_file(filename, lineno, nlines, frame_index, fException)
        return r


    def export_get_source_lines(self, nlines, fAll, frame_index, fException):
        r = self.m_debugger.get_source_lines(nlines, fAll, frame_index, fException)
        return r


    def export_get_thread_list(self):
        r = self.m_debugger.get_thread_list()
        return r


    def export_set_thread(self, tid):
        self.m_debugger.set_thread(tid)
        return 0


    def export_get_namespace(self, nl, filter_level, frame_index, fException, repr_limit, encoding, fraw):
        r = self.m_debugger.get_namespace(nl, filter_level, frame_index, fException, repr_limit, encoding, fraw)
        return r


    def export_evaluate(self, expr, frame_index, fException, encoding, fraw):
        (v, w, e) = self.m_debugger.evaluate(expr, frame_index, fException, encoding, fraw)
        return (v, w, e)


    def export_execute(self, suite, frame_index, fException, encoding):
        (w, e) = self.m_debugger.execute(suite, frame_index, fException, encoding)
        return (w, e)


    def export_stop_debuggee(self):
        self.m_debugger.stop_debuggee()
        return 0

    def export_set_synchronicity(self, fsynchronicity):
        self.m_debugger.set_synchronicity(fsynchronicity)
        return 0

    def export_set_breakonexit(self, fbreakonexit):
        global g_fbreakonexit
        g_fbreakonexit = fbreakonexit
        return 0

    def export_set_trap_unhandled_exceptions(self, ftrap):
        self.m_debugger.set_trap_unhandled_exceptions(ftrap)
        return 0


    def export_is_unhandled_exception(self):
        return self.m_debugger.is_unhandled_exception()


    def export_set_fork_mode(self, ffork_into_child, ffork_auto):
        self.m_debugger.set_fork_mode(ffork_into_child, ffork_auto)
        return 0


    def export_set_environ(self, envmap):
        self.m_debugger.set_environ(envmap)
        return 0


    def export_embedded_sync(self):
        self.m_debugger.embedded_sync()
        return 0



#
# ------------------------------------- RPC Client --------------------------------------------
#



#
# MOD
#
class CTimeoutHTTPConnection(httplib.HTTPConnection):
    """
    Modification of httplib.HTTPConnection with timeout for sockets.
    """

    _rpdb2_timeout = PING_TIMEOUT

    def connect(self):
        """Connect to the host and port specified in __init__."""

        # New Python version of connect().
        if hasattr(self, 'timeout'):
            self.timeout = self._rpdb2_timeout
            return httplib.HTTPConnection.connect(self)

        # Old Python version of connect().
        msg = "getaddrinfo returns an empty list"
        for res in socket.getaddrinfo(self.host, self.port, 0,
                                      socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                self.sock = socket.socket(af, socktype, proto)
                self.sock.settimeout(self._rpdb2_timeout)
                if self.debuglevel > 0:
                    print_debug("connect: (%s, %s)" % (self.host, self.port))
                self.sock.connect(sa)
            except socket.error:
                msg = sys.exc_info()[1]
                if self.debuglevel > 0:
                    print_debug('connect fail: ' + repr((self.host, self.port)))
                if self.sock:
                    self.sock.close()
                self.sock = None
                continue
            break
        if not self.sock:
            raise socket.error(msg)



#
# MOD
#
class CLocalTimeoutHTTPConnection(CTimeoutHTTPConnection):
    """
    Modification of httplib.HTTPConnection with timeout for sockets.
    """

    _rpdb2_timeout = LOCAL_TIMEOUT



if is_py3k():
    class httplib_HTTP(object):
        pass
else:
    httplib_HTTP = httplib.HTTP



#
# MOD
#
class CTimeoutHTTP(httplib_HTTP):
    """
    Modification of httplib.HTTP with timeout for sockets.
    """

    _connection_class = CTimeoutHTTPConnection



#
# MOD
#
class CLocalTimeoutHTTP(httplib_HTTP):
    """
    Modification of httplib.HTTP with timeout for sockets.
    """

    _connection_class = CLocalTimeoutHTTPConnection



#
# MOD
#
class CLocalTransport(xmlrpclib.Transport):
    """
    Modification of xmlrpclib.Transport to work around Zonealarm sockets
    bug.
    """

    _connection_class = httplib.HTTPConnection
    _connection_class_old = httplib_HTTP


    def make_connection(self, host):
        # New Python version of connect().
        # However, make_connection is hacked to always create a new connection
        # Otherwise all threads use single connection and crash.
        if hasattr(self, '_connection'):
            chost, self._extra_headers, x509 = self.get_host_info(host)
            return self._connection_class(chost)

        # Old Python version of connect().
        # create a HTTP connection object from a host descriptor
        host, extra_headers, x509 = self.get_host_info(host)
        return self._connection_class_old(host)


    def __parse_response(self, file, sock):
        # read response from input file/socket, and parse it

        p, u = self.getparser()

        while 1:
            if sock:
                response = sock.recv(1024)
            else:
                time.sleep(0.002)
                response = file.read(1024)
            if not response:
                break
            if self.verbose:
                _print("body: " + repr(response))
            p.feed(response)

        file.close()
        p.close()

        return u.close()

    if os.name == 'nt':
        _parse_response = __parse_response



#
# MOD
#
class CTimeoutTransport(CLocalTransport):
    """
    Modification of xmlrpclib.Transport with timeout for sockets.
    """

    _connection_class = CTimeoutHTTPConnection
    _connection_class_old = CTimeoutHTTP



#
# MOD
#
class CLocalTimeoutTransport(CLocalTransport):
    """
    Modification of xmlrpclib.Transport with timeout for sockets.
    """

    _connection_class = CLocalTimeoutHTTPConnection
    _connection_class_old = CLocalTimeoutHTTP



class CSession:
    """
    Basic class that communicates with the debuggee server.
    """

    def __init__(self, host, port, _rpdb2_pwd, fAllowUnencrypted, rid):
        self.m_crypto = CCrypto(_rpdb2_pwd, fAllowUnencrypted, rid)

        self.m_host = host
        self.m_port = port
        self.m_proxy = None
        self.m_server_info = None
        self.m_exc_info = None

        self.m_fShutDown = False
        self.m_fRestart = False


    def get_encryption(self):
        return self.m_proxy.get_encryption()


    def getServerInfo(self):
        return self.m_server_info


    def pause(self):
        self.m_fRestart = True


    def restart(self, sleep = 0, timeout = 10):
        self.m_fRestart = True

        time.sleep(sleep)

        t0 = time.time()

        try:
            try:
                while time.time() < t0 + timeout:
                    try:
                        self.Connect()
                        return

                    except socket.error:
                        continue

                raise CConnectionException

            except:
                self.m_fShutDown = True
                raise

        finally:
            self.m_fRestart = False


    def shut_down(self):
        self.m_fShutDown = True


    def getProxy(self):
        """
        Return the proxy object.
        With this object you can invoke methods on the server.
        """

        while self.m_fRestart:
            time.sleep(0.1)

        if self.m_fShutDown:
            raise NotAttached

        return self.m_proxy


    def ConnectAsync(self):
        t = threading.Thread(target = self.ConnectNoThrow)
        #thread_set_daemon(t, True)
        t.start()
        return t


    def ConnectNoThrow(self):
        try:
            self.Connect()
        except:
            self.m_exc_info = sys.exc_info()


    def Connect(self):
        host = self.m_host
        if host.lower() == LOCALHOST:
            host = LOOPBACK

        server = CPwdServerProxy(self.m_crypto, calcURL(host, self.m_port), CTimeoutTransport())
        server_info = server.server_info()

        self.m_proxy = CPwdServerProxy(self.m_crypto, calcURL(host, self.m_port), CLocalTransport(), target_rid = server_info.m_rid)
        self.m_server_info = server_info


    def isConnected(self):
        return self.m_proxy is not None


class CConsoleInternal(cmd.Cmd, threading.Thread):
    def __init__(self, session_manager, stdin = None, stdout = None, fSplit = False):
        global g_fDefaultStd

        cmd.Cmd.__init__(self, stdin = stdin, stdout = stdout)
        threading.Thread.__init__(self)

        self.fAnalyzeMode = False
        self.fPrintBroken = True

        self.m_filename = as_unicode('')

        self.m_completion_thread = None

        self.use_rawinput = [1, 0][fSplit]
        self.m_fSplit = fSplit
        self.prompt = [[CONSOLE_PROMPT, CONSOLE_PROMPT_ANALYZE][self.fAnalyzeMode], ""][fSplit]
        self.intro = CONSOLE_INTRO
        if fSplit:
            self.intro += '\n'

        #thread_set_daemon(self, True)

        self.m_session_manager = session_manager
        self.m_session_manager.set_printer(self.printer)

        event_type_dict = {CEventState: {}}
        self.m_session_manager.register_callback(self.event_handler, event_type_dict, fSingleUse = False)

        event_type_dict = {CEventSynchronicity: {}}
        self.m_session_manager.register_callback(self.synchronicity_handler, event_type_dict, fSingleUse = False)

        event_type_dict = {CEventBreakOnExit: {}}
        self.m_session_manager.register_callback(self.breakonexit_handler, event_type_dict, fSingleUse = False)

        event_type_dict = {CEventTrap: {}}
        self.m_session_manager.register_callback(self.trap_handler, event_type_dict, fSingleUse = False)

        event_type_dict = {CEventForkMode: {}}
        self.m_session_manager.register_callback(self.fork_mode_handler, event_type_dict, fSingleUse = False)

        self.m_last_source_line = None
        self.m_last_nlines = DEFAULT_NUMBER_OF_LINES

        self.m_fAddPromptBeforeMsg = False
        self.m_eInLoop = threading.Event()
        self.cmdqueue.insert(0, '')

        self.m_stdout = self.stdout
        self.m_encoding = detect_encoding(self.stdin)

        g_fDefaultStd = (stdin == None)

        if self.use_rawinput:
            try:
                import readline
                cd = readline.get_completer_delims()
                if not '.' in cd:
                    readline.set_completer_delims(cd + '.')
            except:
                pass


    def set_filename(self, filename):
        assert(is_unicode(filename))

        self.m_filename = filename


    def precmd(self, line):
        line = as_unicode(line, self.m_encoding)

        self.m_fAddPromptBeforeMsg = True
        if not event_is_set(self.m_eInLoop):
            self.m_eInLoop.set()
            time.sleep(0.01)

        if not line.strip():
            return line

        command = line.split(' ', 1)[0].split(SOURCE_MORE, 1)[0].split(SOURCE_LESS, 1)[0]
        if command not in ['list', 'l']:
            self.m_last_source_line = None
            self.m_last_nlines = DEFAULT_NUMBER_OF_LINES

        return line


    def postcmd(self, stop, line):
        self.m_fAddPromptBeforeMsg = False

        return stop


    def onecmd(self, line):
        """
        Default Error handling and reporting of session manager errors.
        """

        try:
            return cmd.Cmd.onecmd(self, line)

        except (socket.error, CConnectionException):
            self.m_session_manager.report_exception(*sys.exc_info())
        except CException:
            self.m_session_manager.report_exception(*sys.exc_info())
        except:
            self.m_session_manager.report_exception(*sys.exc_info())
            print_debug_exception(True)

        return False


    def default(self, line):
        """
        Called on an input line when the command prefix is not recognized.
        Over-rides base method at cmd.py.
        """

        self.printer(STR_BAD_SYNTAX % line)


    def emptyline(self):
        pass


    def complete(self, text, state):
        """
        Return the next possible completion for 'text'.
        If a command has not been entered, then complete against command list.
        Otherwise try to call complete_<command> to get list of completions.
        """

        if self.use_rawinput:
            #
            # Import cmd to workaround a strange bug in Python.
            #
            import cmd
            return cmd.Cmd.complete(self, text, state)

        #
        # Without rawinput assuming text includes entire buffer up to cursor.
        #

        try:
            if state != 0:
                return self.completion_matches[state]

            if not ' ' in text:
                self.completion_matches = self.completenames(text)
                return self.completion_matches[state]

            cmd, args, foo = self.parseline(text)
            if cmd == '' or not hasattr(self, 'complete_' + cmd):
                self.completion_matches = self.completedefault(text)
                return self.completion_matches[state]

            compfunc = getattr(self, 'complete_' + cmd)

            self.completion_matches = compfunc(text)
            return self.completion_matches[state]

        except IndexError:
            return None


    def complete_launch(self, text, line = None, begidx = None, endidx = None):
        if line != None and endidx != None:
            text = line[:endidx]

        if text.endswith(' '):
            dn, bn = '', ''
        else:
            path = text.split()[-1]
            dn, bn = os.path.split(path)

        prefix = text
        if bn != '':
            prefix = prefix[:-len(bn)]

        if dn == '' and bn.startswith('~'):
            if bn == os.path.expanduser(bn):
                c = text
            else:
                c = os.path.join(text, '')

            if begidx != None:
                c = c[begidx:]

            return [c]

        pl = [dn]
        if dn == '':
            pl += os.environ['PATH'].split(os.pathsep)

        fl = []
        for p in pl:
            if p == '':
                p = '.'

            try:
                ep = os.path.expanduser(p)
                l = os.listdir(ep)
                for f in l:
                    if not f.startswith(bn):
                        continue

                    root, ext = os.path.splitext(f)
                    if not ext in ['.py', '.pyw', '']:
                        continue

                    if os.path.isdir(os.path.join(ep, f)):
                        c = prefix + os.path.join(f, '')
                    else:
                        c = prefix + f

                    if begidx != None:
                        c = c[begidx:]

                    fl.append(c)
            except:
                pass

        fs = set(fl)
        cl = list(fs)
        cl.sort()

        return cl


    def complete_eval(self, text, line = None, begidx = None, endidx = None):
        t = self.m_completion_thread
        if t != None and thread_is_alive(t):
            return []

        self.m_completion_thread = None
        result = [('', [])]

        if line != None and endidx != None:
            text = line[:endidx]

        t = threading.Thread(target = self.complete_expression_job, args = (text, result))
        t.start()
        t.join(PING_TIMEOUT)

        if thread_is_alive(t):
            self.m_completion_thread = t
            return []

        (prefix, completions) = result[-1]

        if begidx != None:
            prefix = prefix[begidx:]

        ce = [prefix + c for c in completions]

        return ce

    complete_v = complete_eval
    complete_exec = complete_eval
    complete_x = complete_exec


    def complete_expression_job(self, text, result):
        try:
            (prefix, completions) = self.m_session_manager.complete_expression(text)
            result.append((prefix, completions))

        except:
            print_debug_exception()


    def run(self):
        self.cmdloop()


    def __get_str_wrap(self, _str, max_len):
        if len(_str) <= max_len and not '\n' in _str:
            return (_str, '')

        s = _str[: max_len]

        i = s.find('\n')

        if i == -1:
            i = s.rfind(' ')

        if i == -1:
            return (s, _str[max_len:])

        return (_str[: i], _str[i + 1:])


    def printer(self, _str):
        if not event_is_set(self.m_eInLoop):
            self.m_eInLoop.wait()

        fAPBM = self.m_fAddPromptBeforeMsg
        prefix = ['', self.prompt.strip('\n')][fAPBM] + CONSOLE_PRINTER
        suffix = '\n' + [self.prompt.strip('\n'), ''][fAPBM]

        s = _str
        while s != '':
            s, _s = self.__get_str_wrap(s, CONSOLE_WRAP_INDEX - len(prefix + suffix))
            _print(prefix + s + suffix, self.m_stdout, feol = False)
            s = _s

        self.m_stdout.flush()


    def print_notice(self, notice):
        nl = notice.split('\n')

        i = 0
        for l in nl:
            _print(l, self.m_stdout)
            i += 1
            if i % PRINT_NOTICE_LINES_PER_SECTION == 0:
                _print("\n" + PRINT_NOTICE_PROMPT, self.m_stdout, feol = False)
                response = self.stdin.readline()
                if response != '\n':
                    break

                _print('', self.m_stdout)


    def event_handler(self, event):
        state = event.m_state
        if (state == STATE_BROKEN) and self.fPrintBroken:
            self.fPrintBroken = False
            self.printer(STR_DEBUGGER_HAS_BROKEN)
            return

        if (state != STATE_ANALYZE) and self.fAnalyzeMode:
            self.fAnalyzeMode = False
            self.prompt = [CONSOLE_PROMPT, ""][self.m_fSplit]
            self.printer(STR_ANALYZE_MODE_TOGGLE % MODE_OFF)
            return

        if (state == STATE_ANALYZE) and not self.fAnalyzeMode:
            self.fAnalyzeMode = True
            self.prompt = [CONSOLE_PROMPT_ANALYZE, ""][self.m_fSplit]
            self.printer(STR_ANALYZE_MODE_TOGGLE % MODE_ON)
            return


    def synchronicity_handler(self, event):
        self.printer(STR_SYNCHRONICITY_MODE % str(event.m_fsynchronicity))

    def breakonexit_handler( self, event):
        self.printer(STR_BREAKONEXIT_MODE % str(event.m_fbreakonexit))

    def trap_handler(self, event):
        self.printer(STR_TRAP_MODE_SET % str(event.m_ftrap))


    def fork_mode_handler(self, event):
        x = [FORK_PARENT, FORK_CHILD][event.m_ffork_into_child]
        y = [FORK_MANUAL, FORK_AUTO][event.m_ffork_auto]

        self.printer(STR_FORK_MODE_SET % (x, y))


    def do_launch(self, arg):
        fchdir, interpreter, command_line = parse_console_launch( arg )

        self.fPrintBroken = True

        try:
            self.m_session_manager.launch(fchdir, command_line, interpreter)
            return

        except BadArgument:
            self.printer(STR_BAD_ARGUMENT)
        except IOError:
            self.printer(STR_FILE_NOT_FOUND % arg)
        except:
            self.fPrintBroken = False
            raise

        self.fPrintBroken = False


    def do_restart(self, arg):
        if arg != '':
            self.printer(STR_BAD_ARGUMENT)
            return

        try:
            self.m_session_manager.restart()
            return

        except BadArgument:
            self.printer(STR_BAD_ARGUMENT)
        except IOError:
            self.printer(STR_FILE_NOT_FOUND % arg)
        except:
            self.fPrintBroken = False
            raise

        self.fPrintBroken = False


    def do_attach(self, arg):
        if arg == '':
            return self.__scripts(arg)

        self.fPrintBroken = True

        try:
            self.m_session_manager.attach(arg)
            return

        except BadArgument:
            self.printer(STR_BAD_ARGUMENT)
        except:
            self.fPrintBroken = False
            raise

        self.fPrintBroken = False


    def __scripts(self, arg):
        if self.m_session_manager.get_password() is None:
            _print(STR_PASSWORD_MUST_BE_SET, self.m_stdout)
            return

        host = self.m_session_manager.get_host()
        _print(STR_SCRIPTS_CONNECTING % host, self.m_stdout)

        (server_list, errors) = self.m_session_manager.calc_server_list()

        if server_list == []:
            _print(STR_SCRIPTS_NO_SCRIPTS % host, self.m_stdout)
            return

        try:
            spid = self.m_session_manager.get_server_info().m_pid
        except NotAttached:
            spid = None

        _print(STR_SCRIPTS_TO_DEBUG % host, self.m_stdout)
        for s in server_list:
            m = ['', SYMBOL_MARKER][spid == s.m_pid]
            _print(' %1s %-5d  %s' % (m, s.m_pid, s.m_filename), self.m_stdout)


    def do_detach(self, arg):
        if not arg == '':
            self.printer(STR_BAD_ARGUMENT)
            return

        self.m_session_manager.detach()


    def do_host(self, arg):
        if arg == '':
            host = self.m_session_manager.get_host()
            _print(host, self.m_stdout)
            return

        try:
            self.m_session_manager.set_host(arg)

        except socket.gaierror:
            e = sys.exc_info()[1]
            self.printer(MSG_ERROR_HOST_TEXT % (arg, e))


    def do_break(self, arg):
        if arg != '':
            self.printer(STR_BAD_ARGUMENT)
            return

        self.m_session_manager.request_break()

    do_b = do_break


    def __parse_bp_arg(self, arg, fAllowExpr = True):
        _args = arg.split(BP_EVAL_SEP, 1)

        if (len(_args) > 1) and (not fAllowExpr):
            raise BadArgument

        if len(_args) > 1:
            expr = _args[1].strip()
        else:
            expr = ''

        rf = _args[0].rfind(BP_FILENAME_SEP)
        if rf == -1:
            args = [_args[0]]
        else:
            args = [_args[0][:rf], _args[0][rf + 1:]]

        filename = ['', args[0]][len(args) > 1]

        if filename in [None, '']:
            filename = self.m_filename

        try:
            lineno = int(args[-1])
            scope = ''
        except ValueError:
            lineno = 0
            scope = args[-1].strip()

        return (filename, scope, lineno, expr)


    def do_go(self, arg):
        if self.fAnalyzeMode:
            self.printer(STR_ILEGAL_ANALYZE_MODE_CMD)
            return

        try:
            if arg != '':
                (filename, scope, lineno, expr) = self.__parse_bp_arg(arg, fAllowExpr = False)
                self.fPrintBroken = True
                self.m_session_manager.request_go_breakpoint(filename, scope, lineno)
                return

            self.fPrintBroken = True
            self.m_session_manager.request_go()
            return

        except BadArgument:
            self.printer(STR_BAD_ARGUMENT)
        except IOError:
            self.printer(STR_FILE_NOT_FOUND % filename)
        except InvalidScopeName:
            self.printer(STR_SCOPE_NOT_FOUND % scope)
        except DebuggerNotBroken:
            self.m_session_manager.report_exception(*sys.exc_info())
        except:
            self.fPrintBroken = False
            raise

        self.fPrintBroken = False

    do_g = do_go


    def do_step(self, arg):
        if arg != '':
            self.printer(STR_BAD_ARGUMENT)
            return

        if self.fAnalyzeMode:
            self.printer(STR_ILEGAL_ANALYZE_MODE_CMD)
            return

        try:
            self.m_session_manager.request_step()

        except DebuggerNotBroken:
            self.m_session_manager.report_exception(*sys.exc_info())

    do_s = do_step


    def do_next(self, arg):
        if arg != '':
            self.printer(STR_BAD_ARGUMENT)
            return

        if self.fAnalyzeMode:
            self.printer(STR_ILEGAL_ANALYZE_MODE_CMD)
            return

        try:
            self.m_session_manager.request_next()

        except DebuggerNotBroken:
            self.m_session_manager.report_exception(*sys.exc_info())

    do_n = do_next


    def do_return(self, arg):
        if arg != '':
            self.printer(STR_BAD_ARGUMENT)
            return

        if self.fAnalyzeMode:
            self.printer(STR_ILEGAL_ANALYZE_MODE_CMD)
            return

        try:
            self.m_session_manager.request_return()

        except DebuggerNotBroken:
            self.m_session_manager.report_exception(*sys.exc_info())

    do_r = do_return


    def do_jump(self, arg):
        try:
            lineno = int(arg)
        except ValueError:
            self.printer(STR_BAD_ARGUMENT)
            return

        try:
            self.m_session_manager.request_jump(lineno)

        except DebuggerNotBroken:
            self.m_session_manager.report_exception(*sys.exc_info())

    do_j = do_jump


    def do_bp(self, arg):
        if arg == '':
            self.printer(STR_BAD_ARGUMENT)
            return

        try:
            (filename, scope, lineno, expr) = self.__parse_bp_arg(arg, fAllowExpr = True)
            self.m_session_manager.set_breakpoint(filename, scope, lineno, True, expr)

        except BadArgument:
            self.printer(STR_BAD_ARGUMENT)
        except IOError:
            self.printer(STR_FILE_NOT_FOUND % filename)
        except InvalidScopeName:
            self.printer(STR_SCOPE_NOT_FOUND % scope)
        except SyntaxError:
            self.printer(STR_BAD_EXPRESSION % expr)
        except DebuggerNotBroken:
            self.m_session_manager.report_exception(*sys.exc_info())


    def do_be(self, arg):
        if arg == '':
            self.printer(STR_BAD_ARGUMENT)
            return

        try:
            id_list = []
            fAll = (arg == SYMBOL_ALL)

            if not fAll:
                sid_list = arg.split()
                id_list = [int(sid) for sid in sid_list]

            self.m_session_manager.enable_breakpoint(id_list, fAll)

        except ValueError:
            self.printer(STR_BAD_ARGUMENT)


    def do_bd(self, arg):
        if arg == '':
            self.printer(STR_BAD_ARGUMENT)
            return

        try:
            id_list = []
            fAll = (arg == SYMBOL_ALL)

            if not fAll:
                sid_list = arg.split()
                id_list = [int(sid) for sid in sid_list]

            self.m_session_manager.disable_breakpoint(id_list, fAll)

        except ValueError:
            self.printer(STR_BAD_ARGUMENT)


    def do_bc(self, arg):
        if arg == '':
            self.printer(STR_BAD_ARGUMENT)
            return

        try:
            id_list = []
            fAll = (arg == SYMBOL_ALL)

            if not fAll:
                sid_list = arg.split()
                id_list = [int(sid) for sid in sid_list]

            self.m_session_manager.delete_breakpoint(id_list, fAll)

        except ValueError:
            self.printer(STR_BAD_ARGUMENT)


    def do_bl(self, arg):
        bpl = self.m_session_manager.get_breakpoints()

        bplk = list(bpl.keys())
        bplk.sort()

        _print(STR_BREAKPOINTS_LIST, self.m_stdout)
        for id in bplk:
            bp = bpl[id]

            if bp.m_expr:
                expr = bp.m_expr
            else:
                expr = ''

            try:
                expr.encode('ascii', 'strict')
                encoding = ''
            except:
                encoding = bp.m_encoding

            scope = bp.m_scope_fqn

            if scope.startswith(MODULE_SCOPE + '.'):
                scope = scope[len(MODULE_SCOPE) + 1:]

            elif scope.startswith(MODULE_SCOPE2 + '.'):
                scope = scope[len(MODULE_SCOPE2) + 1:]

            state = [STATE_DISABLED, STATE_ENABLED][bp.isEnabled()]
            s = STR_BREAKPOINTS_TEMPLATE % (id, state, bp.m_lineno, clip_filename(bp.m_filename, 45), calc_suffix(scope, 45), calc_prefix(expr, 50), encoding)
            _print(s.rstrip() + '\n', self.m_stdout)


    def do_save(self, arg):
        self.m_session_manager.save_breakpoints(arg)
        _print(STR_BREAKPOINTS_SAVED, self.m_stdout)
        return


    def do_load(self, arg):
        try:
            self.m_session_manager.load_breakpoints(arg)
            _print(STR_BREAKPOINTS_LOADED, self.m_stdout)
            return

        except IOError:
            error = [STR_BREAKPOINTS_FILE_NOT_FOUND, STR_BREAKPOINTS_NOT_FOUND][arg == '']
            self.printer(error)


    def do_stack(self, arg):
        if self.fAnalyzeMode and (arg != ''):
            self.printer(STR_ILEGAL_ANALYZE_MODE_ARG)
            return

        try:
            tid_list = []
            fAll = (arg == SYMBOL_ALL)

            if not fAll:
                sid_list = arg.split()
                tid_list = [int(sid) for sid in sid_list]

            sl = self.m_session_manager.get_stack(tid_list, fAll)

            if len(sl) == 0:
                self.printer(STR_NO_THREADS_FOUND)
                return

            frame_index = self.m_session_manager.get_frame_index()

            m = None
            for st in sl:
                s = st.get(DICT_KEY_STACK, [])
                tid = st.get(DICT_KEY_TID, 0)
                fBroken = st.get(DICT_KEY_BROKEN, False)
                fCurrent = st.get(DICT_KEY_CURRENT_TID, False)

                if m is not None:
                    _print('', self.m_stdout)

                _print(STR_STACK_TRACE % tid, self.m_stdout)
                i = 0
                while i < len(s):
                    e = s[-(1 + i)]

                    marker = [SOURCE_STATE_UNBROKEN, SYMBOL_MARKER][fBroken]

                    if fCurrent:
                        m = ['', marker][i == frame_index]
                    else:
                        m = ['', marker][i == 0]

                    _print(' %1s %5d  %-28s  %4d  %s' % (m, i, calc_suffix(e[0], 28), e[1], calc_prefix(e[2], 20)), self.m_stdout)
                    i += 1

        except ValueError:
            self.printer(STR_BAD_ARGUMENT)
        except (NoExceptionFound, NoThreads):
            self.m_session_manager.report_exception(*sys.exc_info())

    do_k = do_stack


    def do_list(self, arg):
        rf = arg.rfind(BP_FILENAME_SEP)
        if rf == -1:
            _filename = ''
            __args2 = arg
        else:
            _filename = arg[:rf]
            __args2 = arg[rf + 1:]

        _args = __args2.split(BP_EVAL_SEP)

        fAll = (_args[0] == SYMBOL_ALL)
        fMore = (_args[0] == SOURCE_MORE)
        fLess = (_args[0] == SOURCE_LESS)
        fEntire = (_args[0] == SOURCE_ENTIRE_FILE)
        fCurrent = (_args[0] == '')
        fLine = False
        l = 1

        try:
            if len(_args) > 1:
                nlines = int(_args[1])
            else:
                nlines = self.m_last_nlines

            if not (fAll or fMore or fLess or fEntire or fCurrent):
                l = int(_args[0])
                fLine = True

        except ValueError:
            self.printer(STR_BAD_ARGUMENT)
            return

        if self.fAnalyzeMode and fAll:
            self.printer(STR_ILEGAL_ANALYZE_MODE_ARG)
            return

        if fMore and self.m_last_source_line:
            l = max(1, self.m_last_source_line + self.m_last_nlines // 2 + 1)
            fLine = True
        elif fLess and self.m_last_source_line:
            l = max(1, self.m_last_source_line - (self.m_last_nlines - 1) // 2 - nlines)
            fLine = True

        try:
            if fEntire:
                r = [self.m_session_manager.get_source_file(_filename, -1, -1)]
            elif fLine:
                r = [self.m_session_manager.get_source_file(_filename, l, nlines)]
            elif _filename != '':
                r = [self.m_session_manager.get_source_file(_filename, l, nlines)]
            else:
                r = self.m_session_manager.get_source_lines(nlines, fAll)

            if len(r) == 0:
                self.printer(STR_NO_THREADS_FOUND)
                return

            m = None
            for d in r:
                tid = d.get(DICT_KEY_TID, 0)
                filename = d.get(DICT_KEY_FILENAME, '')
                breakpoints = d.get(DICT_KEY_BREAKPOINTS, {})
                source_lines = d.get(DICT_KEY_LINES, [])
                first_lineno = d.get(DICT_KEY_FIRST_LINENO, 0)

                if len(r) == 1 and first_lineno != 0:
                    l = first_lineno

                fBroken = d.get(DICT_KEY_BROKEN, False)
                frame_event = d.get(DICT_KEY_EVENT, '')
                frame_lineno = d.get(DICT_KEY_FRAME_LINENO, 0)

                if m is not None:
                    _print('', self.m_stdout)

                _print(STR_SOURCE_LINES % (tid, filename), self.m_stdout)
                for i, line in enumerate(source_lines):
                    lineno = first_lineno + i
                    if lineno != frame_lineno:
                        m = ''
                    elif not fBroken:
                        m = SOURCE_STATE_UNBROKEN + SYMBOL_MARKER
                    elif frame_event == 'call':
                        m = SOURCE_EVENT_CALL + SYMBOL_MARKER
                    elif frame_event == 'line':
                        m = SOURCE_EVENT_LINE + SYMBOL_MARKER
                    elif frame_event == 'return':
                        m = SOURCE_EVENT_RETURN + SYMBOL_MARKER
                    elif frame_event == 'exception':
                        m = SOURCE_EVENT_EXCEPTION + SYMBOL_MARKER

                    if breakpoints.get(lineno, None) == STATE_ENABLED:
                        b = SOURCE_BP_ENABLED
                    elif breakpoints.get(lineno, None) == STATE_DISABLED:
                        b = SOURCE_BP_DISABLED
                    else:
                        b = ''

                    line = line.replace('\t', ' ' * PYTHON_TAB_WIDTH)

                    _print(' %2s %1s %5d  %s' % (m, b, lineno, calc_prefix(line[:-1], 60)), self.m_stdout)

            if fAll or fEntire:
                self.m_last_source_line = None
            elif len(source_lines) != 0:
                self.m_last_source_line = [l + (nlines - 1) // 2, frame_lineno][l == -1]

            self.m_last_nlines = nlines

        except (InvalidFrame, IOError):
            self.printer(STR_SOURCE_NOT_FOUND)
        except (NoExceptionFound, NoThreads):
            self.m_session_manager.report_exception(*sys.exc_info())

    do_l = do_list


    def do_up(self, arg):
        if arg != '':
            self.printer(STR_BAD_ARGUMENT)
            return

        try:
            fi = self.m_session_manager.get_frame_index()
            self.m_session_manager.set_frame_index(fi - 1)

        except DebuggerNotBroken:
            self.m_session_manager.report_exception(*sys.exc_info())


    def do_down(self, arg):
        if arg != '':
            self.printer(STR_BAD_ARGUMENT)
            return

        try:
            fi = self.m_session_manager.get_frame_index()
            self.m_session_manager.set_frame_index(fi + 1)

        except DebuggerNotBroken:
            self.m_session_manager.report_exception(*sys.exc_info())


    def evaluate_job(self, sync_event, expr):
        try:
            (value, warning, error) = self.m_session_manager.evaluate(expr)

            if warning:
                self.printer(STR_WARNING % warning)

            if error:
                _print(error + '\n', self.m_stdout)

            _print(value, self.m_stdout)

            if event_is_set(sync_event):
                _print(self.prompt, self.m_stdout, feol = False)

            return

        except (NoExceptionFound, DebuggerNotBroken):
            self.m_session_manager.report_exception(*sys.exc_info())

        except (socket.error, CConnectionException):
            self.m_session_manager.report_exception(*sys.exc_info())
        except CException:
            self.m_session_manager.report_exception(*sys.exc_info())
        except:
            self.m_session_manager.report_exception(*sys.exc_info())
            print_debug_exception(True)


    def do_eval(self, arg):
        if arg == '':
            self.printer(STR_BAD_ARGUMENT)
            return

        sync_event = threading.Event()
        t = threading.Thread(target = self.evaluate_job, args = (sync_event, arg))
        t.start()
        t.join(WAIT_FOR_BREAK_TIMEOUT)

        if thread_is_alive(t):
            _print(STR_OUTPUT_WARNING_ASYNC, self.m_stdout)
            sync_event.set()

    do_v = do_eval


    def execute_job(self, sync_event, suite):
        try:
            (warning, error) = self.m_session_manager.execute(suite)

            if warning:
                self.printer(STR_WARNING % warning)

            if error:
                _print(error + '\n', self.m_stdout)

            if event_is_set(sync_event):
                _print(self.prompt, self.m_stdout, feol = False)

            return

        except (NoExceptionFound, DebuggerNotBroken):
            self.m_session_manager.report_exception(*sys.exc_info())

        except (socket.error, CConnectionException):
            self.m_session_manager.report_exception(*sys.exc_info())
        except CException:
            self.m_session_manager.report_exception(*sys.exc_info())
        except:
            self.m_session_manager.report_exception(*sys.exc_info())
            print_debug_exception(True)


    def do_exec(self, arg):
        if arg == '':
            self.printer(STR_BAD_ARGUMENT)
            return

        _print(STR_OUTPUT_WARNING, self.m_stdout)

        sync_event = threading.Event()
        t = threading.Thread(target = self.execute_job, args = (sync_event, arg))
        t.start()
        t.join(WAIT_FOR_BREAK_TIMEOUT)

        if thread_is_alive(t):
            _print(STR_OUTPUT_WARNING_ASYNC, self.m_stdout)
            sync_event.set()

    do_x = do_exec


    def do_encoding(self, arg):
        if arg == '':
            encoding, fraw = self.m_session_manager.get_encoding()
            if encoding != ENCODING_AUTO:
                try:
                    codecs.lookup(encoding)
                except:
                    encoding += ' (?)'

            if fraw:
                encoding += ', ' + ENCODING_RAW

            _print(STR_ENCODING_MODE % encoding, self.m_stdout)
            return

        if ',' in arg:
            encoding, raw = arg.split(',')
        else:
            encoding, raw = arg, ''

        encoding = encoding.strip()
        if encoding == '':
            encoding, fraw = self.m_session_manager.get_encoding()

        fraw = 'raw' in raw

        self.m_session_manager.set_encoding(encoding, fraw)

        if encoding != ENCODING_AUTO:
            try:
                codecs.lookup(encoding)
            except:
                encoding += ' (?)'
                _print(STR_ENCODING_BAD, self.m_stdout)

        if fraw:
            encoding += ', ' + ENCODING_RAW

        _print(STR_ENCODING_MODE_SET % encoding, self.m_stdout)


    def do_thread(self, arg):
        if self.fAnalyzeMode and (arg != ''):
            self.printer(STR_ILEGAL_ANALYZE_MODE_ARG)
            return

        try:
            if arg != '':
                tid = int(arg)
                self.m_session_manager.set_thread(tid)

                _print(STR_THREAD_FOCUS_SET, self.m_stdout)
                return

            (current_thread_id, tl) = self.m_session_manager.get_thread_list()

            _print(STR_ACTIVE_THREADS, self.m_stdout)
            for i, t in enumerate(tl):
                m = ['', SYMBOL_MARKER][t[DICT_KEY_TID] == current_thread_id]
                state = [STATE_RUNNING, STR_STATE_BROKEN][t[DICT_KEY_BROKEN]]
                _print(' %1s %3d  %5d  %-15s  %s' % (m, i, t[DICT_KEY_TID], t[DICT_KEY_NAME], state[:25]), self.m_stdout)

        except ValueError:
            self.printer(STR_BAD_ARGUMENT)
        except ThreadNotFound:
            self.printer(STR_THREAD_NOT_FOUND)
        except DebuggerNotBroken:
            self.m_session_manager.report_exception(*sys.exc_info())

    do_t = do_thread


    def do_analyze(self, arg):
        if arg != '':
            self.printer(STR_BAD_ARGUMENT)
            return

        try:
            self.m_session_manager.set_analyze(not self.fAnalyzeMode)

        except DebuggerNotBroken:
            self.m_session_manager.report_exception(*sys.exc_info())

    do_a = do_analyze

    def do_breakonexit(self, arg):
        if arg == '':
            fbreakonexit = self.m_session_manager.get_breakonexit()
            _print(STR_BREAKONEXIT_MODE % str(fbreakonexit), self.m_stdout)
            return

        if arg == str(True):
            fbreakonexit = True
        elif arg == str(False):
            fbreakonexit = False
        else:
            _print(STR_BAD_ARGUMENT, self.m_stdout)
            return

        self.m_session_manager.set_breakonexit(fbreakonexit)


    def do_synchro(self, arg):
        if arg == '':
            fsynchronicity = self.m_session_manager.get_synchronicity()
            _print(STR_SYNCHRONICITY_MODE % str(fsynchronicity), self.m_stdout)
            return

        if arg == str(True):
            fsynchronicity = True
        elif arg == str(False):
            fsynchronicity = False
        else:
            _print(STR_BAD_ARGUMENT, self.m_stdout)
            return

        self.m_session_manager.set_synchronicity(fsynchronicity)


    def do_trap(self, arg):
        if arg == '':
            ftrap = self.m_session_manager.get_trap_unhandled_exceptions()
            _print(STR_TRAP_MODE % str(ftrap), self.m_stdout)
            return

        if arg == str(True):
            ftrap = True
        elif arg == str(False):
            ftrap = False
        else:
            _print(STR_BAD_ARGUMENT, self.m_stdout)
            return

        self.m_session_manager.set_trap_unhandled_exceptions(ftrap)


    def do_fork(self, arg):
        (ffork_into_child, ffork_auto) = self.m_session_manager.get_fork_mode()

        if arg == '':
            x = [FORK_PARENT, FORK_CHILD][ffork_into_child]
            y = [FORK_MANUAL, FORK_AUTO][ffork_auto]

            _print(STR_FORK_MODE % (x, y), self.m_stdout)
            return

        arg = arg.lower()

        if FORK_PARENT in arg:
            ffork_into_child = False
        elif FORK_CHILD in arg:
            ffork_into_child = True

        if FORK_AUTO in arg:
            ffork_auto = True
        elif FORK_MANUAL in arg:
            ffork_auto = False

        self.m_session_manager.set_fork_mode(ffork_into_child, ffork_auto)


    def do_password(self, arg):
        if arg == '':
            _rpdb2_pwd = self.m_session_manager.get_password()
            if _rpdb2_pwd is None:
                _print(STR_PASSWORD_NOT_SET, self.m_stdout)
            else:
                _print(STR_PASSWORD_SET % _rpdb2_pwd, self.m_stdout)
            return

        _rpdb2_pwd = arg.strip('"\'')

        try:
            self.m_session_manager.set_password(_rpdb2_pwd)
            _print(STR_PASSWORD_SET % _rpdb2_pwd, self.m_stdout)

        except BadArgument:
            _print(STR_PASSWORD_BAD, self.m_stdout)


    def do_remote(self, arg):
        if arg == '':
            fAllowRemote = self.m_session_manager.get_remote()
            _print(STR_REMOTE_MODE % str(fAllowRemote), self.m_stdout)
            return

        if arg == str(True):
            fAllowRemote = True
        elif arg == str(False):
            fAllowRemote = False
        else:
            _print(STR_BAD_ARGUMENT, self.m_stdout)
            return

        self.m_session_manager.set_remote(fAllowRemote)
        _print(STR_REMOTE_MODE % str(fAllowRemote), self.m_stdout)


    def do_env(self, arg):
        env = self.m_session_manager.get_environ()

        if arg == '':
            if len(env) == 0:
                _print(STR_ENVIRONMENT_EMPTY, self.m_stdout)
                return

            _print(STR_ENVIRONMENT, self.m_stdout)
            for k, v in env:
                _print('%s=%s' % (k, v), self.m_stdout)
            return

        if arg[:2] == '-d':
            k = arg[2:].strip()
            _env = [(_k, _v) for (_k, _v) in env if _k != k]
            self.m_session_manager.set_environ(_env)
            return

        try:
            k, v = arg.split('=')
            k = k.strip()
            v = v.strip()

        except ValueError:
            self.printer(STR_BAD_ARGUMENT)
            return

        _env = [(_k, _v) for (_k, _v) in env if _k != k]
        _env.append((k, v))

        self.m_session_manager.set_environ(_env)


    def do_stop(self, arg):
        self.m_session_manager.stop_debuggee()


    def do_exit(self, arg):
        if arg != '':
            self.printer(STR_BAD_ARGUMENT)
            return

        if self.m_session_manager.get_state() != STATE_DETACHED:
            try:
                self.do_stop('')

            except (socket.error, CConnectionException):
                self.m_session_manager.report_exception(*sys.exc_info())
            except CException:
                self.m_session_manager.report_exception(*sys.exc_info())
            except:
                self.m_session_manager.report_exception(*sys.exc_info())
                print_debug_exception(True)

        _print('', self.m_stdout)

        return True

    do_EOF = do_exit


    def do_copyright(self, arg):
        self.print_notice(COPYRIGHT_NOTICE)


    def do_license(self, arg):
        self.print_notice(LICENSE_NOTICE + COPY_OF_THE_GPL_LICENSE)


    def do_credits(self, arg):
        self.print_notice(CREDITS_NOTICE)


    def do_help(self, arg):
        cmd.Cmd.do_help(self, arg)

        if arg == '':
            help_notice = """Security:
----------------

password    - Get or set the channel password.
remote      - Get or set "allow connections from remote machines" mode.

Session Control:
-----------------

env         - Display or set the environment setting for new sessions.
host        - Display or change host.
attach      - Display scripts or attach to a script on host.
detach      - Detach from script.
launch      - Start a script and attach to it.
restart     - Restart a script.
stop        - Shutdown the debugged script.
exit        - Exit from debugger.

Debuggee Control:
-----------------

break       - Request an immediate break.
step        - Continue to the next execution line.
next        - Continue to the next execution line in the current frame.
return      - Continue until the debugger is about to return from the frame.
jump        - Jump to a line in the current scope.
go          - Continue execution.

Breakpoints Control:
--------------------

bp          - Set a break point.
bd          - Disable a breakpoint.
be          - Enable a breakpoint.
bc          - Clear (delete) a breakpoint.
bl          - List all breakpoints.
load        - Load session breakpoints.
save        - save session breakpoints.

Misc:
-----

thread      - Display threads or switch to a particular thread.
list        - List source code.
stack       - Display stack trace.
up          - Go up one frame in stack.
down        - Go down one frame in stack.
encoding    - Set the source encoding used by exec and eval commands.
eval        - Evaluate expression in the context of the current frame.
exec        - Execute suite in the context of the current frame.
analyze     - Toggle analyze last exception mode.
trap        - Get or set "trap unhandled exceptions" mode.
fork        - Get or set fork handling mode.
synchro     - Get or set synchronicity mode.
breakonexit - Get or set break-on-exit mode.

License:
----------------

copyright   - Print copyright notice.
license     - Print license.
credits     - Print credits information.


type help <topic> for futher information."""

            self.print_notice(help_notice)


    def help_copyright(self):
        _print("""copyright

Print copyright notice.""", self.m_stdout)


    def help_license(self):
        _print("""license

Print license.""", self.m_stdout)


    def help_credits(self):
        _print("""credits

Print credits information.""", self.m_stdout)


    def help_help(self):
        _print("""help <cmd>

Print help for command <cmd>.
On the other hand I guess that you already know that, don't you?""", self.m_stdout)


    def help_analyze(self):
        _print("""analyze

(shorthand - a)

Toggle analyze last exception mode.

The following changes to the debugger behavior apply in analyze mode:
The debugger prompt changes to 'Analyze>'.
'go', 'step', 'next', and 'return' are not allowed.
'thread' does not allow to change the thread focus.
'stack' allows no arguments.
'list' does not accept the '*' (all threads) argument
'stack', 'list', 'eval', 'exec', 'up', and 'down' operate on the thrown
exception.""", self.m_stdout)

    help_a = help_analyze


    def help_password(self):
        _print("""password <password>

Get or set the channel password.

Communication between the console and the debuggee is always authenticated and
optionally encrypted. The password (A secret known to the console and the
debuggee alone) governs both security methods. The password is never
communicated between the two components on the communication channel.

A password is always required since unsecured communication between the
console and the debuggee might expose your machine to attacks.""", self.m_stdout)


    def help_remote(self):
        _print("""remote [True | False]

Get or set "allow connections from remote machines" mode.

When set to False:
Newly launched debuggees will listen on localhost only. In this mode, debugger
consoles on remote machines will NOT BE able to see or attach to the debuggee.

When set to True:
Newly launched debuggees will listen on INADDR_ANY. In this mode, debugger
consoles on remote machines will BE able to see and attach to the debuggee.""", self.m_stdout)


    def help_trap(self):
        _print("""trap [True | False]

Get or set "trap unhandled exceptions" mode.

When set to False:
Debuggee will ignore unhandled exceptions.

When set to True:
Debuggee will pause on unhandled exceptions for inspection.""", self.m_stdout)


    def help_breakonexit(self):
        _print("""breakonexit [True | False]

Get or set the break-on-exit mode.

If you want to debug the atexit handlers, you need
to set break-on-exit to True. The debugger will then
break just before executing the atexit handlers.

Default is False.""", self.m_stdout)

    def help_synchro(self):
        _print("""synchro [True | False]

Get or set the synchronicity mode.

Traditional Python debuggers that use the inspected thread
(usually the main thread) to query or modify the script
name-space have to wait until the script hits a break-point.
Synchronicity allows the debugger to query and modify the
script name-space even if its threads are still running or
blocked in C library code by using special worker threads.
In some rare cases querying or modifying data in
synchronicity can crash the script. For example in some
Linux builds of wxPython querying the state of wx objects
from a thread other than the GUI thread can crash the
script. If this happens or if you want to restrict these
operations to the inspected thread, turn synchronicity off.

Default is True.""", self.m_stdout)


    def help_fork(self):
        _print("""fork [parent | child] [manual | auto]

Get or set fork handling mode.

Without arguments returns the current mode.

When 'parent' is specified the debugger will continue to debug the original
parent process after a fork.

When 'child' is specified the debugger will switch to debug the forked
child process after a fork.

When 'manual' is specified the debugger will pause before doing a fork.

When 'auto' is specified the debugger will go through the fork without
pausing and will make the forking decision based on the parent/child
setting.

WARNING:
On some Posix OS such as FreeBSD, Stepping into the child fork
can result in termination of the child process since the debugger
uses threading for its operation and on these systems threading and
forking can conflict.
""", self.m_stdout)


    def help_stop(self):
        _print("""stop

Shutdown the debugged script.""", self.m_stdout)


    def help_launch(self):
        _print("""launch [-k] [-i interpreter] <script_name> [<script_args>]

Start script <script_name> and attach to it.

-k  Don't change the current working directory. By default the working
    directory of the launched script is set to its folder.

-i Specify a custom interpreter to use.""", self.m_stdout)


    def help_restart(self):
        _print("""restart

Restart a script with same arguments from last launch.""", self.m_stdout)



    def help_attach(self):
        _print("""attach [<arg>]

Without an argument, 'attach' prints the scripts available for debugging
on the selected host. To select a host use the 'host' command. A script is
considered available for debugging only if it is using the rpdb2 module or
has been executed by the debugger.
If the debugger is already attached to a script, a special character will
mark that script in the list.

When <arg> is an integer the debugger will try to attach to a script with
that pid.
When <arg> is a string the debugger will try to attach to a script
with that name in the list.""", self.m_stdout)


    def help_detach(self):
        _print("""detach

Detach from the script the debugger is currently attached to. The detached
script will continue execution.""", self.m_stdout)


    def help_break(self):
        _print("""break

(shorthand - b)

Request script to break (pause execution as if it hit a breakpoint).
The 'break' command returns immdeiately but the break is only established
when an active thread submits to the debugger control. If a thread is
doing a system call or executing C code, this will happen only when
it returns to do python code.""", self.m_stdout)

    help_b = help_break


    def help_bp(self):
        _print("""bp [<filename>':'] (<line> | <scope>) [',' <expr>]

Set a breakpoint.

<filename> - either the filename or the module name.
<line>     - is the line number to assign the breakpoint to.
<scope>    - is a "fully qualified" function name. That is, not only the
             function name but also the class name (in case of a member
             function), such as MyClass.MyMemberFunction.
<expr>     - condition to evaluate in the context of the frame. If it
             evaluates to 'True' the break point will break into the debugger.

In case the <filemame> is omitted, the current file is assumed. In this case
the debuggee has to be waiting at break point.

Examples:

    bp test_file.py:20
    bp test_file.py:MyClass.Foo
    bp 304

Type 'help break' for more information on breakpoints and threads.""", self.m_stdout)


    def help_be(self):
        _print("""be (<id_list> | '*')

Enable breakpoints.

<id_list> - is a space delimited list of at least one breakpoint id
'*' - Enable all breakpoints.""", self.m_stdout)


    def help_bd(self):
        _print("""bd (<id_list> | '*')

Disable breakpoints.

<id_list> - is a space delimited list of at least one breakpoint id
'*' - disable all breakpoints.""", self.m_stdout)


    def help_bc(self):
        _print("""bc (<id_list> | '*')

Clear (delete) breakpoints.

<id_list> - is a space delimited list of at least one breakpoint id
'*' - clear all breakpoints.""", self.m_stdout)


    def help_bl(self):
        _print("""bl

List all breakpoints, sorted by their id.""", self.m_stdout)


    def help_load(self):
        _print("""load [<filename>]

Load breakpoints.

<filename> - optional breakpoints filename. The filename should not include
             a file extension.""", self.m_stdout)


    def help_save(self):
        _print("""save [<filename>]

save breakpoints.

<filename> - optional breakpoints filename. The filename should not include
             a file extension.""", self.m_stdout)


    def help_go(self):
        _print("""go [[<filename>':'] (<line> | <scope>)]

(shorthand - g)

Resume execution of a script that is waiting at break point.
If an argument is present, continue execution until that argument is reached.

<filename> - is the file name which basically is the script's name without
             the '.py' extension.
<line>   - is the line number to assign the breakpoint to.
<scope>  - is a "fully qualified" function name. That is, not only the
           function name but also the class name (in case of a member
           function), such as MyClass.MyMemberFunction.""", self.m_stdout)

    help_g = help_go


    def help_exit(self):
        _print("""exit

Exit the debugger. If the debugger is attached to a script, the debugger
will attempt to detach from the script first.""", self.m_stdout)

    help_EOF = help_exit


    def help_host(self):
        _print("""host [<arg>]

Without an argument, 'host' prints the current selected host.
With an argument <arg>, 'host' attempts to resolve <arg> to a known ip
address or a domain name. If it is successful, that host will become the
selected host.
The default selected host is the local host.
Subsequent 'attach' commands will be done on the selected host.

Type 'help attach' for more information.""", self.m_stdout)

    def help_stack(self):
        _print("""stack [<tid> | '*']

(shorthand - k)

Without an argument, 'stack' prints the stack trace of the focused thread.
If the thread is waiting at break point a special character will mark the
focused frame.

<tid> - print the stack of thread <tid>
'*'   - print the stacks of all active threads.

Type 'help break' for more information on breakpoints and threads.
Type 'help up' or 'help down' for more information on focused frames.""", self.m_stdout)

    help_k = help_stack


    def help_list(self):
        _print("""list [<file_name>:][<line_no> | '+' | '-' | '^' | '*'] [',' <nlines>]

(shorthand - l)

Without an argument, 'list' prints the source lines around the current line
of the focused thread in the focused frame. A special character sequence will
mark the current line according to the event:

    'C>' - call - A function is called.
    'L>' - line - The interpreter is about to execute a new line of code.
    'R>' - return - A function is about to return.
    'E>' - exception - An exception has been thrown.
    '*>' - running - The thread is running.

If a breakpoint is assigned to a line, that line will be marked with:

    'B' - if the breakpoint is enabled
    'D' - if the breakpoint is disabled

<file_name> - List source from filename
<line_no>   - Print the source lines around that line number in the same file
              of the current line.
'+'         - Print the next lines in the file.
'-'         - Print the previous lines in the file.
'^'         - Print the entire file.
'*'         - Print the source lines for each of the active threads.
<nlines>    - Print <nlines> of source

Type 'help break' for more information on breakpoints and threads.
Type 'help up' or 'help down' for more information on focused frames.""", self.m_stdout)

    help_l = help_list


    def help_thread(self):
        _print("""thread [<no> | <tid>]

(shorthand - t)

Without an argument, 'thread' prints the list of known active threads, with
their corresponding state, which can be either 'running' or
'waiting at break point'. A special character will mark the focused thread.

With an argument <tid>, 'thread' will attempt to set the debugger focus to
the thread of that tid.
With an argument <no>, 'thread' will attempt to set the debugger focus to
the thread of that order in the thread list.

Type 'help break' for more information on breakpoints and threads.""", self.m_stdout)

    help_t = help_thread


    def help_jump(self):
        _print("""jump <lineno>

(shorthand - j)

Jump to line <lineno> in the current scope.""", self.m_stdout)

    help_j = help_jump


    def help_next(self):
        _print("""next

(shorthand - n)

Continue execution until the next line in the current function
is reached or it returns.""", self.m_stdout)

    help_n = help_next


    def help_step(self):
        _print("""step

(shorthand - s)

Execute the current line, stop at the first possible occasion
(either in a function that is called or in the current function).""", self.m_stdout)

    help_s = help_step


    def help_return(self):
        _print("""return

(shorthand - r)

Continue execution until the current function returns.""", self.m_stdout)

    help_r = help_return


    def help_up(self):
        _print("""up

move the debugger focus one frame up the stack of the debugged thread
(closer to the current, most recently executed frame). Evaluation of
expressions or execution of statements will be done at the local and global
name spaces of the focused frame.

Type 'help eval' for more information on evaluation of expressions.
Type 'help exec' for more information on execution of statements.""", self.m_stdout)


    def help_down(self):
        _print("""down

move the debugger focus one frame down the stack of the debugged thread
(closer to the current, most recently executed frame). Evaluation of
expressions or execution of statements will be done at the local and global
name spaces of the focused frame.

Type 'help eval' for more information on evaluation of expressions.
Type 'help exec' for more information on execution of statements.""", self.m_stdout)


    def help_eval(self):
        _print("""eval <expr>

(shorthand - v)

Evaluate the python expression <expr> under the global and local name spaces
of the currently focused frame.

Example:
'eval locals()' - will display the dictionary of the local variables.

IMPORTANT: Any changes to the global name space will be discarded unless the
focused stack frame is the top most frame.

Type 'help up' or 'help down' for more information on focused frames.""", self.m_stdout)

    help_v = help_eval


    def help_exec(self):
        _print("""exec <stmt>

(shorthand - x)

Execute the python suite <stmt> under the global and local name spaces
of the currently focused frame.

Example:
'exec i += 1'

IMPORTANT: Any changes to the global name space will be discarded unless the
focused stack frame is the top most frame.

Type 'help up' or 'help down' for more information on focused frames.""", self.m_stdout)

    help_x = help_exec


    def help_encoding(self):
        _print("""encoding [<encoding> [, raw]]

Set the source encoding for the exec and eval commands.

Without an argument returns the current encoding.

The specified encoding can be either 'auto' or any encoding accepted
by the codecs module. If 'auto' is specified, the source encoding of
the active scope will be used, which is utf-8 by default.

The default encoding value is 'auto'.

If 'raw' is specified, strings returned by the eval command
will represent non ASCII characters as an escape sequence.""", self.m_stdout)


    def help_env(self):
        _print("""env [-d key | key = value]

Set the environment variables mapping. This mapping is used
when a new script is launched to modify its environment.

Example for a mapping on Windows:
env Path = %Path%;c:\\mydir

Example for a mapping on Linux:
env PATH = $PATH:~/mydir

To delete the mapping for PATH
env -d PATH

Without an argument returns the current list of mappings.

Note that the mapping will be evaluated and used to modify
the environment after the debugger engine at the debuggee
has imported the modules it requires. The order in which the
mappings will be evaluated and applied is:
last set, last evaluated.""", self.m_stdout)



#
# ---------------------------------------- Replacement Functions ------------------------------------
#



def rpdb2_import_wrapper(*args, **kwargs):
    # Workaround for logging library of Python 2.7
    # See issue http://bugs.python.org/issue12718
    if (sys.version_info[:2] == (2,7) and len(args) 
        and hasattr(args[0], '__class__')
        and args[0].__class__.__name__ == 'DictConfigurator' ):
        args = args[1:]

    if len(args) > 0:
        name = args[0]
    elif 'name' in kwargs:
        name = kwargs['name']
    else:
        return g_import(*args, **kwargs)

    if name in sys.modules:
        return g_import(*args, **kwargs)

    #
    # rpdb2 avoids stepping through this
    # function (rpdb2_import_wrapper) to
    # prevent confusion when stepping into
    # an import statement.
    #
    m = g_import(*args, **kwargs)

    if name != 'gtk':
        return m

    try:
        m.gdk.threads_init()
        return m
    except:
        pass

    try:
        m.threads_init()
        return m
    except:
        pass

    return m


def is_func_hidden( name ):
    '''Return whether we should hide this function and frame from display'''
    # in debug mode, we hide nothing
    if g_fDebug: 
        return False
    # currently, only rpdb2 import wrapper is hidden
    return name in ['rpdb2_import_wrapper']


g_import = None

if 0 and __name__ == 'rpdb2' and g_builtins_module.__import__ != rpdb2_import_wrapper:
    g_import = g_builtins_module.__import__
    g_builtins_module.__import__ = rpdb2_import_wrapper



def __find_eval_exec_frame_in_stack():
    f = sys._getframe(0)

    while f != None:
        filename = f.f_code.co_filename
        name = f.f_code.co_name

        if DEBUGGER_FILENAME in filename and name in ['_evaluate', '_execute'] and 'redirect_exc_info' in f.f_locals:
            return f

        f = f.f_back

    return None



def __exc_info():
    f = __find_eval_exec_frame_in_stack()
    if f == None:
        return g_sys_exc_info()

    try:
        frame_index = f.f_locals['frame_index']
        fException = f.f_locals['fException']

        e = g_debugger.get_exception(frame_index, fException)
        exc_info = (e['type'], e['value'], e['traceback'])

        return exc_info

    except:
        return g_sys_exc_info()



g_sys_exc_info = None

if __name__ == 'rpdb2' and 'exc_info' in dir(sys) and sys.exc_info != __exc_info:
    g_sys_exc_info = sys.exc_info
    sys.exc_info = __exc_info



def __setrecursionlimit(rl):
    global g_recursionlimit

    print_debug('rl = %d' % rl)

    g_recursionlimit = max(rl, 64)

    rl = g_recursionlimit
    if sys.version_info[:2] == (2, 6):
        rl *= 3

    return g_sys_setrecursionlimit(rl + 64)



g_sys_setrecursionlimit = None

if __name__ == 'rpdb2' and 'setrecursionlimit' in dir(sys) and sys.setrecursionlimit != __setrecursionlimit:
    g_sys_setrecursionlimit = sys.setrecursionlimit
    sys.setrecursionlimit = __setrecursionlimit
    __setrecursionlimit(sys.getrecursionlimit())



def __find_debugger_frame():
    frame = None

    f = sys._getframe(0)

    while f != None:
        filename = f.f_code.co_filename
        name = f.f_code.co_name

        if DEBUGGER_FILENAME in filename and (name.startswith('trace_dispatch') or name == 'profile'):
            frame = f

        f = f.f_back

    return frame



class CSignalHandler:
    def __del__(self):
        while len(g_signals_pending) != 0:
            (handler, signum, frameobj) = g_signals_pending.pop(0)
            print_debug('Handling pending signal: %s, %s' % (repr(signum), repr(frameobj)))

            try:
                handler(signum, frameobj)

            except:
                #
                # Can not raise from inside a destructor. Report that handler
                # exception will be ignored.
                #
                (t, v, tb) = sys.exc_info()

                _t = safe_repr(t)
                if _t.startswith("<type '"):
                    _t = _t.split("'")[1]

                event = CEventSignalException(signum, '%s: %s' % (_t, safe_repr(v)))
                g_debugger.m_event_dispatcher.fire_event(event)



def signal_handler(signum, frameobj):
    frame = __find_debugger_frame()
    if frame == None:
        #
        # A debugger tracing frame was not found in the stack.
        # This means that the handler can be run without risk
        # for state corruption.
        #
        handler = signal.getsignal(signum)
        return handler(signum, frameobj)

    if frame.f_code.co_name == 'profile' and frame.f_locals['event'] != 'return':
        #
        # signal was caught inside the profile hook but not while
        # doing some debugger stuff. Call the handler but in case
        # of exception schedule the debugger to re-enable the
        # profile hook.
        #
        try:
            handler = signal.getsignal(signum)
            return handler(signum, frameobj)
        except:
            ctx = g_debugger.get_ctx(thread.get_ident())
            ctx.set_tracers(fsignal_exception = True)
            raise

    #
    # Set the handler to be run when the debugger is about
    # to return from the tracing code.
    #

    print_debug('Intercepted signal: %s, %s' % (repr(signum), repr(frameobj)))

    f = frameobj
    while f != None:
        if f == frame:
            frameobj = frame.f_back
            break

        f = f.f_back

    handler = signal.getsignal(signum)
    g_signals_pending.append((handler, signum, frameobj))

    if not 'signal_handler' in frame.f_locals:
        frame.f_locals.update({'signal_handler': CSignalHandler()})

    event = CEventSignalIntercepted(signum)
    g_debugger.m_event_dispatcher.fire_event(event)

    if signum == signal.SIGINT and g_debugger.is_waiting_for_attach():
        g_debugger.set_request_go_timer(0)



def __getsignal(signum):
    handler = g_signal_handlers.get(signum, g_signal_getsignal(signum))
    return handler



g_signal_getsignal = None

if __name__ == 'rpdb2' and 'getsignal' in dir(signal) and signal.getsignal != __getsignal:
    g_signal_getsignal = signal.getsignal
    signal.getsignal = __getsignal



def __signal(signum, handler):
    old_handler = __getsignal(signum)

    if handler in [signal.SIG_IGN, signal.SIG_DFL]:
        g_signal_signal(signum, handler)
        return old_handler

    g_signal_signal(signum, signal_handler)
    g_signal_handlers[signum] = handler

    return old_handler



g_signal_signal = None

if __name__ == 'rpdb2' and 'signal' in dir(signal) and signal.signal != __signal:
    g_signal_signal = signal.signal
    signal.signal = __signal



"""
def __setprofile(foo):
    global g_profile

    print_debug('*** setprofile to %s' % repr(foo))
    traceback.print_stack(file = sys.__stderr__)

    if thread_get_name(current_thread()) == 'MainThread':
        g_profile = foo

    g_sys_setprofile(foo)



g_sys_setprofile = None

if __name__ == 'rpdb2' and sys.setprofile != __setprofile:
    g_sys_setprofile = sys.setprofile
    sys.setprofile = __setprofile
"""



def __fork():
    global g_forktid

    if not g_fignorefork:
        g_forktid = setbreak()

    #
    # os.fork() has been called.
    #
    # You can choose if you would like the debugger
    # to continue with the parent or child fork with
    # the 'fork' console command.
    #
    # For example: 'fork child' or 'fork parent'
    # Type: 'help fork' for more information.
    #
    # WARNING:
    # On some Posix OS such as FreeBSD,
    # Stepping into the child fork can result in
    # termination of the child process.
    #
    # *** RPDB2 SAYS: Read the entire comment! ***
    #
    return g_os_fork()



g_os_fork = None

if __name__ == 'rpdb2' and 'fork' in dir(os) and os.fork != __fork:
    g_os_fork = os.fork
    os.fork = __fork



def __exit(n):
    global g_fos_exit

    if type(n) == int:
        g_fos_exit = (setbreak() != None)

    #
    # os._exit(n) has been called.
    #
    # Stepping on from this point will result
    # in program termination.
    #
    return g_os_exit(n)



g_os_exit = None

if __name__ == 'rpdb2' and '_exit' in dir(os) and os._exit != __exit:
    g_os_exit = os._exit
    os._exit = __exit



def __close(fd):
    global g_fos_exit

    try:
        if fd == g_server.m_server.socket._sock.fileno():
            g_fos_exit = (setbreak() != None)
    except:
        pass

    #
    # os.close(fd) has been called by the debugged script to close
    # the debugger communication channel.
    #
    # This can normally happen if it is trying to spawn a new process
    # in its place.
    #
    # Stepping on from this point will result in termination of the
    # debugging session.
    #
    return g_os_close(fd)



g_os_close = None

if __name__ == 'rpdb2' and 'close' in dir(os) and os.close != __close:
    g_os_close = os.close
    os.close = __close



def __dup2(fd, fd2):
    global g_fos_exit

    try:
        if fd2 == g_server.m_server.socket._sock.fileno():
            g_fos_exit = (setbreak() != None)
    except:
        pass

    #
    # os.dup2(fd, fd2) has been called by the debugged script to close
    # the debugger communication channel.
    #
    # This can normally happen if it is trying to spawn a new process
    # in its place.
    #
    # Stepping on from this point will result in termination of the
    # debugging session.
    #
    return g_os_dup2(fd, fd2)



g_os_dup2 = None

if __name__ == 'rpdb2' and 'dup2' in dir(os) and os.dup2 != __dup2:
    g_os_dup2 = os.dup2
    os.dup2 = __dup2



def __execv(path, args):
    global g_exectid

    if os.path.isfile(path) and not g_fignorefork:
        g_exectid = setbreak()

    #
    # os.execv() has been called.
    #
    # Stepping on from this point will result
    # in termination of the debug session if
    # the exec operation completes successfully.
    #
    return g_os_execv(path, args)



g_os_execv = None

if __name__ == 'rpdb2' and 'execv' in dir(os) and os.execv != __execv:
    g_os_execv = os.execv
    os.execv = __execv



def __execve(path, args, env):
    global g_exectid

    if os.path.isfile(path) and not g_fignorefork:
        g_exectid = setbreak()

    #
    # os.execve() has been called.
    #
    # Stepping on from this point will result
    # in termination of the debug session if
    # the exec operation completes successfully.
    #
    return g_os_execve(path, args, env)



g_os_execve = None

if __name__ == 'rpdb2' and 'execve' in dir(os) and os.execve != __execve:
    g_os_execve = os.execve
    os.execve = __execve



def __excepthook(type, value, traceback, next_excepthook, index):
    if index + 1 < len(g_excepthooks):
        return next_excepthook(type, value, traceback)

    if traceback.tb_frame.f_back == None:
        return next_excepthook(type, value, traceback)

    if not g_debugger.m_ftrap:
        return next_excepthook(type, value, traceback)

    settrace()
    ctx = g_debugger.get_ctx(thread.get_ident())
    ctx.m_fUnhandledException = True
    setbreak()

    #
    # Debuggee breaks (pauses) here
    # on unhandled exceptions.
    # Use analyze mode for post mortem.
    # type 'help analyze' for more information.
    #
    return next_excepthook(type, value, traceback)



g_excepthooks = []

g_excepthook = None

#
# Set the debugger hook for unhandled exceptions. It only kicks in on
# unhandled exceptions that are declared unhandled in the middle of the
# stack as in wxPython. Normally unhandled exceptions are trapped at the
# last stack frame by another mechanism.
#
# This mechaism is designed to work even if the excepthook is over-written.
# by the debugged script.
#
def set_excepthook():
    global g_excepthook

    if len(g_excepthooks) >= 4:
        #
        # Give up. We have been over-written 4 times already.
        #
        return

    next_excepthook = sys.excepthook
    index = len(g_excepthooks)

    eh = lambda type, value, traceback: __excepthook(type, value, traceback, next_excepthook, index)

    g_excepthooks.append(eh)
    g_excepthook = eh
    sys.excepthook = eh



def __function_wrapper(function, args, kwargs):
    __settrace(depth = 1)

    #
    # Debuggee breaks (pauses) here
    # on unhandled exceptions.
    # Use analyze mode for post mortem.
    # type 'help analyze' for more information.
    #
    return function(*args, **kwargs)



def __start_new_thread(function, args, kwargs = {}):
    return g_thread_start_new_thread(__function_wrapper, (function, args, kwargs))



g_thread_start_new_thread = None

if __name__ == 'rpdb2' and 'start_new_thread' in dir(thread) and thread.start_new_thread != __start_new_thread:
    g_thread_start_new_thread = thread.start_new_thread
    thread.start_new_thread = __start_new_thread



#
# ---------------------------------------- main ------------------------------------
#



def __settrace(depth = 2):
    if g_debugger is None:
        return

    f = sys._getframe(depth)
    g_debugger.settrace(f, f_break_on_init = False)



def __setbreak(depth = 2):
    if g_debugger is None:
        return

    f = sys._getframe(depth)
    g_debugger.setbreak(f)

    return thread.get_ident()



def __set_temp_breakpoint(path, scopename, lineno):
    return g_debugger.m_bp_manager.set_temp_breakpoint(path, scopename, lineno)



def _atexit(fabort = False):
    if g_fignore_atexit:
        return

    print_debug("Entered _atexit() in pid %d" % _getpid())

    if g_debugger is None:
        return

    if not fabort:
        g_debugger.stoptrace()

    g_debugger.send_event_exit()

    time.sleep(1.0)

    g_server.shutdown()
    g_debugger.shutdown()

    if not fabort:
        return

    if hasattr(os, 'kill') and hasattr(signal, 'SIGKILL'):
        os.kill(os.getpid(), signal.SIGKILL)
    else:
        os.abort()



def my_pickle_import(*args, **kwargs):
    name = ''

    if len(args) > 0:
        name = args[0]

    if 'name' in kwargs:
        name = kwargs['name']

    if name == 'rpdb2':
        return

    return __import__(*args, **kwargs)



#
# MOD
#
def workaround_import_deadlock():
    if is_py3k() and hasattr(pickle, '_Pickler'):
        pickle.Pickler = pickle._Pickler

    xmlrpclib.loads(XML_DATA)
    s = as_bytes("(S'hello'\np0\nS'world'\np1\ntp2\n.")
    #s = as_bytes('(S\'\\xb3\\x95\\xf9\\x1d\\x105c\\xc6\\xe2t\\x9a\\xa5_`\\xa59\'\np0\nS"(I0\\nI1\\nS\'5657827\'\\np0\\n(S\'server_info\'\\np1\\n(tI0\\ntp2\\ntp3\\n."\np1\ntp2\n.0000000')
    pickle.loads(s)
    pickle.__import__ = my_pickle_import



def __start_embedded_debugger(_rpdb2_pwd, fAllowUnencrypted, fAllowRemote, timeout, source_provider, fDebug, depth):
    global g_server
    global g_debugger

    _rpdb2_pwd = as_unicode(_rpdb2_pwd)

    try:
        g_server_lock.acquire()

        if g_debugger is not None and timeout == 0:
            f = sys._getframe(depth)
            g_debugger.settrace(f, f_break_on_init = False)
            return

        if g_debugger is not None:
            f = sys._getframe(depth)
            g_debugger.record_client_heartbeat(0, True, False)
            g_debugger.setbreak(f)
            return

        if not is_valid_pwd(_rpdb2_pwd):
            raise BadArgument(STR_PASSWORD_BAD)

        src.globals.g_fDebug = fDebug
        src.source_provider.g_source_provider_aux = source_provider

        workaround_import_deadlock()

        if (not fAllowUnencrypted) and not is_encryption_supported():
            raise EncryptionNotSupported

        f = sys._getframe(depth)
        filename = calc_frame_path(f)

        #
        # This is an attempt to address the Python problem of recording only
        # relative paths in __file__ members of modules in the following case.
        #
        if sys.path[0] == '':
            try:
                src.globals.g_initial_cwd = [getcwd(), getcwdu()]

            except UnicodeDecodeError:
                #
                # This exception can be raised in py3k (alpha) on nt.
                #
                src.globals.g_initial_cwd = [getcwdu()]


        atexit.register(_atexit)

        g_debugger = CDebuggerEngine(fembedded = True)

        g_server = CDebuggeeServer(filename, g_debugger, _rpdb2_pwd, fAllowUnencrypted, fAllowRemote)
        g_server.start()

        if timeout == 0:
            g_debugger.settrace(f, f_break_on_init = False)
            return

        g_debugger.settrace(f, timeout = timeout)

    finally:
        g_server_lock.release()



def StartServer(args, fchdir, _rpdb2_pwd, fAllowUnencrypted, fAllowRemote, rid):
    assert(is_unicode(_rpdb2_pwd))

    global g_server
    global g_debugger
    global g_module_main

    try:
        ExpandedFilename = FindFile(args[0])
        _path = g_found_unicode_files.get(ExpandedFilename, ExpandedFilename)

        if fchdir:
            os.chdir(os.path.dirname(_path))

        if ExpandedFilename in g_found_unicode_files:
            prefix = os.path.join(getcwdu(), '')
            _path = _path.replace(winlower(prefix), '')

    except IOError:
        _print('File ' + args[0] + ' not found.')
        return

    print_debug('Starting server with: %s' % ExpandedFilename)

    workaround_import_deadlock()

    #
    # Replace the rpdb2.py directory with the script directory in
    # the search path
    #

    spe = ExpandedFilename
    if os.path.islink(ExpandedFilename):
        spe = os.path.realpath(ExpandedFilename)

    sys.path[0] = os.path.dirname(spe)

    encoding = detect_locale()
    argv = [as_string(arg, encoding) for arg in args]
    sys.argv = argv

    atexit.register(_atexit)

    g_debugger = CDebuggerEngine()

    g_server = CDebuggeeServer(ExpandedFilename, g_debugger, _rpdb2_pwd, fAllowUnencrypted, fAllowRemote, rid)
    g_server.start()

    try:
        g_debugger.m_bp_manager.set_temp_breakpoint(ExpandedFilename, '', 1, fhard = True)
    except:
        pass

    f = sys._getframe(0)
    g_debugger.settrace(f, f_break_on_init = False, builtins_hack = ExpandedFilename)

    g_module_main = -1
    del sys.modules['__main__']

    #
    # An exception in this line occurs if
    # there is a syntax error in the debugged script or if
    # there was a problem loading the debugged script.
    #

    imp.load_source('__main__', _path)



def StartClient(command_line, fAttach, fchdir, _rpdb2_pwd, fAllowUnencrypted, fAllowRemote, host, interpreter):
    assert(is_unicode(command_line))
    assert(is_unicode(interpreter))
    assert(_rpdb2_pwd == None or is_unicode(_rpdb2_pwd))

    if (not fAllowUnencrypted) and not is_encryption_supported():
        _print(STR_ENCRYPTION_SUPPORT_ERROR)
        return 2

    sm = CSessionManager(_rpdb2_pwd, fAllowUnencrypted, fAllowRemote, host)
    c = CConsole(sm)
    c.start()

    time.sleep(1.0)

    try:
        if fAttach:
            sm.attach(command_line)
        elif command_line != '':
            sm.launch(fchdir, command_line, interpreter)

    except (socket.error, CConnectionException):
        sm.report_exception(*sys.exc_info())
    except CException:
        sm.report_exception(*sys.exc_info())
    except:
        sm.report_exception(*sys.exc_info())
        print_debug_exception(True)

    c.join()
    sm.shutdown()



def PrintUsage(fExtended = False):
    scriptName = os.path.basename(sys.argv[0])
    _print(""" %(rpdb)s [options] [<script-name> [<script-args>...]]

    %(rpdb)s uses the client-server model where the debugger UI/console is
    the client and the debugged script is the server (also called debuggee).
    The client and the server are separate processes and communicate over
    sockets.

    Example: The following command starts the debugger UI/console and then
    launches and attaches to the specified script:
    %(rpdb)s some_script.py

    Options can be a combination of the following:
    -h, --help      Print this help.
    -d, --debuggee  Start the debugged script (server) and wait for a
                    debugger console (client) to attach.
    -a, --attach    Start the debugger console (client) and attach to the
                    specified debugged script (server).
    -o, --host=     Specify host (or IP address) for remote connections.
    -r, --remote    Allow debuggees to accept connections from remote machines.
    -e, --encrypt   Force encrypted socket communication.
    -p, --pwd=      Specify password for socket communication.
                    This flag is available only on Windows. On other
                    systems the password will be queried interactively
                    if it is needed.
    -s, --screen    Use the Unix screen utility when starting the debuggee.
                    Note that the debugger should be started as follows:
                    screen rpdb2 -s [options] [<script-name> [<script-args>...]]
    -c, --chdir     Change the working directory to that of the launched
                    script.
    -i, --interpreter= Launch debuggee with the given interpreter executable
    -v, --version   Print version information.
    --debug         Debug prints.

    Note that each option is available in short form (example -e) and in a
    long form (example --encrypt).

    Options that end with '=' accept an argument that should follow without
    a space. For example to specify 192.168.0.10 as host use the following
    option:

        long form: --host=192.168.0.10
        short form: -o192.168.0.10
""" % {"rpdb": scriptName})

    if not fExtended:
        return

    _print(__doc__)



def main(StartClient_func = StartClient, version =RPDB_TITLE):
    global g_fScreen
    global g_fFirewallTest
    global g_fbreakonexit

    create_rpdb_settings_folder()

    encoding = detect_locale()
    argv = [as_unicode(arg, encoding) for arg in sys.argv]

    try:
        options, _rpdb2_args = getopt.getopt(
                            argv[1:],
                            'hdao:rtep:scvi:',
                            ['help', 'debugee', 'debuggee', 'attach', 'host=', 'remote', 
                             'plaintext', 'encrypt', 'pwd=', 'rid=', 'screen', 'chdir', 
                             'base64=', 'nofwtest', 'version', 'debug', 'interpreter=' ]
                            )

    except getopt.GetoptError:
        PrintUsage()
        return 2

    fWrap = False
    fAttach = False
    fSpawn = False
    fStart = False

    encoded_path = None
    secret = None
    host = None
    _rpdb2_pwd = None
    fchdir = False
    fAllowRemote = False
    fAllowUnencrypted = True
    interpreter = as_unicode('')

    for o, a in options:
        if o in ['-h', '--help']:
            PrintUsage()
            return 0
        if o in ['-v', '--version']:
            _print(version)
            return 0
        if o in ['--debug']:
            src.globals.g_fDebug = True
        if o in ['-d', '--debugee', '--debuggee']:
            fWrap = True
        if o in ['-a', '--attach']:
            fAttach = True
        if o in ['-o', '--host']:
            host = a
        if o in ['-r', '--remote']:
            fAllowRemote = True
        if o in ['-t', '--plaintext']:
            fAllowUnencrypted = True
        if o in ['-e', '--encrypt']:
            fAllowUnencrypted = False
        if o in ['-p', '--pwd']:
            _rpdb2_pwd = a
        if o in ['--rid']:
            secret = a
        if o in ['-s', '--screen']:
            g_fScreen = True
        if o in ['-c', '--chdir']:
            fchdir = True
        if o in ['--base64']:
            encoded_path = a
        if o in ['--nofwtest']:
            g_fFirewallTest = False
        if o in ['-i', '--interpreter']:
            interpreter = a

    arg = None
    argv = None
    options = None
    o = None
    a = None

    if (_rpdb2_pwd is not None) and (os.name != 'nt'):
        _print(STR_PASSWORD_NOT_SUPPORTED)
        return 2

    if _rpdb2_pwd is not None and not is_valid_pwd(_rpdb2_pwd):
        _print(STR_PASSWORD_BAD)
        return 2

    if fWrap and (len(_rpdb2_args) == 0):
        _print("--debuggee option requires a script name with optional <script-arg> arguments")
        return 2

    if fWrap and fAttach:
        _print("--debuggee and --attach can not be used together.")
        return 2

    if fAttach and (len(_rpdb2_args) == 0):
        _print("--attach option requires a script name to attach to.")
        return 2

    if fAttach and (len(_rpdb2_args) > 1):
        _print("--attach option does not accept <script-arg> arguments.")
        return 2

    if fAttach and fAllowRemote:
        _print("--attach and --remote can not be used together.")
        return 2

    if fAttach and interpreter:
        _print("--attach and --interpreter can not be used together")
        return 2

    if fWrap and interpreter:
        _print("--debuggee and --interpreter can not be used together")
        return 2

    if (host is not None) and not fAttach:
        _print("--host can only be used together with --attach.")
        return 2

    if host is None:
        host = LOCALHOST

    fSpawn = (len(_rpdb2_args) != 0) and (not fWrap) and (not fAttach)
    fStart = (len(_rpdb2_args) == 0)

    if fchdir and not (fWrap or fSpawn):
        _print("-c can only be used when launching or starting a script from command line.")
        return 2

    assert (fWrap + fAttach + fSpawn + fStart) == 1

    if fAttach and (os.name == POSIX):
        try:
            int(_rpdb2_args[0])

            _rpdb2_pwd = read_pwd_file(_rpdb2_args[0])
            delete_pwd_file(_rpdb2_args[0])

        except (ValueError, IOError):
            pass

    if (secret is not None) and (os.name == POSIX):
        _rpdb2_pwd = read_pwd_file(secret)

    if (fWrap or fAttach) and not is_valid_pwd(_rpdb2_pwd):
        _print(STR_PASSWORD_MUST_BE_SET)

        while True:
            _rpdb2_pwd = _raw_input(STR_PASSWORD_INPUT)
            if is_valid_pwd(_rpdb2_pwd):
                break

            _print(STR_PASSWORD_BAD)

        _print(STR_PASSWORD_CONFIRM)

    if fWrap or fSpawn:
        try:
            if encoded_path != None:
                _b = as_bytes(encoded_path).translate(g_safe_base64_from)
                _u = base64_decodestring(_b)
                _path = as_unicode(_u)
                _rpdb2_args[0] = _path

            FindFile(_rpdb2_args[0])
        except IOError:
            _print(STR_FILE_NOT_FOUND % _rpdb2_args[0])
            return 2

    # XXX Make sure interpreter is correctly encoded

    if fWrap:
        if (not fAllowUnencrypted) and not is_encryption_supported():
            _print(STR_ENCRYPTION_SUPPORT_ERROR)
            return 2

        StartServer(_rpdb2_args, fchdir, _rpdb2_pwd, fAllowUnencrypted, fAllowRemote, secret)

    elif fAttach:
        StartClient_func(_rpdb2_args[0], fAttach, fchdir, _rpdb2_pwd, fAllowUnencrypted, fAllowRemote, host, interpreter)

    elif fStart:
        StartClient_func(as_unicode(''), fAttach, fchdir, _rpdb2_pwd, fAllowUnencrypted, fAllowRemote, host, interpreter)

    else:
        if len(_rpdb2_args) == 0:
            _rpdb2_args = ''
        else:
            _rpdb2_args = '"' + '" "'.join(_rpdb2_args) + '"'

        StartClient_func(_rpdb2_args, fAttach, fchdir, _rpdb2_pwd, fAllowUnencrypted, fAllowRemote, host, interpreter)

    return 0

def run_rpdb2():
    import rpdb2

    #
    # Debuggee breaks (pauses) here
    # on unhandled exceptions.
    # Use analyze mode for post mortem.
    # type 'help analyze' for more information.
    #
    ret = rpdb2.main()

    #
    # Debuggee breaks (pauses) here
    # before program termination if breakonexit is set
    #
    # You can step to debug any exit handlers.
    #
    if rpdb2.g_fbreakonexit:
        rpdb2.print_debug( 'Breaking before exit')
        rpdb2.setbreak()

if __name__ == '__main__':
    run_rpdb2()


