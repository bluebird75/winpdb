import sys
import threading

from typing import Dict, List

#
# In debug mode errors and tracebacks are printed to stdout
# and frames of rpdb2 are visible to the user in the debugger
#
g_fDebug = False

#
# Lock for the traceback module to prevent it from interleaving
# output from different threads.
#
g_traceback_lock = threading.RLock()
g_builtins_module = sys.modules.get('__builtin__', sys.modules.get('builtins'))
g_initial_cwd = []  # type: List[str]
g_fScreen = False
g_fDefaultStd = True
g_server_lock = threading.RLock()
g_server = None
g_ignore_broken_pipe = 0

#
# Unicode version of path names that do not encode well witn the windows
# 'mbcs' encoding. This dict is used to work with such path names on
# windows.
#
g_found_unicode_files = {}  # type: Dict[str, str]