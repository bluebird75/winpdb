import _thread as thread
import os.path
import pickle
import re
import socket
import subprocess
import sys
import threading
import time

from rpdb2 import  FindFile, delete_pwd_file, \
    g_fScreen, base64_encodestring, g_safe_base64_to, CalcUserShell, CalcTerminalCommand, osSpawn, getcwdu, \
    CalcMacTerminalCommand, g_fDefaultStd, CSession, ControlRate, calc_bpl_filename, generate_random_password

from src.breakpoint import CBreakPointsManagerProxy
from src.const import *
from src.events import *
from src.exceptions import *
from src.globals import g_fDebug
from src.source_provider import g_found_unicode_files
from src.utils import as_unicode, _print, print_debug, is_unicode, as_bytes, ENCODING_AUTO, detect_locale, as_string, \
    get_python_executable, print_debug_exception, print_exception, generate_rid, split_command_line_path_filename_args, \
    my_os_path_join
from src.state_manager import CStateManager
from src.firewall_test import CFirewallTest


g_fFirewallTest = True

def calc_pwd_file_path(rid):
    """
    Calc password file path for Posix systems:
    '~/.rpdb2_settings/<rid>'
    """

    home = os.path.expanduser('~')
    rsf = os.path.join(home, RPDB_PWD_FOLDER)
    pwd_file_path = os.path.join(rsf, rid)

    return pwd_file_path
    
def is_valid_pwd(_rpdb2_pwd):
    if _rpdb2_pwd in [None, '']:
        return False

    try:
        if not is_unicode(_rpdb2_pwd):
            _rpdb2_pwd = _rpdb2_pwd.decode('ascii')

        _rpdb2_pwd.encode('ascii')

    except:
        return False

    for c in _rpdb2_pwd:
        if c.isalnum():
            continue

        if c == '_':
            continue

        return False

    return True


def create_pwd_file(rid, _rpdb2_pwd):
    """
    Create password file for Posix systems.
    """

    if os.name != POSIX:
        return

    path = calc_pwd_file_path(rid)

    fd = os.open(path, os.O_WRONLY | os.O_CREAT, int('0600', 8))

    os.write(fd, as_bytes(_rpdb2_pwd))
    os.close(fd)

