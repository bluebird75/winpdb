"""
    const.py

    A remote Python debugger for CPython

    Copyright (C) 2013-2017 Philippe Fremy
    Copyright (C) 2005-2009 Nir Aides

    This program is free software; you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation; either version 2 of the License, or any later
    version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02111-1307 USA
"""


COPYRIGHT_NOTICE = """Copyright (C) 2013-2017 Philippe Fremy, 2005-2009 Nir Aides"""
CREDITS_NOTICE = """Work on version 1.4.8 was sponsored by Investortools, Inc."""
LICENSE_NOTICE = """
This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 2 of the License, or any later
version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

A copy of the GPL with the precise terms and conditions for
copying, distribution and modification follow:
"""
COPY_OF_THE_GPL_LICENSE = """
TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

0.
This License applies to any program or other work which contains a notice
placed by the copyright holder saying it may be distributed under the terms
of this General Public License. The "Program", below, refers to any such
program or work, and a "work based on the Program" means either the Program
or any derivative work under copyright law: that is to say, a work containing
the Program or a portion of it, either verbatim or with modifications and/or
translated into another language. (Hereinafter, translation is included
without limitation in the term "modification".) Each licensee is addressed
as "you".

Activities other than copying, distribution and modification are not covered
by this License; they are outside its scope. The act of running the Program
is not restricted, and the output from the Program is covered only if its
contents constitute a work based on the Program (independent of having been
made by running the Program). Whether that is true depends on what the
Program does.

1.
You may copy and distribute verbatim copies of the Program's source code as
you receive it, in any medium, provided that you conspicuously and
appropriately publish on each copy an appropriate copyright notice and
disclaimer of warranty; keep intact all the notices that refer to this
License and to the absence of any warranty; and give any other recipients of
the Program a copy of this License along with the Program.

You may charge a fee for the physical act of transferring a copy, and you
may at your option offer warranty protection in exchange for a fee.

2.
You may modify your copy or copies of the Program or any portion of it, thus
forming a work based on the Program, and copy and distribute such modifications
or work under the terms of Section 1 above, provided that you also meet all
of these conditions:

    a) You must cause the modified files to carry prominent notices stating
    that you changed the files and the date of any change.

    b) You must cause any work that you distribute or publish, that in whole
    or in part contains or is derived from the Program or any part thereof,
    to be licensed as a whole at no charge to all third parties under the
    terms of this License.

    c) If the modified program normally reads commands interactively when
    run, you must cause it, when started running for such interactive use in
    the most ordinary way, to print or display an announcement including an
    appropriate copyright notice and a notice that there is no warranty (or
    else, saying that you provide a warranty) and that users may redistribute
    the program under these conditions, and telling the user how to view a
    copy of this License. (Exception: if the Program itself is interactive
    but does not normally print such an announcement, your work based on the
    Program is not required to print an announcement.)

These requirements apply to the modified work as a whole. If identifiable
sections of that work are not derived from the Program, and can be reasonably
considered independent and separate works in themselves, then this License,
and its terms, do not apply to those sections when you distribute them as
separate works. But when you distribute the same sections as part of a whole
which is a work based on the Program, the distribution of the whole must be
on the terms of this License, whose permissions for other licensees extend to
the entire whole, and thus to each and every part regardless of who wrote it.

Thus, it is not the intent of this section to claim rights or contest your
rights to work written entirely by you; rather, the intent is to exercise the
right to control the distribution of derivative or collective works based on
the Program.

In addition, mere aggregation of another work not based on the Program with
the Program (or with a work based on the Program) on a volume of a storage or
distribution medium does not bring the other work under the scope of this
License.

3. You may copy and distribute the Program (or a work based on it, under
Section 2) in object code or executable form under the terms of Sections 1
and 2 above provided that you also do one of the following:

    a) Accompany it with the complete corresponding machine-readable source
    code, which must be distributed under the terms of Sections 1 and 2 above
    on a medium customarily used for software interchange; or,

    b) Accompany it with a written offer, valid for at least three years, to
    give any third party, for a charge no more than your cost of physically
    performing source distribution, a complete machine-readable copy of the
    corresponding source code, to be distributed under the terms of Sections
    1 and 2 above on a medium customarily used for software interchange; or,

    c) Accompany it with the information you received as to the offer to
    distribute corresponding source code. (This alternative is allowed only
    for noncommercial distribution and only if you received the program in
    object code or executable form with such an offer, in accord with
    Subsection b above.)

The source code for a work means the preferred form of the work for making
modifications to it. For an executable work, complete source code means all
the source code for all modules it contains, plus any associated interface
definition files, plus the scripts used to control compilation and
installation of the executable. However, as a special exception, the source
code distributed need not include anything that is normally distributed (in
either source or binary form) with the major components (compiler, kernel,
and so on) of the operating system on which the executable runs, unless that
component itself accompanies the executable.

If distribution of executable or object code is made by offering access to
copy from a designated place, then offering equivalent access to copy the
source code from the same place counts as distribution of the source code,
even though third parties are not compelled to copy the source along with
the object code.

4. You may not copy, modify, sublicense, or distribute the Program except as
expressly provided under this License. Any attempt otherwise to copy, modify,
sublicense or distribute the Program is void, and will automatically
terminate your rights under this License. However, parties who have received
copies, or rights, from you under this License will not have their licenses
terminated so long as such parties remain in full compliance.

5. You are not required to accept this License, since you have not signed it.
However, nothing else grants you permission to modify or distribute the
Program or its derivative works. These actions are prohibited by law if you
do not accept this License. Therefore, by modifying or distributing the
Program (or any work based on the Program), you indicate your acceptance of
this License to do so, and all its terms and conditions for copying,
distributing or modifying the Program or works based on it.

6. Each time you redistribute the Program (or any work based on the Program),
the recipient automatically receives a license from the original licensor to
copy, distribute or modify the Program subject to these terms and conditions.
You may not impose any further restrictions on the recipients' exercise of
the rights granted herein. You are not responsible for enforcing compliance
by third parties to this License.

7. If, as a consequence of a court judgment or allegation of patent
infringement or for any other reason (not limited to patent issues),
conditions are imposed on you (whether by court order, agreement or otherwise)
that contradict the conditions of this License, they do not excuse you from
the conditions of this License. If you cannot distribute so as to satisfy
simultaneously your obligations under this License and any other pertinent
obligations, then as a consequence you may not distribute the Program at all.
For example, if a patent license would not permit royalty-free redistribution
of the Program by all those who receive copies directly or indirectly through
you, then the only way you could satisfy both it and this License would be to
refrain entirely from distribution of the Program.

If any portion of this section is held invalid or unenforceable under any
particular circumstance, the balance of the section is intended to apply and
the section as a whole is intended to apply in other circumstances.

It is not the purpose of this section to induce you to infringe any patents
or other property right claims or to contest validity of any such claims;
this section has the sole purpose of protecting the integrity of the free
software distribution system, which is implemented by public license
practices. Many people have made generous contributions to the wide range of
software distributed through that system in reliance on consistent
application of that system; it is up to the author/donor to decide if he or
she is willing to distribute software through any other system and a licensee
cannot impose that choice.

This section is intended to make thoroughly clear what is believed to be a
consequence of the rest of this License.

8. If the distribution and/or use of the Program is restricted in certain
countries either by patents or by copyrighted interfaces, the original
copyright holder who places the Program under this License may add an
explicit geographical distribution limitation excluding those countries,
so that distribution is permitted only in or among countries not thus
excluded. In such case, this License incorporates the limitation as if
written in the body of this License.

9. The Free Software Foundation may publish revised and/or new versions of
the General Public License from time to time. Such new versions will be
similar in spirit to the present version, but may differ in detail to
address new problems or concerns.

Each version is given a distinguishing version number. If the Program
specifies a version number of this License which applies to it and
"any later version", you have the option of following the terms and
conditions either of that version or of any later version published by the
Free Software Foundation. If the Program does not specify a version number
of this License, you may choose any version ever published by the
Free Software Foundation.

10. If you wish to incorporate parts of the Program into other free programs
whose distribution conditions are different, write to the author to ask for
permission. For software which is copyrighted by the Free Software
Foundation, write to the Free Software Foundation; we sometimes make
exceptions for this. Our decision will be guided by the two goals of
preserving the free status of all derivatives of our free software and of
promoting the sharing and reuse of software generally.

NO WARRANTY

11. BECAUSE THE PROGRAM IS LICENSED FREE OF CHARGE, THERE IS NO WARRANTY FOR
THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE LAW. EXCEPT WHEN OTHERWISE
STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES PROVIDE THE
PROGRAM "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS FOR A PARTICULAR PURPOSE. THE ENTIRE RISK AS TO THE QUALITY AND
PERFORMANCE OF THE PROGRAM IS WITH YOU. SHOULD THE PROGRAM PROVE DEFECTIVE,
YOU ASSUME THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

12. IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MAY MODIFY AND/OR
REDISTRIBUTE THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES,
INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING
OUT OF THE USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO
LOSS OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR
THIRD PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER
PROGRAMS), EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE
POSSIBILITY OF SUCH DAMAGES.

END OF TERMS AND CONDITIONS
"""

