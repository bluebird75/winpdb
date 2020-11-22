import os
import socket
import socketserver as SocketServer
import sys
import threading
import time
import weakref
from http import client as httplib
from xmlrpc import client as xmlrpclib, server as SimpleXMLRPCServer

from typing import Dict, Any, Tuple, Callable, cast, BinaryIO, Optional, List, Union, Iterable, TypeVar

from rpdb.const import SHUTDOWN_TIMEOUT, POSIX, get_interface_compatibility_version, PING_TIMEOUT, LOCAL_TIMEOUT
from rpdb.crypto import is_encryption_supported, CCrypto
from rpdb.exceptions import AuthenticationBadIndex, BadVersion, EncryptionExpected, EncryptionNotSupported, \
    DecryptionFailure, AuthenticationBadData, AuthenticationFailure, CConnectionException
from rpdb.repr import class_name
from rpdb.state_manager import lock_notify_all
from rpdb.utils import print_debug, safe_wait, thread_set_name, current_thread, print_debug_exception, as_unicode, _print, \
                        _getpid
import rpdb.globals

N_WORK_QUEUE_THREADS = 8

DISPACHER_METHOD = 'dispatcher_method'


class CWorkQueue:
    """
    Worker threads pool mechanism for RPC server.
    """

    def __init__(self, size: int = N_WORK_QUEUE_THREADS) -> None:
        self.m_lock = threading.Condition()
        self.m_work_items = []  # type: List[Tuple[Callable[...,None], Any, str]]
        self.m_f_shutdown = False

        self.m_size = size
        self.m_n_threads = 0
        self.m_n_available = 0

        self.__create_thread()


    def __create_thread(self) -> None:
        t = CThread(name = '__worker_target', target = self.__worker_target, shutdown = self.shutdown)
        #thread_set_daemon(t, True)
        t.start()


    def shutdown(self) -> None:
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


    def __worker_target(self) -> None:
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


    def post_work_item(self, target: Callable[..., None], args: Any, name: str ) -> None:
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


class CUnTracedThreadingMixIn(SocketServer.ThreadingMixIn):
    """
    Modification of SocketServer.ThreadingMixIn that uses a worker thread
    queue instead of spawning threads to process requests.
    This mod was needed to resolve deadlocks that were generated in some
    circumstances.
    """

    def process_request(self, request: bytes, client_address: Tuple[str, int]) -> None:
        assert rpdb.globals.g_server is not None
        rpdb.globals.g_server.m_work_queue.post_work_item(target = SocketServer.ThreadingMixIn.process_request_thread, args = (self, request, client_address), name ='process_request')


class CXMLRPCServer(CUnTracedThreadingMixIn, SimpleXMLRPCServer.SimpleXMLRPCServer):
    if os.name == POSIX:
        allow_reuse_address = True
    else:
        allow_reuse_address = False

    def handle_error(self, request: bytes, client_address: Tuple[str, int]) -> None:
        print_debug("handle_error() in pid %d" % _getpid())

        if rpdb.globals.g_ignore_broken_pipe + 5 > time.time():
            return

        return SimpleXMLRPCServer.SimpleXMLRPCServer.handle_error(self, request, client_address)


class CPwdServerProxy:
    """
    Encrypted proxy to the debuggee.
    Works by wrapping a xmlrpclib.ServerProxy object.
    """

    def __init__(self, crypto: CCrypto, uri: str, transport: Any = None, target_rid: int = 0):
        self.m_crypto = crypto
        self.m_proxy = xmlrpclib.ServerProxy(uri, transport)

        self.m_fEncryption = is_encryption_supported()
        self.m_target_rid = target_rid

        self.m_method = getattr(self.m_proxy, DISPACHER_METHOD)


    def __set_encryption(self, fEncryption: bool) -> None:
        self.m_fEncryption = fEncryption


    def get_encryption(self) -> bool:
        return self.m_fEncryption


    def __request(self, name: str, params: Any) -> Any:
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
                e = cast(AuthenticationBadIndex, sys.exc_info()[1])
                print_debug("Caught AuthenticationBadIndex: %s" % str(e))
                self.m_crypto.set_index(e.m_max_index, e.m_anchor)
                continue

            except xmlrpclib.Fault:
                fault = cast(xmlrpclib.Fault, sys.exc_info()[1])
                print_debug("Caught xmlrpclib.Fault: %s" % fault.faultString)
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


    def __getattr__(self, name: str) -> Any:
        return xmlrpclib._Method(self.__request, name)


