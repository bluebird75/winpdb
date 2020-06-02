from rpdb2 import CException


class InvalidScopeName(CException):
    """
    Invalid scope name.
    This exception might be thrown when a request was made to set a breakpoint
    to an unknown scope.
    """