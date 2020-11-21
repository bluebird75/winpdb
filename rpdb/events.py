import copy
import signal
import sys
import copyreg

from typing import Optional, List, Dict, Any, Callable, TYPE_CHECKING, Tuple
if TYPE_CHECKING:
    from rpdb.breakpoint import CBreakPoint

from rpdb.utils import as_unicode

EVENT_EXCLUDE = 'exclude'
EVENT_INCLUDE = 'include'

def calc_signame(signum: int) -> str:
    for k, v in vars(signal).items():
        if not k.startswith('SIG') or k in ['SIG_IGN', 'SIG_DFL', 'SIGRTMIN', 'SIGRTMAX']:
            continue

        if v == signum:
            return k

    return '?'

def breakpoint_copy(bp: 'Optional[CBreakPoint]') -> 'Optional[CBreakPoint]':
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

    def __reduce__(self) -> Tuple[Any, Any, Any, None, None]:
        rv = (copyreg.__newobj__, (type(self), ), vars(self), None, None)   # type: ignore
        return rv


    def is_match(self, arg: Any) -> bool:
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

    def __init__(self, signum: int) -> None:
        self.m_signum = signum
        self.m_signame = calc_signame(signum)


class CEventSignalException(CEvent):
    """
    This event is sent when the handler of a previously intercepted signal
    raises an exception. Such exceptions are ignored because of technical
    limitations.
    """

    def __init__(self, signum: int, description: str) -> None:
        self.m_signum = signum
        self.m_signame = calc_signame(signum)
        self.m_description = description


class CEventEncoding(CEvent):
    """
    The encoding has been set.
    """

    def __init__(self, encoding: str, fraw: bool) -> None:
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

    def __init__(self, modules_list: List[str]) -> None:
        self.m_modules_list = modules_list


class CEventSyncReceivers(CEvent):
    """
    A base class for events that need to be received by all listeners at
    the same time. The synchronization mechanism is internal to rpdb2.
    """

    def __init__(self, sync_n: bool) -> None:
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

    def __init__(self, state: str) -> None:
        self.m_state = as_unicode(state)


    def is_match(self, arg: str) -> bool:
        return self.m_state == as_unicode(arg)


class CEventSynchronicity(CEvent):
    """
    Mode of synchronicity.
    Sent when mode changes.
    """

    def __init__(self, fsynchronicity: bool) -> None:
        self.m_fsynchronicity = fsynchronicity


    def is_match(self, arg: bool) -> bool:
        return self.m_fsynchronicity == arg


class CEventBreakOnExit(CEvent):
    """
    Mode of break on exit
    Sent when mode changes
    """
    def __init__(self, fbreakonexit: bool) -> None:
        self.m_fbreakonexit = fbreakonexit

    def is_match(self, arg: bool) -> bool:
        return self.m_fbreakonexit == arg


class CEventTrap(CEvent):
    """
    Mode of "trap unhandled exceptions".
    Sent when the mode changes.
    """

    def __init__(self, ftrap: bool) -> None:
        self.m_ftrap = ftrap


    def is_match(self, arg: bool) -> bool:
        return self.m_ftrap == arg


class CEventForkMode(CEvent):
    """
    Mode of fork behavior has changed.
    Sent when the mode changes.
    """

    def __init__(self, ffork_into_child: bool, ffork_auto: bool) -> None:
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

    def __init__(self, _current_thread: int, thread_list: List[Dict[str, Any]]) -> None:
        self.m_current_thread = _current_thread
        self.m_thread_list = thread_list


class CEventThreadBroken(CEvent):
    """
    A thread has broken.
    """

    def __init__(self, tid: int, name: str) -> None:
        self.m_tid = tid
        self.m_name = as_unicode(name)


class CEventStack(CEvent):
    """
    Stack of current thread.
    """

    def __init__(self, stack: Any) -> None:
        self.m_stack = stack


class CEventStackFrameChange(CEvent):
    """
    Stack frame has changed.
    This event is sent when the debugger goes up or down the stack.
    """

    def __init__(self, frame_index: int) -> None:
        self.m_frame_index = frame_index


class CEventStackDepth(CEvent):
    """
    Stack depth has changed.
    """

    def __init__(self, stack_depth: int, stack_depth_exception: Any) -> None:
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

    def __init__(self, bp: 'Optional[CBreakPoint]', action: str = SET, id_list: Optional[List[int]] = None, fAll: bool = False) -> None:
        self.m_bp = breakpoint_copy(bp)
        self.m_action = action
        self.m_id_list = id_list or []
        self.m_fAll = fAll


class CEventSync(CEvent):
    """
    Internal (not sent to the debugger) event that trigers the
    firing of other events that help the debugger synchronize with
    the state of the debuggee.
    """

    def __init__(self, fException: bool, fSendUnhandled: bool) -> None:
        self.m_fException = fException
        self.m_fSendUnhandled = fSendUnhandled


