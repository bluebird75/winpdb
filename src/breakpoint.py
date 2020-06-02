import copyreg as copy_reg
import threading

from src.events import CEventBreakpoint
from src.utils import as_bytes, as_unicode, print_debug, winlower
from src.source_provider import  ENCODING_SOURCE, MODULE_SCOPE, MODULE_SCOPE2, SCOPE_SEP
from src.breakinfo import CBreakInfoManager



class CBreakPoint(object):
    def __init__(self, filename, scope_fqn, scope_first_line, lineno, fEnabled, expr, encoding, fTemporary = False):
        """
        Breakpoint constructor.

        scope_fqn - scope fully qualified name. e.g: module.class.method
        """

        self.m_id = None
        self.m_fEnabled = fEnabled
        self.m_filename = filename
        self.m_scope_fqn = scope_fqn
        self.m_scope_name = scope_fqn.split(SCOPE_SEP)[-1]
        self.m_scope_first_line = scope_first_line
        self.m_scope_offset = lineno - scope_first_line
        self.m_lineno = lineno
        self.m_expr = expr
        self.m_encoding = encoding
        self.m_code = None
        self.m_fTemporary = fTemporary

        if (expr is not None) and (expr != ''):
            _expr = as_bytes(ENCODING_SOURCE % encoding + expr, encoding)
            print_debug('Breakpoint expression: %s' % repr(_expr))
            self.m_code = compile(_expr, '<string>', 'eval')


    def __reduce__(self):
        rv = (copy_reg.__newobj__, (type(self), ), vars(self), None, None)
        return rv


    def calc_enclosing_scope_name(self):
        if self.m_scope_offset != 0:
            return None

        if self.m_scope_fqn in [MODULE_SCOPE, MODULE_SCOPE2]:
            return None

        scope_name_list = self.m_scope_fqn.split(SCOPE_SEP)
        enclosing_scope_name = scope_name_list[-2]

        return enclosing_scope_name


    def enable(self):
        self.m_fEnabled = True


    def disable(self):
        self.m_fEnabled = False


    def isEnabled(self):
        return self.m_fEnabled


    def __str__(self):
        return "('" + self.m_filename + "', '" + self.m_scope_fqn + "', " + str(self.m_scope_first_line) + ', ' + str(self.m_scope_offset) + ', ' + str(self.m_lineno) + ')'


class CBreakPointsManagerProxy:
    """
    A proxy for the breakpoint manager.
    While the breakpoint manager resides on the debuggee (the server),
    the proxy resides in the debugger (the client - session manager)
    """

    def __init__(self, session_manager):
        self.m_session_manager = session_manager

        self.m_break_points_by_file = {}
        self.m_break_points_by_id = {}

        self.m_lock = threading.Lock()

        #
        # The breakpoint proxy inserts itself between the two chained
        # event dispatchers in the session manager.
        #

        event_type_dict = {CEventBreakpoint: {}}

        self.m_session_manager.m_event_dispatcher_proxy.register_callback(self.update_bp, event_type_dict, fSingleUse = False)
        self.m_session_manager.m_event_dispatcher.register_chain_override(event_type_dict)


    def update_bp(self, event):
        """
        Handle breakpoint updates that arrive via the event dispatcher.
        """

        try:
            self.m_lock.acquire()

            if event.m_fAll:
                id_list = list(self.m_break_points_by_id.keys())
            else:
                id_list = event.m_id_list

            if event.m_action == CEventBreakpoint.REMOVE:
                for id in id_list:
                    try:
                        bp = self.m_break_points_by_id.pop(id)
                        bpm = self.m_break_points_by_file[bp.m_filename]
                        del bpm[bp.m_lineno]
                        if len(bpm) == 0:
                            del self.m_break_points_by_file[bp.m_filename]
                    except KeyError:
                        pass
                return

            if event.m_action == CEventBreakpoint.DISABLE:
                for id in id_list:
                    try:
                        bp = self.m_break_points_by_id[id]
                        bp.disable()
                    except KeyError:
                        pass
                return

            if event.m_action == CEventBreakpoint.ENABLE:
                for id in id_list:
                    try:
                        bp = self.m_break_points_by_id[id]
                        bp.enable()
                    except KeyError:
                        pass
                return

            bpm = self.m_break_points_by_file.get(event.m_bp.m_filename, {})
            bpm[event.m_bp.m_lineno] = event.m_bp

            self.m_break_points_by_id[event.m_bp.m_id] = event.m_bp

        finally:
            self.m_lock.release()

            self.m_session_manager.m_event_dispatcher.fire_event(event)


    def sync(self):
        try:
            self.m_lock.acquire()

            self.m_break_points_by_file = {}
            self.m_break_points_by_id = {}

        finally:
            self.m_lock.release()

        break_points_by_id = self.m_session_manager.getSession().getProxy().get_breakpoints()

        try:
            self.m_lock.acquire()

            self.m_break_points_by_id.update(break_points_by_id)

            for bp in list(self.m_break_points_by_id.values()):
                bpm = self.m_break_points_by_file.get(bp.m_filename, {})
                bpm[bp.m_lineno] = bp

        finally:
            self.m_lock.release()


    def clear(self):
        try:
            self.m_lock.acquire()

            self.m_break_points_by_file = {}
            self.m_break_points_by_id = {}

        finally:
            self.m_lock.release()


    def get_breakpoints(self):
        return self.m_break_points_by_id


    def get_breakpoint(self, filename, lineno):
        bpm = self.m_break_points_by_file[filename]
        bp = bpm[lineno]
        return bp


