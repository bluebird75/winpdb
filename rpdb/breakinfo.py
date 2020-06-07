import copy

from rpdb.source_provider import MODULE_SCOPE, MODULE_SCOPE2, get_source, SCOPE_SEP
from rpdb.utils import as_string, as_unicode, print_debug
from rpdb.exceptions import InvalidScopeName

def myord(c):
    try:
        return ord(c)
    except:
        return c



class CScopeBreakInfo:
    def __init__(self, fqn, valid_lines):
        self.m_fqn = fqn
        self.m_first_line = valid_lines[0]
        self.m_last_line = valid_lines[-1]
        self.m_valid_lines = valid_lines


    def CalcScopeLine(self, lineno):
        rvl = copy.copy(self.m_valid_lines)
        rvl.reverse()

        for l in rvl:
            if lineno >= l:
                break

        return l


    def __str__(self):
        return "('" + self.m_fqn + "', " + str(self.m_valid_lines) + ')'


class CFileBreakInfo:
    """
    Break info structure for a source file.
    """

    def __init__(self, filename):
        self.m_filename = filename
        self.m_first_line = 0
        self.m_last_line = 0
        self.m_scope_break_info = []


    def CalcBreakInfo(self):
        (source, encoding) = get_source(self.m_filename)
        _source = as_string(source + as_unicode('\n'), encoding)

        code = compile(_source, self.m_filename, "exec")

        self.m_scope_break_info = []
        self.m_first_line = code.co_firstlineno
        self.m_last_line = 0

        fqn = []
        t = [code]

        while len(t) > 0:
            c = t.pop(0)

            if type(c) == tuple:
                self.m_scope_break_info.append(CScopeBreakInfo(*c))
                fqn.pop()
                continue

            fqn = fqn + [c.co_name]
            valid_lines = CalcValidLines(c)
            self.m_last_line = max(self.m_last_line, valid_lines[-1])
            _fqn = as_unicode('.'.join(fqn), encoding)
            si = (_fqn, valid_lines)
            subcodeslist = self.__CalcSubCodesList(c)
            t = subcodeslist + [si] + t


    def __CalcSubCodesList(self, code):
        tc = type(code)
        t = [(c.co_firstlineno, c) for c in code.co_consts if type(c) == tc]
        t.sort()
        scl = [c[1] for c in t]
        return scl


    def FindScopeByLineno(self, lineno):
        lineno = max(min(lineno, self.m_last_line), self.m_first_line)

        smaller_element = None
        exact_element = None

        for sbi in self.m_scope_break_info:
            if lineno > sbi.m_last_line:
                if (smaller_element is None) or (sbi.m_last_line >= smaller_element.m_last_line):
                    smaller_element = sbi
                continue

            if (lineno >= sbi.m_first_line) and (lineno <= sbi.m_last_line):
                exact_element = sbi
                break

        assert(exact_element is not None)

        scope = exact_element
        l = exact_element.CalcScopeLine(lineno)

        if (smaller_element is not None) and (l <= smaller_element.m_last_line):
            scope = smaller_element
            l = smaller_element.CalcScopeLine(lineno)

        return (scope, l)


    def FindScopeByName(self, name, offset):
        if name.startswith(MODULE_SCOPE):
            alt_scope = MODULE_SCOPE2 + name[len(MODULE_SCOPE):]
        elif name.startswith(MODULE_SCOPE2):
            alt_scope = MODULE_SCOPE + name[len(MODULE_SCOPE2):]
        else:
            return self.FindScopeByName(MODULE_SCOPE2 + SCOPE_SEP + name, offset)

        for sbi in self.m_scope_break_info:
            if sbi.m_fqn in [name, alt_scope]:
                l = sbi.CalcScopeLine(sbi.m_first_line + offset)
                return (sbi, l)

        print_debug('Invalid scope: %s' % repr(name))

        raise InvalidScopeName


class CBreakInfoManager:
    """
    Manage break info dictionary per filename.
    """

    def __init__(self):
        self.m_file_info_dic = {}


    def addFile(self, filename):
        mbi = CFileBreakInfo(filename)
        mbi.CalcBreakInfo()
        self.m_file_info_dic[filename] = mbi


    def getFile(self, filename):
        if not filename in self.m_file_info_dic:
            self.addFile(filename)

        return self.m_file_info_dic[filename]


def CalcValidLines(code):
    l = code.co_firstlineno
    vl = [l]

    bl = [myord(c) for c in code.co_lnotab[2::2]]
    sl = [myord(c) for c in code.co_lnotab[1::2]]

    for (bi, si) in zip(bl, sl):
        l += si

        if bi == 0:
            continue

        if l != vl[-1]:
            vl.append(l)

    if len(sl) > 0:
        l += sl[-1]

        if l != vl[-1]:
            vl.append(l)

    return vl