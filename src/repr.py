import sys

from src.utils import as_unicode, is_unicode, print_debug_exception, ENCODING_RAW_I, as_bytes

def is_py3k():
    return sys.version_info[0] >= 3


DEFAULT_PATH_SUFFIX_LENGTH = 55

ELLIPSIS_UNICODE = as_unicode('...')
ELLIPSIS_BYTES = as_bytes('...')

def calc_suffix(_str, n):
    """
    Return an n charaters suffix of the argument string of the form
    '...suffix'.
    """

    if len(_str) <= n:
        return _str

    return '...' + _str[-(n - 3):]

def class_name(c):
    s = safe_str(c)

    if "'" in s:
        s = s.split("'")[1]

    assert(s.startswith(__name__ + '.'))

    return s


def clip_filename(path, n = DEFAULT_PATH_SUFFIX_LENGTH):
    suffix = calc_suffix(path, n)
    if not suffix.startswith('...'):
        return suffix

    index = suffix.find(os.sep)
    if index == -1:
        return suffix

    clip = '...' + suffix[index:]

    return clip


def safe_str(x):
    try:
        return str(x)

    except:
        return 'N/A'


def safe_repr(x):
    try:
        return repr(x)

    except:
        return 'N/A'


def parse_type(t):
    rt = safe_repr(t)
    if not "'" in rt:
        return rt

    st = rt.split("'")[1]
    return st


def repr_list(pattern, l, length, encoding, is_valid):
    length = max(0, length - len(pattern) + 2)

    s = ''

    index = 0

    try:
        for i in l:
            #
            # Remove any trace of session password from data structures that
            # go over the network.
            #
            if type(i) == str and i in ['_rpdb2_args', '_rpdb2_pwd', 'm_rpdb2_pwd']:
                continue

            s += repr_ltd(i, length - len(s), encoding, is_valid)

            index += 1

            if index < len(l) and len(s) > length:
                is_valid[0] = False
                if not s.endswith('...'):
                    s += '...'
                break

            if index < len(l) or (index == 1 and pattern[0] == '('):
                s += ', '

    except AttributeError:
        is_valid[0] = False

    return as_unicode(pattern % s)


def repr_dict(pattern, d, length, encoding, is_valid):
    length = max(0, length - len(pattern) + 2)

    s = ''

    index = 0

    try:
        for k in d:
            #
            # Remove any trace of session password from data structures that
            # go over the network.
            #
            if type(k) == str and k in ['_rpdb2_args', '_rpdb2_pwd', 'm_rpdb2_pwd']:
                continue

            v = d[k]

            s += repr_ltd(k, length - len(s), encoding, is_valid)

            if len(s) > length:
                is_valid[0] = False
                if not s.endswith('...'):
                    s += '...'
                break

            s +=  ': ' + repr_ltd(v, length - len(s), encoding, is_valid)

            index += 1

            if index < len(d) and len(s) > length:
                is_valid[0] = False
                if not s.endswith('...'):
                    s += '...'
                break

            if index < len(d):
                s += ', '

    except AttributeError:
        is_valid[0] = False

    return as_unicode(pattern % s)


def repr_bytearray(s, length, encoding, is_valid):
    try:
        s = s.decode(encoding)
        r = repr_unicode(s, length, is_valid)
        return 'bytearray(b' + r[1:] + ')'

    except:
        #
        # If a string is not encoded as utf-8 its repr() will be done with
        # the regular repr() function.
        #
        return repr_str_raw(s, length, is_valid)


def repr_bytes(s, length, encoding, is_valid):
    try:
        s = s.decode(encoding)
        r = repr_unicode(s, length, is_valid)
        return 'b' + r[1:]

    except:
        #
        # If a string is not encoded as utf-8 its repr() will be done with
        # the regular repr() function.
        #
        return repr_str_raw(s, length, is_valid)


def repr_str8(s, length, encoding, is_valid):
    try:
        s = s.decode(encoding)
        r = repr_unicode(s, length, is_valid)
        return 's' + r[1:]

    except:
        #
        # If a string is not encoded as utf-8 its repr() will be done with
        # the regular repr() function.
        #
        return repr_str_raw(s, length, is_valid)


def repr_str(s, length, encoding, is_valid):
    try:
        s = as_unicode(s, encoding, fstrict = True)
        r = repr_unicode(s, length, is_valid)
        return r[1:]

    except:
        #
        # If a string is not encoded as utf-8 its repr() will be done with
        # the regular repr() function.
        #
        return repr_str_raw(s, length, is_valid)


def repr_unicode(s, length, is_valid):
    index = [2, 1][is_py3k()]

    rs = ''

    for c in s:
        if len(rs) > length:
            is_valid[0] = False
            rs += '...'
            break

        if ord(c) < 128:
            rs += repr(c)[index: -1]
        else:
            rs += c

    if not "'" in rs:
        return as_unicode("u'%s'" % rs)

    if not '"' in rs:
        return as_unicode('u"%s"' % rs)

    return as_unicode("u'%s'" % rs.replace("'", "\\'"))


def repr_str_raw(s, length, is_valid):
    if is_unicode(s):
        eli = ELLIPSIS_UNICODE
    else:
        eli = ELLIPSIS_BYTES

    if len(s) > length:
        is_valid[0] = False
        s = s[: length] + eli

    return as_unicode(repr(s))


def repr_base(v, length, is_valid):
    r = repr(v)

    if len(r) > length:
        is_valid[0] = False
        r = r[: length] + '...'

    return as_unicode(r)


def repr_ltd(x, length, encoding, is_valid = [True]):
    try:
        length = max(0, length)

        try:
            if isinstance(x, frozenset):
                return repr_list('frozenset([%s])', x, length, encoding, is_valid)

            if isinstance(x, set):
                return repr_list('set([%s])', x, length, encoding, is_valid)

        except NameError:
            pass

        if isinstance(x, sets.Set):
            return repr_list('sets.Set([%s])', x, length, encoding, is_valid)

        if isinstance(x, sets.ImmutableSet):
            return repr_list('sets.ImmutableSet([%s])', x, length, encoding, is_valid)

        if isinstance(x, list):
            return repr_list('[%s]', x, length, encoding, is_valid)

        if isinstance(x, tuple):
            return repr_list('(%s)', x, length, encoding, is_valid)

        if isinstance(x, dict):
            return repr_dict('{%s}', x, length, encoding, is_valid)

        if encoding == ENCODING_RAW_I and [True for t in [str, unicode, bytearray, bytes] if t is type(x)]:
            return repr_str_raw(x, length, is_valid)

        if type(x) is unicode:
            return repr_unicode(x, length, is_valid)

        if type(x) is bytearray:
            return repr_bytearray(x, length, encoding, is_valid)

        if type(x) is bytes:
            return repr_bytes(x, length, encoding, is_valid)

        if type(x) is str:
            return repr_str(x, length, encoding, is_valid)

        if [True for t in [bool, int, float, type(None)] if t is type(x)]:
            return repr_base(x, length, is_valid)

        is_valid[0] = False

        y = safe_repr(x)[: length]
        if len(y) == length:
            y += '...'

        if encoding == ENCODING_RAW_I:
            encoding = 'utf-8'

        try:
            y = as_unicode(y, encoding, fstrict = True)
            return y

        except:
            pass

        encoding = sys.getfilesystemencoding()
        y = as_unicode(y, encoding)

        return y

    except:
        print_debug_exception()
        return as_unicode('N/A')