class CSessionManager:
    """
    Interface to the session manager.
    This is the interface through which the debugger controls and
    communicates with the debuggee.

    Accepted strings are either utf-8 or Unicode unless specified otherwise.
    Returned strings are Unicode (also when embedded in data structures).

    You can study the way it is used in StartClient()
    """

    def __init__(self, _rpdb2_pwd, fAllowUnencrypted, fAllowRemote, host):
        if _rpdb2_pwd != None:
            assert(is_valid_pwd(_rpdb2_pwd))
            _rpdb2_pwd = as_unicode(_rpdb2_pwd, fstrict = True)

        self.__smi = CSessionManagerInternal(
                            _rpdb2_pwd,
                            fAllowUnencrypted,
                            fAllowRemote,
                            host
                            )


    def shutdown(self):
        return self.__smi.shutdown()


    def set_printer(self, printer):
        """
        'printer' is a function that takes one argument and prints it.
        You can study CConsoleInternal.printer() as example for use
        and rational.
        """

        return self.__smi.set_printer(printer)


    def report_exception(self, type, value, tb):
        """
        Sends exception information to the printer.
        """

        return self.__smi.report_exception(type, value, tb)


    def register_callback(self, callback, event_type_dict, fSingleUse):
        """
        Receive events from the session manager.
        The session manager communicates it state mainly by firing events.
        You can study CConsoleInternal.__init__() as example for use.
        For details see CEventDispatcher.register_callback()
        """

        return self.__smi.register_callback(
                                callback,
                                event_type_dict,
                                fSingleUse
                                )


    def remove_callback(self, callback):
        return self.__smi.remove_callback(callback)


    def refresh(self):
        """
        Fire again all relevant events needed to establish the current state.
        """

        return self.__smi.refresh()


    def launch(self, fchdir, command_line, interpreter, encoding = 'utf-8', fload_breakpoints = True):
        """
        Launch debuggee in a new process and attach.
        fchdir - Change current directory to that of the debuggee.
        command_line - command line arguments pass to the script as a string.
        fload_breakpoints - Load breakpoints of last session.

        if command line is not a unicode string it will be decoded into unicode
        with the given encoding
        """

        command_line = as_unicode(command_line, encoding, fstrict = True)
        interpreter = as_unicode(interpreter, encoding, fstrict = True)

        return self.__smi.launch(fchdir, command_line, interpreter, fload_breakpoints)

    def wait_for_debuggee(self):
        """
        Wait until the debugee has been started and is ready to accept connections.
        """
        return self.__smi.wait_for_debuggee()


    def restart(self):
        """
        Restart debug session with same command_line and fchdir arguments
        which were used in last launch.
        """

        return self.__smi.restart()


    def get_launch_args(self):
        """
        Return command_line and fchdir arguments which were used in last
        launch as (last_fchdir, last_command_line).
        Returns (None, None) if there is no info.
        """

        return self.__smi.get_launch_args()


    def attach(self, key, name = None, encoding = 'utf-8'):
        """
        Attach to a debuggee (establish communication with the debuggee-server)
        key - a string specifying part of the filename or PID of the debuggee.

        if key is not a unicode string it will be decoded into unicode
        with the given encoding
        """

        key = as_unicode(key, encoding, fstrict = True)

        return self.__smi.attach(key, name)


    def detach(self):
        """
        Let the debuggee go...
        """

        return self.__smi.detach()


    def request_break(self):
        return self.__smi.request_break()


    def request_go(self):
        return self.__smi.request_go()


    def request_go_breakpoint(self, filename, scope, lineno):
        """
        Go (run) until the specified location is reached.
        """

        filename = as_unicode(filename, fstrict = True)
        scope = as_unicode(scope, fstrict = True)

        return self.__smi.request_go_breakpoint(filename, scope, lineno)


    def request_step(self):
        """
        Go until the next line of code is reached.
        """

        return self.__smi.request_step()


    def request_next(self):
        """
        Go until the next line of code in the same scope is reached.
        """

        return self.__smi.request_next()


    def request_return(self):
        """
        Go until end of scope is reached.
        """

        return self.__smi.request_return()


    def request_jump(self, lineno):
        """
        Jump to the specified line number in the same scope.
        """

        return self.__smi.request_jump(lineno)


    #
    # REVIEW: should return breakpoint ID
    #
    def set_breakpoint(self, filename, scope, lineno, fEnabled, expr):
        """
        Set a breakpoint.

            filename - (Optional) can be either a file name or a module name,
                       full path, relative path or no path at all.
                       If filname is None or '', then the current module is
                       used.
            scope    - (Optional) Specifies a dot delimited scope for the
                       breakpoint, such as: foo or myClass.foo
            lineno   - (Optional) Specify a line within the selected file or
                       if a scope is specified, an zero-based offset from the
                       start of the scope.
            expr     - (Optional) A Python expression that will be evaluated
                       locally when the breakpoint is hit. The break will
                       occur only if the expression evaluates to true.
        """

        filename = as_unicode(filename, fstrict = True)
        scope = as_unicode(scope, fstrict = True)
        expr = as_unicode(expr, fstrict = True)

        return self.__smi.set_breakpoint(
                                filename,
                                scope,
                                lineno,
                                fEnabled,
                                expr
                                )


    def disable_breakpoint(self, id_list, fAll):
        """
        Disable breakpoints

            id_list - (Optional) A list of breakpoint ids.
            fAll    - disable all breakpoints regardless of id_list.
        """

        return self.__smi.disable_breakpoint(id_list, fAll)


    def enable_breakpoint(self, id_list, fAll):
        """
        Enable breakpoints

            id_list - (Optional) A list of breakpoint ids.
            fAll    - disable all breakpoints regardless of id_list.
        """

        return self.__smi.enable_breakpoint(id_list, fAll)


    def delete_breakpoint(self, id_list, fAll):
        """
        Delete breakpoints

            id_list - (Optional) A list of breakpoint ids.
            fAll    - disable all breakpoints regardless of id_list.
        """

        return self.__smi.delete_breakpoint(id_list, fAll)


    def get_breakpoints(self):
        """
        Return breakpoints in a dictionary of id keys to CBreakPoint values
        """

        return self.__smi.get_breakpoints()


    def save_breakpoints(self, _filename = ''):
        """
        Save breakpoints to file, locally (on the client side)
        """

        return self.__smi.save_breakpoints(_filename)


    def load_breakpoints(self, _filename = ''):
        """
        Load breakpoints from file, locally (on the client side)
        """

        return self.__smi.load_breakpoints(_filename)


    def set_trap_unhandled_exceptions(self, ftrap):
        """
        Set trap-unhandled-exceptions mode.
        ftrap with a value of False means unhandled exceptions will be ignored.
        The session manager default is True.
        """

        return self.__smi.set_trap_unhandled_exceptions(ftrap)


    def get_trap_unhandled_exceptions(self):
        """
        Get trap-unhandled-exceptions mode.
        """

        return self.__smi.get_trap_unhandled_exceptions()


    def set_fork_mode(self, ffork_into_child, ffork_auto):
        """
        Determine how to handle os.fork().

        ffork_into_child - True|False - If True, the debugger will debug the
            child process after a fork, otherwise the debugger will continue
            to debug the parent process.

        ffork_auto - True|False - If True, the debugger will not pause before
            a fork and will automatically make a decision based on the
            value of the ffork_into_child flag.
        """

        return self.__smi.set_fork_mode(ffork_into_child, ffork_auto)


    def get_fork_mode(self):
        """
        Return the fork mode in the form of a (ffork_into_child, ffork_auto)
        flags tuple.
        """

        return self.__smi.get_fork_mode()


    def get_stack(self, tid_list, fAll):
        return self.__smi.get_stack(tid_list, fAll)


    def get_source_file(self, filename, lineno, nlines):
        filename = as_unicode(filename, fstrict = True)

        return self.__smi.get_source_file(filename, lineno, nlines)


    def get_source_lines(self, nlines, fAll):
        return self.__smi.get_source_lines(nlines, fAll)


    def set_frame_index(self, frame_index):
        """
        Set frame index. 0 is the current executing frame, and 1, 2, 3,
        are deeper into the stack.
        """

        return self.__smi.set_frame_index(frame_index)


    def get_frame_index(self):
        """
        Get frame index. 0 is the current executing frame, and 1, 2, 3,
        are deeper into the stack.
        """

        return self.__smi.get_frame_index()


    def set_analyze(self, fAnalyze):
        """
        Toggle analyze mode. In analyze mode the stack switches to the
        exception stack for examination.
        """

        return self.__smi.set_analyze(fAnalyze)


    def set_host(self, host):
        """
        Set host to specified host (string) for attaching to debuggies on
        specified host. host can be a host name or ip address in string form.
        """

        return self.__smi.set_host(host)


    def get_host(self):
        return self.__smi.get_host()


    def calc_server_list(self):
        """
        Calc servers (debuggable scripts) list on specified host.
        Returns a tuple of a list and a dictionary.
        The list is a list of CServerInfo objects sorted by their age
        ordered oldest last.
        The dictionary is a dictionary of errors that were encountered
        during the building of the list. The dictionary has error (exception)
        type as keys and number of occurances as values.
        """

        return self.__smi.calc_server_list()


    def get_server_info(self):
        """
        Return CServerInfo server info object that corresponds to the
        server (debugged script) to which the session manager is
        attached.
        """

        return self.__smi.get_server_info()


    def get_namespace(self, nl, filter_level, repr_limit = 128, fFilter = "DEPRECATED"):
        """
        get_namespace is designed for locals/globals panes that let
        the user inspect a namespace tree in GUI debuggers such as Winpdb.
        You can study the way it is used in Winpdb.

        nl - List of tuples, where each tuple is made of a python expression
             as string and a flag that controls whether to "expand" the
             value, that is, to return its children as well in case it has
             children e.g. lists, dictionaries, etc...

        filter_level - 0, 1, or 2. Filter out methods and functions from
            classes and objects. (0 - None, 1 - Medium, 2 - Maximum).

        repr_limit - Length limit (approximated) to be imposed on repr() of
             returned items.

        examples of expression lists:

          [('x', false), ('y', false)]
          [('locals()', true)]
          [('a.b.c', false), ('my_object.foo', false), ('another_object', true)]

        Return value is a list of dictionaries, where every element
        in the list corresponds to an element in the input list 'nl'.

        Each dictionary has the following keys and values:
          DICT_KEY_EXPR - the original expression string.
          DICT_KEY_REPR - A repr of the evaluated value of the expression.
          DICT_KEY_IS_VALID - A boolean that indicates if the repr value is
                          valid for the purpose of re-evaluation.
          DICT_KEY_TYPE - A string representing the type of the experession's
                          evaluated value.
          DICT_KEY_N_SUBNODES - If the evaluated value has children like items
                          in a list or in a dictionary or members of a class,
                          etc, this key will have their number as value.
          DICT_KEY_SUBNODES - If the evaluated value has children and the
                          "expand" flag was set for this expression, then the
                          value of this key will be a list of dictionaries as
                          described below.
          DICT_KEY_ERROR - If an error prevented evaluation of this expression
                          the value of this key will be a repr of the
                          exception info: repr(sys.exc_info())

        Each dictionary for child items has the following keys and values:
          DICT_KEY_EXPR - The Python expression that designates this child.
                          e.g. 'my_list[0]' designates the first child of the
                          list 'my_list'
          DICT_KEY_NAME - a repr of the child name, e.g '0' for the first item
                          in a list.
          DICT_KEY_REPR - A repr of the evaluated value of the expression.
          DICT_KEY_IS_VALID - A boolean that indicates if the repr value is
                          valid for the purpose of re-evaluation.
          DICT_KEY_TYPE - A string representing the type of the experession's
                          evaluated value.
          DICT_KEY_N_SUBNODES - If the evaluated value has children like items
                          in a list or in a dictionary or members of a class,
                          etc, this key will have their number as value.
        """

        if fFilter != "DEPRECATED":
            filter_level = fFilter

        filter_level = int(filter_level)

        return self.__smi.get_namespace(nl, filter_level, repr_limit)


    #
    # REVIEW: remove warning item.
    #
    def evaluate(self, expr):
        """
        Evaluate a python expression in the context of the current thread
        and frame.

        Return value is a tuple (v, w, e) where v is a repr of the evaluated
        expression value, w is always '', and e is an error string if an error
        occurred.

        NOTE: This call might not return since debugged script logic can lead
        to tmporary locking or even deadlocking.
        """

        expr = as_unicode(expr, fstrict = True)

        return self.__smi.evaluate(expr)


    def execute(self, suite):
        """
        Execute a python statement in the context of the current thread
        and frame.

        Return value is a tuple (w, e) where w and e are warning and
        error strings (respectively) if an error occurred.

        NOTE: This call might not return since debugged script logic can lead
        to tmporary locking or even deadlocking.
        """

        suite = as_unicode(suite, fstrict = True)

        return self.__smi.execute(suite)


    def complete_expression(self, expr):
        """
        Return matching completions for expression.
        Accepted expressions are of the form a.b.c

        Dictionary lookups or functions call are not evaluated. For
        example: 'getobject().complete' or 'dict[item].complete' are
        not processed.

        On the other hand partial expressions and statements are
        accepted. For example: 'foo(arg1, arg2.member.complete' will
        be accepted and the completion for 'arg2.member.complete' will
        be calculated.

        Completions are returned as a tuple of two items. The first item
        is a prefix to expr and the second item is a list of completions.
        For example if expr is 'foo(self.comp' the returned tuple can
        be ('foo(self.', ['complete', 'completion', etc...])
        """

        expr = as_unicode(expr, fstrict = True)

        return self.__smi.complete_expression(expr)


    def set_encoding(self, encoding, fraw = False):
        """
        Set the encoding that will be used as source encoding for execute()
        evaluate() commands and in strings returned by get_namespace().

        The encoding value can be either 'auto' or any encoding accepted by
        the codecs module. If 'auto' is specified, the encoding used will be
        the source encoding of the active scope, which is utf-8 by default.

        The default encoding value is 'auto'.

        If fraw is True, strings returned by evaluate() and get_namespace()
        will represent non ASCII characters as an escape sequence.
        """

        return self.__smi.set_encoding(encoding, fraw)


    def get_encoding(self):
        """
        return the (encoding, fraw) tuple.
        """
        return self.__smi.get_encoding()


    def set_synchronicity(self, fsynchronicity):
        """
        Set the synchronicity mode.

        Traditional Python debuggers that use the inspected thread (usually
        the main thread) to query or modify the script name-space have to
        wait until the script hits a break-point. Synchronicity allows the
        debugger to query and modify the script name-space even if its
        threads are still running or blocked in C library code by using
        special worker threads. In some rare cases querying or modifying data
        in synchronicity can crash the script. For example in some Linux
        builds of wxPython querying the state of wx objects from a thread
        other than the GUI thread can crash the script. If this happens or
        if you want to restrict these operations to the inspected thread,
        turn synchronicity off.

        On the other hand when synchronicity is off it is possible to
        accidentally deadlock or block indefinitely the script threads by
        querying or modifying particular data structures.

        The default is on (True).
        """

        return self.__smi.set_synchronicity(fsynchronicity)

    def get_synchronicity(self):
        return self.__smi.get_synchronicity()

    def set_breakonexit(self, fbreakonexit):
        return self.__smi.set_breakonexit(fbreakonexit)

    def get_breakonexit(self):
        return self.__smi.get_breakonexit()

    def get_state(self):
        """
        Get the session manager state. Return one of the STATE_* constants
        defined below, for example STATE_DETACHED, STATE_BROKEN, etc...
        """

        return self.__smi.get_state()


    #
    # REVIEW: Improve data strucutre.
    #
    def get_thread_list(self):
        return self.__smi.get_thread_list()


    def set_thread(self, tid):
        """
        Set the focused thread to the soecified thread.
        tid - either the OS thread id or the zero based index of the thread
              in the thread list returned by get_thread_list().
        """

        return self.__smi.set_thread(tid)


    def set_password(self, _rpdb2_pwd):
        """
        Set the password that will govern the authentication and encryption
        of client-server communication.
        """

        _rpdb2_pwd = as_unicode(_rpdb2_pwd, fstrict = True)

        return self.__smi.set_password(_rpdb2_pwd)


    def get_password(self):
        """
        Get the password that governs the authentication and encryption
        of client-server communication.
        """

        return self.__smi.get_password()


    def get_encryption(self):
        """
        Get the encryption mode. Return True if unencrypted connections are
        not allowed. When launching a new debuggee the debuggee will inherit
        the encryption mode. The encryption mode can be set via command-line
        only.
        """

        return self.__smi.get_encryption()


    def set_remote(self, fAllowRemote):
        """
        Set the remote-connections mode. if True, connections from remote
        machine are allowed. When launching a new debuggee the debuggee will
        inherit this mode. This mode is only relevant to the debuggee.
        """

        return self.__smi.set_remote(fAllowRemote)


    def get_remote(self):
        """
        Get the remote-connections mode. Return True if connections from
        remote machine are allowed. When launching a new debuggee the
        debuggee will inherit this mode. This mode is only relevant to the
        debuggee.
        """

        return self.__smi.get_remote()


    def set_environ(self, envmap):
        """
        Set the environment variables mapping. This mapping is used
        when a new script is launched to modify its environment.

        Example for a mapping on Windows: [('Path', '%Path%;c:\\mydir')]
        Example for a mapping on Linux: [('PATH', '$PATH:~/mydir')]

        The mapping should be a list of tupples where each tupple is
        composed of a key and a value. Keys and Values must be either
        strings or Unicode strings. Other types will raise the BadArgument
        exception.

        Invalid arguments will be silently ignored.
        """

        return self.__smi.set_environ(envmap)


    def get_environ(self):
        """
        Return the current environment mapping.
        """

        return self.__smi.get_environ()


    def stop_debuggee(self):
        """
        Stop the debuggee immediately.
        """

        return self.__smi.stop_debuggee()