import os.path

#############################################
#
#   General Constants controlling the program 
#
#############################################

TIMEOUT_FIVE_MINUTES = 5 * 60.0
VERSION = (1, 5, 0, 0, 'Tychod')
RPDB_TITLE = "RPDB 1.5.0 - Tychod"
RPDB_VERSION = "RPDB_1_5_0"
RPDB_COMPATIBILITY_VERSION = "RPDB_1_5_0"
PYTHON_TAB_WIDTH = 4
RPDB_SETTINGS_FOLDER = '.rpdb2_settings'
RPDB_PWD_FOLDER = os.path.join(RPDB_SETTINGS_FOLDER, 'passwords')
RPDB_BPL_FOLDER = os.path.join(RPDB_SETTINGS_FOLDER, 'breakpoints')
RPDB_BPL_FOLDER_NT = 'rpdb2_breakpoints'
MAX_BPL_FILES = 100
EMBEDDED_SYNC_THRESHOLD = 1.0
EMBEDDED_SYNC_TIMEOUT = 5.0
HEARTBEAT_TIMEOUT = 16
IDLE_MAX_RATE = 2.0
PING_TIMEOUT = 4.0
LOCAL_TIMEOUT = 1.0
COMMUNICATION_RETRIES = 5
WAIT_FOR_BREAK_TIMEOUT = 3.0
SHUTDOWN_TIMEOUT = 4.0
STARTUP_TIMEOUT = 3.0
STARTUP_RETRIES = 3
LOOPBACK = '127.0.0.1'
LOCALHOST = 'localhost'
SERVER_PORT_RANGE_START = 51000
SERVER_PORT_RANGE_LENGTH = 24

