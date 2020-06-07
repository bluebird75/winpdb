import os.path
import sys

from src.globals import g_found_unicode_files
from src.utils import as_unicode, is_unicode, winlower, as_bytes, mygetfile

BLENDER_SOURCE_NOT_AVAILABLE = as_unicode('Blender script source code is not available.')
SOURCE_NOT_AVAILABLE = as_unicode('Source code is not available.')

ENCODING_UTF8_PREFIX_1 = '\xef\xbb\xbf'
ENCODING_SOURCE = '# -*- coding: %s -*-\n'
MODULE_SCOPE = '?'
MODULE_SCOPE2 = '<module>'
SCOPE_SEP = '.'

g_source_provider_aux = None
g_lines_cache = {}


def ParseLineEncoding(l):
    if l.startswith('# -*- coding: '):
        e = l[len('# -*- coding: '):].split()[0]
        return e

    if l.startswith('# vim:fileencoding='):
        e = l[len('# vim:fileencoding='):].strip()
        return e

    return None


def ParseEncoding(txt):
    """
    Parse document encoding according to:
    http://docs.python.org/ref/encodings.html
    """

    eol = '\n'
    if not is_unicode(txt):
        eol = as_bytes('\n')

    l = txt.split(eol, 20)[:-1]

    for line in l:
        line = as_unicode(line)
        encoding = ParseLineEncoding(line)
        if encoding is not None:
            try:
                codecs.lookup(encoding)
                return encoding

            except:
                return 'utf-8'

    return 'utf-8'

def lines_cache(filename):
    filename = g_found_unicode_files.get(filename, filename)

    if filename in g_lines_cache:
        return g_lines_cache[filename]

    (source, encoding, ffilesystem) = source_provider(filename)
    source = source.replace(as_unicode('\r\n'), as_unicode('\n'))

    lines = source.split(as_unicode('\n'))

    g_lines_cache[filename] = (lines, encoding, ffilesystem)

    return (lines, encoding, ffilesystem)


def get_source(filename):
    (lines, encoding, ffilesystem) = lines_cache(filename)
    source = as_unicode('\n').join(lines)

    return (source, encoding)


def source_provider(filename):
    source = None
    ffilesystem = False

    try:
        if g_source_provider_aux != None:
            source = g_source_provider_aux(filename)

    except IOError:
        v = sys.exc_info()[1]
        if SOURCE_NOT_AVAILABLE in v.args:
            raise

    try:
        if source == None:
            source = source_provider_blender(filename)

    except IOError:
        v = sys.exc_info()[1]
        if BLENDER_SOURCE_NOT_AVAILABLE in v.args:
            raise

    if source == None:
        source = source_provider_filesystem(filename)
        ffilesystem = True

    encoding = ParseEncoding(source)

    if not is_unicode(source):
        source = as_unicode(source, encoding)

    return source, encoding, ffilesystem


def source_provider_blender(filename):
    """
    Return source code of the file referred by filename.

    Support for debugging of Blender Python scripts.
    Blender scripts are not always saved on disk, and their
    source has to be queried directly from the Blender API.
    http://www.blender.org
    """

    if not 'Blender.Text' in sys.modules:
        raise IOError

    if filename.startswith('<'):
        #
        # This specifies blender source whose source is not
        # available.
        #
        raise IOError(BLENDER_SOURCE_NOT_AVAILABLE)

    _filename = os.path.basename(filename)

    try:
        t = sys.modules['Blender.Text'].get(_filename)
        lines = t.asLines()
        return '\n'.join(lines) + '\n'

    except NameError:
        f = winlower(_filename)
        tlist = sys.modules['Blender.Text'].get()

        t = None
        for _t in tlist:
            n = winlower(_t.getName())
            if n == f:
                t = _t
                break

        if t == None:
            #
            # filename does not specify a blender file. Raise IOError
            # so that search can continue on file system.
            #
            raise IOError

        lines = t.asLines()
        return '\n'.join(lines) + '\n'


def source_provider_filesystem(filename):
    l = mygetfile(filename)

    if l[:3] == as_bytes(ENCODING_UTF8_PREFIX_1):
        l = l[3:]

    return l


def get_source_line(filename, lineno):
    (lines, encoding, ffilesystem) = lines_cache(filename)

    if lineno > len(lines):
        return as_unicode('')

    return lines[lineno - 1] + as_unicode('\n')


def is_provider_filesystem(filename):
    try:
        (lines, encoding, ffilesystem) = lines_cache(filename)
        return ffilesystem

    except IOError:
        v = sys.exc_info()[1]
        return not (BLENDER_SOURCE_NOT_AVAILABLE in v.args or SOURCE_NOT_AVAILABLE in v.args)


