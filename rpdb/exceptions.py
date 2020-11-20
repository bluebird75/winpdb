import socket

from typing import Any

from rpdb.const import STR_COMMUNICATION_FAILURE, STR_LOST_CONNECTION, STR_FIREWALL_BLOCK, STR_BAD_VERSION, \
    STR_UNEXPECTED_DATA, STR_SPAWN_UNSUPPORTED, STR_DEBUGGEE_UNKNOWN, STR_PASSWORD_MUST_BE_SET, \
    STR_DEBUGGEE_NO_ENCRYPTION, STR_ENCRYPTION_EXPECTED, STR_DECRYPTION_FAILURE, STR_ACCESS_DENIED, STR_BAD_MBCS_PATH, \
    STR_ALREADY_ATTACHED, STR_NOT_ATTACHED, STR_DEBUGGEE_NOT_BROKEN, STR_NO_THREADS, STR_EXCEPTION_NOT_FOUND


class CException(Exception):
    """
    Base exception class for the debugger.
    """

    def __init__(self, *args: Any) -> None:
        Exception.__init__(self, *args)


class InvalidScopeName(CException):
    """
    Invalid scope name.
    This exception might be thrown when a request was made to set a breakpoint
    to an unknown scope.
    """


class BadMBCSPath(CException):
    """
    Raised on Windows systems when the python executable or debugger script
    path can not be encoded with the file system code page. This means that
    the Windows code page is misconfigured.
    """


class NotPythonSource(CException):
    """
    Raised when an attempt to load non Python source is made.
    """


class BadArgument(CException):
    """
    Bad Argument.
    """


class ThreadNotFound(CException):
    """
    Thread not found.
    """


class NoThreads(CException):
    """
    No Threads.
    """


class ThreadDone(CException):
    """
    Thread Done.
    """


class DebuggerNotBroken(CException):
    """
    Debugger is not broken.
    This exception is thrown when an operation that can only be performed
    while the debuggee is broken, is requested while the debuggee is running.
    """


class InvalidFrame(CException):
    """
    Invalid Frame.
    This exception is raised if an operation is requested on a stack frame
    that does not exist.
    """


class NoExceptionFound(CException):
    """
    No Exception Found.
    This exception is raised when exception information is requested, but no
    exception is found, or has been thrown.
    """


class CConnectionException(CException):
    def __init__(self, *args: Any) -> None:
        CException.__init__(self, *args)


class FirewallBlock(CConnectionException):
    """Firewall is blocking socket communication."""


class BadVersion(CConnectionException):
    """Bad Version."""
    def __init__(self, version: str) -> None:
        CConnectionException.__init__(self)

        self.m_version = version

    def __str__(self) -> str:
        return repr(self.m_version)


class UnexpectedData(CConnectionException):
    """Unexpected data."""


class AlreadyAttached(CConnectionException):
    """Already Attached."""


class NotAttached(CConnectionException):
    """Not Attached."""


class SpawnUnsupported(CConnectionException):
    """Spawn Unsupported."""


class UnknownServer(CConnectionException):
    """Unknown Server."""


class CSecurityException(CConnectionException):
    def __init__(self, *args: Any) -> None:
        CConnectionException.__init__(self, *args)


class UnsetPassword(CSecurityException):
    """Unset Password."""


class EncryptionNotSupported(CSecurityException):
    """Encryption Not Supported."""


class EncryptionExpected(CSecurityException):
    """Encryption Expected."""


class DecryptionFailure(CSecurityException):
    """Decryption Failure."""


class AuthenticationBadData(CSecurityException):
    """Authentication Bad Data."""


class AuthenticationFailure(CSecurityException):
    """Authentication Failure."""


class AuthenticationBadIndex(CSecurityException):
    """Authentication Bad Index."""
    def __init__(self, max_index: int = 0, anchor: int = 0) -> None:
        CSecurityException.__init__(self)

        self.m_max_index = max_index
        self.m_anchor = anchor

    def __str__(self) -> str:
        return repr((self.m_max_index, self.m_anchor))


g_error_mapping = {
    socket.error: STR_COMMUNICATION_FAILURE,

    CConnectionException: STR_LOST_CONNECTION,
    FirewallBlock: STR_FIREWALL_BLOCK,
    BadVersion: STR_BAD_VERSION,
    UnexpectedData: STR_UNEXPECTED_DATA,
    SpawnUnsupported: STR_SPAWN_UNSUPPORTED,
    UnknownServer: STR_DEBUGGEE_UNKNOWN,
    UnsetPassword: STR_PASSWORD_MUST_BE_SET,
    EncryptionNotSupported: STR_DEBUGGEE_NO_ENCRYPTION,
    EncryptionExpected: STR_ENCRYPTION_EXPECTED,
    DecryptionFailure: STR_DECRYPTION_FAILURE,
    AuthenticationBadData: STR_ACCESS_DENIED,
    AuthenticationFailure: STR_ACCESS_DENIED,
    BadMBCSPath: STR_BAD_MBCS_PATH,

    AlreadyAttached: STR_ALREADY_ATTACHED,
    NotAttached: STR_NOT_ATTACHED,
    DebuggerNotBroken: STR_DEBUGGEE_NOT_BROKEN,
    NoThreads: STR_NO_THREADS,
    NoExceptionFound: STR_EXCEPTION_NOT_FOUND,
}