class CSimpleSessionManager:
    """
    This is a wrapper class that simplifies launching and controlling of a
    debuggee from within another program. For example, an IDE that launches
    a script for debugging puposes can use this class to launch, debug and
    stop a script.
    """

    def __init__(self, fAllowUnencrypted = True):
        self.__sm = CSessionManagerInternal(
                            _rpdb2_pwd = None,
                            fAllowUnencrypted = fAllowUnencrypted,
                            fAllowRemote = False,
                            host =LOCALHOST
                            )

        self.m_fRunning = False

        event_type_dict = {CEventUnhandledException: {}}
        self.__sm.register_callback(self.__unhandled_exception, event_type_dict, fSingleUse = False)

        event_type_dict = {CEventState: {}}
        self.__sm.register_callback(self.__state_calback, event_type_dict, fSingleUse = False)

        event_type_dict = {CEventExit: {}}
        self.__sm.register_callback(self.__termination_callback, event_type_dict, fSingleUse = False)


    def shutdown(self):
        self.__sm.shutdown()


    def launch(self, fchdir, command_line, interpreter, encoding = 'utf-8', fload_breakpoints = False):
        command_line = as_unicode(command_line, encoding, fstrict = True)
        interpreter = as_unicode(interpreter, encoding, fstrict = True)

        self.m_fRunning = False

        self.__sm.launch(fchdir, command_line, interpreter, fload_breakpoints)


    def request_go(self):
        self.__sm.request_go()


    def detach(self):
        self.__sm.detach()


    def stop_debuggee(self):
        self.__sm.stop_debuggee()


    def get_session_manager(self):
        return self.__sm


    def prepare_attach(self):
        """
        Use this method to attach a debugger to the debuggee after an
        exception is caught.
        """

        _rpdb2_pwd = self.__sm.get_password()

        si = self.__sm.get_server_info()
        rid = si.m_rid

        if os.name == 'posix':
            #
            # On posix systems the password is set at the debuggee via
            # a special temporary file.
            #
            create_pwd_file(rid, _rpdb2_pwd)
            _rpdb2_pwd = None

        return (rid, _rpdb2_pwd)


    #
    # Override these callbacks to react to the related events.
    #

    def unhandled_exception_callback(self):
        _print('unhandled_exception_callback')
        self.request_go()


    def script_paused(self):
        _print('script_paused')
        self.request_go()


    def script_terminated_callback(self):
        _print('script_terminated_callback')


    #
    # Private Methods
    #

    def __unhandled_exception(self, event):
        self.unhandled_exception_callback()


    def __termination_callback(self, event):
        self.script_terminated_callback()


    def __state_calback(self, event):
        """
        Handle state change notifications from the debugge.
        """

        if event.m_state != STATE_BROKEN:
            return

        if not self.m_fRunning:
            #
            # First break comes immediately after launch.
            #
            print_debug('Simple session manager continues on first break.')
            self.m_fRunning = True
            self.request_go()
            return

        if self.__sm.is_unhandled_exception():
            return

        sl = self.__sm.get_stack(tid_list = [], fAll = False)
        if len(sl) == 0:
            self.request_go()
            return

        st = sl[0]
        s = st.get(DICT_KEY_STACK, [])
        if len(s) == 0:
            self.request_go()
            return

        e = s[-1]

        function_name = e[2]
        filename = os.path.basename(e[0])

        if filename != DEBUGGER_FILENAME:
            #
            # This is a user breakpoint (e.g. rpdb2.setbreak())
            #
            self.script_paused()
            return

        #
        # This is the setbreak() before a fork, exec or program
        # termination.
        #
        self.request_go()
        return