SOURCE_EVENT_CALL = 'C'
SOURCE_EVENT_LINE = 'L'
SOURCE_EVENT_RETURN = 'R'
SOURCE_EVENT_EXCEPTION = 'E'
SOURCE_STATE_UNBROKEN = '*'
SOURCE_BP_ENABLED = 'B'
SOURCE_BP_DISABLED = 'D'
SYMBOL_MARKER = '>'
SYMBOL_ALL = '*'
SOURCE_MORE = '+'
SOURCE_LESS = '-'
SOURCE_ENTIRE_FILE = '^'

CONSOLE_WRAP_INDEX = 78
PRINT_NOTICE_LINES_PER_SECTION = 20


#############################################
#
#   Messages to the user
#
#############################################

CONSOLE_PRINTER = '*** '
CONSOLE_PROMPT = '\n> '
CONSOLE_PROMPT_ANALYZE = '\nAnalayze> '
CONSOLE_INTRO = ("""RPDB2 - The Remote Python Debugger, version %s,
Copyright (C) 2005-2009 Nir Aides, 2013-2017 Philippe Fremy
Type "help", "copyright", "license", "credits" for more information.""" % (RPDB_VERSION))

PRINT_NOTICE_PROMPT = "Hit Return for more, or q (and Return) to quit:"

