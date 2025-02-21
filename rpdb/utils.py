import _thread as thread
import codecs
import locale
import os.path
import random
import sys
import threading
import time
import traceback

#
# Pre-Import needed by my_abspath1
#
import zipfile
import zipimport

try:
    from nt import _getfullpathname
except ImportError:
    pass

from rpdb.globals import g_fDebug, g_traceback_lock, g_initial_cwd, g_found_unicode_files
from rpdb.const import PYTHONW_FILE_EXTENSION, PYTHON_FILE_EXTENSION, PYTHONW_SO_EXTENSION


def is_py3k():
    return sys.version_info[0] >= 3


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
    #if not g_fDebug:
    #    return

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

    #if not g_fDebug and not fForce:
    #    return

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
    if f is not None:
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

    # if not g_fDebug and not fForce:
    #     return

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

    if g_fDebug == True or True:
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


def generate_random_char(_str):
    """
    Return a random character from string argument.
    """

    if _str == '':
        return ''

    i = random.randint(0, len(_str) - 1)
    return _str[i]


def generate_rid():
    """
    Return a 7 digits random id.
    """

    rid = repr(random.randint(1000000, 9999999))
    rid = as_unicode(rid)

    return rid


def safe_wait(lock, timeout = None):
    #
    # workaround windows bug where signal handlers might raise exceptions
    # even if they return normally.
    #

    while True:
        t0 = time.time()
        try:
            return lock.wait(timeout)

        except:
            if timeout == None:
                continue

            timeout -= (time.time() - t0)
            if timeout <= 0:
                return


def split_command_line_path_filename_args(command_line):
    """
    Split command line to a 3 elements tuple (path, filename, args)
    """

    command_line = command_line.strip()
    if len(command_line) == 0:
        return ('', '', '')

    if myisfile(command_line):
        (_path, _filename) = split_path(command_line)
        return (_path, _filename, '')

    if command_line[0] in ['"', "'"]:
        _command_line = command_line[1:]
        i = _command_line.find(command_line[0])
        if i == -1:
            (_path, filename) = split_path(_command_line)
            return (_path, filename, '')
        else:
            (_path, filename) = split_path(_command_line[: i])
            args = _command_line[i + 1:].strip()
            return (_path, filename, args)
    else:
        i = command_line.find(' ')
        if i == -1:
            (_path, filename) = split_path(command_line)
            return (_path, filename, '')
        else:
            args = command_line[i + 1:].strip()
            (_path, filename) = split_path(command_line[: i])
            return (_path, filename, args)


def my_os_path_join(dirname, basename):
    if is_py3k() or (type(dirname) == str and type(basename) == str):
        return os.path.join(dirname, basename)

    encoding = sys.getfilesystemencoding()

    if type(dirname) == str:
        dirname = dirname.decode(encoding)

    if type(basename) == str:
        basename = basename.decode(encoding)

    return os.path.join(dirname, basename)


def FindFile(
        filename,
        sources_paths = [],
        fModules = False,
        fAllowAnyExt = True
        ):

    """
    FindFile looks for the full path of a script in a rather non-strict
    and human like behavior.

    ENCODING:
    filename should be either Unicode or encoded with sys.getfilesystemencoding()!
    Returned value is encoded with sys.getfilesystemencoding().

    It will always look for .py or .pyw files even if a .pyc or no
    extension is given.

    1. It will check against loaded modules if asked.
    1. full path (if exists).
    2. sources_paths.
    2. current path.
    3. PYTHONPATH
    4. PATH
    """

    if filename in g_found_unicode_files:
        return filename

    if filename.startswith('<'):
        raise IOError

    filename = filename.strip('\'"')
    filename = os.path.expanduser(filename)

    if fModules and not (os.path.isabs(filename) or filename.startswith('.')):
        try:
            return winlower(FindFileAsModule(filename))
        except IOError:
            pass

    if fAllowAnyExt:
        try:
            abspath = FindFile(
                            filename,
                            sources_paths,
                            fModules = False,
                            fAllowAnyExt = False
                            )
            return abspath
        except IOError:
            pass

    if os.path.isabs(filename) or filename.startswith('.'):
        try:
            scriptname = None

            abspath = my_abspath(filename)
            lowered = winlower(abspath)
            scriptname = CalcScriptName(lowered, fAllowAnyExt)

            if myisfile(scriptname):
                return scriptname

            #
            # Check .pyw files
            #
            scriptname += 'w'
            if scriptname.endswith(PYTHONW_FILE_EXTENSION) and myisfile(scriptname):
                return scriptname

            scriptname = None
            raise IOError

        finally:
            if not is_py3k() and is_unicode(scriptname):
                fse = sys.getfilesystemencoding()
                _l = as_string(scriptname, fse)
                if '?' in _l:
                    g_found_unicode_files[_l] = scriptname
                return _l

    scriptname = CalcScriptName(filename, fAllowAnyExt)

    try:
        cwd = [getcwd(), getcwdu()]

    except UnicodeDecodeError:
        #
        # This exception can be raised in py3k (alpha) on nt.
        #
        cwd = [getcwdu()]

    env_path = os.environ['PATH']
    paths = sources_paths + cwd + g_initial_cwd + sys.path + env_path.split(os.pathsep)

    try:
        lowered = None

        for p in paths:
            f = my_os_path_join(p, scriptname)
            abspath = my_abspath(f)
            lowered = winlower(abspath)

            if myisfile(lowered):
                return lowered

            #
            # Check .pyw files
            #
            lowered += 'w'
            if lowered.endswith(PYTHONW_FILE_EXTENSION) and myisfile(lowered):
                return lowered

        lowered = None
        raise IOError

    finally:
        if not is_py3k() and is_unicode(lowered):
            fse = sys.getfilesystemencoding()
            _l = as_string(lowered, fse)
            if '?' in _l:
                g_found_unicode_files[_l] = lowered
            return _l


