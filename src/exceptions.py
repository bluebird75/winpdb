

class CException(Exception):
    """
    Base exception class for the debugger.
    """

    def __init__(self, *args):
        Exception.__init__(self, *args)


class InvalidScopeName(CException):
    """
    Invalid scope name.
    This exception might be thrown when a request was made to set a breakpoint
    to an unknown scope.
    """