STR_BAD_PYTHON_VERSION = "Rpdb2/winpdb requires at least Python 3.2 to work. Exiting"
STR_NO_THREADS = "Operation failed since no traced threads were found."
STR_STARTUP_NOTICE = "Attaching to debuggee..."
STR_SPAWN_UNSUPPORTED = "The debugger does not know how to open a new console on this system. You can start the debuggee manually with the -d flag on a separate console and then use the 'attach' command to attach to it."
STR_SPAWN_UNSUPPORTED_SCREEN_SUFFIX =  """Alternatively, you can use the screen utility and invoke rpdb2 in screen mode with the -s command-line flag as follows:
screen rpdb2 -s some-script.py script-arg1 script-arg2..."""
STR_AUTOMATIC_LAUNCH_UNKNOWN = STR_SPAWN_UNSUPPORTED
STR_STARTUP_SPAWN_NOTICE = "Starting debuggee..."
STR_KILL_NOTICE = "Stopping debuggee..."
STR_STARTUP_FAILURE = "Debuggee failed to start in a timely manner."
STR_OUTPUT_WARNING = "Textual output will be done at the debuggee."
STR_OUTPUT_WARNING_ASYNC = "The operation will continue to run in the background."
STR_ANALYZE_GLOBALS_WARNING = "In analyze mode the globals and locals dictionaries are read only."
STR_BREAKPOINTS_LOADED = "Breakpoints were loaded."
STR_BREAKPOINTS_SAVED = "Breakpoints were saved."
STR_BREAKPOINTS_SAVE_PROBLEM = "A problem occurred while saving the breakpoints."
STR_BREAKPOINTS_LOAD_PROBLEM = "A problem occurred while loading the breakpoints."
STR_BREAKPOINTS_NOT_SAVED = "Breakpoints were not saved."
STR_BREAKPOINTS_NOT_LOADED = "Breakpoints were not loaded."
STR_BREAKPOINTS_FILE_NOT_FOUND = "Breakpoints file was not found."
STR_BREAKPOINTS_NOT_FOUND = "No Breakpoints were found."
STR_BAD_FILENAME = "Bad File Name."
STR_SOME_BREAKPOINTS_NOT_LOADED = "Some breakpoints were not loaded, because of an error."
STR_BAD_EXPRESSION = "Bad expression '%s'."
STR_FILE_NOT_FOUND = "File '%s' not found."
STR_DISPLAY_ERROR = """If the X server (Windowing system) is not started you need to use rpdb2 with the screen utility and invoke rpdb2 in screen mode with the -s command-line flag as follows:
screen rpdb2 -s some-script.py script-arg1 script-arg2..."""
STR_EXCEPTION_NOT_FOUND = "No exception was found."
STR_SCOPE_NOT_FOUND = "Scope '%s' not found."
STR_NO_SUCH_BREAKPOINT = "Breakpoint not found."
STR_THREAD_NOT_FOUND = "Thread was not found."
STR_NO_THREADS_FOUND = "No threads were found."
STR_THREAD_NOT_BROKEN = "Thread is running."
STR_THREAD_FOCUS_SET = "Focus was set to chosen thread."
STR_ILEGAL_ANALYZE_MODE_ARG = "Argument is not allowed in analyze mode. Type 'help analyze' for more info."
STR_ILEGAL_ANALYZE_MODE_CMD = "Command is not allowed in analyze mode. Type 'help analyze' for more info."
STR_ANALYZE_MODE_TOGGLE = "Analyze mode was set to: %s."
STR_BAD_ARGUMENT = "Bad Argument."
STR_BAD_SYNTAX = 'Unknown syntax: %s\nDid you forget to use the exec or eval console commands?'
STR_PSYCO_WARNING = "The psyco module was detected. The debugger is incompatible with the psyco module and will not function correctly as long as the psyco module is imported and used."
STR_CONFLICTING_MODULES = "The modules: %s, which are incompatible with the debugger were detected and can possibly cause the debugger to fail."
STR_SIGNAL_INTERCEPT = "The signal %s(%d) was intercepted inside debugger tracing logic. It will be held pending until the debugger continues. Any exceptions raised by the handler will be ignored!"
STR_SIGNAL_EXCEPTION = "Exception %s raised by handler of signal %s(%d) inside debugger tracing logic was ignored!"
STR_DEBUGGEE_TERMINATED = "Debuggee has terminated."
STR_DEBUGGEE_NOT_BROKEN = "Debuggee has to be waiting at break point to complete this command."
STR_DEBUGGER_HAS_BROKEN = "Debuggee is waiting at break point for further commands."
STR_ALREADY_ATTACHED = "Already attached. Detach from debuggee and try again."
STR_NOT_ATTACHED = "Not attached to any script. Attach to a script and try again."
STR_COMMUNICATION_FAILURE = "Failed to communicate with debugged script."
STR_ERROR_OTHER = "Command returned the following error:\n%(type)s, %(value)s.\nPlease check stderr for stack trace and report to support."
STR_BAD_MBCS_PATH = "The debugger can not launch the script since the path to the Python executable or the debugger scripts can not be encoded into the default system code page. Please check the settings of 'Language for non-Unicode programs' in the Advanced tab of the Windows Regional and Language Options dialog."
STR_LOST_CONNECTION = "Lost connection to debuggee."
STR_FIREWALL_BLOCK = "A firewall is blocking the local communication chanel (socket) that is required between the debugger and the debugged script. Please make sure that the firewall allows that communication."
STR_BAD_VERSION = "A debuggee was found with incompatible debugger version %(value)s."
STR_BAD_VERSION2 = "While attempting to find the specified debuggee at least one debuggee was found that uses incompatible version of RPDB2."
STR_UNEXPECTED_DATA = "Unexpected data received."
STR_ACCESS_DENIED = "While attempting to find debuggee, at least one debuggee denied connection because of mismatched passwords. Please verify your password."
STR_ACCESS_DENIED2 = "Communication is denied because of un-matching passwords."
STR_ENCRYPTION_EXPECTED = "While attempting to find debuggee, at least one debuggee denied connection since it accepts encrypted connections only."
STR_ENCRYPTION_EXPECTED2 = "Debuggee will only talk over an encrypted channel."
STR_DECRYPTION_FAILURE = "Bad packet was received by the debuggee."
STR_DEBUGGEE_NO_ENCRYPTION = "Debuggee does not support encrypted mode. Either install the python-crypto package on the debuggee machine or allow unencrypted connections."
STR_RANDOM_PASSWORD = "Password has been set to a random password."
STR_PASSWORD_INPUT = "Please type a password:"
STR_PASSWORD_CONFIRM = "Password has been set."
STR_PASSWORD_NOT_SUPPORTED = "The --pwd flag is only supported on NT systems."
STR_PASSWORD_MUST_BE_SET = "A password should be set to secure debugger client-server communication."
STR_BAD_DATA = "Bad data received from debuggee."
STR_BAD_FILE_DATA = "Bad data received from file."
STR_ATTACH_FAILED = "Failed to attach"
STR_ATTACH_FAILED_NAME = "Failed to attach to '%s'."
STR_ATTACH_CRYPTO_MODE = "Debug Channel is%s encrypted."
STR_ATTACH_CRYPTO_MODE_NOT = "NOT"
STR_ATTACH_SUCCEEDED = "Successfully attached to '%s'."
STR_ATTEMPTING_TO_STOP = "Requesting script to stop."
STR_ATTEMPTING_TO_DETACH = "Detaching from script..."
STR_DETACH_SUCCEEDED = "Detached from script."
STR_DEBUGGEE_UNKNOWN = "Failed to find script."
STR_MULTIPLE_DEBUGGEES = "WARNING: There is more than one debuggee '%s'."
MSG_ERROR_HOST_TEXT = """The debugger was not able to set the host to '%s'.
The following error was returned:
%s"""
STR_SOURCE_NOT_FOUND = "Failed to get source from debuggee."
STR_SCRIPTS_CONNECTING = "Connecting to '%s'..."
STR_SCRIPTS_NO_SCRIPTS = "No scripts to debug on '%s'"
STR_SCRIPTS_TO_DEBUG = """Scripts to debug on '%s':

   pid    name
--------------------------"""
STR_STACK_TRACE = """Stack trace for thread %d:

   Frame  File Name                     Line  Function
------------------------------------------------------------------------------"""
STR_SOURCE_LINES = """Source lines for thread %d from file '%s':
"""
STR_ACTIVE_THREADS = """List of active threads known to the debugger:

    No    Tid  Name             State
-----------------------------------------------"""
STR_BREAKPOINTS_LIST = """List of breakpoints:

 Id  State      Line  Filename-Scope-Condition-Encoding
------------------------------------------------------------------------------"""
STR_BREAKPOINTS_TEMPLATE = """ %2d  %-8s  %5d  %s
                      %s
                      %s
                      %s"""
