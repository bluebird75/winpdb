import os.path
import sys, codecs

from typing import Dict, Tuple, List, Optional, Union

from rpdb.globals import g_found_unicode_files
from rpdb.utils import as_unicode, is_unicode, winlower, as_bytes, mygetfile

BLENDER_SOURCE_NOT_AVAILABLE = as_unicode('Blender script source code is not available.')
SOURCE_NOT_AVAILABLE = as_unicode('Source code is not available.')

ENCODING_UTF8_PREFIX_1 = '\xef\xbb\xbf'
ENCODING_SOURCE = '# -*- coding: %s -*-\n'
MODULE_SCOPE = '?'
MODULE_SCOPE2 = '<module>'
SCOPE_SEP = '.'

g_source_provider_aux = None
g_lines_cache = {}  # type: Dict[str, Tuple[List[str], str, bool]]


def ParseLineEncoding(l: str) -> Optional[str]:
    if l.startswith('# -*- coding: '):
        e = l[len('# -*- coding: '):].split()[0]
        return e

    if l.startswith('# vim:fileencoding='):
        e = l[len('# vim:fileencoding='):].strip()
        return e

    return None


def ParseEncoding(txt: Union[str, bytes]) -> str:
    """
    Parse document encoding according to:
    http://docs.python.org/ref/encodings.html
    """

    if isinstance(txt, str):
        seol = '\n'  # type: str
        l = txt.split(seol, 20)[:-1]    # type: Union[List[str], List[bytes]]

    elif isinstance(txt, bytes):
        beol = as_bytes('\n')
        l = txt.split(beol, 20)[:-1]

    else:
        raise ValueError('Unknown type for txt: %s' % type(txt))

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

def lines_cache(filename: str) -> Tuple[List[str], str, bool]:
    filename = g_found_unicode_files.get(filename, filename)

    if filename in g_lines_cache:
        return g_lines_cache[filename]

    (source, encoding, ffilesystem) = source_provider(filename)
    source = source.replace(as_unicode('\r\n'), as_unicode('\n'))

    lines = source.split(as_unicode('\n'))

    g_lines_cache[filename] = (lines, encoding, ffilesystem)

    return (lines, encoding, ffilesystem)


def get_source(filename: str) -> Tuple[str, str]:
    (lines, encoding, ffilesystem) = lines_cache(filename)
    source = as_unicode('\n').join(lines)

    return (source, encoding)


def source_provider(filename: str) -> Tuple[str, str, bool]:
    source = None   # type: Union[str, bytes, None]
    ffilesystem = False

    try:
        if g_source_provider_aux is not None:
            source = g_source_provider_aux(filename)

    except IOError:
        v = sys.exc_info()[1]
        if v is None or SOURCE_NOT_AVAILABLE in v.args:
            raise

    try:
        if source is None:
            source = source_provider_blender(filename)

    except IOError:
        v = sys.exc_info()[1]
        if v is not None and BLENDER_SOURCE_NOT_AVAILABLE in v.args:
            raise

    if source is None:
        source = source_provider_filesystem(filename)
        ffilesystem = True

    encoding = ParseEncoding(source)

    if isinstance(source, bytes):
        source = as_unicode(source, encoding)

    return source, encoding, ffilesystem


def source_provider_blender(filename: str) -> str:
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
        t = sys.modules['Blender.Text'].get(_filename)  # type: ignore
        lines = t.asLines()
        return '\n'.join(lines) + '\n'

    except NameError:
        f = winlower(_filename)
        tlist = sys.modules['Blender.Text'].get()   # type: ignore

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


def source_provider_filesystem(filename: str) -> bytes:
    l = mygetfile(filename)

    if l[:3] == as_bytes(ENCODING_UTF8_PREFIX_1):
        l = l[3:]

    return l


def get_source_line(filename: str, lineno: int) -> str:
    (lines, encoding, ffilesystem) = lines_cache(filename)

    if lineno > len(lines):
        return as_unicode('')

    return lines[lineno - 1] + as_unicode('\n')


def is_provider_filesystem(filename: str) -> bool:
    try:
        (lines, encoding, ffilesystem) = lines_cache(filename)
        return ffilesystem

    except IOError:
        v = sys.exc_info()[1]
        if v is None:
            return False
        return not (BLENDER_SOURCE_NOT_AVAILABLE in v.args or SOURCE_NOT_AVAILABLE in v.args)


