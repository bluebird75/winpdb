import hmac
import pickle
import random
import threading
import time
import zlib

try:
    from Crypto.Cipher import DES
except ImportError:
    pass

from rpdb.compat import _md5, base64_encodestring, base64_decodestring
from rpdb.exceptions import EncryptionExpected, EncryptionNotSupported, DecryptionFailure, AuthenticationFailure, \
    AuthenticationBadData, AuthenticationBadIndex
from rpdb.utils import is_unicode, as_bytes, as_unicode, print_debug_exception

INDEX_TABLE_SIZE = 100

def is_encryption_supported():
    """
    Is the Crypto module imported/available.
    """

    return 'DES' in globals()

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


