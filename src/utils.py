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