class CSessionManagerInternal:
    def __init__(self, _rpdb2_pwd, fAllowUnencrypted, fAllowRemote, host):
        self.m_rpdb2_pwd = [_rpdb2_pwd, None][_rpdb2_pwd in [None, '']]
        self.m_fAllowUnencrypted = fAllowUnencrypted
        self.m_fAllowRemote = fAllowRemote
        self.m_rid = generate_rid()

        self.m_host = host
        self.m_server_list_object = CServerList(host)

        self.m_session = None
        self.m_server_info = None

        self.m_worker_thread = None
        self.m_worker_thread_ident = None
        self.m_fStop = False

        self.m_stack_depth = None
        self.m_stack_depth_exception = None
        self.m_frame_index = 0
        self.m_frame_index_exception = 0

        self.m_completions = {}

        self.m_remote_event_index = 0
        self.m_event_dispatcher_proxy = CEventDispatcher()
        self.m_event_dispatcher = CEventDispatcher(self.m_event_dispatcher_proxy)
        self.m_state_manager = CStateManager(STATE_DETACHED, self.m_event_dispatcher, self.m_event_dispatcher_proxy)

        self.m_breakpoints_proxy = CBreakPointsManagerProxy(self)

        event_type_dict = {CEventState: {EVENT_EXCLUDE: [STATE_BROKEN, STATE_ANALYZE]}}
        self.register_callback(self.reset_frame_indexes, event_type_dict, fSingleUse = False)

        event_type_dict = {CEventStackDepth: {}}
        self.register_callback(self.set_stack_depth, event_type_dict, fSingleUse = False)

        event_type_dict = {CEventNoThreads: {}}
        self.register_callback(self._reset_frame_indexes, event_type_dict, fSingleUse = False)

        event_type_dict = {CEventExit: {}}
        self.register_callback(self.on_event_exit, event_type_dict, fSingleUse = False)

        event_type_dict = {CEventConflictingModules: {}}
        self.register_callback(self.on_event_conflicting_modules, event_type_dict, fSingleUse = False)

        event_type_dict = {CEventSignalIntercepted: {}}
        self.register_callback(self.on_event_signal_intercept, event_type_dict, fSingleUse = False)

        event_type_dict = {CEventSignalException: {}}
        self.register_callback(self.on_event_signal_exception, event_type_dict, fSingleUse = False)

        event_type_dict = {CEventEmbeddedSync: {}}
        self.register_callback(self.on_event_embedded_sync, event_type_dict, fSingleUse = False)

        event_type_dict = {CEventSynchronicity: {}}
        self.m_event_dispatcher_proxy.register_callback(self.on_event_synchronicity, event_type_dict, fSingleUse = False)
        self.m_event_dispatcher.register_chain_override(event_type_dict)

        event_type_dict = {CEventBreakOnExit: {}}
        self.m_event_dispatcher_proxy.register_callback(self.on_event_breakonexit, event_type_dict, fSingleUse = False)
        self.m_event_dispatcher.register_chain_override(event_type_dict)

        event_type_dict = {CEventTrap: {}}
        self.m_event_dispatcher_proxy.register_callback(self.on_event_trap, event_type_dict, fSingleUse = False)
        self.m_event_dispatcher.register_chain_override(event_type_dict)

        event_type_dict = {CEventForkMode: {}}
        self.m_event_dispatcher_proxy.register_callback(self.on_event_fork_mode, event_type_dict, fSingleUse = False)
        self.m_event_dispatcher.register_chain_override(event_type_dict)

        self.m_printer = self.__nul_printer

        self.m_last_command_line = None
        self.m_last_fchdir = None
        self.m_last_interpreter = None

        self.m_fsynchronicity = True
        self.m_ftrap = True
        self.m_breakonexit = False

        self.m_ffork_into_child = False
        self.m_ffork_auto = False

        self.m_environment = []

        self.m_encoding = ENCODING_AUTO
        self.m_fraw = False


    def shutdown(self):
        self.m_event_dispatcher_proxy.shutdown()
        self.m_event_dispatcher.shutdown()
        self.m_state_manager.shutdown()


    def __nul_printer(self, _str):
        pass


    def set_printer(self, printer):
        self.m_printer = printer


    def register_callback(self, callback, event_type_dict, fSingleUse):
        return self.m_event_dispatcher.register_callback(callback, event_type_dict, fSingleUse)


    def remove_callback(self, callback):
        return self.m_event_dispatcher.remove_callback(callback)


    def wait_for_debuggee(self):
        return self.__wait_for_debuggee(None)

    def __wait_for_debuggee(self, rid):
        try:
            time.sleep(STARTUP_TIMEOUT / 2)

            for i in range(STARTUP_RETRIES):
                try:
                    print_debug('Scanning for debuggee...')

                    t0 = time.time()
                    return self.m_server_list_object.calcList(self.m_rpdb2_pwd, self.m_rid, rid)

                except UnknownServer:
                    dt = time.time() - t0
                    if dt < STARTUP_TIMEOUT:
                        time.sleep(STARTUP_TIMEOUT - dt)

                    continue

            return self.m_server_list_object.calcList(self.m_rpdb2_pwd, self.m_rid, rid)

        finally:
            errors = self.m_server_list_object.get_errors()
            self.__report_server_errors(errors, fsupress_pwd_warning = True)


    def get_encryption(self):
        return self.getSession().get_encryption()


    def launch(self, fchdir, command_line, interpreter, fload_breakpoints = True ):
        assert(is_unicode(command_line))
        assert(is_unicode(interpreter))

        self.__verify_unattached()

        if not os.name in [POSIX, 'nt']:
            self.m_printer(STR_SPAWN_UNSUPPORTED)
            raise SpawnUnsupported

        if g_fFirewallTest:
            firewall_test = CFirewallTest(self.get_remote())
            if not firewall_test.run():
                raise FirewallBlock
        else:
            print_debug('Skipping firewall test.')

        if self.m_rpdb2_pwd is None:
            self.set_random_password()

        if command_line == '':
            raise BadArgument

        (path, filename, args) = split_command_line_path_filename_args(command_line)

        #if not IsPythonSourceFile(filename):
        #    raise NotPythonSource

        _filename = my_os_path_join(path, filename)

        ExpandedFilename = FindFile(_filename)
        self.set_host(LOCALHOST)

        self.m_printer(STR_STARTUP_SPAWN_NOTICE)

        rid = generate_rid()

        create_pwd_file(rid, self.m_rpdb2_pwd)

        self.m_state_manager.set_state(STATE_SPAWNING)

        try:
            try:
                self._spawn_server(fchdir, ExpandedFilename, args, rid, interpreter)
                server = self.__wait_for_debuggee(rid)
                self.attach(server.m_rid, server.m_filename, fsupress_pwd_warning = True, fsetenv = True, ffirewall_test = False, server = server, fload_breakpoints = fload_breakpoints)

                self.m_last_command_line = command_line
                self.m_last_fchdir = fchdir
                self.m_last_interpreter = interpreter

            except:
                if self.m_state_manager.get_state() != STATE_DETACHED:
                    self.m_state_manager.set_state(STATE_DETACHED)

                raise

        finally:
            delete_pwd_file(rid)


    def restart(self):
        """
        Restart debug session with same command_line and fchdir arguments
        which were used in last launch.
        """

        if None in (self.m_last_fchdir, self.m_last_command_line, self.m_last_interpreter):
            return

        if self.m_state_manager.get_state() != STATE_DETACHED:
            self.stop_debuggee()

        self.launch(self.m_last_fchdir, self.m_last_command_line, self.m_last_interpreter)


    def get_launch_args(self):
        """
        Return command_line and fchdir arguments which were used in last
        launch as (last_fchdir, last_command_line, last_interpreter).
        Returns None if there is no info.
        """

        if None in (self.m_last_fchdir, self.m_last_command_line, self.m_last_interpreter):
            return (None, None, None)

        return (self.m_last_fchdir, self.m_last_command_line, self.m_last_interpreter)


    def _spawn_server(self, fchdir, ExpandedFilename, args, rid, interpreter):
        """
        Start an OS console to act as server.
        What it does is to start rpdb again in a new console in server only mode.
        """

        if g_fScreen:
            name = SCREEN
        elif sys.platform == DARWIN:
            name = DARWIN
        else:
            try:
                import terminalcommand
                name = MAC
            except:
                name = os.name

        if name == 'nt' and g_fDebug:
            name = NT_DEBUG

        e = ['', ' --encrypt'][not self.m_fAllowUnencrypted]
        r = ['', ' --remote'][self.m_fAllowRemote]
        c = ['', ' --chdir'][fchdir]
        p = ['', ' --pwd="%s"' % self.m_rpdb2_pwd][os.name == 'nt']

        # Adjust filename to base64 to circumvent encoding problems
        b = ''

        encoding = detect_locale()
        fse = sys.getfilesystemencoding()

        ExpandedFilename = g_found_unicode_files.get(ExpandedFilename, ExpandedFilename)
        ExpandedFilename = as_unicode(ExpandedFilename, fse)

        if as_bytes('?') in as_bytes(ExpandedFilename, encoding, fstrict = False):
            _u = as_bytes(ExpandedFilename)
            _b = base64_encodestring(_u)
            _b = _b.strip(as_bytes('\n')).translate(g_safe_base64_to)
            _b = as_string(_b, fstrict = True)
            b = ' --base64=%s' % _b

        # for .pyc files, strip the c
        debugger = os.path.abspath(__file__)
        if debugger[-1:] == 'c':
            debugger = debugger[:-1]

        debugger = as_unicode(debugger, fse)

        debug_prints = ['', ' --debug'][g_fDebug]

        options = '"%s"%s --debugee%s%s%s%s%s --rid=%s "%s" %s' % (debugger, debug_prints, p, e, r, c, b, rid,
            ExpandedFilename, args)

        # XXX Should probably adjust path of interpreter if any

        python_exec = get_python_executable(interpreter)

        if as_bytes('?') in as_bytes(python_exec + debugger, encoding, fstrict = False):
            raise BadMBCSPath

        if name == POSIX:
            shell = CalcUserShell()
            terminal_command = CalcTerminalCommand()

            if terminal_command in osSpawn:
                command = osSpawn[terminal_command] % {'shell': shell, 'exec': python_exec, 'options': options}
            else:
                command = osSpawn[name] % {'term': terminal_command, 'shell': shell, 'exec': python_exec, 'options': options}
        else:
            command = osSpawn[name] % {'exec': python_exec, 'options': options}

        if name == DARWIN:
            s = 'cd "%s" ; %s' % (getcwdu(), command)
            command = CalcMacTerminalCommand(s)

        print_debug('Terminal open string: %s' % repr(command))

        command = as_string(command, encoding)

        if name == MAC:
            terminalcommand.run(command)
        else:
            subprocess.Popen(command, shell=True)


    def attach(self, key, name = None, fsupress_pwd_warning = False, fsetenv = False, ffirewall_test = True, server = None, fload_breakpoints = True):
        assert(is_unicode(key))

        self.__verify_unattached()

        if key == '':
            raise BadArgument

        if self.m_rpdb2_pwd is None:
            #self.m_printer(STR_PASSWORD_MUST_BE_SET)
            raise UnsetPassword

        if g_fFirewallTest and ffirewall_test:
            firewall_test = CFirewallTest(self.get_remote())
            if not firewall_test.run():
                raise FirewallBlock
        elif not g_fFirewallTest and ffirewall_test:
            print_debug('Skipping firewall test.')

        if name is None:
            name = key

        _name = name

        self.m_printer(STR_STARTUP_NOTICE)
        self.m_state_manager.set_state(STATE_ATTACHING)

        try:
            servers = [server]
            if server == None:
                self.m_server_list_object.calcList(self.m_rpdb2_pwd, self.m_rid)
                servers = self.m_server_list_object.findServers(key)
                server = servers[0]

            _name = server.m_filename

            errors = self.m_server_list_object.get_errors()
            if not key in [server.m_rid, str(server.m_pid)]:
                self.__report_server_errors(errors, fsupress_pwd_warning)

            self.__attach(server, fsetenv)
            if len(servers) > 1:
                self.m_printer(STR_MULTIPLE_DEBUGGEES % key)
            self.m_printer(STR_ATTACH_CRYPTO_MODE % ([' ' + STR_ATTACH_CRYPTO_MODE_NOT, ''][self.get_encryption()]))
            self.m_printer(STR_ATTACH_SUCCEEDED % server.m_filename)

            try:
                if fload_breakpoints:
                    self.load_breakpoints()
            except:
                pass

        except (socket.error, CConnectionException):
            self.m_printer(STR_ATTACH_FAILED_NAME % _name)
            self.m_state_manager.set_state(STATE_DETACHED)
            raise

        except:
            print_debug_exception()
            assert False


    def report_exception(self, _type, value, tb):
        msg = g_error_mapping.get(_type, STR_ERROR_OTHER)

        if _type == SpawnUnsupported and os.name == POSIX and not g_fScreen and g_fDefaultStd:
            msg += ' ' + STR_SPAWN_UNSUPPORTED_SCREEN_SUFFIX

        if _type == UnknownServer and os.name == POSIX and not g_fScreen and g_fDefaultStd:
            msg += ' ' + STR_DISPLAY_ERROR

        _str = msg % {'type': _type, 'value': value, 'traceback': tb}
        self.m_printer(_str)

        if not _type in g_error_mapping:
            print_exception(_type, value, tb, True)


    def __report_server_errors(self, errors, fsupress_pwd_warning = False):
        for k, el in errors.items():
            if fsupress_pwd_warning and k in [BadVersion, AuthenticationBadData, AuthenticationFailure]:
                continue

            if k in [BadVersion]:
                for (t, v, tb) in el:
                    self.report_exception(t, v, None)
                continue

            (t, v, tb) = el[0]
            self.report_exception(t, v, tb)


    def __attach(self, server, fsetenv):
        self.__verify_unattached()

        session = CSession(self.m_host, server.m_port, self.m_rpdb2_pwd, self.m_fAllowUnencrypted, self.m_rid)
        session.Connect()

        if (session.getServerInfo().m_pid != server.m_pid) or (session.getServerInfo().m_filename != server.m_filename):
            raise UnexpectedData

        self.m_session = session

        self.m_server_info = self.get_server_info()

        self.getSession().getProxy().set_synchronicity(self.m_fsynchronicity)
        self.getSession().getProxy().set_breakonexit(self.m_breakonexit)
        self.getSession().getProxy().set_trap_unhandled_exceptions(self.m_ftrap)
        self.getSession().getProxy().set_fork_mode(self.m_ffork_into_child, self.m_ffork_auto)

        if fsetenv and len(self.m_environment) != 0:
            self.getSession().getProxy().set_environ(self.m_environment)

        self.request_break()
        self.refresh(True)

        self.__start_event_monitor()

        print_debug('Attached to debuggee on port %d.' % session.m_port)

        #self.enable_breakpoint([], fAll = True)


    def __verify_unattached(self):
        if self.__is_attached():
            raise AlreadyAttached


    def __verify_attached(self):
        if not self.__is_attached():
            raise NotAttached


    def __is_attached(self):
        return (self.m_state_manager.get_state() != STATE_DETACHED) and (self.m_session is not None)


    def __verify_broken(self):
        if self.m_state_manager.get_state() not in [STATE_BROKEN, STATE_ANALYZE]:
            raise DebuggerNotBroken


    def refresh(self, fSendUnhandled = False):
        fAnalyzeMode = (self.m_state_manager.get_state() == STATE_ANALYZE)

        self.m_remote_event_index = self.getSession().getProxy().sync_with_events(fAnalyzeMode, fSendUnhandled)
        self.m_breakpoints_proxy.sync()


    def __start_event_monitor(self):
        self.m_fStop = False
        self.m_worker_thread = threading.Thread(target = self.__event_monitor_proc)
        #thread_set_daemon(self.m_worker_thread, True)
        self.m_worker_thread.start()


    def __event_monitor_proc(self):
        self.m_worker_thread_ident = thread.get_ident()
        t = 0
        nfailures = 0

        while not self.m_fStop:
            try:
                t = ControlRate(t, IDLE_MAX_RATE)
                if self.m_fStop:
                    return

                (n, sel) = self.getSession().getProxy().wait_for_event(PING_TIMEOUT, self.m_remote_event_index)

                if True in [isinstance(e, CEventForkSwitch) for e in sel]:
                    print_debug('Received fork switch event.')

                    self.getSession().pause()
                    threading.Thread(target = self.restart_session_job).start()

                if True in [isinstance(e, CEventExecSwitch) for e in sel]:
                    print_debug('Received exec switch event.')

                    self.getSession().pause()
                    threading.Thread(target = self.restart_session_job, args = (True, )).start()

                if True in [isinstance(e, CEventExit) for e in sel]:
                    self.getSession().shut_down()
                    self.m_fStop = True

                if n > self.m_remote_event_index:
                    #print >> sys.__stderr__, (n, sel)
                    self.m_remote_event_index = n
                    self.m_event_dispatcher_proxy.fire_events(sel)

                nfailures = 0

            except CConnectionException:
                if not self.m_fStop:
                    self.report_exception(*sys.exc_info())
                    threading.Thread(target = self.detach_job).start()

                return

            except socket.error:
                if nfailures < COMMUNICATION_RETRIES:
                    nfailures += 1
                    continue

                if not self.m_fStop:
                    self.report_exception(*sys.exc_info())
                    threading.Thread(target = self.detach_job).start()

                return


    def on_event_conflicting_modules(self, event):
        s = ', '.join(event.m_modules_list)
        self.m_printer(STR_CONFLICTING_MODULES % s)


    def on_event_signal_intercept(self, event):
        if self.m_state_manager.get_state() in [STATE_ANALYZE, STATE_BROKEN]:
            self.m_printer(STR_SIGNAL_INTERCEPT % (event.m_signame, event.m_signum))


    def on_event_signal_exception(self, event):
        self.m_printer(STR_SIGNAL_EXCEPTION % (event.m_description, event.m_signame, event.m_signum))


    def on_event_embedded_sync(self, event):
        #
        # time.sleep() allows pending break requests to go through...
        #
        time.sleep(0.001)
        self.getSession().getProxy().embedded_sync()


    def on_event_exit(self, event):
        self.m_printer(STR_DEBUGGEE_TERMINATED)
        threading.Thread(target = self.detach_job).start()


    def restart_session_job(self, fSendExitOnFailure = False):
        try:
            self.getSession().restart(sleep = 3)
            return

        except:
            pass

        self.m_fStop = True

        if fSendExitOnFailure:
            e = CEventExit()
            self.m_event_dispatcher_proxy.fire_event(e)
            return

        self.m_printer(STR_LOST_CONNECTION)
        self.detach_job()


    def detach_job(self):
        try:
            self.detach()
        except:
            pass


    def detach(self):
        self.__verify_attached()

        try:
            self.save_breakpoints()
        except:
            print_debug_exception()
            pass

        self.m_printer(STR_ATTEMPTING_TO_DETACH)

        self.m_state_manager.set_state(STATE_DETACHING)

        self.__stop_event_monitor()

        try:
            #self.disable_breakpoint([], fAll = True)

            try:
                self.getSession().getProxy().set_trap_unhandled_exceptions(False)
                self.request_go(fdetach = True)

            except DebuggerNotBroken:
                pass

        finally:
            self.m_state_manager.set_state(STATE_DETACHED)
            self.m_session = None
            self.m_printer(STR_DETACH_SUCCEEDED)


    def __stop_event_monitor(self):
        self.m_fStop = True
        if self.m_worker_thread is not None:
            if thread.get_ident() != self.m_worker_thread_ident:
                try:
                    self.getSession().getProxy().null()
                except:
                    pass

                self.m_worker_thread.join()

            self.m_worker_thread = None
            self.m_worker_thread_ident = None


    def request_break(self):
        self.getSession().getProxy().request_break()


    def request_go(self, fdetach = False):
        self.getSession().getProxy().request_go(fdetach)


    def request_go_breakpoint(self, filename, scope, lineno):
        frame_index = self.get_frame_index()
        fAnalyzeMode = (self.m_state_manager.get_state() == STATE_ANALYZE)

        self.getSession().getProxy().request_go_breakpoint(filename, scope, lineno, frame_index, fAnalyzeMode)


    def request_step(self):
        self.getSession().getProxy().request_step()


    def request_next(self):
        self.getSession().getProxy().request_next()


    def request_return(self):
        self.getSession().getProxy().request_return()


    def request_jump(self, lineno):
        self.getSession().getProxy().request_jump(lineno)


    def set_breakpoint(self, filename, scope, lineno, fEnabled, expr, encoding = None):
        frame_index = self.get_frame_index()
        fAnalyzeMode = (self.m_state_manager.get_state() == STATE_ANALYZE)

        if encoding == None:
            encoding = self.m_encoding

        self.getSession().getProxy().set_breakpoint(filename, scope, lineno, fEnabled, expr, frame_index, fAnalyzeMode, encoding)


    def disable_breakpoint(self, id_list, fAll):
        self.getSession().getProxy().disable_breakpoint(id_list, fAll)


    def enable_breakpoint(self, id_list, fAll):
        self.getSession().getProxy().enable_breakpoint(id_list, fAll)


    def delete_breakpoint(self, id_list, fAll):
        self.getSession().getProxy().delete_breakpoint(id_list, fAll)


    def get_breakpoints(self):
        self.__verify_attached()

        bpl = self.m_breakpoints_proxy.get_breakpoints()
        return bpl


    def save_breakpoints(self, filename = ''):
        self.__verify_attached()

        module_name = self.getSession().getServerInfo().m_module_name
        if module_name[:1] == '<':
            return

        if sys.platform == 'OpenVMS':
            #
            # OpenVMS filesystem does not support byte stream.
            #
            mode = 'w'
        else:
            mode = 'wb'

        path = calc_bpl_filename(module_name + filename)
        file = open(path, mode)

        try:
            try:
                bpl = self.get_breakpoints()
                sbpl = pickle.dumps(bpl)
                file.write(sbpl)

            except:
                print_debug_exception()
                raise CException

        finally:
            file.close()


    def load_breakpoints(self, filename = ''):
        self.__verify_attached()

        module_name = self.getSession().getServerInfo().m_module_name
        if module_name[:1] == '<':
            return

        if sys.platform == 'OpenVMS':
            #
            # OpenVMS filesystem does not support byte stream.
            #
            mode = 'r'
        else:
            mode = 'rb'

        path = calc_bpl_filename(module_name + filename)
        file = open(path, mode)

        ferror = False

        try:
            try:
                bpl = pickle.load(file)
                self.delete_breakpoint([], True)

            except:
                print_debug_exception()
                raise CException

            #
            # No Breakpoints were found in file.
            #
            if filename == '' and len(bpl.values()) == 0:
                raise IOError

            for bp in bpl.values():
                try:
                    if bp.m_scope_fqn != None:
                        bp.m_scope_fqn = as_unicode(bp.m_scope_fqn)

                    if bp.m_filename != None:
                        bp.m_filename = as_unicode(bp.m_filename)

                    if bp.m_expr != None:
                        bp.m_expr = as_unicode(bp.m_expr)

                    if bp.m_expr in [None, '']:
                        bp.m_encoding = as_unicode('utf-8')

                    self.set_breakpoint(bp.m_filename, bp.m_scope_fqn, bp.m_scope_offset, bp.m_fEnabled, bp.m_expr, bp.m_encoding)
                except:
                    print_debug_exception()
                    ferror = True

            if ferror:
                raise CException

        finally:
            file.close()


    def on_event_synchronicity(self, event):
        ffire = self.m_fsynchronicity != event.m_fsynchronicity
        self.m_fsynchronicity = event.m_fsynchronicity

        if ffire:
            event = CEventSynchronicity(event.m_fsynchronicity)
            self.m_event_dispatcher.fire_event(event)


    def set_synchronicity(self, fsynchronicity):
        self.m_fsynchronicity = fsynchronicity

        if self.__is_attached():
            try:
                self.getSession().getProxy().set_synchronicity(fsynchronicity)
            except NotAttached:
                pass

        event = CEventSynchronicity(fsynchronicity)
        self.m_event_dispatcher.fire_event(event)

    def get_synchronicity(self):
        return self.m_fsynchronicity

    def on_event_breakonexit(self, event):
        ffire = self.m_breakonexit != event.m_fbreakonexit
        self.m_fbreakonexit = event.m_fbreakonexit

        if ffire:
            event = CEventBreakOnExit(event.m_fbreakonexit)
            self.m_event_dispatcher.fire_event(event)

    def set_breakonexit(self, fbreakonexit):
        self.m_breakonexit = fbreakonexit
        if self.__is_attached():
            try:
                self.getSession().getProxy().set_breakonexit(fbreakonexit)
            except NotAttached:
                pass

        event = CEventBreakOnExit(fbreakonexit)
        self.m_event_dispatcher.fire_event(event)

    def get_breakonexit(self):
        return self.m_breakonexit

    def on_event_trap(self, event):
        ffire = self.m_ftrap != event.m_ftrap
        self.m_ftrap = event.m_ftrap

        if ffire:
            event = CEventTrap(event.m_ftrap)
            self.m_event_dispatcher.fire_event(event)


    def set_trap_unhandled_exceptions(self, ftrap):
        self.m_ftrap = ftrap

        if self.__is_attached():
            try:
                self.getSession().getProxy().set_trap_unhandled_exceptions(self.m_ftrap)
            except NotAttached:
                pass

        event = CEventTrap(ftrap)
        self.m_event_dispatcher.fire_event(event)


    def get_trap_unhandled_exceptions(self):
        return self.m_ftrap


    def is_unhandled_exception(self):
        self.__verify_attached()

        return self.getSession().getProxy().is_unhandled_exception()


    def on_event_fork_mode(self, event):
        ffire = ((self.m_ffork_into_child , self.m_ffork_auto) !=
            (event.m_ffork_into_child, event.m_ffork_auto))

        self.m_ffork_into_child = event.m_ffork_into_child
        self.m_ffork_auto = event.m_ffork_auto

        if ffire:
            event = CEventForkMode(self.m_ffork_into_child, self.m_ffork_auto)
            self.m_event_dispatcher.fire_event(event)


    def set_fork_mode(self, ffork_into_child, ffork_auto):
        self.m_ffork_into_child = ffork_into_child
        self.m_ffork_auto = ffork_auto

        if self.__is_attached():
            try:
                self.getSession().getProxy().set_fork_mode(
                    self.m_ffork_into_child,
                    self.m_ffork_auto
                    )

            except NotAttached:
                pass

        event = CEventForkMode(ffork_into_child, ffork_auto)
        self.m_event_dispatcher.fire_event(event)


    def get_fork_mode(self):
        return (self.m_ffork_into_child, self.m_ffork_auto)


    def get_stack(self, tid_list, fAll):
        fAnalyzeMode = (self.m_state_manager.get_state() == STATE_ANALYZE)
        r = self.getSession().getProxy().get_stack(tid_list, fAll, fAnalyzeMode)
        return r


    def get_source_file(self, filename, lineno, nlines):
        assert(is_unicode(filename))

        frame_index = self.get_frame_index()
        fAnalyzeMode = (self.m_state_manager.get_state() == STATE_ANALYZE)

        r = self.getSession().getProxy().get_source_file(filename, lineno, nlines, frame_index, fAnalyzeMode)
        return r


    def get_source_lines(self, nlines, fAll):
        frame_index = self.get_frame_index()
        fAnalyzeMode = (self.m_state_manager.get_state() == STATE_ANALYZE)

        r = self.getSession().getProxy().get_source_lines(nlines, fAll, frame_index, fAnalyzeMode)
        return r


    def get_thread_list(self):
        (current_thread_id, thread_list) = self.getSession().getProxy().get_thread_list()
        return (current_thread_id, thread_list)


    def set_thread(self, tid):
        self.reset_frame_indexes(None)
        self.getSession().getProxy().set_thread(tid)


    def get_namespace(self, nl, filter_level, repr_limit):
        ''' See CSessionManager.get_namespace() for more details.
        Arguments:
        :param nl: list of (expr, boolean) with:
                    expr: expression to be computed
                    boolean: tells whether subnodes of the expression should be returned as well (class content,
                             list content, ...)
        :param filter_level: int, 0 1 or 2
        :param repr_limit: max length of the expression to return
        :return: a list of dictionnaries, where each item of the list represent an item in nl
        '''
        frame_index = self.get_frame_index()
        fAnalyzeMode = (self.m_state_manager.get_state() == STATE_ANALYZE)

        r = self.getSession().getProxy().get_namespace(nl, filter_level, frame_index, fAnalyzeMode, repr_limit, self.m_encoding, self.m_fraw)
        return r


    def evaluate(self, expr, fclear_completions = True):
        assert(is_unicode(expr))

        self.__verify_attached()
        self.__verify_broken()

        frame_index = self.get_frame_index()
        fAnalyzeMode = (self.m_state_manager.get_state() == STATE_ANALYZE)

        (value, warning, error) = self.getSession().getProxy().evaluate(expr, frame_index, fAnalyzeMode, self.m_encoding, self.m_fraw)

        if fclear_completions:
            self.m_completions.clear()

        return (value, warning, error)


    def execute(self, suite):
        assert(is_unicode(suite))

        self.__verify_attached()
        self.__verify_broken()

        frame_index = self.get_frame_index()
        fAnalyzeMode = (self.m_state_manager.get_state() == STATE_ANALYZE)

        (warning, error) = self.getSession().getProxy().execute(suite, frame_index, fAnalyzeMode, self.m_encoding)

        self.m_completions.clear()

        return (warning, error)


    def set_encoding(self, encoding, fraw):
        if (self.m_encoding, self.m_fraw) == (encoding, fraw):
            return

        self.m_encoding = encoding
        self.m_fraw = fraw

        event = CEventEncoding(encoding, fraw)
        self.m_event_dispatcher.fire_event(event)

        if self.__is_attached():
            self.refresh()


    def get_encoding(self):
        return (self.m_encoding, self.m_fraw)


    def set_host(self, host):
        self.__verify_unattached()

        try:
            if not is_unicode(host):
                host = host.decode('ascii')

            host.encode('ascii')

        except:
            raise BadArgument

        host = as_string(host, 'ascii')

        try:
            socket.getaddrinfo(host, 0, 0, socket.SOCK_STREAM)

        except socket.gaierror:
            if host.lower() != LOCALHOST:
                raise

            #
            # Work-around for gaierror: (-8, 'Servname not supported for ai_socktype')
            #
            return self.set_host(LOOPBACK)

        self.m_host = host
        self.m_server_list_object = CServerList(host)


    def get_host(self):
        return as_unicode(self.m_host)


    def calc_server_list(self):
        if self.m_rpdb2_pwd is None:
            raise UnsetPassword

        if g_fFirewallTest:
            firewall_test = CFirewallTest(self.get_remote())
            if not firewall_test.run():
                raise FirewallBlock
        else:
            print_debug('Skipping firewall test.')

        server_list = self.m_server_list_object.calcList(self.m_rpdb2_pwd, self.m_rid)
        errors = self.m_server_list_object.get_errors()
        self.__report_server_errors(errors)

        return (server_list, errors)


    def get_server_info(self):
        return self.getSession().getServerInfo()


    def complete_expression(self, expr):
        match = re.search(
                r'(?P<unsupported> \.)? (?P<match> ((?P<scope> (\w+\.)* \w+) \.)? (?P<complete>\w*) $)',
                expr,
                re.U | re.X
                )

        if match == None:
            raise BadArgument

        d = match.groupdict()

        unsupported, scope, complete = (d['unsupported'], d['scope'], d['complete'])

        if unsupported != None:
            raise BadArgument

        if scope == None:
            _scope = as_unicode('list(globals().keys()) + list(locals().keys()) + list(_RPDB2_builtins.keys())')
        else:
            _scope = as_unicode('dir(%s)' % scope)

        if not _scope in self.m_completions:
            (v, w, e) = self.evaluate(_scope, fclear_completions = False)
            if w != '' or e != '':
                print_debug('evaluate() returned the following warning/error: %s' % w + e)
                return (expr, [])

            cl = list(set(eval(v)))
            if '_RPDB2_builtins' in cl:
                cl.remove('_RPDB2_builtins')
            self.m_completions[_scope] = cl

        completions = [attr for attr in self.m_completions[_scope] if attr.startswith(complete)]
        completions.sort()

        if complete == '':
            prefix = expr
        else:
            prefix = expr[:-len(complete)]

        return (prefix, completions)



    def _reset_frame_indexes(self, event):
        self.reset_frame_indexes(None)


    def reset_frame_indexes(self, event):
        try:
            self.m_state_manager.acquire()
            if event is None:
                self.__verify_broken()
            elif self.m_state_manager.get_state() in [STATE_BROKEN, STATE_ANALYZE]:
                return

            self.m_stack_depth = None
            self.m_stack_depth_exception = None
            self.m_frame_index = 0
            self.m_frame_index_exception = 0

            self.m_completions.clear()

        finally:
            self.m_state_manager.release()


    def set_stack_depth(self, event):
        try:
            self.m_state_manager.acquire()
            self.__verify_broken()

            self.m_stack_depth = event.m_stack_depth
            self.m_stack_depth_exception = event.m_stack_depth_exception
            self.m_frame_index = min(self.m_frame_index, self.m_stack_depth - 1)
            self.m_frame_index_exception = min(self.m_frame_index_exception, self.m_stack_depth_exception - 1)

        finally:
            self.m_state_manager.release()


    def set_frame_index(self, frame_index):
        try:
            self.m_state_manager.acquire()
            self.__verify_broken()

            if (frame_index < 0) or (self.m_stack_depth is None):
                return self.get_frame_index(fLock = False)

            if self.m_state_manager.get_state() == STATE_ANALYZE:
                self.m_frame_index_exception = min(frame_index, self.m_stack_depth_exception - 1)
                si = self.m_frame_index_exception

            else:
                self.m_frame_index = min(frame_index, self.m_stack_depth - 1)
                si = self.m_frame_index

        finally:
            self.m_state_manager.release()

        event = CEventStackFrameChange(si)
        self.m_event_dispatcher.fire_event(event)

        event = CEventNamespace()
        self.m_event_dispatcher.fire_event(event)

        return si


    def get_frame_index(self, fLock = True):
        try:
            if fLock:
                self.m_state_manager.acquire()

            self.__verify_attached()

            if self.m_state_manager.get_state() == STATE_ANALYZE:
                return self.m_frame_index_exception
            else:
                return self.m_frame_index

        finally:
            if fLock:
                self.m_state_manager.release()


    def set_analyze(self, fAnalyze):
        try:
            self.m_state_manager.acquire()

            if fAnalyze and (self.m_state_manager.get_state() != STATE_BROKEN):
                raise DebuggerNotBroken

            if (not fAnalyze) and (self.m_state_manager.get_state() != STATE_ANALYZE):
                return

            state = [STATE_BROKEN, STATE_ANALYZE][fAnalyze]
            self.m_state_manager.set_state(state, fLock = False)

        finally:
            self.m_state_manager.release()

            self.refresh()


    def getSession(self):
        self.__verify_attached()

        return self.m_session


    def get_state(self):
        return as_unicode(self.m_state_manager.get_state())


    def set_password(self, _rpdb2_pwd):
        assert(is_unicode(_rpdb2_pwd))

        if not is_valid_pwd(_rpdb2_pwd):
            raise BadArgument

        try:
            self.m_state_manager.acquire()

            self.__verify_unattached()

            self.m_rpdb2_pwd = _rpdb2_pwd
        finally:
            self.m_state_manager.release()


    def set_random_password(self):
        try:
            self.m_state_manager.acquire()

            self.__verify_unattached()

            self.m_rpdb2_pwd = generate_random_password()
            self.m_printer(STR_RANDOM_PASSWORD)

        finally:
            self.m_state_manager.release()


    def get_password(self):
        return self.m_rpdb2_pwd


    def set_remote(self, fAllowRemote):
        try:
            self.m_state_manager.acquire()

            self.__verify_unattached()

            self.m_fAllowRemote = fAllowRemote
        finally:
            self.m_state_manager.release()


    def get_remote(self):
        return self.m_fAllowRemote


    def set_environ(self, envmap):
        self.m_environment = []

        try:
            for k, v in envmap:
                k = as_unicode(k, fstrict = True)
                v = as_unicode(v, fstrict = True)

                self.m_environment.append((k, v))

        except:
            raise BadArgument


    def get_environ(self):
        return self.m_environment


    def stop_debuggee(self):
        self.__verify_attached()

        try:
            self.save_breakpoints()
        except:
            print_debug_exception()
            pass

        self.m_printer(STR_ATTEMPTING_TO_STOP)
        self.m_printer(STR_ATTEMPTING_TO_DETACH)

        self.m_state_manager.set_state(STATE_DETACHING)

        self.__stop_event_monitor()

        try:
            self.getSession().getProxy().stop_debuggee()

        finally:
            self.m_state_manager.set_state(STATE_DETACHED)
            self.m_session = None
            self.m_printer(STR_DETACH_SUCCEEDED)