class CTimeoutHTTPConnection(httplib.HTTPConnection):
    """
    Modification of httplib.HTTPConnection with timeout for sockets.
    """

    _rpdb2_timeout = PING_TIMEOUT

    def connect(self) -> None:
        """Connect to the host and port specified in __init__."""

        # New Python version of connect().
        if hasattr(self, 'timeout'):
            self.timeout = self._rpdb2_timeout
            return httplib.HTTPConnection.connect(self)

        # Old Python version of connect().
        msg = "getaddrinfo returns an empty list"    # type: Union[str, OSError]
        for res in socket.getaddrinfo(self.host, self.port, 0,
                                      socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                self.sock = socket.socket(af, socktype, proto)
                self.sock.settimeout(self._rpdb2_timeout)
                if self.debuglevel > 0: # type: ignore # debugLevel exists in httplib.HTTPConnection
                    print_debug("connect: (%s, %s)" % (self.host, self.port))
                self.sock.connect(sa)
            except socket.error:
                msg = cast(OSError, sys.exc_info()[1])
                if self.debuglevel > 0: # type: ignore # debugLevel exists in httplib.HTTPConnection
                    print_debug('connect fail: ' + repr((self.host, self.port)))
                if self.sock:
                    self.sock.close()
                self.sock = None
                continue
            break
        if not self.sock:
            raise socket.error(msg)


class CLocalTimeoutHTTPConnection(CTimeoutHTTPConnection):
    """
    Modification of httplib.HTTPConnection with timeout for sockets.
    """

    _rpdb2_timeout = LOCAL_TIMEOUT


class httplib_HTTP(object):
    pass


class CTimeoutHTTP(httplib_HTTP):
    """
    Modification of httplib.HTTP with timeout for sockets.
    """

    _connection_class = CTimeoutHTTPConnection


class CLocalTimeoutHTTP(httplib_HTTP):
    """
    Modification of httplib.HTTP with timeout for sockets.
    """

    _connection_class = CLocalTimeoutHTTPConnection


class CLocalTransport(xmlrpclib.Transport):
    """
    Modification of xmlrpclib.Transport to work around Zonealarm sockets
    bug.
    """

    _connection_class = httplib.HTTPConnection


    def make_connection(self, host: Union[Tuple[str, Dict[str, str]], str]) -> httplib.HTTPConnection:
        chost, self._extra_headers, x509 = self.get_host_info(host)
        return self._connection_class(chost)

    def __parse_response(self, file: BinaryIO, sock: socket.socket) -> Any:
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
            if self.verbose:    # type: ignore # verbose exists in Transport but is dynamically created
                _print("body: " + repr(response))
            p.feed(response)

        file.close()
        p.close()

        return u.close()

    if os.name == 'nt':
        _parse_response = __parse_response


class CTimeoutTransport(CLocalTransport):
    """
    Modification of xmlrpclib.Transport with timeout for sockets.
    """

    _connection_class = CTimeoutHTTPConnection


class CLocalTimeoutTransport(CLocalTransport):
    """
    Modification of xmlrpclib.Transport with timeout for sockets.
    """

    _connection_class = CLocalTimeoutHTTPConnection

class CThread (threading.Thread):
    m_fstop = False
    m_threads = {}  # type: Dict[int, Any]

    m_lock = threading.RLock()
    m_id = 0


    def __init__(self, name: Optional[str] = None,
                 target: Optional[Callable[..., None]] = None,
                 args: Tuple[Any, ...] = (),
                 shutdown: Optional[Callable[..., None]] = None) -> None:
        threading.Thread.__init__(self, name = name, target = target, args = args) # type: ignore

        self.m_fstarted = False
        self.m_shutdown_callback = shutdown

        self.m_id = self.__getId()


    def __del__(self) -> None:
        #print_debug('Destructor called for ' + thread_get_name(self))

        #threading.Thread.__del__(self)

        if self.m_fstarted:
            try:
                del CThread.m_threads[self.m_id]
            except KeyError:
                pass


    def start(self) -> None:
        if CThread.m_fstop:
            return

        CThread.m_threads[self.m_id] = weakref.ref(self)

        if CThread.m_fstop:
            del CThread.m_threads[self.m_id]
            return

        self.m_fstarted = True

        threading.Thread.start(self)


    def run(self) -> None:
        sys.settrace(None)
        sys.setprofile(None)

        threading.Thread.run(self)


    def join(self, timeout: Optional[float] = None) -> None:
        try:
            threading.Thread.join(self, timeout)
        except AssertionError:
            pass


    def shutdown(self) -> None:
        if self.m_shutdown_callback:
            self.m_shutdown_callback()


    @classmethod
    def joinAll(cls) -> None:
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

    @classmethod
    def clearJoin(cls) -> None:
        CThread.m_fstop = False


    def __getId(self) -> int:
        CThread.m_lock.acquire()
        id = CThread.m_id
        CThread.m_id += 1
        CThread.m_lock.release()

        return id