def split_path(path):
    (_path, filename) = os.path.split(path)

    #
    # Make sure path separator (e.g. '/') ends the splitted path if it was in
    # the original path.
    #
    if (_path[-1:] not in [os.path.sep, os.path.altsep]) and \
            (path[len(_path): len(_path) + 1] in [os.path.sep, os.path.altsep]):
        _path = _path + path[len(_path): len(_path) + 1]

    return (_path, filename)

def FindFileAsModule(filename):
    lowered = winlower(filename)
    (root, ext) = os.path.splitext(lowered)

    root_dotted = root.replace('\\', '.').replace('/', '.').replace(':', '.')

    match_list = []
    for (module_name, m) in list(sys.modules.items()):
        lowered_module_name = winlower(module_name)
        if (root_dotted + '.').startswith(lowered_module_name + '.'):
            match_list.append((len(module_name), module_name))

            if lowered_module_name == root_dotted:
                break

    match_list.sort()
    match_list.reverse()

    for (matched_len, matched_module) in match_list:
        try:
            module_dir = FindModuleDir(matched_module)
        except IOError:
            continue

        suffix = root[matched_len:]
        if suffix == '':
            path = module_dir + ext
        else:
            path = my_os_path_join(module_dir, suffix.strip('\\')) + ext

        scriptname = CalcScriptName(path, fAllowAnyExt = False)
        if myisfile(scriptname):
            return scriptname

        #
        # Check .pyw files
        #
        scriptname += 'w'
        if scriptname.endswith(PYTHONW_FILE_EXTENSION) and myisfile(scriptname):
            return scriptname

    raise IOError


def my_abspath(path):
    """
    We need our own little version of os.path.abspath since the original
    code imports modules in the 'nt' code path which can cause our debugger
    to deadlock in unexpected locations.
    """

    if path[:1] == '<':
        #
        # 'path' may also be '<stdin>' in which case it is left untouched.
        #
        return path

    if os.name == 'nt':
        return my_abspath1(path)

    return  os.path.abspath(path)


def my_abspath1(path):
    """
    Modification of ntpath.abspath() that avoids doing an import.
    """

    if path:
        try:
            path = _getfullpathname(path)
        except WindowsError:
            pass
    else:
        try:
            path = getcwd()

        except UnicodeDecodeError:
            #
            # This exception can be raised in py3k (alpha) on nt.
            #
            path = getcwdu()

    np = os.path.normpath(path)

    if (len(np) >= 2) and (np[1:2] == ':'):
        np = np[:1].upper() + np[1:]

    return np


def CalcScriptName(filename, fAllowAnyExt = True):
    if filename.endswith(PYTHON_FILE_EXTENSION):
        return filename

    if filename.endswith(PYTHONW_FILE_EXTENSION):
        return filename

    if filename.endswith(PYTHONW_SO_EXTENSION):
        scriptname = filename[:-3] + PYTHON_FILE_EXTENSION
        return scriptname

    if filename[:-1].endswith(PYTHON_FILE_EXTENSION):
        scriptname = filename[:-1]
        return scriptname

    if fAllowAnyExt:
        return filename

    scriptname = filename + PYTHON_FILE_EXTENSION

    return scriptname


def getcwd():
    try:
        return os.getcwd()

    except UnicodeDecodeError:
        print_debug_exception(True)
        raise


def getcwdu():
    if hasattr(os, 'getcwdu'):
        return os.getcwdu()

    return getcwd()


g_safe_base64_to = bytes.maketrans(as_bytes('/+='), as_bytes('_-#'))
g_safe_base64_from = bytes.maketrans(as_bytes('_-#'), as_bytes('/+='))


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


#
# myisfile() is similar to os.path.isfile() but also works with
# Python eggs.
#
def myisfile(path):
    try:
        mygetfile(path, False)
        return True

    except:
        return False


#
# Read a file even if inside a Python egg.
#
def mygetfile(path, fread_file = True):
    if os.path.isfile(path):
        if not fread_file:
            return

        if sys.platform == 'OpenVMS':
            #
            # OpenVMS filesystem does not support byte stream.
            #
            mode = 'r'
        else:
            mode = 'rb'

        f = open(path, mode)
        data = f.read()
        f.close()
        return data

    d = os.path.dirname(path)

    while True:
        if os.path.exists(d):
            break

        _d = os.path.dirname(d)
        if _d in [d, '']:
            raise IOError

        d = _d

    if not zipfile.is_zipfile(d):
        raise IOError

    z = zipimport.zipimporter(d)

    try:
        data = z.get_data(path[len(d) + 1:])
        return data

    except:
        raise IOError


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