class CBreakPointsManager:
    def __init__(self):
        self.m_break_info_manager = CBreakInfoManager()
        self.m_active_break_points_by_file = {}
        self.m_break_points_by_function = {}
        self.m_break_points_by_file = {}
        self.m_break_points_by_id = {}
        self.m_lock = threading.Lock()

        self.m_temp_bp = None
        self.m_fhard_tbp = False


    def get_active_break_points_by_file(self, filename):
        """
        Get active breakpoints for file.
        """

        _filename = winlower(filename)

        return self.m_active_break_points_by_file.setdefault(_filename, {})


    def __calc_active_break_points_by_file(self, filename):
        bpmpt = self.m_active_break_points_by_file.setdefault(filename, {})
        bpmpt.clear()

        bpm = self.m_break_points_by_file.get(filename, {})
        for bp in list(bpm.values()):
            if bp.m_fEnabled:
                bpmpt[bp.m_lineno] = bp

        tbp = self.m_temp_bp
        if (tbp is not None) and (tbp.m_filename == filename):
            bpmpt[tbp.m_lineno] = tbp


    def __remove_from_function_list(self, bp):
        function_name = bp.m_scope_name

        try:
            bpf = self.m_break_points_by_function[function_name]
            del bpf[bp]
            if len(bpf) == 0:
                del self.m_break_points_by_function[function_name]
        except KeyError:
            pass

        #
        # In some cases a breakpoint belongs to two scopes at the
        # same time. For example a breakpoint on the declaration line
        # of a function.
        #

        _function_name = bp.calc_enclosing_scope_name()
        if _function_name is None:
            return

        try:
            _bpf = self.m_break_points_by_function[_function_name]
            del _bpf[bp]
            if len(_bpf) == 0:
                del self.m_break_points_by_function[_function_name]
        except KeyError:
            pass


    def __add_to_function_list(self, bp):
        function_name = bp.m_scope_name

        bpf = self.m_break_points_by_function.setdefault(function_name, {})
        bpf[bp] = True

        #
        # In some cases a breakpoint belongs to two scopes at the
        # same time. For example a breakpoint on the declaration line
        # of a function.
        #

        _function_name = bp.calc_enclosing_scope_name()
        if _function_name is None:
            return

        _bpf = self.m_break_points_by_function.setdefault(_function_name, {})
        _bpf[bp] = True


    def get_breakpoint(self, filename, lineno):
        """
        Get breakpoint by file and line number.
        """

        bpm = self.m_break_points_by_file[filename]
        bp = bpm[lineno]
        return bp


    def del_temp_breakpoint(self, fLock = True, breakpoint = None):
        """
        Delete a temoporary breakpoint.
        A temporary breakpoint is used when the debugger is asked to
        run-to a particular line.
        Hard temporary breakpoints are deleted only when actually hit.
        """
        if self.m_temp_bp is None:
            return

        try:
            if fLock:
                self.m_lock.acquire()

            if self.m_temp_bp is None:
                return

            if self.m_fhard_tbp and not breakpoint is self.m_temp_bp:
                return

            bp = self.m_temp_bp
            self.m_temp_bp = None
            self.m_fhard_tbp = False

            self.__remove_from_function_list(bp)
            self.__calc_active_break_points_by_file(bp.m_filename)

        finally:
            if fLock:
                self.m_lock.release()


    def set_temp_breakpoint(self, filename, scope, lineno, fhard = False):
        """
        Set a temoporary breakpoint.
        A temporary breakpoint is used when the debugger is asked to
        run-to a particular line.
        Hard temporary breakpoints are deleted only when actually hit.
        """

        _filename = winlower(filename)

        mbi = self.m_break_info_manager.getFile(_filename)

        if scope != '':
            (s, l) = mbi.FindScopeByName(scope, lineno)
        else:
            (s, l) = mbi.FindScopeByLineno(lineno)

        bp = CBreakPoint(_filename, s.m_fqn, s.m_first_line, l, fEnabled = True, expr = as_unicode(''), encoding = as_unicode('utf-8'), fTemporary = True)

        try:
            self.m_lock.acquire()

            self.m_fhard_tbp = False
            self.del_temp_breakpoint(fLock = False)
            self.m_fhard_tbp = fhard
            self.m_temp_bp = bp

            self.__add_to_function_list(bp)
            self.__calc_active_break_points_by_file(bp.m_filename)

        finally:
            self.m_lock.release()


    def set_breakpoint(self, filename, scope, lineno, fEnabled, expr, encoding):
        """
        Set breakpoint.

        scope - a string (possibly empty) with the dotted scope of the
                breakpoint. eg. 'my_module.my_class.foo'

        expr - a string (possibly empty) with a python expression
               that will be evaluated at the scope of the breakpoint.
               The breakpoint will be hit if the expression evaluates
               to True.
        """

        _filename = winlower(filename)

        mbi = self.m_break_info_manager.getFile(_filename)

        if scope != '':
            (s, l) = mbi.FindScopeByName(scope, lineno)
        else:
            (s, l) = mbi.FindScopeByLineno(lineno)

        bp = CBreakPoint(_filename, s.m_fqn, s.m_first_line, l, fEnabled, expr, encoding)

        try:
            self.m_lock.acquire()

            bpm = self.m_break_points_by_file.setdefault(_filename, {})

            #
            # If a breakpoint on the same line is found we use its ID.
            # Since the debugger lists breakpoints by IDs, this has
            # a similar effect to modifying the breakpoint.
            #

            try:
                old_bp = bpm[l]
                id = old_bp.m_id
                self.__remove_from_function_list(old_bp)
            except KeyError:
                #
                # Find the smallest available ID.
                #

                bpids = list(self.m_break_points_by_id.keys())
                bpids.sort()

                id = 0
                while id < len(bpids):
                    if bpids[id] != id:
                        break
                    id += 1

            bp.m_id = id

            self.m_break_points_by_id[id] = bp
            bpm[l] = bp
            if fEnabled:
                self.__add_to_function_list(bp)

            self.__calc_active_break_points_by_file(bp.m_filename)

            return bp

        finally:
            self.m_lock.release()


    def disable_breakpoint(self, id_list, fAll):
        """
        Disable breakpoint.
        """

        try:
            self.m_lock.acquire()

            if fAll:
                id_list = list(self.m_break_points_by_id.keys())

            for id in id_list:
                try:
                    bp = self.m_break_points_by_id[id]
                except KeyError:
                    continue

                bp.disable()
                self.__remove_from_function_list(bp)
                self.__calc_active_break_points_by_file(bp.m_filename)

        finally:
            self.m_lock.release()


    def enable_breakpoint(self, id_list, fAll):
        """
        Enable breakpoint.
        """

        try:
            self.m_lock.acquire()

            if fAll:
                id_list = list(self.m_break_points_by_id.keys())

            for id in id_list:
                try:
                    bp = self.m_break_points_by_id[id]
                except KeyError:
                    continue

                bp.enable()
                self.__add_to_function_list(bp)
                self.__calc_active_break_points_by_file(bp.m_filename)

        finally:
            self.m_lock.release()


    def delete_breakpoint(self, id_list, fAll):
        """
        Delete breakpoint.
        """

        try:
            self.m_lock.acquire()

            if fAll:
                id_list = list(self.m_break_points_by_id.keys())

            for id in id_list:
                try:
                    bp = self.m_break_points_by_id[id]
                except KeyError:
                    continue

                filename = bp.m_filename
                lineno = bp.m_lineno

                bpm = self.m_break_points_by_file[filename]
                if bp == bpm[lineno]:
                    del bpm[lineno]

                if len(bpm) == 0:
                    del self.m_break_points_by_file[filename]

                self.__remove_from_function_list(bp)
                self.__calc_active_break_points_by_file(bp.m_filename)

                del self.m_break_points_by_id[id]

        finally:
            self.m_lock.release()


    def get_breakpoints(self):
        return self.m_break_points_by_id