import _thread as thread
import codecs
import locale
import os.path
import sys
import threading
import time
import traceback

from src.globals import g_fDebug, g_traceback_lock

def is_unicode(s):
    if type(s) == str:
        return True
    return False


def as_unicode(s, encoding = 'utf-8', fstrict = False):
    '''Return an unicode string, corresponding to s, encoding it if necessary'''
    if is_unicode(s):
        return s

    if fstrict:
        u = s.decode(encoding)
    else:
        u = s.decode(encoding, 'replace')

    return u

ENCODING_AUTO = as_unicode('auto')
ENCODING_RAW = as_unicode('raw')
ENCODING_RAW_I = as_unicode('__raw')


def as_string(s, encoding = 'utf-8', fstrict = False):
    if is_unicode(s):
        return s

    if fstrict:
        e = s.decode(encoding)
    else:
        e = s.decode(encoding, 'replace')

    return e


def as_bytes(s, encoding = 'utf-8', fstrict = True):
    if not is_unicode(s):
        return s

    if fstrict:
        b = s.encode(encoding)
    else:
        b = s.encode(encoding, 'replace')

    return b


def print_debug(_str):
    if not g_fDebug:
        return

    t = time.time()
    l = time.localtime(t)
    s = time.strftime('%H:%M:%S', l) + '.%03d' % ((t - int(t)) * 1000)

    f = sys._getframe(1)

    tid = thread.get_ident()
    tname = thread_get_name( current_thread() )
    threadinfo = '%s/%d' % ( tname, tid )
    filename = os.path.basename(f.f_code.co_filename)
    lineno = f.f_lineno
    name = f.f_code.co_name

    str = '%s %s:%d %s %s(): %s' % (s, filename, lineno, threadinfo, name, _str)

    _print(str, sys.__stderr__)


def print_debug_exception(fForce = False):
    """
    Print exceptions to stdout when in debug mode.
    """

    if not g_fDebug and not fForce:
        return

    (t, v, tb) = sys.exc_info()
    print_exception(t, v, tb, fForce)


def winlower(path):
    """
    return lowercase version of 'path' on NT systems.

    On NT filenames are case insensitive so lowercase filenames
    for comparison purposes on NT.
    """

    if os.name == 'nt':
        return path.lower()

    return path


def _print(s, f = sys.stdout, feol = True):
    s = as_unicode(s)

    encoding = detect_encoding(f)

    s = as_bytes(s, encoding, fstrict = False)
    s = as_string(s, encoding)

    if feol:
        f.write(s + '\n')
    else:
        f.write(s)


def print_exception(t, v, tb, fForce = False):
    """
    Print exceptions to stderr when in debug mode.
    """

    if not g_fDebug and not fForce:
        return

    try:
        g_traceback_lock.acquire()
        traceback.print_exception(t, v, tb, file = CFileWrapper(sys.stderr))

    finally:
        g_traceback_lock.release()


def thread_set_daemon(thread, fdaemon):
    thread.daemon = fdaemon


def thread_is_alive(thread):
    return thread.is_alive()


def thread_set_name(thread, name):
    thread.name = name


def thread_get_name(thread):
    return thread.name


def current_thread():
    return threading.current_thread()


def detect_encoding(file):
    try:
        encoding = file.encoding
        if encoding == None:
            return detect_locale()

    except:
        return detect_locale()

    try:
        codecs.lookup(encoding)
        return encoding

    except:
        pass

    if encoding.lower().startswith('utf_8'):
        return 'utf-8'

    return 'ascii'


def detect_locale():
    encoding = locale.getpreferredencoding()

    if encoding == None:
        return 'ascii'

    try:
        codecs.lookup(encoding)
        return encoding


    except:
        pass

    if encoding.lower().startswith('utf_8'):
        return 'utf-8'

    return 'ascii'

class CFileWrapper:
    def __init__(self, f):
        self.m_f = f


    def write(self, s):
        _print(s, self.m_f, feol = False)


    def __getattr__(self, name):
        return self.m_f.__getattr__(name)


def print_stack():
    """
    Print exceptions to stdout when in debug mode.
    """

    if g_fDebug == True:
        try:
            g_traceback_lock.acquire()
            traceback.print_stack(file = CFileWrapper(sys.stderr))

        finally:
            g_traceback_lock.release()


def get_python_executable( interpreter=None ):
    '''Return the python executable, usable to launch the debuggee.
    Pass a value that may override the default executable.

    Executable is returned as unicode, taking into accoun the file system encoding.'''
    fse = sys.getfilesystemencoding()
    if interpreter:
        python_exec = interpreter
    else:
        python_exec = sys.executable
    if python_exec.endswith('w.exe'):
        python_exec = python_exec[:-5] + '.exe'
    python_exec = as_unicode(python_exec, fse)
    return python_exec