class CEventDispatcher:
    """
    Events dispatcher.

    Dispatchers can be chained together by specifying a source event dispatcher in constructor.

    By default, the source event distpacher will duplicate all events to this dispatcher.

    It is possible to forwarded to the second dispatcher and not fired in the source dispatcher
    by using register_chain_override() on those events, before event registration.
    """

    def __init__(self, chained_event_dispatcher: Optional[Any] = None) -> None:
        self.m_chained_event_dispatcher = chained_event_dispatcher
        self.m_chain_override_types = {}    # type: Dict[type, bool]

        self.m_registrants = {} # type: Dict[CEventDispatcherRecord, bool]


    def shutdown(self) -> None:
        for er in list(self.m_registrants.keys()):
            self.__remove_dispatcher_record(er)


    def register_callback(self, 
                          callback: Callable[[CEvent], None],
                          event_type_dict: Dict[type, Dict[Any, Any]],
                          fSingleUse: bool) -> 'CEventDispatcherRecord':
        er = CEventDispatcherRecord(callback, event_type_dict, fSingleUse)

        #
        # If we have a chained dispatcher, register the callback on the
        # chained dispatcher as well.
        #
        if self.m_chained_event_dispatcher is not None:
            _er = self.__register_callback_on_chain(er, event_type_dict, fSingleUse)
            self.m_registrants[er] = _er
            return er

        self.m_registrants[er] = True
        return er


    def remove_callback(self, callback: Any) -> None:
        erl = [er for er in list(self.m_registrants.keys()) if er.m_callback == callback]
        for er in erl:
            self.__remove_dispatcher_record(er)


    def fire_events(self, event_list: List[CEvent]) -> None:
        for event in event_list:
            self.fire_event(event)


    def fire_event(self, event: CEvent) -> None:
        for er in list(self.m_registrants.keys()):
            self.__fire_er(event, er)


    def __fire_er(self, event: CEvent, er: 'CEventDispatcherRecord') -> None:
        if not er.is_match(event):
            return

        try:
            er.m_callback(event)
        except:
            pass

        if not er.m_fSingleUse:
            return

        try:
            del self.m_registrants[er]
        except KeyError:
            pass


    def register_chain_override(self, event_type_dict: Dict[type, Dict[Any, Any]]) -> None:
        """
        Chain override prevents registration on chained
        dispatchers for specific event types.
        """

        for t in list(event_type_dict.keys()):
            self.m_chain_override_types[t] = True


    def __register_callback_on_chain(self, er: 'CEventDispatcherRecord',
                                     event_type_dict: Dict[type, Dict[Any, Any]],
                                     fSingleUse: bool) -> bool:
        _event_type_dict = copy.copy(event_type_dict)
        for t in self.m_chain_override_types:
            if t in _event_type_dict:
                del _event_type_dict[t]

        if len(_event_type_dict) == 0:
            return False


        def callback(event: CEvent, er: 'CEventDispatcherRecord' = er) -> None:
            self.__fire_er(event, er)

        assert self.m_chained_event_dispatcher is not None
        _er = bool(self.m_chained_event_dispatcher.register_callback(callback, _event_type_dict, fSingleUse))
        return _er


    def __remove_dispatcher_record(self, er: 'CEventDispatcherRecord') -> None:
        try:
            if self.m_chained_event_dispatcher is not None:
                _er = self.m_registrants[er]
                if _er != False:
                    self.m_chained_event_dispatcher.__remove_dispatcher_record(_er)

            del self.m_registrants[er]

        except KeyError:
            pass


class CEventDispatcherRecord:
    """
    Internal structure that binds a callback to particular events.

    The match rules are:
    - event must always be a instance of a registered type
    - further filtering is possible on events that have a state:
        + if event_type_dict contains a key EVENT_INCLUDE, only event whose state is
           listed EVENT_INCLUDE are matched successfully
        + or if event_type_dict contains a key EVENT_EXCLUDE, only event whose state is not
           listed EVENT_EXCLUDE are matched successfully

    EVENT_INCLUDE and EVENT_EXCLUDE may not be used together
    """

    def __init__(self, callback: Callable[[CEvent], None],
                 event_type_dict: Dict[type, Dict[Any, Any]],
                 fSingleUse: bool) -> None:
        self.m_callback = callback
        self.m_event_type_dict = copy.copy(event_type_dict)
        self.m_fSingleUse = fSingleUse


    def is_match(self, event: CEvent) -> bool:
        rtl = [t for t in self.m_event_type_dict.keys() if isinstance(event, t)]
        if len(rtl) == 0:
            return False

        #
        # Examine first match only.
        #

        rt = rtl[0]
        rte = self.m_event_type_dict[rt].get(EVENT_EXCLUDE, [])
        if len(rte) != 0:
            for e in rte:
                if event.is_match(e):
                    return False
            return True

        rte = self.m_event_type_dict[rt].get(EVENT_INCLUDE, [])
        if len(rte) != 0:
            for e in rte:
                if event.is_match(e):
                    return True
            return False

        return True