STR_ENCRYPTION_SUPPORT_ERROR = "Encryption is not supported since the python-crypto package was not found. Either install the python-crypto package or allow unencrypted connections."
STR_PASSWORD_NOT_SET = 'Password is not set.'
STR_PASSWORD_SET = 'Password is set to: "%s"'
STR_PASSWORD_BAD = 'The password should begin with a letter and continue with any combination of digits, letters or underscores (\'_\'). Only English characters are accepted for letters.'
STR_ENCRYPT_MODE = 'Force encryption mode: %s'
STR_REMOTE_MODE = 'Allow remote machines mode: %s'
STR_ENCODING_MODE = 'Encoding is set to: %s'
STR_ENCODING_MODE_SET = 'Encoding was set to: %s'
STR_ENCODING_BAD = 'The specified encoding was not recognized by the debugger.'
STR_ENVIRONMENT = 'The current environment mapping is:'
STR_ENVIRONMENT_EMPTY = 'The current environment mapping is not set.'
STR_SYNCHRONICITY_BAD = "Can not process command when thread is running unless synchronicity mode is turned on. Type 'help synchro' at the command prompt for more information."
STR_SYNCHRONICITY_MODE = 'The synchronicity mode is set to: %s'
STR_BREAKONEXIT_MODE = 'The break-on-exit mode is set to: %s'
STR_TRAP_MODE = 'Trap unhandled exceptions mode is set to: %s'
STR_TRAP_MODE_SET = "Trap unhandled exceptions mode was set to: %s."
STR_FORK_MODE = "Fork mode is set to: %s, %s."
STR_FORK_MODE_SET = "Fork mode was set to: %s, %s."
STR_LOCAL_NAMESPACE_WARNING = 'Debugger modifications to the original bindings of the local namespace of this frame will be committed before the execution of the next statement of the frame. Any code using these variables executed before that point will see the original values.'
STR_WARNING = 'Warning: %s'
STR_MAX_NAMESPACE_WARNING_TITLE = 'Namespace Warning'
STR_MAX_NAMESPACE_WARNING_TYPE = '*** WARNING ***'
STR_MAX_NAMESPACE_WARNING_MSG = 'Number of items exceeds capacity of namespace browser.'
STR_MAX_EVALUATE_LENGTH_WARNING = 'Output length exeeds maximum capacity.'


