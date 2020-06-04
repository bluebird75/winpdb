from src.globals import g_builtins_module


class _stub_type:
    pass

class sets:
    Set = _stub_type
    BaseSet = _stub_type
    ImmutableSet = _stub_type

unicode = _stub_type
str8 = _stub_type



def _rpdb2_bytes(s, e):
    return s.encode(e)



if not hasattr(g_builtins_module, 'unicode'):
    pass

if not hasattr(g_builtins_module, 'str8'):
    #
    # Pickle on Python 2.5 should know how to handle byte strings
    # that arrive from Python 3.0 over sockets.
    #
    # g_builtins_module.bytes = _rpdb2_bytes
    pass