class CServerList:
    def __init__(self, host):
        self.m_host = host
        self.m_list = []
        self.m_errors = {}


    def calcList(self, _rpdb2_pwd, rid, key = None):
        sil = []
        sessions = []
        self.m_errors = {}

        port = SERVER_PORT_RANGE_START
        while port < SERVER_PORT_RANGE_START + SERVER_PORT_RANGE_LENGTH:
            s = CSession(self.m_host, port, _rpdb2_pwd, fAllowUnencrypted = True, rid = rid)
            t = s.ConnectAsync()
            sessions.append((s, t))
            port += 1

        for (s, t) in sessions:
            t.join()

            if (s.m_exc_info is not None):
                if not issubclass(s.m_exc_info[0], socket.error):
                    self.m_errors.setdefault(s.m_exc_info[0], []).append(s.m_exc_info)

                continue

            si = s.getServerInfo()
            if si is not None:
                sil.append((-si.m_age, si))

            sil.sort()
            self.m_list = [s[1] for s in sil]

            if key != None:
                try:
                    return self.findServers(key)[0]
                except:
                    pass

        if key != None:
            raise UnknownServer

        sil.sort()
        self.m_list = [s[1] for s in sil]

        return self.m_list


    def get_errors(self):
        return self.m_errors


    def findServers(self, key):
        try:
            n = int(key)
            _s = [s for s in self.m_list if (s.m_pid == n) or (s.m_rid == key)]

        except ValueError:
            key = as_string(key, sys.getfilesystemencoding())
            _s = [s for s in self.m_list if key in s.m_filename]

        if _s == []:
            raise UnknownServer

        return _s