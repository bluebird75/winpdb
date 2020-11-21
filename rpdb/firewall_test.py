import errno
import socket
import sys
import threading
import time
import os

from typing import Any, Optional, cast

from rpdb.const import LOOPBACK, POSIX, SERVER_PORT_RANGE_START, SERVER_PORT_RANGE_LENGTH
from rpdb.utils import thread_is_alive, as_bytes, print_debug


class CFirewallTest:
    m_port = None
    m_thread_server = None
    m_thread_client = None
    m_lock = threading.RLock()


    def __init__(self, fremote: bool = False, timeout: int = 4) -> None:
        if fremote:
            self.m_loopback = ''
        else:
            self.m_loopback = LOOPBACK

        self.m_timeout = timeout

        self.m_result = None    # type: Optional[bool]

        self.m_last_server_error = None  # type: Optional[socket.error]
        self.m_last_client_error = None  # type: Optional[socket.error]


    def run(self) -> bool:
        print_debug('CFirewallTest.run()')
        CFirewallTest.m_lock.acquire()

        try:
            #
            # If either the server or client are alive after a timeout
            # it means they are blocked by a firewall. Return False.
            #
            server = CFirewallTest.m_thread_server
            if server is not None and thread_is_alive(server):
                server.join(self.m_timeout * 1.5)
                if thread_is_alive(server):
                    return False

            client = CFirewallTest.m_thread_client
            if client is not None and thread_is_alive(client):
                client.join(self.m_timeout * 1.5)
                if thread_is_alive(client):
                    return False

            CFirewallTest.m_port = None
            self.m_result = None

            t0 = time.time()
            server = threading.Thread(target = self.__server)
            server.start()
            CFirewallTest.m_thread_server = server

            #
            # If server exited or failed to setup after a timeout
            # it means it was blocked by a firewall.
            #
            while CFirewallTest.m_port == None and thread_is_alive(server):
                if time.time() - t0 > self.m_timeout * 1.5:
                    return False

                time.sleep(0.1)

            if not thread_is_alive(server):
                return False

            t0 = time.time()
            client = threading.Thread(target = self.__client)
            client.start()
            CFirewallTest.m_thread_client = client

            while self.m_result == None and thread_is_alive(client):
                if time.time() - t0 > self.m_timeout * 1.5:
                    return False

                time.sleep(0.1)

            print_debug('CFirewallTest.run() - returning %s' % self.m_result)
            assert self.m_result is not None
            return self.m_result

        finally:
            CFirewallTest.m_lock.release()


    def __client(self) -> None:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.m_timeout)

        try:
            try:
                s.connect((LOOPBACK, CFirewallTest.m_port))

                s.send(as_bytes('Hello, world'))
                _data = self.__recv(s, 1024)
                self.m_result = True

            except socket.error:
                e = cast(socket.error, sys.exc_info()[1])
                self.m_last_client_error = e
                self.m_result = False

        finally:
            s.close()


    def __server(self) -> None:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.m_timeout)

        if os.name == POSIX:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        port = SERVER_PORT_RANGE_START

        while True:
            try:
                s.bind((self.m_loopback, port))
                break

            except socket.error:
                e = cast(socket.error, sys.exc_info()[1])

                if self.__GetSocketError(e) != errno.EADDRINUSE:
                    self.m_last_server_error = e
                    s.close()
                    return

                if port >= SERVER_PORT_RANGE_START + SERVER_PORT_RANGE_LENGTH - 1:
                    self.m_last_server_error = e
                    s.close()
                    return

                port += 1

        CFirewallTest.m_port = port

        conn = None
        try:
            try:
                s.listen(1)
                conn, addr = s.accept()

                while True:
                    data = self.__recv(conn, 1024)
                    if not data:
                        return

                    conn.send(data)

            except socket.error:
                e = cast(socket.error, sys.exc_info()[1])
                self.m_last_server_error = e

        finally:
            if conn is not None:
                conn.close()
            s.close()


    def __recv(self, s: socket.socket, _len: int) -> bytes:
        t0 = time.time()

        while True:
            try:
                data = s.recv(1024)
                return data

            except socket.error:
                e = sys.exc_info()[1]
                if self.__GetSocketError(e) != errno.EWOULDBLOCK:
                    print_debug('socket error was caught, %s' % repr(e))
                    raise

                if time.time() - t0 > self.m_timeout:
                    raise

                continue


    def __GetSocketError(self, e: Any) -> int:
        if (not isinstance(e.args, tuple)) or (len(e.args) == 0):
            return -1

        return cast(int, e.args[0])
