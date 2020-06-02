import copy
import copyreg as copy_reg
import signal
import sys

from src.utils import as_unicode

def calc_signame(signum):
    for k, v in vars(signal).items():
        if not k.startswith('SIG') or k in ['SIG_IGN', 'SIG_DFL', 'SIGRTMIN', 'SIGRTMAX']:
            continue

        if v == signum:
            return k

    return '?'

def breakpoint_copy(bp):
    if bp is None:
        return None

    _bp = copy.copy(bp)

    #filename = g_found_unicode_files.get(bp.m_filename, bp.m_filename)

    _bp.m_filename = as_unicode(bp.m_filename, sys.getfilesystemencoding())
    _bp.m_code = None

    return _bp

class CEvent(object):
    """
    Base class for events.
    """

    def __reduce__(self):
        rv = (copy_reg.__newobj__, (type(self), ), vars(self), None, None)
        return rv


    def is_match(self, arg):
        pass


class CEventNull(CEvent):
    """
    Sent to release event listeners (Internal, speeds up shutdown).
    """

    pass


class CEventEmbeddedSync(CEvent):
    """
    Sent when an embedded interpreter becomes active if it needs to
    determine if there are pending break requests. (Internal)
    """

    pass


class CEventClearSourceCache(CEvent):
    """
    Sent when the source cache is cleared.
    """

    pass


class CEventSignalIntercepted(CEvent):
    """
    This event is sent when a signal is intercepted inside tracing code.
    Such signals are held pending until tracing code is returned from.
    """

    def __init__(self, signum):
        self.m_signum = signum
        self.m_signame = calc_signame(signum)


class CEventSignalException(CEvent):
    """
    This event is sent when the handler of a previously intercepted signal
    raises an exception. Such exceptions are ignored because of technical
    limitations.
    """

    def __init__(self, signum, description):
        self.m_signum = signum
        self.m_signame = calc_signame(signum)
        self.m_description = description


class CEventEncoding(CEvent):
    """
    The encoding has been set.
    """

    def __init__(self, encoding, fraw):
        self.m_encoding = encoding
        self.m_fraw = fraw


class CEventPsycoWarning(CEvent):
    """
    The psyco module was detected. rpdb2 is incompatible with this module.
    """

    pass


class CEventConflictingModules(CEvent):
    """
    Conflicting modules were detected. rpdb2 is incompatible with these modules.
    """

    def __init__(self, modules_list):
        self.m_modules_list = modules_list


class CEventSyncReceivers(CEvent):
    """
    A base class for events that need to be received by all listeners at
    the same time. The synchronization mechanism is internal to rpdb2.
    """

    def __init__(self, sync_n):
        self.m_sync_n = sync_n


class CEventForkSwitch(CEventSyncReceivers):
    """
    Debuggee is about to fork. Try to reconnect.
    """

    pass


class CEventExecSwitch(CEventSyncReceivers):
    """
    Debuggee is about to exec. Try to reconnect.
    """

    pass


class CEventExit(CEvent):
    """
    Debuggee is terminating.
    """

    pass


class CEventState(CEvent):
    """
    State of the debugger.
    Value of m_state can be one of the STATE_* globals.
    """

    def __init__(self, state):
        self.m_state = as_unicode(state)


    def is_match(self, arg):
        return self.m_state == as_unicode(arg)


class CEventSynchronicity(CEvent):
    """
    Mode of synchronicity.
    Sent when mode changes.
    """

    def __init__(self, fsynchronicity):
        self.m_fsynchronicity = fsynchronicity


    def is_match(self, arg):
        return self.m_fsynchronicity == arg


class CEventBreakOnExit(CEvent):
    """
    Mode of break on exit
    Sent when mode changes
    """
    def __init__(self,fbreakonexit):
        self.m_fbreakonexit = fbreakonexit

    def is_match(self,arg):
        return self.m_fbreakonexit == arg


class CEventTrap(CEvent):
    """
    Mode of "trap unhandled exceptions".
    Sent when the mode changes.
    """

    def __init__(self, ftrap):
        self.m_ftrap = ftrap


    def is_match(self, arg):
        return self.m_ftrap == arg


class CEventForkMode(CEvent):
    """
    Mode of fork behavior has changed.
    Sent when the mode changes.
    """

    def __init__(self, ffork_into_child, ffork_auto):
        self.m_ffork_into_child = ffork_into_child
        self.m_ffork_auto = ffork_auto


class CEventUnhandledException(CEvent):
    """
    Unhandled Exception
    Sent when an unhandled exception is caught.
    """


class CEventNamespace(CEvent):
    """
    Namespace has changed.
    This tells the debugger it should query the namespace again.
    """

    pass


class CEventNoThreads(CEvent):
    """
    No threads to debug.
    Debuggee notifies the debugger that it has no threads. This can
    happen in embedded debugging and in a python interpreter session.
    """

    pass


class CEventThreads(CEvent):
    """
    State of threads.
    """

    def __init__(self, _current_thread, thread_list):
        self.m_current_thread = _current_thread
        self.m_thread_list = thread_list


class CEventThreadBroken(CEvent):
    """
    A thread has broken.
    """

    def __init__(self, tid, name):
        self.m_tid = tid
        self.m_name = as_unicode(name)


class CEventStack(CEvent):
    """
    Stack of current thread.
    """

    def __init__(self, stack):
        self.m_stack = stack


class CEventStackFrameChange(CEvent):
    """
    Stack frame has changed.
    This event is sent when the debugger goes up or down the stack.
    """

    def __init__(self, frame_index):
        self.m_frame_index = frame_index


class CEventStackDepth(CEvent):
    """
    Stack depth has changed.
    """

    def __init__(self, stack_depth, stack_depth_exception):
        self.m_stack_depth = stack_depth
        self.m_stack_depth_exception = stack_depth_exception


class CEventBreakpoint(CEvent):
    """
    A breakpoint or breakpoints changed.
    """

    DISABLE = as_unicode('disable')
    ENABLE = as_unicode('enable')
    REMOVE = as_unicode('remove')
    SET = as_unicode('set')

    def __init__(self, bp, action = SET, id_list = [], fAll = False):
        self.m_bp = breakpoint_copy(bp)
        self.m_action = action
        self.m_id_list = id_list
        self.m_fAll = fAll


class CEventSync(CEvent):
    """
    Internal (not sent to the debugger) event that trigers the
    firing of other events that help the debugger synchronize with
    the state of the debuggee.
    """

    def __init__(self, fException, fSendUnhandled):
        self.m_fException = fException
        self.m_fSendUnhandled = fSendUnhandled


