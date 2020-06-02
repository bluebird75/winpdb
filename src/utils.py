import _thread as thread
import os.path
import sys
import time

from rpdb2 import g_fDebug, thread_get_name, current_thread, _print, print_exception


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