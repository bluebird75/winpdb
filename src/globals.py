import sys
import threading

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