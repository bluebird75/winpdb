import copyreg as copy_reg
import errno
import socket
import sys
import time

from rpdb2 import CThread, _getpid, CPwdServerProxy, calcURL, CLocalTimeoutTransport, CWorkQueue, \
    CXMLRPCServer, GetSocketError, CServerInfo, CalcModuleName
from src.const import LOOPBACK, get_interface_compatibility_version, get_version, SERVER_PORT_RANGE_START, \
    SERVER_PORT_RANGE_LENGTH
from src.exceptions import CException, BadVersion, AuthenticationBadIndex, NotAttached
from src.utils import is_unicode, thread_set_daemon, print_debug, thread_is_alive, as_unicode, print_debug_exception, \
    generate_rid
from src.crypto import CCrypto


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