# TODO: use variable directly
def get_version():
    return RPDB_VERSION

# TODO: use variable directly
def get_interface_compatibility_version():
    return RPDB_COMPATIBILITY_VERSION


NT_DEBUG = 'nt_debug'
SCREEN = 'screen'
MAC = 'mac'
DARWIN = 'darwin'
POSIX = 'posix'
STR_STATE_BROKEN = 'waiting at break point'
STATE_BROKEN = 'broken'
STATE_RUNNING = 'running'
STATE_ANALYZE = 'analyze'
STATE_DETACHED = 'detached'
STATE_DETACHING = 'detaching'
STATE_SPAWNING = 'spawning'
STATE_ATTACHING = 'attaching'
DEBUGGER_FILENAME = 'rpdb2.py'
THREADING_FILENAME = 'threading.py'
DEFAULT_NUMBER_OF_LINES = 20
DICT_KEY_TID = 'tid'
DICT_KEY_STACK = 'stack'
DICT_KEY_CODE_LIST = 'code_list'
DICT_KEY_CURRENT_TID = 'current tid'
DICT_KEY_BROKEN = 'broken'
DICT_KEY_BREAKPOINTS = 'breakpoints'
DICT_KEY_LINES = 'lines'
DICT_KEY_FILENAME = 'filename'
DICT_KEY_FIRST_LINENO = 'first_lineno'
DICT_KEY_FRAME_LINENO = 'frame_lineno'
DICT_KEY_EVENT = 'event'
DICT_KEY_EXPR = 'expr'
DICT_KEY_NAME = 'name'
DICT_KEY_REPR = 'repr'
DICT_KEY_IS_VALID = 'fvalid'
DICT_KEY_TYPE = 'type'
DICT_KEY_SUBNODES = 'subnodes'
DICT_KEY_N_SUBNODES = 'n_subnodes'
DICT_KEY_ERROR = 'error'
BREAKPOINTS_FILE_EXT = '.bpl'
PYTHON_FILE_EXTENSION = '.py'
PYTHONW_FILE_EXTENSION = '.pyw'
PYTHONW_SO_EXTENSION = '.so'
PYTHON_EXT_LIST = ['.py', '.pyw', '.pyc', '.pyd', '.pyo', '.so']