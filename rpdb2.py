#! /usr/bin/env python

"""
    rpdb2.py - version 2.2.3

    A remote Python debugger for CPython

    Copyright (C) 2005-2007 Nir Aides

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

COPYRIGHT_NOTICE = """Copyright (C) 2005-2007 Nir Aides"""

CREDITS_NOTICE = """Jurjen N.E. Bos - Compatibility with OS X."""

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



if '.' in __name__:
    raise ImportError('rpdb2 must not be imported as part of a package!')


    
import SimpleXMLRPCServer 
import SocketServer
import xmlrpclib
import threading
import linecache
import traceback
import commands
import tempfile
import __main__
import compiler
import weakref
import httplib
import os.path
import pickle
import socket
import getopt
import string
import thread
import random
import base64
import atexit
import locale
import errno
import time
import copy
import hmac
import stat
import sets
import sys
import cmd
import md5
import imp
import os

try:
    from Crypto.Cipher import DES
except ImportError:
    pass

#
# Pre-Import needed by my_abspath1 
#
try:
    from nt import _getfullpathname
except ImportError:
    pass



#
#-------------------------------- Design Notes -------------------------------
#

"""
  Design:
  
    RPDB2 divides the world into two main parts: debugger and debuggee.
    The debuggee is the script that needs to be debugged.
    The debugger is another script that attaches to the debuggee for the 
    purpose of debugging.

    Thus RPDB2 includes two main components: The debuggee-server that runs 
    in the debuggee and the session-manager that runs in the debugger.
    
    The session manager and the debuggee-server communicate via XML-RPC.

    The main classes are: CSessionManager and CDebuggeeServer
"""



#
#--------------------------------- Export functions ------------------------
#



TIMEOUT_FIVE_MINUTES = 5 * 60.0



def start_embedded_debugger(
            _rpdb2_pwd, 
            fAllowUnencrypted = True, 
            fAllowRemote = False, 
            timeout = TIMEOUT_FIVE_MINUTES, 
            fDebug = False
            ):

    """
    Use 'start_embedded_debugger' to invoke the debugger engine in embedded 
    scripts. put the following line as the first line in your script:

    import rpdb2; rpdb2.start_embedded_debugger(<some-password-string>)

    This will cause the script to freeze until a debugger console attaches.

    _rpdb2_pwd - The password that governs security of client/server communication
    fAllowUnencrypted - Allow unencrypted communications. Communication will
                        be authenticated but encrypted only if possible.
    fAllowRemote - Allow debugger consoles from remote machines to connect.
    timeout - Seconds to wait for attachment before giving up. If None, 
              never give up. Once the timeout period expires, the debuggee will
              resume execution.
    fDebug  - debug output.

    IMPORTNAT SECURITY NOTE:
    USING A HARDCODED PASSWORD MAY BE UNSECURE SINCE ANYONE WITH READ
    PERMISSION TO THE SCRIPT WILL BE ABLE TO READ THE PASSWORD AND CONNECT TO 
    THE DEBUGGER AND DO WHATEVER THEY WISH VIA THE 'EXEC' DEBUGGER COMMAND.

    It is safer to use: start_embedded_debugger_interactive_password()    
    """

    return __start_embedded_debugger(
                        _rpdb2_pwd, 
                        fAllowUnencrypted, 
                        fAllowRemote, 
                        timeout, 
                        fDebug
                        )
    


def start_embedded_debugger_interactive_password(
                fAllowUnencrypted = True, 
                fAllowRemote = False, 
                timeout = TIMEOUT_FIVE_MINUTES, 
                fDebug = False, 
                stdin = sys.stdin, 
                stdout = sys.stdout
                ):
                
    if g_server is not None:
        return

    if stdout is not None:
        stdout.write('Please type password:')
        
    _rpdb2_pwd = stdin.readline().rstrip('\n')
    
    return __start_embedded_debugger(
                        _rpdb2_pwd, 
                        fAllowUnencrypted, 
                        fAllowRemote, 
                        timeout, 
                        fDebug
                        )
    


def settrace():
    """
    Trace threads that were created with thread.start_new_thread()
    To trace, call this function from the thread target function.
    
    NOTE: The main thread and any threads created with the threading module 
    are automatically traced, and there is no need to invoke this function 
    for them. 

    Note: This call does not pause the script.
    """

    return __settrace()



def setbreak():
    """
    Pause the script for inspection at next script statement.
    """

    return __setbreak()

    
    
#
#----------------------------------- Interfaces ------------------------------
#



VERSION = (2, 2, 3, 0, '')
RPDB_VERSION = "RPDB_2_2_3"
RPDB_COMPATIBILITY_VERSION = "RPDB_2_2_3"



def get_version():
    return RPDB_VERSION


    
def get_interface_compatibility_version():
    return RPDB_COMPATIBILITY_VERSION

    

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
                            host = LOCALHOST
                            )

        self.m_fRunning = False
        self.m_termination_lineno = None
        
        event_type_dict = {CEventUnhandledException: {}}
        self.__sm.register_callback(self.__unhandled_exception, event_type_dict, fSingleUse = False)

        event_type_dict = {CEventState: {}}
        self.__sm.register_callback(self.__state_calback, event_type_dict, fSingleUse = False)

        event_type_dict = {CEventExit: {}}
        self.__sm.register_callback(self.__termination_callback, event_type_dict, fSingleUse = False)


    def launch(self, fchdir, command_line):
        self.m_fRunning = False
        self.m_termination_lineno = None
        self.__sm.launch(fchdir, command_line, fload_breakpoints = False)


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
        print 'unhandled_exception_callback'
        self.request_go()


    def script_paused(self):
        print 'script_paused'
        self.request_go()


    def script_terminated_callback(self):
        print 'script_terminated_callback'


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
            self.m_fRunning = True
            self.request_go()
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

        

class CSessionManager:
    """
    Interface to the session manager.
    This is the interface through which the debugger controls and 
    communicates with the debuggee.

    You can study the way it is used in StartClient()
    """
    
    def __init__(self, _rpdb2_pwd, fAllowUnencrypted, fAllowRemote, host):
        self.__smi = CSessionManagerInternal(
                            _rpdb2_pwd, 
                            fAllowUnencrypted, 
                            fAllowRemote, 
                            host
                            )


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


    def launch(self, fchdir, command_line):
        """
        Launch debuggee in a new process and attach.
        fchdir - Change current directory to that of the debuggee.
        command_line - command line arguments pass to the script as a string.
        """
        
        return self.__smi.launch(fchdir, command_line)

        
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

        
    def attach(self, key, name = None):
        """
        Attach to a debuggee (establish communication with the debuggee-server)
        key - a string specifying part of the filename or PID of the debuggee.
        """
        
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


    def get_namespace(self, nl, fFilter, repr_limit = 128):
        """
        get_namespace is designed for locals/globals panes that let 
        the user inspect a namespace tree in GUI debuggers such as Winpdb.
        You can study the way it is used in Winpdb.

        nl - List of tuples, where each tuple is made of a python expression 
             as string and a flag that controls whether to "expand" the 
             value, that is, to return its children as well in case it has 
             children e.g. lists, dictionaries, etc...
             
        fFilter - Flag. Filter out __methods__ from objects and classes in 
             the namespace viewer.

        repr_limit - Length limit (approximated) to be imposed repr() of 
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
        
        return self.__smi.get_namespace(nl, fFilter, repr_limit)


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
        
        return self.__smi.execute(suite)


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


    def stop_debuggee(self):
        """
        Stop the debuggee with the os.abort() command.
        """
        
        return self.__smi.stop_debuggee()



class CConsole:
    """
    Interface to a debugger console.
    """
    
    def __init__(
            self, 
            session_manager, 
            stdin = None, 
            stdout = None, 
            fSplit = False
            ):
            
        """
        Constructor of CConsole

        session_manager - session manager object.
        stdin, stdout - redirection for IO.
        fsplit - Set flag to True when Input and Ouput belong to different 
                 panes. For example take a look at Winpdb.
        """
        
        self.m_ci = CConsoleInternal(
                        session_manager, 
                        stdin, 
                        stdout, 
                        fSplit
                        )


    def start(self):
        return self.m_ci.start()


    def join(self):
        """
        Wait until the console ends.
        """
        
        return self.m_ci.join()


    def set_filename(self, filename):
        """
        Set current filename for the console. The current filename can change
        from outside the console when the console is embeded in other 
        components, for example take a look at Winpdb. 
        """
        return self.m_ci.set_filename(filename)

    

#
# ---------------------------- Exceptions ----------------------------------
#




class CException(Exception):
    """
    Base exception class for the debugger.
    """
    
    def __init__(self, *args):
        Exception.__init__(self, *args)



class BadMBCSPath(CException):
    """
    Raised on Windows systems when the python executable or debugger script
    path can not be encoded with the file system code page. This means that
    the Windows code page is misconfigured.
    """



class NotPythonSource(CException):
    """
    Raised when an attempt to load non Python source is made.
    """
    


class InvalidScopeName(CException):
    """
    Invalid scope name.
    This exception may be thrown when a request was made to set a breakpoint
    to an unknown scope.
    """



class BadArgument(CException):
    """
    Bad Argument.
    """



class ThreadNotFound(CException):
    """
    Thread not found.
    """



class NoThreads(CException):
    """
    No Threads.
    """



class ThreadDone(CException):
    """
    Thread Done.
    """



class DebuggerNotBroken(CException):
    """
    Debugger is not broken.
    This exception is thrown when an operation that can only be performed
    while the debuggee is broken, is requested while the debuggee is running.
    """



class InvalidFrame(CException):
    """
    Invalid Frame.
    This exception is raised if an operation is requested on a stack frame
    that does not exist.
    """



class NoExceptionFound(CException):
    """
    No Exception Found.
    This exception is raised when exception information is requested, but no
    exception is found, or has been thrown.
    """

    

class CConnectionException(CException):
    def __init__(self, *args):
        CException.__init__(self, *args)



class BadVersion(CConnectionException):
    """Bad Version."""
    def __init__(self, version):
        CConnectionException.__init__(self)

        self.m_version = version

    def __str__(self):
        return repr(self.m_version)


    
class UnexpectedData(CConnectionException):
    """Unexpected data."""



class AlreadyAttached(CConnectionException):
    """Already Attached."""



class NotAttached(CConnectionException):
    """Not Attached."""



class SpawnUnsupported(CConnectionException):
    """Spawn Unsupported."""



class UnknownServer(CConnectionException):
    """Unknown Server."""



class CSecurityException(CConnectionException):
    def __init__(self, *args):
        CConnectionException.__init__(self, *args)


    
class UnsetPassword(CSecurityException):
    """Unset Password."""


    
class EncryptionNotSupported(CSecurityException):
    """Encryption Not Supported."""



class EncryptionExpected(CSecurityException):
    """Encryption Expected."""


class DecryptionFailure(CSecurityException):
    """Decryption Failure."""



class AuthenticationBadData(CSecurityException):
    """Authentication Bad Data."""



class AuthenticationFailure(CSecurityException):
    """Authentication Failure."""



class AuthenticationBadIndex(CSecurityException):
    """Authentication Bad Index."""
    def __init__(self, max_index = 0, anchor = 0):
        CSecurityException.__init__(self)

        self.m_max_index = max_index
        self.m_anchor = anchor

    def __str__(self):
        return repr((self.m_max_index, self.m_anchor))



#
#----------------------- Infinite List of Globals ---------------------------
#



GNOME_DEFAULT_TERM = 'gnome-terminal'
NT_DEBUG = 'nt_debug'
SCREEN = 'screen'
MAC = 'mac'
DARWIN = 'darwin'
POSIX = 'posix'

#
# Map between OS type and relevant command to initiate a new OS console.
# entries for other OSs can be added here. 
# '%s' serves as a place holder.
#
# Currently there is no difference between 'nt' and NT_DEBUG, since now
# both of them leave the terminal open after termination of debuggee to
# accommodate scenarios of scripts with child processes.
#
osSpawn = {
    'nt': 'start "rpdb2 - Version ' + get_version() + ' - Debuggee Console" cmd /k ""%(exec)s" %(options)s"', 
    NT_DEBUG: 'start "rpdb2 - Version ' + get_version() + ' - Debuggee Console" cmd /k ""%(exec)s" %(options)s"', 
    POSIX: "%(term)s -e %(shell)s -c '%(exec)s %(options)s; %(shell)s' &", 
    GNOME_DEFAULT_TERM: "gnome-terminal --disable-factory -x %(shell)s -c '%(exec)s %(options)s; %(shell)s' &", 
    MAC: '%(exec)s %(options)s',
    DARWIN: '%(exec)s %(options)s',
    SCREEN: 'screen -t debuggee_console %(exec)s %(options)s'
}

RPDBTERM = 'RPDBTERM'
COLORTERM = 'COLORTERM'
TERM = 'TERM'
KDE_PREFIX = 'KDE'
GNOME_PREFIX = 'GNOME'

KDE_DEFAULT_TERM_QUERY = "kreadconfig --file kdeglobals --group General --key TerminalApplication --default konsole"
XTERM = 'xterm'
RXVT = 'rxvt'

RPDB_SETTINGS_FOLDER = '.rpdb2_settings'
RPDB_PWD_FOLDER = os.path.join(RPDB_SETTINGS_FOLDER, 'passwords')
RPDB_BPL_FOLDER = os.path.join(RPDB_SETTINGS_FOLDER, 'breakpoints')
RPDB_BPL_FOLDER_NT = 'rpdb2_breakpoints'
MAX_BPL_FILES = 100

HEARTBEAT_TIMEOUT = 16
IDLE_MAX_RATE = 2.0
PING_TIMEOUT = 4.0
LOCAL_TIMEOUT = 1.0
COMMUNICATION_RETRIES = 5

WAIT_FOR_BREAK_TIMEOUT = 3.0

STARTUP_TIMEOUT = 3.0
STARTUP_RETRIES = 3

LOOPBACK = '127.0.0.1'
LOCALHOST = 'localhost'

SERVER_PORT_RANGE_START = 51000
SERVER_PORT_RANGE_LENGTH = 20

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
CONSOLE_PRINTER = '*** '
CONSOLE_WRAP_INDEX = 78
CONSOLE_PROMPT = '\n> '
CONSOLE_PROMPT_ANALYZE = '\nAnalayze> '
CONSOLE_INTRO = ("""RPDB - The Remote Python Debugger, version %s,
Copyright (C) 2005-2007 Nir Aides.
Type "help", "copyright", "license", "credits" for more information.""" % (RPDB_VERSION))

PRINT_NOTICE_PROMPT = "Hit Return for more, or q (and Return) to quit:"
PRINT_NOTICE_LINES_PER_SECTION = 20

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
STR_PSYCO_WARNING = "The psyco module was detected. The debugger is incompatible with the psyco module and will not function correctly as long as the psyco module is imported and used."
STR_DEBUGGEE_TERMINATED = "Debuggee has terminated."
STR_DEBUGGEE_NOT_BROKEN = "Debuggee has to be waiting at break point to complete this command."
STR_DEBUGGER_HAS_BROKEN = "Debuggee is waiting at break point for further commands."
STR_ALREADY_ATTACHED = "Already attached. Detach from debuggee and try again."
STR_NOT_ATTACHED = "Not attached to any script. Attach to a script and try again."
STR_COMMUNICATION_FAILURE = "Failed to communicate with debugged script."
STR_ERROR_OTHER = "Command returned the following error:\n%(type)s, %(value)s.\nPlease check stderr for stack trace and report to support."
STR_BAD_MBCS_PATH = "The debugger can not launch the script since the path to the Python executable or the debugger scripts can not be encoded into the default system code page. Please check the settings of 'Language for non-Unicode programs' in the Advanced tab of the Windows Regional and Language Options dialog."
STR_LOST_CONNECTION = "Lost connection to debuggee."
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
STR_ATTEMPTING_TO_STOP = "Requesting script to stop (with os.abort())."
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

 Id  State      Line  Filename-Scope-Condition
------------------------------------------------------------------------------""" 

STR_BREAKPOINTS_TEMPLATE = """ %2d  %-8s  %5d  %s
                      %s
                      %s"""

STR_ENCRYPTION_SUPPORT_ERROR = "Encryption is not supported since the python-crypto package was not found. Either install the python-crypto package or allow unencrypted connections."
STR_PASSWORD_NOT_SET = 'Password is not set.'
STR_PASSWORD_SET = 'Password is set to: "%s"'
STR_ENCRYPT_MODE = 'Force encryption mode: %s'
STR_REMOTE_MODE = 'Allow remote machines mode: %s'
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

FORK_CHILD = 'child'
FORK_PARENT = 'parent'
FORK_MANUAL = 'manual'
FORK_AUTO = 'auto'

ENCRYPTION_ENABLED = 'encrypted'
ENCRYPTION_DISABLED = 'plain-text'

ENCRYPTION_PREFIX = 'encrypted'

STATE_ENABLED = 'enabled'
STATE_DISABLED = 'disabled'

BREAKPOINTS_FILE_EXT = '.bpl'
PYTHON_FILE_EXTENSION = '.py'
PYTHONW_FILE_EXTENSION = '.pyw'
PYTHONW_SO_EXTENSION = '.so'
PYTHON_EXT_LIST = ['.py', '.pyw', '.pyc', '.pyd', '.pyo', '.so']

MODULE_SCOPE = '?'
MODULE_SCOPE2 = '<module>'
BLENDER_NO_SOURCE_FILENAME = '<string>'
ERROR_NO_BLENDER_SOURCE = 'Blender script source not available.'

SCOPE_SEP = '.'

BP_FILENAME_SEP = ':'
BP_EVAL_SEP = ','

DEBUGGER_FILENAME = 'rpdb2.py'
THREADING_FILENAME = 'threading.py'

STR_STATE_BROKEN = 'waiting at break point'

STATE_BROKEN = 'broken'
STATE_RUNNING = 'running'

STATE_ANALYZE = 'analyze'
STATE_DETACHED = 'detached'
STATE_DETACHING = 'detaching'
STATE_SPAWNING = 'spawning'
STATE_ATTACHING = 'attaching'

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

RPDB_EXEC_INFO = 'rpdb_exception_info'

MODE_ON = 'ON'
MODE_OFF = 'OFF'

MAX_EVALUATE_LENGTH = 256 * 1024
MAX_NAMESPACE_ITEMS = 1024
MAX_SORTABLE_LENGTH = 256 * 1024
REPR_ID_LENGTH = 4096

MAX_NAMESPACE_WARNING = {
    DICT_KEY_EXPR: STR_MAX_NAMESPACE_WARNING_TITLE, 
    DICT_KEY_NAME: STR_MAX_NAMESPACE_WARNING_TITLE, 
    DICT_KEY_REPR: STR_MAX_NAMESPACE_WARNING_MSG,
    DICT_KEY_IS_VALID: False,
    DICT_KEY_TYPE: STR_MAX_NAMESPACE_WARNING_TYPE, 
    DICT_KEY_N_SUBNODES: 0
    }

MAX_EVENT_LIST_LENGTH = 1000

EVENT_EXCLUDE = 'exclude'
EVENT_INCLUDE = 'include'

INDEX_TABLE_SIZE = 100

DISPACHER_METHOD = 'dispatcher_method'

BASIC_TYPES_LIST = ['str', 'unicode', 'int', 'long', 'float', 'bool', 'NoneType']

XML_DATA = """<?xml version='1.0'?>
<methodCall>
<methodName>dispatcher_method</methodName>
<params>
<param>
<value><string>%s</string></value>
</param>
</params>
</methodCall>""" % RPDB_COMPATIBILITY_VERSION

N_WORK_QUEUE_THREADS = 8

DEFAULT_PATH_SUFFIX_LENGTH = 55



g_server_lock = threading.RLock()
g_server = None
g_debugger = None

g_fScreen = False
g_fDefaultStd = True

#
# In debug mode errors and tracebacks are printed to stdout
#
g_fDebug = False

#
# Lock for the traceback module to prevent it from interleaving 
# output from different threads.
#
g_traceback_lock = threading.RLock()

#
# Filename to Source-lines dictionary of blender Python scripts.
#
g_blender_text = {}

g_initial_cwd = []

g_error_mapping = {
    socket.error: STR_COMMUNICATION_FAILURE,
   
    CConnectionException: STR_LOST_CONNECTION,
    BadVersion: STR_BAD_VERSION,
    UnexpectedData: STR_UNEXPECTED_DATA,
    SpawnUnsupported: STR_SPAWN_UNSUPPORTED,
    UnknownServer: STR_DEBUGGEE_UNKNOWN,
    UnsetPassword: STR_PASSWORD_MUST_BE_SET,
    EncryptionNotSupported: STR_DEBUGGEE_NO_ENCRYPTION,
    EncryptionExpected: STR_ENCRYPTION_EXPECTED,
    DecryptionFailure: STR_DECRYPTION_FAILURE,
    AuthenticationBadData: STR_ACCESS_DENIED,
    AuthenticationFailure: STR_ACCESS_DENIED,
    BadMBCSPath: STR_BAD_MBCS_PATH,

    AlreadyAttached: STR_ALREADY_ATTACHED,    
    NotAttached: STR_NOT_ATTACHED,
    DebuggerNotBroken: STR_DEBUGGEE_NOT_BROKEN,
    NoThreads: STR_NO_THREADS,
    NoExceptionFound: STR_EXCEPTION_NOT_FOUND,
}

#
# These globals are related to handling the os.fork() os._exit() and exec
# pattern.
#
g_forkpid = None
g_forktid = None

g_exectid = None
g_execpid = None

g_fos_exit = False


#
# To hold a reference to __main__ to prevent its release if an unhandled
# exception is raised.
#
g_module_main = None

g_fsent_psyco_warning = False

g_fignore_atexit = False
g_ignore_broken_pipe = 0


#
# Unicode version of path names that do not encode well witn the windows 
# 'mbcs' encoding. This dict is used to work with such path names on
# windows.
#
g_found_unicode_files = {}

g_frames_path = {}

g_safe_base64_to = string.maketrans('/+=', '_-#')
g_safe_base64_from = string.maketrans('_-#', '/+=')



#
# ---------------------------- General Utils ------------------------------
#
            


def class_name(c):
    s = str(c)
    
    if "'" in s:
        s = s.split("'")[1]

    assert(s.startswith(__name__ + '.'))
    
    return s

    

def clip_filename(path, n = DEFAULT_PATH_SUFFIX_LENGTH):
    suffix = calc_suffix(path, n)
    if not suffix.startswith('...'):
        return suffix

    index = suffix.find(os.sep)
    if index == -1:
        return suffix

    clip = '...' + suffix[index:]

    return clip
    


def safe_repr(x):
    try:
        y = repr(x)
        return y

    except:
        return 'N/A'



def repr_list(pattern, l, length, is_valid, fraw = False):
    length = max(0, length - len(pattern) + 2)

    s = ''

    index = 0

    try:
        for i in l:
            #
            # Remove any trace of session password from data structures that 
            # go over the network.
            #
            if i in ['_rpdb2_args', '_rpdb2_pwd', 'm_rpdb2_pwd']:
                continue
            
            s += repr_ltd(i, length - len(s), is_valid, fraw = fraw)

            index += 1
            
            if index < len(l) and len(s) > length:
                is_valid[0] = False
                if not s.endswith('...'):
                    s += '...'
                break

            if index < len(l):
                s += ', '

    except AttributeError:
        is_valid[0] = False 

    return pattern % s



def repr_dict(pattern, d, length, is_valid, fraw = False):
    length = max(0, length - len(pattern) + 2)

    s = ''

    index = 0

    try:
        for k in d:
            #
            # Remove any trace of session password from data structures that 
            # go over the network.
            #
            if k in ['_rpdb2_args', '_rpdb2_pwd', 'm_rpdb2_pwd']:
                continue
            
            v = d[k]

            s += repr_ltd(k, length - len(s), is_valid, fraw = fraw)

            if len(s) > length:
                is_valid[0] = False
                if not s.endswith('...'):
                    s += '...'
                break

            s +=  ': ' + repr_ltd(v, length - len(s), is_valid, fraw = fraw)

            index += 1

            if index < len(d) and len(s) > length:
                is_valid[0] = False
                if not s.endswith('...'):
                    s += '...'
                break

            if index < len(d):
                s += ', '

    except AttributeError:
        is_valid[0] = False 

    return pattern % s



def repr_str(s, length, is_valid):
    try:
        u = s.decode('utf8')
        r = repr_unicode(u, length, is_valid)
        return r[1:]

    except:
        return repr_str_raw(s, length, is_valid)



def repr_unicode(s, length, is_valid):
    rs = ''

    for c in s:
        if len(rs) > length:
            is_valid[0] = False
            rs += '...'
            break

        if ord(c) < 128:
            rs += repr(c)[2:-1]
        else:
            rs += c.encode('utf8')

    if not "'" in rs:
        return "u'%s'" % rs

    if not '"' in rs:
        return 'u"%s"' % rs
   
    return "u'%s'" % rs.replace("'", "\\'")



def repr_str_raw(s, length, is_valid):
    if len(s) > length:
        is_valid[0] = False
        s = s[: length] + '...'

    return repr(s)



def repr_base(v, length, is_valid):
    r = repr(v)

    if len(r) > length:
        is_valid[0] = False
        r = r[: length] + '...'

    return r



def repr_ltd(x, length, is_valid = [True], fraw = False):
    length = max(0, length)

    try:
        if isinstance(x, set):
            return repr_list('set([%s])', x, length, is_valid, fraw = fraw)

        if isinstance(x, frozenset):
            return repr_list('frozenset([%s])', x, length, is_valid, fraw = fraw)

    except NameError:
        pass

    if isinstance(x, sets.Set):
        return repr_list('sets.Set([%s])', x, length, is_valid, fraw = fraw)

    if isinstance(x, sets.ImmutableSet):
        return repr_list('sets.ImmutableSet([%s])', x, length, is_valid, fraw = fraw)

    if isinstance(x, list):
        return repr_list('[%s]', x, length, is_valid, fraw = fraw)

    if isinstance(x, tuple):
        return repr_list('(%s)', x, length, is_valid, fraw = fraw)

    if isinstance(x, dict):
        return repr_dict('{%s}', x, length, is_valid, fraw = fraw)

    if fraw and type(x) in [str, unicode]:
        return repr_str_raw(x, length, is_valid)

    if type(x) == str:
        return repr_str(x, length, is_valid)

    if type(x) == unicode:
        return repr_unicode(x, length, is_valid)

    if type(x) in [bool, int, float, long, type(None)]:
        return repr_base(x, length, is_valid)

    is_valid[0] = False

    y = safe_repr(x)[: length]
    if len(y) == length:
        y += '...'

    return y



def print_debug(str):
    if not g_fDebug:
        return

    t = time.time()
    l = time.localtime(t)
    s = time.strftime('%H:%M:%S', l) + '.%03d' % ((t - int(t)) * 1000, )

    print >> sys.__stderr__, s, 'RPDB2:', str



def print_debug_exception(fForce = False):
    """
    Print exceptions to stdout when in debug mode.
    """
    
    if not g_fDebug and not fForce:
        return

    (t, v, tb) = sys.exc_info()
    print_exception(t, v, tb, fForce)

       

def print_exception(t, v, tb, fForce = False):
    """
    Print exceptions to stderr when in debug mode.
    """
    
    if not g_fDebug and not fForce:
        return
        
    try:
        g_traceback_lock.acquire()
        traceback.print_exception(t, v, tb, file = sys.stderr)
        
    finally:    
        g_traceback_lock.release()

       

def print_stack():
    """
    Print exceptions to stdout when in debug mode.
    """
    
    if g_fDebug == True:
        try:
            g_traceback_lock.acquire()
            traceback.print_stack(file = sys.stderr)
            
        finally:    
            g_traceback_lock.release()

       

def split_command_line_path_filename_args(command_line):
    """
    Split command line to a 3 elements tuple (path, filename, args)
    """
    
    command_line = command_line.strip()
    if len(command_line) == 0:
        return ('', '', '')

    if os.path.isfile(command_line):
        (_path, _filename) = split_path(command_line)
        return (_path, _filename, '')
        
    if command_line[0] in ['"', "'"]:
        _command_line = command_line[1:]
        i = _command_line.find(command_line[0])
        if i == -1:
            (_path, filename) = split_path(_command_line)
            return (_path, filename, '')
        else:
            (_path, filename) = split_path(_command_line[: i])
            args = _command_line[i + 1:].strip()
            return (_path, filename, args)
    else:
        i = command_line.find(' ')
        if i == -1:
            (_path, filename) = split_path(command_line)
            return (_path, filename, '')
        else:
            args = command_line[i + 1:].strip()
            (_path, filename) = split_path(command_line[: i])
            return (_path, filename, args)



def split_path(path):
    (_path, filename) = os.path.split(path)

    #
    # Make sure path separator (e.g. '/') ends the splitted path if it was in
    # the original path.
    #
    if (_path[-1:] not in [os.path.sep, os.path.altsep]) and \
        (path[len(_path): len(_path) + 1] in [os.path.sep, os.path.altsep]):
        _path = _path + path[len(_path): len(_path) + 1]
        
    return (_path, filename)



def calc_frame_path(frame):
    filename = frame.f_code.co_filename
    
    if filename.startswith('<'):
        return filename

    if filename in g_frames_path:
        return g_frames_path[filename]

    if os.path.isabs(filename):
        abspath = my_abspath(filename)
        lowered = winlower(abspath)
        g_frames_path[filename] = lowered
        return lowered
        
    globals_file = frame.f_globals.get('__file__', None)
    
    if globals_file != None and os.path.isabs(globals_file):    
        dirname = os.path.dirname(globals_file)
        basename = os.path.basename(filename)
        path = os.path.join(dirname, basename)        
        abspath = my_abspath(path)
        lowered = winlower(abspath)        
        g_frames_path[filename] = lowered
        return lowered

    try:
        abspath = FindFile(filename, fModules = True)
        lowered = winlower(abspath)    
        g_frames_path[filename] = lowered
        return lowered

    except IOError:
        lowered = winlower(filename)    
        return lowered
        
            

def my_abspath(path):
    """
    We need our own little version of os.path.abspath since the original
    code imports modules in the 'nt' code path which can cause our debugger
    to deadlock in unexpected locations.
    """
    
    if path[:1] == '<':
        #
        # 'path' may also be '<stdin>' in which case it is left untouched.
        #
        return path

    if os.name == 'nt':
        return my_abspath1(path)

    return  os.path.abspath(path)   



def my_abspath1(path):
    """
    Modification of ntpath.abspath() that avoids doing an import.
    """
    
    if path:
        try:
            path = _getfullpathname(path)
        except WindowsError:
            pass
    else:
        path = os.getcwd()
        
    np = os.path.normpath(path)

    if (len(np) >= 2) and (np[1:2] == ':'):
        np = np[:1].upper() + np[1:]

    return np    



def IsPythonSourceFile(path):
    if path.endswith(PYTHON_FILE_EXTENSION):
        return True
        
    if path.endswith(PYTHONW_FILE_EXTENSION):
        return True

    path = g_found_unicode_files.get(path, path)

    try:
        f = open(path, 'r')
        c = f.read(10000)
        f.close()
  
        ll = c.split('\n')

        for l in ll:
            if l.startswith('#!') and 'python' in l:
                return True

        compiler.parseFile(path) 
        return True

    except:
        return False



def CalcModuleName(filename):
    _basename = os.path.basename(filename)
    (modulename, ext) = os.path.splitext(_basename)

    if ext in PYTHON_EXT_LIST:
        return modulename

    return  _basename   



def CalcScriptName(filename, fAllowAnyExt = True):
    if filename.endswith(PYTHON_FILE_EXTENSION):
        return filename
        
    if filename.endswith(PYTHONW_FILE_EXTENSION):
        return filename
        
    if filename.endswith(PYTHONW_SO_EXTENSION):
        scriptname = filename[:-3] + PYTHON_FILE_EXTENSION
        return scriptname

    if filename[:-1].endswith(PYTHON_FILE_EXTENSION):
        scriptname = filename[:-1]
        return scriptname

    if fAllowAnyExt:
        return filename

    scriptname = filename + PYTHON_FILE_EXTENSION
        
    return scriptname
        


def FindModuleDir(module_name):
    if module_name == '':
        raise IOError
        
    dot_index = module_name.rfind('.')
    if dot_index != -1:
        parent = module_name[: dot_index]
        child = module_name[dot_index + 1:]
    else:
        parent = ''
        child = module_name
    
    m = sys.modules[module_name]
    
    if not hasattr(m, '__file__') or m.__file__ == None:
        parent_dir = FindModuleDir(parent)
        module_dir = os.path.join(parent_dir, winlower(child))
        return module_dir

    if not os.path.isabs(m.__file__):
        parent_dir = FindModuleDir(parent)
        module_dir = os.path.join(parent_dir, winlower(child))
        return module_dir        
        
    (root, ext) = os.path.splitext(m.__file__)
    if root.endswith('__init__'):
        root = os.path.dirname(root)
    
    abspath = my_abspath(root)
    lowered = winlower(abspath)

    return lowered
    

    
def FindFileAsModule(filename):
    lowered = winlower(filename)
    (root, ext) = os.path.splitext(lowered)
    
    root_dotted = root.replace('\\', '.').replace('/', '.').replace(':', '.')

    match_list = []    
    for (module_name, m) in sys.modules.items():
        lowered_module_name = winlower(module_name)
        if (root_dotted + '.').startswith(lowered_module_name + '.'):
            match_list.append((len(module_name), module_name))

            if lowered_module_name == root_dotted:
                break

    match_list.sort()
    match_list.reverse()
    
    for (matched_len, matched_module) in match_list:
        try:
            module_dir = FindModuleDir(matched_module)
        except IOError:
            continue
        
        suffix = root[matched_len:]        
        if suffix == '':
            path = module_dir + ext
        else:    
            path = os.path.join(module_dir, suffix.strip('\\')) + ext
        
        scriptname = CalcScriptName(path, fAllowAnyExt = False)
        if os.path.isfile(scriptname):
            return scriptname

        #
        # Check .pyw files
        #
        scriptname += 'w'
        if scriptname.endswith(PYTHONW_FILE_EXTENSION) and os.path.isfile(scriptname):
            return scriptname
        
    raise IOError



def FindFile(
        filename, 
        sources_paths = [], 
        fModules = False, 
        fAllowAnyExt = True
        ):
        
    """ 
    FindFile looks for the full path of a script in a rather non-strict
    and human like behavior.

    It will always look for .py or .pyw files even if a .pyc or no 
    extension is given.

    1. It will check against loaded modules if asked.
    1. full path (if exists).
    2. sources_paths.
    2. current path.
    3. PYTHONPATH
    4. PATH
    """

    if filename in g_found_unicode_files:
        return filename

    if filename.startswith('<'):
        raise IOError
        
    filename = filename.strip('\'"')
    filename = os.path.expanduser(filename)

    if fModules and not (os.path.isabs(filename) or filename.startswith('.')):
        try:    
            return FindFileAsModule(filename)
        except IOError:
            pass
                
    if fAllowAnyExt:
        try:
            abspath = FindFile(
                            filename, 
                            sources_paths, 
                            fModules = False, 
                            fAllowAnyExt = False
                            )
            return abspath
        except IOError:
            pass

    if os.path.isabs(filename) or filename.startswith('.'):
        try:
            abspath = my_abspath(filename)
            lowered = winlower(abspath)
            scriptname = CalcScriptName(lowered, fAllowAnyExt)
            
            if os.path.isfile(scriptname):
                return scriptname

            #
            # Check .pyw files
            #
            scriptname += 'w'
            if scriptname.endswith(PYTHONW_FILE_EXTENSION) and os.path.isfile(scriptname):
                return scriptname
            
            scriptname = None
            raise IOError

        finally:
            if type(scriptname) == unicode:
                fse = sys.getfilesystemencoding()
                _l = scriptname.encode(fse)
                if '?' in _l:
                    g_found_unicode_files[_l] = scriptname
                return _l

    scriptname = CalcScriptName(filename, fAllowAnyExt)
    
    cwd = [os.getcwd(), os.getcwdu()]
    env_path = os.environ['PATH']
    paths = sources_paths + cwd + g_initial_cwd + sys.path + env_path.split(os.pathsep)
    
    try:
        for p in paths:
            f = os.path.join(p, scriptname)
            abspath = my_abspath(f)
            lowered = winlower(abspath)
            
            if os.path.isfile(lowered):
                return lowered

            #
            # Check .pyw files
            #
            lowered += 'w'
            if lowered.endswith(PYTHONW_FILE_EXTENSION) and os.path.isfile(lowered):
                return lowered

        lowered = None
        raise IOError

    finally:
        if type(lowered) == unicode:
            fse = sys.getfilesystemencoding()
            _l = lowered.encode(fse)
            if '?' in _l:
                g_found_unicode_files[_l] = lowered
            return _l



def IsFileInPath(filename):
    if filename == '':
        return False

    try:
        FindFile(filename)
        return True
        
    except IOError:
        return False



def IsPrefixInEnviron(str):
    for e in os.environ.keys():
        if e.startswith(str):
            return True

    return False
    


def CalcTerminalCommand():
    """
    Calc the unix command to start a new terminal, for example: xterm
    """
    
    if RPDBTERM in os.environ:
        term = os.environ[RPDBTERM]
        if IsFileInPath(term):
            return term

    if COLORTERM in os.environ:
        term = os.environ[COLORTERM]
        if IsFileInPath(term):
            return term

    if IsPrefixInEnviron(KDE_PREFIX):
        (s, term) = commands.getstatusoutput(KDE_DEFAULT_TERM_QUERY)
        if (s == 0) and IsFileInPath(term):
            return term
            
    elif IsPrefixInEnviron(GNOME_PREFIX):
        if IsFileInPath(GNOME_DEFAULT_TERM):
            return GNOME_DEFAULT_TERM
        
    if IsFileInPath(XTERM):
        return XTERM

    if IsFileInPath(RXVT):
        return RXVT

    raise SpawnUnsupported    



def CalcMacTerminalCommand(command):
    """
    Calculate what to put in popen to start a given script.
    Starts a tiny Applescript that performs the script action.
    """

    #
    # Quoting is a bit tricky; we do it step by step.
    # Make Applescript string: put backslashes before double quotes and 
    # backslashes.
    #
    command = command.replace('\\', '\\\\').replace('"', '\\"')

    #
    # Make complete Applescript command.
    #
    command = 'tell application "Terminal" to do script "%s"' % command

    #
    # Make a shell single quoted string (put backslashed single quotes 
    # outside string).
    #
    command = command.replace("'", "'\\''")

    #
    # Make complete shell command.
    #
    return "osascript -e '%s'" % command



def winlower(path):
    """
    return lowercase version of 'path' on NT systems.
    
    On NT filenames are case insensitive so lowercase filenames
    for comparison purposes on NT.
    """
    
    if os.name == 'nt':
        return path.lower()

    return path
    
    

def is_blender_file(filename):
    """
    Return True if filename refers to a blender file.
    
    Support for debugging of Blender Python scripts.
    Blender scripts are not always saved on disk, and their 
    source has to be queried directly from the Blender API.
    http://www.blender.org
    """
    
    if not 'Blender.Text' in sys.modules:
        return False

    if filename == BLENDER_NO_SOURCE_FILENAME:
        return True
    
    _filename = os.path.basename(filename)

    try:
        sys.modules['Blender.Text'].get(_filename)
        return True

    except NameError:
        f = winlower(_filename)
        tlist = sys.modules['Blender.Text'].get()
        for t in tlist:
            n = winlower(t.getName())
            if n == f:
                return True
            
        return False



def get_blender_source(filename):
    """
    Return list of lines in the file refered by filename.
    
    Support for debugging of Blender Python scripts.
    Blender scripts are not always saved on disk, and their 
    source has to be queried directly from the Blender API.
    http://www.blender.org
    """

    if filename.startswith('<'):
        raise IOError(ERROR_NO_BLENDER_SOURCE)
        
    _filename = os.path.basename(filename)

    lines = g_blender_text.get(_filename, None)
    if lines is not None:
        return lines
        
    f = winlower(_filename)
    lines = g_blender_text.get(f, None)
    if lines is not None:
        return lines

    try:
        t = sys.modules['Blender.Text'].get(_filename)
        lines = t.asLines()
        g_blender_text[_filename] = lines
        return lines
        
    except NameError:
        f = winlower(_filename)
        tlist = sys.modules['Blender.Text'].get()

        for _t in tlist:
            n = winlower(_t.getName())
            if n == f:
                t = _t
                break
        
        lines = t.asLines()
        g_blender_text[f] = lines
        return lines

    
            
def get_source_line(filename, lineno, fBlender):
    """
    Return source line from file.
    """
    
    if fBlender:
        lines = get_blender_source(filename)

        try:
            line = lines[lineno - 1] + '\n'
            return line
            
        except IndexError:
            return '' 

    filename = g_found_unicode_files.get(filename, filename)
    line = linecache.getline(filename, lineno) 
    return line



def _getpid():
    try:
        return os.getpid()
    except:
        return -1



def calcURL(host, port):
    """
    Form HTTP URL from 'host' and 'port' arguments.
    """
    
    url = "http://" + str(host) + ":" + str(port)
    return url
    
    

def GetSocketError(e):
    if (not isinstance(e.args, tuple)) or (len(e.args) == 0):
        return -1

    return e.args[0]



def ControlRate(t_last_call, max_rate):
    """
    Limits rate at which this function is called by sleeping.
    Returns the time of invocation.
    """
    
    p = 1.0 / max_rate
    t_current = time.time()
    dt = t_current - t_last_call

    if dt < p:
        time.sleep(p - dt)

    return t_current



def generate_rid():
    """
    Return a 7 digits random id.
    """
    
    return repr(random.randint(1000000, 9999999))



def generate_random_char(str):
    """
    Return a random character from string argument.
    """
    
    if str == '':
        return ''
        
    i = random.randint(0, len(str) - 1)
    return str[i]



def generate_random_password():
    """
    Generate an 8 characters long password.
    """
    
    s = 'abdefghijmnqrt' + 'ABDEFGHJLMNQRTY'
    ds = '23456789_' + s
        
    _rpdb2_pwd = generate_random_char(s)

    for i in range(0, 7):
        _rpdb2_pwd += generate_random_char(ds)

    return _rpdb2_pwd    



def is_encryption_supported():
    """
    Is the Crypto module imported/available.
    """
    
    return 'DES' in globals()



def calc_suffix(str, n):
    """
    Return an n charaters suffix of the argument string of the form
    '...suffix'.
    """
    
    if len(str) <= n:
        return str

    return '...' + str[-(n - 3):]


    
def calc_prefix(str, n):
    """
    Return an n charaters prefix of the argument string of the form
    'prefix...'.
    """
    
    if len(str) <= n:
        return str

    return str[: (n - 3)] + '...'



def create_rpdb_settings_folder():
    """
    Create the settings folder on Posix systems:
    '~/.rpdb2_settings' with mode 700.
    """
    
    if os.name != POSIX:
        return
        
    home = os.path.expanduser('~')

    rsf = os.path.join(home, RPDB_SETTINGS_FOLDER)
    if not os.path.exists(rsf):
        os.mkdir(rsf, 0700)

    pwds = os.path.join(home, RPDB_PWD_FOLDER)    
    if not os.path.exists(pwds):
        os.mkdir(pwds, 0700)

    bpl = os.path.join(home, RPDB_BPL_FOLDER)    
    if not os.path.exists(bpl):
        os.mkdir(bpl, 0700)



def cleanup_bpl_folder(path):
    if random.randint(0, 10) > 0:
        return

    l = os.listdir(path)
    if len(l) < MAX_BPL_FILES:
        return
    
    try:
        ll = [(os.stat(os.path.join(path, f))[stat.ST_ATIME], f) for f in l]
    except:
        return
        
    ll.sort()

    print ll
    
    for (t, f) in ll[: -MAX_BPL_FILES]:
        try:
            os.remove(os.path.join(path, f))
        except:
            pass

        

def calc_bpl_filename(filename):
    tmp_filename = md5.new(filename).hexdigest()[:10]

    if os.name == POSIX:
        home = os.path.expanduser('~')
        bpldir = os.path.join(home, RPDB_BPL_FOLDER)
        cleanup_bpl_folder(bpldir)
        path = os.path.join(bpldir, tmp_filename) + BREAKPOINTS_FILE_EXT
        return path

    #
    # gettempdir() is used since it works with unicode user names on 
    # Windows.
    #
        
    tmpdir = tempfile.gettempdir()
    bpldir = os.path.join(tmpdir, RPDB_BPL_FOLDER_NT)

    if not os.path.exists(bpldir):
        #
        # Folder creation is done here since this is a temp folder.
        #
        try:
            os.mkdir(bpldir, 0700)
        except:
            print_debug_exception()
            raise CException

    else:    
        cleanup_bpl_folder(bpldir)
        
    path = os.path.join(bpldir, tmp_filename) + BREAKPOINTS_FILE_EXT
    return path
    

    
def calc_pwd_file_path(rid):
    """
    Calc password file path for Posix systems:
    '~/.rpdb2_settings/<rid>'
    """
    
    home = os.path.expanduser('~')
    rsf = os.path.join(home, RPDB_PWD_FOLDER)
    pwd_file_path = os.path.join(rsf, rid)
    
    return pwd_file_path

            

def create_pwd_file(rid, _rpdb2_pwd):
    """
    Create password file for Posix systems.
    """
    
    if os.name != POSIX:
        return

    path = calc_pwd_file_path(rid)

    fd = os.open(path, os.O_WRONLY | os.O_CREAT, 0600)
    
    os.write(fd, _rpdb2_pwd)
    os.close(fd)
    
        

def read_pwd_file(rid):
    """
    Read password from password file for Posix systems.
    """

    assert(os.name == POSIX)

    path = calc_pwd_file_path(rid)

    p = open(path, 'r')
    _rpdb2_pwd = p.read()
    p.close()

    return _rpdb2_pwd
    
    
    
def delete_pwd_file(rid):
    """
    Delete password file for Posix systems.
    """

    if os.name != POSIX:
        return

    path = calc_pwd_file_path(rid)

    try:
        os.remove(path)
    except:
        pass



def ParseLineEncoding(l):
    if l.startswith('# -*- coding: '):
        e = l[len('# -*- coding: '):].split()[0]
        return e

    if l.startswith('# vim:fileencoding='):
        e = l[len('# vim:fileencoding='):].strip()
        return e

    return None    

        
        
def ParseEncoding(txt):
    """
    Parse document encoding according to: 
    http://docs.python.org/ref/encodings.html
    """
    
    if txt.startswith('\xef\xbb\xbf'):
        return 'utf8'

    l = txt.split('\n', 2)

    e = ParseLineEncoding(l[0])
    if e is not None:
        return e
        
    if len(l) == 1:
        return None 
        
    e = ParseLineEncoding(l[1])
    return e



def CalcUserShell():
    try:
        s = os.getenv('SHELL')
        if s != None:
            return s

        import getpass
        username = getpass.getuser()

        f = open('/etc/passwd', 'r')
        l = f.read()
        f.close()

        ll = l.split('\n')
        d = dict([(e.split(':', 1)[0], e.split(':')[-1]) for e in ll])

        return d[username]

    except:
        return 'sh'



def IsFilteredProperty(a):
    if not (a.startswith('__') and a.endswith('__')):
        return False

    if a in ['__class__', '__bases__', '__file__', '__doc__', '__name__']:
        return False

    return True



def CalcFilteredDir(r, fFilter):
    d = dir(r)

    if not fFilter:
        return d

    fd = [e for e in d if not IsFilteredProperty(e)]

    return fd



def CalcIdentity(r, fFilter):
    if not fFilter:
        return r

    if not hasattr(r, 'im_func'):
        return r

    return r.im_func



def CalcDictKeys(r, fFilter):
    d = CalcFilteredDir(r, fFilter)
    rs = sets.Set(d)

    if hasattr(r, '__class__'):
        c = getattr(r, '__class__')
        d = CalcFilteredDir(c, fFilter)
        cs = sets.Set(d)
        s = rs & cs

        for e in s:
            o1 = getattr(r, e)
            o2 = getattr(c, e)

            if CalcIdentity(o1, fFilter) is CalcIdentity(o2, fFilter):
                rs.discard(e)

    if hasattr(r, '__bases__'):
        bl = getattr(r, '__bases__')
        if type(bl) == tuple:
            for b in bl:
                d = CalcFilteredDir(b, fFilter)
                bs = sets.Set(d)
                s = rs & bs

                for e in s:
                    o1 = getattr(r, e)
                    o2 = getattr(b, e)

                    if CalcIdentity(o1, fFilter) is CalcIdentity(o2, fFilter):
                        rs.discard(e)
      
    l = [a for a in rs]

    return l



class _RPDB2_FindRepr:
    def __init__(self, o, repr_limit):
        self.m_object = o
        self.m_repr_limit = repr_limit


    def __getitem__(self, key):
        index = 0
        for i in self.m_object:
            if repr_ltd(i, self.m_repr_limit, fraw = True).replace('"', '&quot') == key:
                if isinstance(self.m_object, dict):
                    return self.m_object[i]

                return i

            index += 1
            if index > MAX_SORTABLE_LENGTH:
                return None


    def __setitem__(self, key, value):
        if not isinstance(self.m_object, dict):
            return 

        index = 0
        for i in self.m_object:
            if repr_ltd(i, self.m_repr_limit, fraw = True).replace('"', '&quot') == key:
                self.m_object[i] = value
                return

            index += 1
            if index > MAX_SORTABLE_LENGTH:
                return



def SafeCmp(x, y):
    try:
        return cmp(x, y)

    except:
        pass

    return cmp(repr_ltd(x, 256, fraw = True), repr_ltd(y, 256, fraw = True))



#
# ---------------------------------- CThread ---------------------------------------
#



class CThread (threading.Thread):
    m_fstop = False
    m_threads = {}

    m_lock = threading.RLock()
    m_id = 0


    def __init__(self, name = None, target = None, args = (), shutdown = None):
        threading.Thread.__init__(self, name = name, target = target, args = args)

        self.m_fstarted = False
        self.m_shutdown_callback = shutdown

        self.m_id = self.__getId()


    def __del__(self):
        #print_debug('Destructor called for ' + self.getName())
        
        #threading.Thread.__del__(self)

        if self.m_fstarted:
            try:
                del CThread.m_threads[self.m_id]
            except KeyError:
                pass


    def start(self):
        if CThread.m_fstop:
            return

        CThread.m_threads[self.m_id] = weakref.ref(self)

        if CThread.m_fstop:
            del CThread.m_threads[self.m_id]
            return

        self.m_fstarted = True

        threading.Thread.start(self)


    def run(self):
        sys.settrace(None)
        sys.setprofile(None)
 
        threading.Thread.run(self)

    
    def join(self, timeout = None):
        try:
            threading.Thread.join(self, timeout)
        except AssertionError:
            pass


    def shutdown(self):
        if self.m_shutdown_callback:
            self.m_shutdown_callback()


    def joinAll(cls):
        print_debug('Shutting down debugger threads...')

        CThread.m_fstop = True

        for tid, w in CThread.m_threads.items():
            t = w()
            if not t:
                continue

            try:
                #print_debug('Calling shutdown of thread %s.' % (t.getName(), ))
                t.shutdown()
            except:
                pass

            t = None

        t0 = time.time()

        while len(CThread.m_threads) > 0:
            if time.time() - t0 > 16:
                print_debug('Shut down of debugger threads has TIMED OUT!')
                return

            #print_debug(repr(CThread.m_threads))
            time.sleep(0.1)

        print_debug('Shut down debugger threads, done.')

    joinAll = classmethod(joinAll)


    def clearJoin(cls):
        CThread.m_fstop = False

    clearJoin = classmethod(clearJoin)


    def __getId(self):
        CThread.m_lock.acquire()
        id = CThread.m_id
        CThread.m_id += 1
        CThread.m_lock.release()

        return id

    

#
#--------------------------------------- Crypto ---------------------------------------
#



class CCrypto:
    """
    Handle authentication and encryption of data, using password protection.
    """

    m_keys = {}
    
    def __init__(self, _rpdb2_pwd, fAllowUnencrypted, rid):
        self.m_rpdb2_pwd = _rpdb2_pwd
        self.m_key = self.__calc_key(_rpdb2_pwd)
        
        self.m_fAllowUnencrypted = fAllowUnencrypted
        self.m_rid = rid

        self.m_failure_lock = threading.RLock()

        self.m_lock = threading.RLock()

        self.m_index_anchor_in = random.randint(0, 1000000000)
        self.m_index_anchor_ex = 0

        self.m_index = 0
        self.m_index_table = {}
        self.m_index_table_size = INDEX_TABLE_SIZE
        self.m_max_index = 0


    def __calc_key(self, _rpdb2_pwd):
        """
        Create and return a key from a password.
        A Weak password means a weak key.
        """
        
        if _rpdb2_pwd in CCrypto.m_keys:
            return CCrypto.m_keys[_rpdb2_pwd]

        d = md5.new()
        key = _rpdb2_pwd 

        #
        # The following loop takes around a second to complete
        # and should strengthen the password by ~16 bits.
        # a good password is ~30 bits strong so we are looking
        # at ~45 bits strong key
        #
        for i in range(2 ** 16):
            d.update(key * 64)       
            key = d.digest()
            
        CCrypto.m_keys[_rpdb2_pwd] = key

        return key
        
    
    def set_index(self, i, anchor):
        try:    
            self.m_lock.acquire()

            self.m_index = i
            self.m_index_anchor_ex = anchor
            
        finally:
            self.m_lock.release()


    def get_max_index(self):
        return self.m_max_index


    def is_encrypted(self, str):
        return str.startswith(ENCRYPTION_PREFIX)

        
    def do_crypto(self, s, fEncryption):
        """
        Sign string s and possibly encrypt it. 
        Return signed/encrypted string.
        """
        
        _s = self.__sign(s)

        if not fEncryption:
            if self.m_fAllowUnencrypted:
                return _s

            raise EncryptionExpected  
            
        if not is_encryption_supported():
            raise EncryptionNotSupported

        s_encrypted = self.__encrypt(_s)
        return s_encrypted    


    def undo_crypto(self, s_encrypted, fVerifyIndex = True):
        """
        Take crypto string, verify its signature and decrypt it, if
        needed.
        """

        (_s, fEncryption) = self.__decrypt(s_encrypted)            
        s, id = self.__verify_signature(_s, fVerifyIndex)

        return (s, id, fEncryption)

    
    def __encrypt(self, s):
        s_padded = s + '0' * (DES.block_size - (len(s) % DES.block_size))

        key_padded = (self.m_key + '0' * (DES.key_size - (len(self.m_key) % DES.key_size)))[:DES.key_size]
        iv = '0' * DES.block_size
        
        d = DES.new(key_padded, DES.MODE_CBC, iv)
        r = d.encrypt(s_padded)

        s_encoded = base64.encodestring(r)
        return ENCRYPTION_PREFIX + s_encoded


    def __decrypt(self, s):
        if not s.startswith(ENCRYPTION_PREFIX):
            if self.m_fAllowUnencrypted:
                return (s, False)
                
            raise EncryptionExpected

        if not is_encryption_supported():
            raise EncryptionNotSupported
        
        s_encoded = s[len(ENCRYPTION_PREFIX):]
        
        try:
            _r = base64.decodestring(s_encoded)

            key_padded = (self.m_key + '0' * (DES.key_size - (len(self.m_key) % DES.key_size)))[:DES.key_size]
            iv = '0' * DES.block_size
            
            d = DES.new(key_padded, DES.MODE_CBC, iv)
            _s = d.decrypt(_r)

            return (_s, True)
            
        except:
            self.__wait_a_little()
            raise DecryptionFailure


    def __sign(self, s):
        i = self.__get_next_index()
        _s = pickle.dumps((self.m_index_anchor_ex, i, self.m_rid, s))
        
        h = hmac.new(self.m_key, _s, md5)
        _d = h.digest()
        r = (_d, _s)
        s_signed = pickle.dumps(r)

        return s_signed


    def __get_next_index(self):
        try:    
            self.m_lock.acquire()

            self.m_index += 1
            return self.m_index

        finally:
            self.m_lock.release()


    def __verify_signature(self, s, fVerifyIndex):
        try:
            r = pickle.loads(s)
            
            (_d, _s) = r
            
            h = hmac.new(self.m_key, _s, md5)
            d = h.digest()

            if _d != d:
                self.__wait_a_little()
                raise AuthenticationFailure

            (anchor, i, id, s_original) = pickle.loads(_s)
                
        except AuthenticationFailure:
            raise
        except:
            print_debug_exception()
            self.__wait_a_little()
            raise AuthenticationBadData
            
        if fVerifyIndex:
            self.__verify_index(anchor, i, id)

        return s_original, id

        
    def __verify_index(self, anchor, i, id):
        """
        Manage messages ids to prevent replay of old messages.
        """
        
        try:
            try:    
                self.m_lock.acquire()

                if anchor != self.m_index_anchor_in:
                    raise AuthenticationBadIndex(self.m_max_index, self.m_index_anchor_in)

                if i > self.m_max_index + INDEX_TABLE_SIZE / 2:
                    raise AuthenticationBadIndex(self.m_max_index, self.m_index_anchor_in)

                i_mod = i % INDEX_TABLE_SIZE
                (iv, idl) = self.m_index_table.get(i_mod, (None, None))

                #print >> sys.__stderr__, i, i_mod, iv, self.m_max_index

                if (iv is None) or (i > iv):
                    idl = [id]
                elif (iv == i) and (not id in idl):
                    idl.append(id)
                else:
                    raise AuthenticationBadIndex(self.m_max_index, self.m_index_anchor_in)

                self.m_index_table[i_mod] = (i, idl) 

                if i > self.m_max_index:
                    self.m_max_index = i

                return self.m_index

            finally:
                self.m_lock.release()
                
        except:        
            self.__wait_a_little()
            raise


    def __wait_a_little(self):
        self.m_failure_lock.acquire()
        time.sleep((1.0 + random.random()) / 2)
        self.m_failure_lock.release()


        
#
# --------------------------------- Events List --------------------------
#



class CEvent:
    """
    Base class for events.
    """
    
    def is_match(self, arg):
        pass



class CEventPsycoWarning(CEvent):
    """
    The psyco module was detected. Rpdb2 is incompatible with this module.
    """
    
    pass



class CEventSyncReceivers(CEvent):
    """
    A base class for events that sync all receivers before being fired.
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
        self.m_state = state


    def is_match(self, arg):
        return self.m_state == arg



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
    
    def __init__(self, current_thread, thread_list):
        self.m_current_thread = current_thread
        self.m_thread_list = thread_list



class CEventThreadBroken(CEvent):
    """
    A thread has broken.
    """
    
    def __init__(self, tid, name):
        self.m_tid = tid
        self.m_name = name


        
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
    
    DISABLE = 'disable'
    ENABLE = 'enable'
    REMOVE = 'remove'
    SET = 'set'
    
    def __init__(self, bp, action = SET, id_list = [], fAll = False):
        self.m_bp = copy.copy(bp)
        if self.m_bp is not None:
            self.m_bp.m_code = None
        
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
    

    
#
# --------------------------------- Event Manager --------------------------
#



class CEventDispatcherRecord:
    """
    Internal structure that binds a callback to particular events.
    """
    
    def __init__(self, callback, event_type_dict, fSingleUse):
        self.m_callback = callback
        self.m_event_type_dict = event_type_dict
        self.m_fSingleUse = fSingleUse


    def is_match(self, event):
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

        
        
class CEventDispatcher:
    """
    Events dispatcher.
    Dispatchers can be chained together.
    """
    
    def __init__(self, chained_event_dispatcher = None):
        self.m_chained_event_dispatcher = chained_event_dispatcher
        self.m_chain_override_types = {}

        self.m_registrants = {}


    def shutdown(self):
        for er in self.m_registrants.keys():
            self.__remove_dispatcher_record(er)

        
    def register_callback(self, callback, event_type_dict, fSingleUse):
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


    def remove_callback(self, callback):
        erl = [er for er in self.m_registrants.keys() if er.m_callback == callback]
        for er in erl:
            self.__remove_dispatcher_record(er)


    def fire_events(self, event_list):
        for event in event_list:
            self.fire_event(event)


    def fire_event(self, event):
        for er in self.m_registrants.keys():
            self.__fire_er(event, er)

                        
    def __fire_er(self, event, er):
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

                    
    def register_chain_override(self, event_type_dict):
        """
        Chain override prevents registration on chained 
        dispatchers for specific event types.
        """
        
        for t in event_type_dict.keys():
            self.m_chain_override_types[t] = True


    def __register_callback_on_chain(self, er, event_type_dict, fSingleUse):
        _event_type_dict = copy.copy(event_type_dict)
        for t in self.m_chain_override_types:
            if t in _event_type_dict:
                del _event_type_dict[t]

        if len(_event_type_dict) == 0:
            return False


        def callback(event, er = er):
            self.__fire_er(event, er)
            
        _er = self.m_chained_event_dispatcher.register_callback(callback, _event_type_dict, fSingleUse)
        return _er

        
    def __remove_dispatcher_record(self, er):
        try:
            if self.m_chained_event_dispatcher is not None:
                _er = self.m_registrants[er]
                if _er != False:
                    self.m_chained_event_dispatcher.__remove_dispatcher_record(_er)

            del self.m_registrants[er]
            
        except KeyError:
            pass
                


class CEventQueue:
    """
    Add queue semantics above an event dispatcher.
    Instead of firing event callbacks, new events are returned in a list
    upon request.
    """
    
    def __init__(self, event_dispatcher, max_event_list_length = MAX_EVENT_LIST_LENGTH):
        self.m_event_dispatcher = event_dispatcher

        self.m_event_lock = threading.Condition(threading.RLock())
        self.m_max_event_list_length = max_event_list_length
        self.m_event_list = []
        self.m_event_index = 0

        self.m_n_waiters = []

 
    def shutdown(self):
        self.m_event_dispatcher.remove_callback(self.event_handler)

    
    def register_event_types(self, event_type_dict):
        self.m_event_dispatcher.register_callback(self.event_handler, event_type_dict, fSingleUse = False)


    def event_handler(self, event):
        try:
            self.m_event_lock.acquire()

            if isinstance(event, CEventSyncReceivers):
                t0 = time.time()
                while len(self.m_n_waiters) < event.m_sync_n and time.time() < t0 + HEARTBEAT_TIMEOUT:
                    time.sleep(0.1)

            self.m_event_list.append(event)
            if len(self.m_event_list) > self.m_max_event_list_length:
                self.m_event_list.pop(0)
                
            self.m_event_index += 1    
            self.m_event_lock.notifyAll()

        finally:
            self.m_event_lock.release()


    def get_event_index(self):
        return self.m_event_index


    def wait_for_event(self, timeout, event_index):
        """
        Return the new events which were fired. 
        """
        
        try:
            self.m_n_waiters.append(0)

            self.m_event_lock.acquire()
            if event_index >= self.m_event_index:
                self.m_event_lock.wait(timeout)

            if event_index >= self.m_event_index:
                return (self.m_event_index, [])
                
            sub_event_list = self.m_event_list[event_index - self.m_event_index:]
            return (self.m_event_index, sub_event_list)
            
        finally:
            self.m_n_waiters.pop()

            self.m_event_lock.release()



class CStateManager:
    """
    Manage possible debugger states (broken, running, etc...)

    The state manager can receive state changes via an input event 
    dispatcher or via the set_state() method

    It sends state changes forward to the output event dispatcher.

    The state can also be queried or waited for.
    """
    
    def __init__(self, initial_state, event_dispatcher_output = None, event_dispatcher_input = None):
        self.m_event_dispatcher_input = event_dispatcher_input
        self.m_event_dispatcher_output = event_dispatcher_output

        if self.m_event_dispatcher_input is not None:
            event_type_dict = {CEventState: {}}
            self.m_event_dispatcher_input.register_callback(self.event_handler, event_type_dict, fSingleUse = False)

            if self.m_event_dispatcher_output is not None:
                self.m_event_dispatcher_output.register_chain_override(event_type_dict)

        self.m_state_lock = threading.Condition(threading.Lock())

        self.m_state_queue = []
        self.m_state_index = 0        
        self.m_waiter_list = {}
        
        self.set_state(initial_state) 


    def shutdown(self):
        if self.m_event_dispatcher_input is not None:
            self.m_event_dispatcher_input.remove_callback(self.event_handler)


    def event_handler(self, event):
        self.set_state(event.m_state)


    def get_state(self):
        return self.m_state_queue[-1]


    def __add_state(self, state):
        self.m_state_queue.append(state)
        self.m_state_index += 1

        self.__remove_states()


    def __remove_states(self, treshold = None):
        """
        Clean up old state changes from the state queue.
        """
        
        index = self.__calc_min_index()

        if (treshold is not None) and (index <= treshold):
            return
            
        _delta = 1 + self.m_state_index - index

        self.m_state_queue = self.m_state_queue[-_delta:]

        
    def __calc_min_index(self):
        """
        Calc the minimum state index.
        The calculated index is the oldest state of which all state
        waiters are aware of. That is, no one cares for older states
        and these can be removed from the state queue.
        """
        
        if len(self.m_waiter_list) == 0:
            return self.m_state_index

        index_list = self.m_waiter_list.keys()
        min_index = min(index_list)

        return min_index

        
    def __add_waiter(self):
        index = self.m_state_index
        n = self.m_waiter_list.get(index, 0)
        self.m_waiter_list[index] = n + 1

        return index


    def __remove_waiter(self, index):
        n = self.m_waiter_list[index]
        if n == 1:
            del self.m_waiter_list[index]
            self.__remove_states(index)
        else:
            self.m_waiter_list[index] = n - 1


    def __get_states(self, index):
        _delta = 1 + self.m_state_index - index
        states = self.m_state_queue[-_delta:]
        return states

        
    def set_state(self, state = None, fLock = True):
        try:
            if fLock:
                self.m_state_lock.acquire()

            if state is None:
                state = self.get_state()
                
            self.__add_state(state)            

            self.m_state_lock.notifyAll()

        finally:    
            if fLock:
                self.m_state_lock.release()

        if self.m_event_dispatcher_output is not None:
            event = CEventState(state)
            self.m_event_dispatcher_output.fire_event(event)

        
    def wait_for_state(self, state_list):
        """
        Wait for any of the states in the state list.
        """
        
        try:
            self.m_state_lock.acquire()

            if self.get_state() in state_list:
                return self.get_state()
            
            while True:
                index = self.__add_waiter()
            
                self.m_state_lock.wait(PING_TIMEOUT)

                states = self.__get_states(index)
                self.__remove_waiter(index)

                for state in states:
                    if state in state_list:
                        return state
            
        finally:
            self.m_state_lock.release()


    def acquire(self):
        self.m_state_lock.acquire()


    def release(self):
        self.m_state_lock.release()



#
# -------------------------------------- Break Info manager ---------------------------------------
#



def CalcValidLines(code):
    l = code.co_firstlineno
    vl = [l]

    bl = [ord(c) for c in code.co_lnotab[2::2]]
    sl = [ord(c) for c in code.co_lnotab[1::2]]

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
        if is_blender_file(self.m_filename):
            lines = get_blender_source(self.m_filename)
            source = '\n'.join(lines) + '\n'
        else:    
            fn = g_found_unicode_files.get(self.m_filename, self.m_filename)
            f = open(fn, "r")
            source = f.read()
            f.close()
        
        self.__CalcBreakInfoFromSource(source)


    def __CalcBreakInfoFromSource(self, source):
        _source = source.replace('\r\n', '\n') + '\n'
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
            _fqn = '.'.join(fqn)
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



#
# -------------------------------- Break Point Manager -----------------------------
#



class CBreakPoint:    
    def __init__(self, filename, scope_fqn, scope_first_line, lineno, fEnabled, expr, fTemporary = False):
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
        self.m_code = None
        self.m_fTemporary = fTemporary

        if (expr is not None) and (expr != ''):
            self.m_code = compile(expr, '', 'eval')

        
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
                id_list = self.m_break_points_by_id.keys()
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

            for bp in self.m_break_points_by_id.values():
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
        for bp in bpm.values():
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

        bp = CBreakPoint(_filename, s.m_fqn, s.m_first_line, l, fEnabled = True, expr = '', fTemporary = True)

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


    def set_breakpoint(self, filename, scope, lineno, fEnabled, expr):
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

        bp = CBreakPoint(_filename, s.m_fqn, s.m_first_line, l, fEnabled, expr)

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
                
                bpids = self.m_break_points_by_id.keys()
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
                id_list = self.m_break_points_by_id.keys()

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
                id_list = self.m_break_points_by_id.keys()

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
                id_list = self.m_break_points_by_id.keys()

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



#
# ----------------------------------- Core Debugger ------------------------------------
#



class CCodeContext:
    """
    Class represents info related to code objects.
    """
    
    def __init__(self, frame, bp_manager):
        self.m_code = frame.f_code
        self.m_filename = calc_frame_path(frame)
        self.m_basename = os.path.basename(self.m_filename)

        self.m_file_breakpoints = bp_manager.get_active_break_points_by_file(self.m_filename)

        self.m_fExceptionTrap = False


    def is_untraced(self):
        """
        Return True if this code object should not be traced.
        """
        
        return self.m_basename in [THREADING_FILENAME, DEBUGGER_FILENAME]


    def is_exception_trap_frame(self):
        """
        Return True if this frame should be a trap for unhandled
        exceptions.
        """
        
        if self.m_basename == THREADING_FILENAME:
            return True

        if self.m_basename == DEBUGGER_FILENAME and self.m_code.co_name in ['__execv', '__execve', '__function_wrapper']:
            return True

        return False



class CDebuggerCoreThread:
    """
    Class represents a debugged thread.
    This is a core structure of the debugger. It includes most of the
    optimization tricks and hacks, and includes a good amount of 
    subtle bug fixes, be carefull not to mess it up...
    """
    
    def __init__(self, name, core_debugger, frame, event):
        self.m_thread_id = thread.get_ident()
        self.m_thread_name = name
        self.m_fBroken = False
        self.m_fUnhandledException = False
        
        self.m_frame = frame
        self.m_event = event
        self.m_ue_lineno = None
        self.m_uef_lineno = None
        
        self.m_code_context = core_debugger.get_code_context(frame)

        self.m_locals_copy = {}

        self.m_core = core_debugger
        self.m_bp_manager = core_debugger.m_bp_manager

        self.m_frame_lock = threading.Condition(threading.Lock())
        self.m_frame_external_references = 0

        
    def profile(self, frame, event, arg): 
        """
        Profiler method.
        The Python profiling mechanism is used by the debugger
        mainly to handle synchronization issues related to the 
        life time of the frame structure.
        """
        
        if event == 'return':            
            self.m_frame = frame.f_back

            try:
                self.m_code_context = self.m_core.m_code_contexts[self.m_frame.f_code]
            except AttributeError:
                if self.m_event != 'return' and self.m_core.m_ftrap:
                    #
                    # An exception is raised from the outer-most frame.
                    # This means an unhandled exception.
                    #
                
                    self.m_frame = frame
                    self.m_event = 'exception'
                    
                    self.m_uef_lineno = self.m_ue_lineno
                    
                    self.m_fUnhandledException = True                    
                    self.m_core._break(self, frame, event, arg)
                    
                    self.m_uef_lineno = None 
                    
                    if frame in self.m_locals_copy:
                        self.update_locals()

                    self.m_frame = None
                
                self.m_core.remove_thread(self.m_thread_id)
                sys.setprofile(None)
                sys.settrace(self.m_core.trace_dispatch_init)
            
            if self.m_frame_external_references == 0:
                return

            #
            # Wait until no one references the frame object
            #
            
            try:
                self.m_frame_lock.acquire() 

                while self.m_frame_external_references != 0:
                    self.m_frame_lock.wait(1.0)

            finally:
                self.m_frame_lock.release()

                            
    def frame_acquire(self):
        """
        Aquire a reference to the frame.
        """
        
        try:
            self.m_frame_lock.acquire()
            
            self.m_frame_external_references += 1
            f = self.m_frame
            if f is None:
                raise ThreadDone

            return f    

        finally:    
            self.m_frame_lock.release()


    def frame_release(self):
        """
        Release a reference to the frame.
        """
        
        try:
            self.m_frame_lock.acquire()
                
            self.m_frame_external_references -= 1
            if self.m_frame_external_references == 0:
                self.m_frame_lock.notify()

        finally:    
            self.m_frame_lock.release()

        
    def get_frame(self, base_frame, index, fException = False):
        """
        Get frame at index depth down the stack.
        Starting from base_frame return the index depth frame 
        down the stack. If fException is True use the exception
        stack (traceback).
        """
        
        if fException:
            tb = base_frame.f_exc_traceback
            if tb is None:
                raise NoExceptionFound
                
            while tb.tb_next is not None:
                tb = tb.tb_next

            f = tb.tb_frame
        else:    
            f = base_frame
            
        while (index > 0) and (f is not None):
            f = f.f_back
            index -= 1

        if (index < 0) or (f is None):
            raise InvalidFrame

        if (self.m_uef_lineno is not None) and (f.f_back is None):
            lineno = self.m_uef_lineno
        else:    
            lineno = f.f_lineno
            
        if fException:
            tb = base_frame.f_exc_traceback
            while tb is not None:
                if tb.tb_frame == f:
                    lineno = tb.tb_lineno
                    break
                tb = tb.tb_next

        return (f, lineno)  


    def get_locals_copy(self, frame_index, fException, fReadOnly):
        """
        Get globals and locals of frame.
        A copy scheme is used for locals to work around a bug in 
        Python 2.3 and 2.4 that prevents modifying the local dictionary.
        """
        
        try:
            base_frame = self.frame_acquire()

            (f, lineno) = self.get_frame(base_frame, frame_index, fException)

            if fReadOnly:
                gc = copy.copy(f.f_globals)
            else:    
                gc = f.f_globals

            try:
                (lc, olc) = self.m_locals_copy[f]

            except KeyError:
                if f.f_code.co_name in [MODULE_SCOPE, MODULE_SCOPE2]:
                    lc = gc
                    olc = gc
                    
                else:    
                    lc = copy.copy(f.f_locals)
                    olc = copy.copy(lc)
                    
                    if not fReadOnly:
                        self.m_locals_copy[f] = (lc, olc)
                        self.set_local_trace(f)

            return (gc, lc, olc)

        finally:
            f = None
            base_frame = None
            
            self.frame_release()


    def update_locals_copy(self):
        """
        Update copy of locals with changes in locals.
        """
        
        lct = self.m_locals_copy.get(self.m_frame, None)
        if lct is None:
            return

        (lc, base) = lct
        cr = copy.copy(self.m_frame.f_locals)
        
        b = [(k, repr(v)) for k, v in base.items()]
        sb = sets.Set(b)

        c = [(k, repr(v)) for k, v in cr.items()]
        sc = sets.Set(c)

        nsc = [k for (k, v) in sc - sb]

        for k in nsc:
            lc[k] = cr[k]

            
    def update_locals(self):
        """
        Update locals with changes from copy of locals.
        """
        
        lct = self.m_locals_copy.pop(self.m_frame, None)
        if lct is None:
            return

        self.m_frame.f_locals.update(lct[0])

            
    def __eval_breakpoint(self, frame, bp):
        """
        Return True if the breakpoint is hit.
        """
        
        if not bp.m_fEnabled:
            return False

        if bp.m_expr == '':
            return True

        try:
            if frame in self.m_locals_copy:
                l = self.m_locals_copy[frame][0]
                v = eval(bp.m_code, frame.f_globals, l)
            else:
                v = eval(bp.m_code, frame.f_globals, frame.f_locals)
                
            return (v != False)
            
        except:
            return False


    def set_local_trace(self, frame):
        """
        Set trace callback of frame. 
        Specialized trace methods are selected here to save switching time 
        during actual tracing.
        """
        
        if not self.m_core.m_ftrace:
            frame.f_trace = self.trace_dispatch_stop
            return

        code_context = self.m_core.get_code_context(frame)

        if self.m_core.is_break(self, frame):
            frame.f_trace = self.trace_dispatch_break
            
        elif code_context.m_fExceptionTrap or (frame.f_back is None):    
            frame.f_trace = self.trace_dispatch_trap
            
        elif frame.f_code.co_name in self.m_bp_manager.m_break_points_by_function:
            frame.f_trace = self.trace_dispatch
            
        elif frame in self.m_locals_copy:
            frame.f_trace = self.trace_dispatch
            
        elif frame == self.m_core.m_return_frame:
            frame.f_trace = self.trace_dispatch
            
        else:    
            del frame.f_trace


    def set_tracers(self): 
        """
        Set trace callbacks for all frames in stack.
        """
        
        try:
            try:
                f = self.frame_acquire()
                while f is not None:
                    self.set_local_trace(f)
                    f = f.f_back
                    
            except ThreadDone:
                f = None
                
        finally:      
            f = None
            self.frame_release()


    def trace_dispatch_stop(self, frame, event, arg):
        """
        Disable tracing for this thread.
        """
        
        if frame in self.m_locals_copy:
            self.update_locals()

        sys.settrace(None)
        sys.setprofile(None)
        return None


    def trace_dispatch_break(self, frame, event, arg):
        """
        Trace method for breaking a thread.
        """
        
        if event not in ['line', 'return', 'exception']:
            return frame.f_trace

        if event == 'exception':
            self.set_exc_info(arg)
            
        self.m_event = event

        if frame in self.m_locals_copy:
            self.update_locals_copy()

        self.m_core._break(self, frame, event, arg)

        if frame in self.m_locals_copy:
            self.update_locals()
            self.set_local_trace(frame)
        
        return frame.f_trace            


    def trace_dispatch_call(self, frame, event, arg):
        """
        Initial trace method for thread.
        """
        
        if not self.m_core.m_ftrace:
            return self.trace_dispatch_stop(frame, event, arg)
            
        self.m_frame = frame

        try:
            self.m_code_context = self.m_core.m_code_contexts[frame.f_code]
        except KeyError:
            self.m_code_context = self.m_core.get_code_context(frame)

        if self.m_core.m_fBreak or (self.m_core.m_step_tid == self.m_thread_id):
            self.m_event = event
            self.m_core._break(self, frame, event, arg)
            if frame in self.m_locals_copy:
                self.update_locals()
                self.set_local_trace(frame)
            return frame.f_trace

        if not frame.f_code.co_name in self.m_bp_manager.m_break_points_by_function:
            return None

        bp = self.m_code_context.m_file_breakpoints.get(frame.f_lineno, None)
        if bp is not None and self.__eval_breakpoint(frame, bp): 
            self.m_event = event
            self.m_core._break(self, frame, event, arg)
            if frame in self.m_locals_copy:
                self.update_locals()
                self.set_local_trace(frame)
            return frame.f_trace     
    
        return self.trace_dispatch     

        
    def trace_dispatch(self, frame, event, arg):
        """
        General trace method for thread.
        """
        
        if (event == 'line'):
            if frame in self.m_locals_copy:
                self.update_locals_copy()

            bp = self.m_code_context.m_file_breakpoints.get(frame.f_lineno, None)                

            if bp is not None and self.__eval_breakpoint(frame, bp): 
                self.m_event = event
                self.m_core._break(self, frame, event, arg)
                
            if frame in self.m_locals_copy:
                self.update_locals()
                self.set_local_trace(frame)

            return frame.f_trace     
                        
        if event == 'return':
            if frame in self.m_locals_copy:
                self.update_locals_copy()

            if frame == self.m_core.m_return_frame:
                self.m_event = event
                self.m_core._break(self, frame, event, arg)
                
            if frame in self.m_locals_copy:
                self.update_locals()

            return None     
            
        if event == 'exception':
            if frame in self.m_locals_copy:
                self.update_locals()
                self.set_local_trace(frame)

            if not frame.f_exc_traceback is arg[2]:
                (frame.f_exc_type, frame.f_exc_value, frame.f_exc_traceback) = arg

            return frame.f_trace     

        return frame.f_trace     

        
    def trace_dispatch_trap(self, frame, event, arg):
        """
        Trace method used for frames in which unhandled exceptions
        should be caught.
        """
        
        if (event == 'line'):
            self.m_event = event

            if frame in self.m_locals_copy:
                self.update_locals_copy()

            bp = self.m_code_context.m_file_breakpoints.get(frame.f_lineno, None)                
            if bp is not None and self.__eval_breakpoint(frame, bp): 
                self.m_core._break(self, frame, event, arg)
                
            if frame in self.m_locals_copy:
                self.update_locals()
                self.set_local_trace(frame)

            return frame.f_trace     
                        
        if event == 'return':
            last_event = self.m_event
            self.m_event = event

            if frame in self.m_locals_copy:
                self.update_locals_copy()

            if frame == self.m_core.m_return_frame:
                self.m_core._break(self, frame, event, arg)
                
            if frame in self.m_locals_copy:
                self.update_locals()

            if last_event == 'exception':
                self.m_event = last_event
                
            return None     
            
        if event == 'exception':
            self.m_event = event

            if self.m_code_context.m_fExceptionTrap and self.m_core.m_ftrap:                
                self.set_exc_info(arg)
                
                self.m_fUnhandledException = True
                self.m_core._break(self, frame, event, arg)

                if frame in self.m_locals_copy:
                    self.update_locals()
                    
                return frame.f_trace

            self.m_ue_lineno = frame.f_lineno
            
            if frame in self.m_locals_copy:
                self.update_locals()
                self.set_local_trace(frame)

            if not frame.f_exc_traceback is arg[2]:
                (frame.f_exc_type, frame.f_exc_value, frame.f_exc_traceback) = arg

            return frame.f_trace     

        return frame.f_trace     

        
    def set_exc_info(self, arg):
        """
        Set exception information in frames of stack.
        """
        
        (t, v, tb) = arg

        while tb is not None:
            f = tb.tb_frame            
            f.f_exc_type = t
            f.f_exc_value = v 
            f.f_exc_traceback = tb

            tb = tb.tb_next


    def is_breakpoint(self):
        """
        Calc if current line is hit by breakpoint.
        """
        
        bp = self.m_code_context.m_file_breakpoints.get(self.m_frame.f_lineno, None)
        if bp is not None and self.__eval_breakpoint(self.m_frame, bp):
            return True

        return False    


    def get_breakpoint(self):
        """
        Return current line breakpoint if any.
        """
        
        return self.m_code_context.m_file_breakpoints.get(self.m_frame.f_lineno, None)



class CDebuggerCore:
    """
    Base class for the debugger. 
    Handles basic debugger functionality.
    """
    
    def __init__(self, fembedded = False):
        self.m_ftrace = True

        self.m_current_ctx = None 
        self.m_f_first_to_break = True
        self.m_f_break_on_init = False
        
        self.m_builtins_hack = None

        self.m_timer_embedded_giveup = None
        
        self.m_threads_lock = threading.Condition(threading.Lock())

        self.m_threads = {}

        self.m_event_dispatcher = CEventDispatcher()
        self.m_state_manager = CStateManager(STATE_RUNNING, self.m_event_dispatcher)

        self.m_ffork_into_child = False
        self.m_ffork_auto = False

        self.m_ftrap = True
        self.m_fUnhandledException = False        
        self.m_fBreak = False

        self.m_lastest_event = None
        self.m_step_tid = None
        self.m_next_frame = None
        self.m_return_frame = None       
        self.m_saved_step = (None, None, None)
        self.m_saved_next = None

        self.m_bp_manager = CBreakPointsManager()

        self.m_code_contexts = {None: None}

        self.m_fembedded = fembedded

        self.m_heartbeats = {0: time.time() + 3600}
        

    def shutdown(self):
        self.m_event_dispatcher.shutdown()
        self.m_state_manager.shutdown()

        
    def is_embedded(self):
        return self.m_fembedded

        
    def send_fork_switch(self, sync_n):
        """
        Notify client that debuggee is forking and that it should
        try to reconnect to the child.
        """
        
        print_debug('Sending fork switch event')

        event = CEventForkSwitch(sync_n)
        self.m_event_dispatcher.fire_event(event)


    def send_exec_switch(self, sync_n):
        """
        Notify client that debuggee is doing an exec and that it should 
        try to reconnect (in case the exec failed).
        """
        
        print_debug('Sending exec switch event')

        event = CEventExecSwitch(sync_n)
        self.m_event_dispatcher.fire_event(event)


    def send_event_exit(self):
        """
        Notify client that the debuggee is shutting down.
        """
        
        event = CEventExit()
        self.m_event_dispatcher.fire_event(event)


    def send_events(self, event):
        pass

        
    def set_request_go_timer(self, timeout):
        """
        Set timeout thread to release debugger from waiting for a client
        to attach.
        """
        
        if timeout is None:
            return
            
        _timeout = max(5.0, timeout)
        self.m_timer_embedded_giveup = threading.Timer(_timeout, self.request_go)
        self.m_timer_embedded_giveup.start()

    
    def cancel_request_go_timer(self):
        t = self.m_timer_embedded_giveup
        if t is not None:
            self.m_timer_embedded_giveup = None
            t.cancel()


    def setbreak(self, f):
        """
        Set thread to break on next statement.
        """
        
        if not self.m_ftrace:
            return 
            
        tid = thread.get_ident()

        if not tid in self.m_threads:
            return self.settrace(f)
        
        ctx = self.m_threads[tid]
        f.f_trace = ctx.trace_dispatch_break
        self.m_saved_next = self.m_next_frame
        self.m_next_frame = f

        
    def settrace(self, f = None, f_break_on_init = True, timeout = None, builtins_hack = None):
        """
        Start tracing mechanism for thread.
        """
        
        if not self.m_ftrace:
            return 
            
        tid = thread.get_ident()
        if tid in self.m_threads:
            return

        self.set_request_go_timer(timeout)
            
        self.m_f_break_on_init = f_break_on_init
        self.m_builtins_hack = builtins_hack
        
        threading.settrace(self.trace_dispatch_init)
        sys.settrace(self.trace_dispatch_init)

        if f is not None:
            f.f_trace = self.trace_dispatch_init


    def stoptrace(self):
        """
        Stop tracing mechanism.
        """
        
        global g_fignore_atexit
        
        g_fignore_atexit = True

        threading.settrace(None)
        sys.settrace(None)
        sys.setprofile(None)
        
        self.m_ftrace = False
        self.set_all_tracers()

        try:
            self.request_go()
        except DebuggerNotBroken:
            pass
            
        #self.m_threads = {}


    def get_code_context(self, frame):
        try:
            return self.m_code_contexts[frame.f_code]
        except KeyError:
            if self.m_builtins_hack != None:
                if calc_frame_path(frame) == self.m_builtins_hack:
                    self.m_builtins_hack = None
                    frame.f_globals['__builtins__'] = sys.modules['__builtin__']

            code_context = CCodeContext(frame, self.m_bp_manager)
            return self.m_code_contexts.setdefault(frame.f_code, code_context)


    def get_current_ctx(self):
        if len(self.m_threads) == 0:
            raise NoThreads

        return self.m_current_ctx 

        
    def wait_for_first_thread(self):
        """
        Wait until at least one debuggee thread is alive.
        Python can have 0 threads in some circumstances as
        embedded Python and the Python interpreter console.
        """
        
        if self.m_current_ctx is not None:
            return

        try:
            self.m_threads_lock.acquire() 

            while self.m_current_ctx is None:
                self.m_threads_lock.wait(1.0)

        finally:
            self.m_threads_lock.release()


    def notify_first_thread(self):
        """
        Notify that first thread is available for tracing.
        """
        
        try:
            self.m_threads_lock.acquire()
            self.m_threads_lock.notify()
        finally:
            self.m_threads_lock.release()


    def set_exception_trap_frame(self, frame):
        """
        Set trap for unhandled exceptions in relevant frame.
        """
        
        while frame is not None:
            code_context = self.get_code_context(frame)
            if code_context.is_exception_trap_frame():                
                code_context.m_fExceptionTrap = True
                return

            frame = frame.f_back


    def trace_dispatch_init(self, frame, event, arg):   
        """
        Initial tracing method.
        """
        
        if event not in ['call', 'line', 'return']:
            return None

        code_context = self.get_code_context(frame)
        if event == 'call' and code_context.is_untraced():
            return None

        self.set_exception_trap_frame(frame)

        try:
            t = threading.currentThread()
            name = t.getName()
        except:
            name = ''
        
        ctx = CDebuggerCoreThread(name, self, frame, event)
        ctx.set_tracers()
        self.m_threads[ctx.m_thread_id] = ctx

        if len(self.m_threads) == 1:
            g_blender_text.clear()
            
            self.m_current_ctx = ctx
            self.notify_first_thread()

            if self.m_f_break_on_init:
                self.m_f_break_on_init = False
                self.request_break()

        sys.settrace(ctx.trace_dispatch_call)
        sys.setprofile(ctx.profile)
        
        if event == 'call':
            return ctx.trace_dispatch_call(frame, event, arg)
        elif hasattr(frame, 'f_trace') and (frame.f_trace is not None):    
            return frame.f_trace(frame, event, arg)
        else:
            return None


    def set_all_tracers(self):
        """
        Set trace methods for all frames of all threads.
        """
        
        for ctx in self.m_threads.values():
            ctx.set_tracers()

            
    def remove_thread(self, thread_id):
        try:
            del self.m_threads[thread_id]
            
            if self.m_current_ctx.m_thread_id == thread_id:
                self.m_current_ctx = self.m_threads.values()[0]
                
        except (KeyError, IndexError):
            pass            


    def set_break_flag(self):
        self.m_fBreak = (self.m_state_manager.get_state() == STATE_BROKEN)

        
    def is_break(self, ctx, frame, event = None):
        if self.m_fBreak:
            return True

        if ctx.m_fUnhandledException:
            return True
            
        if self.m_step_tid == ctx.m_thread_id:
            return True

        if self.m_next_frame == frame:
            return True

        if (self.m_return_frame == frame) and (event == 'return'):
            return True

        return False    

    
    def record_client_heartbeat(self, id, finit, fdetach):
        """
        Record that client id is still attached.
        """
       
        if finit:
            self.m_heartbeats.pop(0, None)

        if fdetach:
            self.m_heartbeats.pop(id, None)
            return

        if finit or id in self.m_heartbeats:
            self.m_heartbeats[id] = time.time()


    def get_clients_attached(self):
        n = 0
        t = time.time()
        
        for v in self.m_heartbeats.values():
            if t < v + HEARTBEAT_TIMEOUT:
                n += 1

        return n


    def _break(self, ctx, frame, event, arg):
        """
        Main break logic.
        """

        global g_fos_exit
        global g_module_main
        
        if not self.is_break(ctx, frame, event) and not ctx.is_breakpoint():
            ctx.set_tracers()
            return 
            
        ctx.m_fBroken = True
        f_full_notification = False
        f_uhe_notification = False
        
        try: 
            self.m_state_manager.acquire()
            if self.m_state_manager.get_state() != STATE_BROKEN:
                self.set_break_dont_lock()

            if g_module_main == -1:
                try:
                    g_module_main = sys.modules['__main__']
                except:
                    g_module_main = None

            if not frame.f_exc_traceback is None:
                ctx.set_exc_info((frame.f_exc_type, frame.f_exc_value, frame.f_exc_traceback))

            try:
                t = threading.currentThread()
                ctx.m_thread_name = t.getName()
            except:
                pass
            
            if ctx.m_fUnhandledException and not self.m_fUnhandledException:
                self.m_fUnhandledException = True
                f_uhe_notification = True
            
            if self.is_auto_fork_first_stage(ctx.m_thread_id):
                self.m_saved_step = (self.m_step_tid, self.m_saved_next, self.m_return_frame)
                self.m_saved_next = None
                self.m_bp_manager.m_fhard_tbp = True

            if self.m_f_first_to_break or (self.m_current_ctx == ctx):                
                self.m_current_ctx = ctx
                self.m_lastest_event = event

                self.m_step_tid = None
                self.m_next_frame = None
                self.m_return_frame = None       
                self.m_saved_next = None

                self.m_bp_manager.del_temp_breakpoint(breakpoint = ctx.get_breakpoint())

                self.m_f_first_to_break = False
                f_full_notification = True

        finally:
            self.m_state_manager.release()

        ffork_second_stage = self.handle_fork(ctx)
        self.handle_exec(ctx)

        if self.is_auto_fork_first_stage(ctx.m_thread_id):
            self.request_go_quiet()

        elif self.m_ffork_auto and ffork_second_stage:
            (self.m_step_tid, self.m_next_frame, self.m_return_frame) = self.m_saved_step
            self.m_saved_step = (None, None, None)
            self.m_bp_manager.m_fhard_tbp = False
            self.request_go_quiet()

        elif self.get_clients_attached() == 0:
            #print_debug('state: %s' % self.m_state_manager.get_state())
            self.request_go_quiet()

        else:
            if f_full_notification:
                self.send_events(None) 
            else:
                self.notify_thread_broken(ctx.m_thread_id, ctx.m_thread_name)
                self.notify_namespace()

            if f_uhe_notification:
                self.send_unhandled_exception_event()
                
            state = self.m_state_manager.wait_for_state([STATE_RUNNING])
      
        self.prepare_fork_step(ctx.m_thread_id)
        self.prepare_exec_step(ctx.m_thread_id)

        ctx.m_fUnhandledException = False
        ctx.m_fBroken = False 
        ctx.set_tracers()

        if g_fos_exit:
            g_fos_exit = False
            self.send_event_exit()
            
            time.sleep(1.0)


    def is_auto_fork_first_stage(self, tid):
        if not self.m_ffork_auto:
            return False

        return tid == g_forktid and g_forkpid == None


    def prepare_fork_step(self, tid):
        global g_forkpid
        global g_ignore_broken_pipe

        if tid != g_forktid:
            return

        self.m_step_tid = tid
        g_forkpid = os.getpid()
        
        if not self.m_ffork_into_child:
            return

        n = self.get_clients_attached()
        self.send_fork_switch(n)
        time.sleep(0.5)
        g_server.shutdown()
        CThread.joinAll()

        g_ignore_broken_pipe = time.time()


    def handle_fork(self, ctx):
        global g_forktid
        global g_forkpid

        tid = ctx.m_thread_id

        if g_forkpid == None or tid != g_forktid:
            return False

        forkpid = g_forkpid
        g_forkpid = None
        g_forktid = None

        if os.getpid() == forkpid:
            #
            # Parent side of fork().
            #

            if not self.m_ffork_into_child:
                #CThread.clearJoin()
                #g_server.jumpstart()
               
                return True

            self.stoptrace()
            return False

        #
        # Child side of fork().
        #

        if not self.m_ffork_into_child:
            self.stoptrace()
            return False
       
        self.m_threads = {tid: ctx}
        
        CThread.clearJoin()
        g_server.jumpstart()
        
        return True


    def prepare_exec_step(self, tid):
        global g_execpid

        if tid != g_exectid:
            return

        self.m_step_tid = tid
        g_execpid = os.getpid()

        n = self.get_clients_attached()
        self.send_exec_switch(n)
        time.sleep(0.5)
        g_server.shutdown()
        CThread.joinAll()


    def handle_exec(self, ctx):
        global g_exectid
        global g_execpid

        tid = ctx.m_thread_id

        if g_execpid == None or tid != g_exectid:
            return False

        g_execpid = None
        g_exectid = None

        #
        # If we are here it means that the exec failed.
        # Jumpstart the debugger to allow debugging to continue.
        #

        CThread.clearJoin()
        g_server.jumpstart()
        
        return True


    def notify_thread_broken(self, tid, name):
        """
        Notify that thread (tid) has broken.
        This notification is sent for each thread that breaks after
        the first one.
        """
        
        _event = CEventThreadBroken(tid, name)
        self.m_event_dispatcher.fire_event(_event)

    
    def notify_namespace(self):
        """
        Notify that a namespace update query should be done.
        """
        
        _event = CEventNamespace()
        self.m_event_dispatcher.fire_event(_event)


    def get_state(self):
        return self.m_state_manager.get_state()


    def verify_broken(self):
        if self.m_state_manager.get_state() != STATE_BROKEN:
            raise DebuggerNotBroken

    
    def get_current_filename(self, frame_index, fException):
        """
        Return path of sources corresponding to the frame at depth
        'frame_index' down the stack of the current thread.
        """
        
        ctx = self.get_current_ctx()
        
        try:
            f = None
            base_frame = ctx.frame_acquire()

            (f, frame_lineno) = ctx.get_frame(base_frame, frame_index, fException)
            frame_filename = calc_frame_path(f)

            return frame_filename

        finally:
            f = None
            base_frame = None            
            ctx.frame_release()

        
    def get_threads(self):
        return self.m_threads


    def set_break_dont_lock(self):
        self.m_f_first_to_break = True            

        self.m_state_manager.set_state(STATE_BROKEN, fLock = False)

        self.set_break_flag()
        self.set_all_tracers()


    def request_break(self):
        """
        Ask debugger to break (pause debuggee).
        """
        
        if len(self.m_threads) == 0:
            self.wait_for_first_thread()
        
        try:
            self.m_state_manager.acquire()
            if self.m_state_manager.get_state() == STATE_BROKEN:
                return

            self.set_break_dont_lock()

        finally:    
            self.m_state_manager.release()

        self.send_events(None)


    def request_go_quiet(self, fLock = True):
        try:
            self.request_go(fLock)
        
        except DebuggerNotBroken:
            pass


    def request_go(self, fLock = True):
        """
        Let debugger run.
        """
        
        try:
            if fLock:
                self.m_state_manager.acquire()
                
            self.verify_broken()

            self.m_fUnhandledException = False
            self.m_state_manager.set_state(STATE_RUNNING, fLock = False)

            if self.m_fembedded:
                time.sleep(0.33)
                
            self.set_break_flag()

        finally:    
            if fLock:
                self.m_state_manager.release()


    def request_go_breakpoint(self, filename, scope, lineno, frame_index, fException):
        """
        Let debugger run until temp breakpoint as defined in the arguments.
        """
        
        try:
            self.m_state_manager.acquire()
            self.verify_broken()

            if filename in [None, '']:
                _filename = self.get_current_filename(frame_index, fException)
            elif is_blender_file(filename):
                _filename = filename
            else:
                _filename = FindFile(filename, fModules = True)

            self.m_bp_manager.set_temp_breakpoint(_filename, scope, lineno)
            self.set_all_tracers()
            self.request_go(fLock = False)

        finally:    
            self.m_state_manager.release()


    def request_step(self, fLock = True):
        """
        Let debugger run until next statement is reached or a breakpoint 
        is hit in another thread.
        """
        
        try:
            if fLock:
                self.m_state_manager.acquire()
                
            self.verify_broken()

            try:
                ctx = self.get_current_ctx()
            except NoThreads:
                return
                
            self.m_step_tid = ctx.m_thread_id
            self.m_next_frame = None
            self.m_return_frame = None       

            self.request_go(fLock = False)

        finally:    
            if fLock:
                self.m_state_manager.release()

        
    def request_next(self): 
        """
        Let debugger run until next statement in the same frame 
        is reached or a breakpoint is hit in another thread.
        """
        
        try:
            self.m_state_manager.acquire()
            self.verify_broken()

            try:
                ctx = self.get_current_ctx()
            except NoThreads:
                return
                
            if self.m_lastest_event in ['return', 'exception']:
                return self.request_step(fLock = False)

            self.m_next_frame = ctx.m_frame
            self.m_return_frame = None
            
            self.request_go(fLock = False)

        finally:    
            self.m_state_manager.release()

        
    def request_return(self):    
        """
        Let debugger run until end of frame frame is reached 
        or a breakpoint is hit in another thread.
        """
        
        try:
            self.m_state_manager.acquire()
            self.verify_broken()

            try:
                ctx = self.get_current_ctx()
            except NoThreads:
                return
                
            if self.m_lastest_event == 'return':
                return self.request_step(fLock = False)
                
            self.m_next_frame = None
            self.m_return_frame = ctx.m_frame

            self.request_go(fLock = False)

        finally:    
            self.m_state_manager.release()

        
    def request_jump(self, lineno):
        """
        Jump to line number 'lineno'.
        """
        
        try:
            self.m_state_manager.acquire()
            self.verify_broken()

            try:
                ctx = self.get_current_ctx()
            except NoThreads:
                return
                
            frame = ctx.m_frame
            code = frame.f_code

            valid_lines = CalcValidLines(code)
            sbi = CScopeBreakInfo('', valid_lines)
            l = sbi.CalcScopeLine(lineno)

            frame.f_lineno = l

        finally:    
            frame = None
            self.m_state_manager.release()

        self.send_events(None)


    def set_thread(self, tid):
        """
        Switch focus to specified thread.
        """
        
        try:
            self.m_state_manager.acquire()
            self.verify_broken()

            try:
                if (tid >= 0) and (tid < 100):
                    _tid = self.m_threads.keys()[tid]
                else:
                    _tid = tid
                    
                ctx = self.m_threads[_tid]
            except (IndexError, KeyError):
                raise ThreadNotFound

            self.m_current_ctx = ctx
            self.m_lastest_event = ctx.m_event

        finally:
            self.m_state_manager.release()

        self.send_events(None) 



class CDebuggerEngine(CDebuggerCore):
    """
    Main class for the debugger.
    Adds functionality on top of CDebuggerCore.
    """
    
    def __init__(self, fembedded = False):
        CDebuggerCore.__init__(self, fembedded)

        event_type_dict = {
            CEventState: {}, 
            CEventStackDepth: {}, 
            CEventBreakpoint: {}, 
            CEventThreads: {},
            CEventNoThreads: {},
            CEventThreadBroken: {},
            CEventNamespace: {},
            CEventUnhandledException: {},
            CEventStack: {},
            CEventExit: {},
            CEventForkSwitch: {},
            CEventExecSwitch: {},
            CEventTrap: {},
            CEventForkMode: {},
            CEventPsycoWarning: {}
            }

        self.m_event_queue = CEventQueue(self.m_event_dispatcher)
        self.m_event_queue.register_event_types(event_type_dict)

        event_type_dict = {CEventSync: {}}
        self.m_event_dispatcher.register_callback(self.send_events, event_type_dict, fSingleUse = False)


    def shutdown(self):
        self.m_event_queue.shutdown()
        
        CDebuggerCore.shutdown(self)


       
    def sync_with_events(self, fException, fSendUnhandled):
        """
        Send debugger state to client.
        """
        
        if len(self.m_threads) == 0:
            self.wait_for_first_thread()
        
        index = self.m_event_queue.get_event_index()
        event = CEventSync(fException, fSendUnhandled)
        self.m_event_dispatcher.fire_event(event)
        return index


    def trap_psyco_module(self):
        global g_fsent_psyco_warning
       
        if g_fsent_psyco_warning or not 'psyco' in sys.modules:
            return

        g_fsent_psyco_warning = True

        event = CEventPsycoWarning()
        self.m_event_dispatcher.fire_event(event)


    def wait_for_event(self, timeout, event_index):
        """
        Wait for new events and return them as list of events.
        """

        self.cancel_request_go_timer()
        self.trap_psyco_module()

        (new_event_index, sel) = self.m_event_queue.wait_for_event(timeout, event_index)
        return (new_event_index, sel)


    def set_breakpoint(self, filename, scope, lineno, fEnabled, expr, frame_index, fException):
        print_debug('Setting breakpoint to: %s, %s, %d' % (repr(filename), scope, lineno))

        if expr != '':
            try:
                compile(expr, '', 'eval')
            except:
                raise SyntaxError

        fLock = False
        
        try:    
            if filename in [None, '']:
                self.m_state_manager.acquire()
                fLock = True
                self.verify_broken()
                
                _filename = self.get_current_filename(frame_index, fException)
            elif is_blender_file(filename):
                _filename = filename
            else:
                _filename = FindFile(filename, fModules = True)
                
            bp = self.m_bp_manager.set_breakpoint(_filename, scope, lineno, fEnabled, expr)
            self.set_all_tracers()

            event = CEventBreakpoint(bp)
            self.m_event_dispatcher.fire_event(event)

        finally:
            if fLock:
                self.m_state_manager.release()

        
    def disable_breakpoint(self, id_list, fAll):
        self.m_bp_manager.disable_breakpoint(id_list, fAll)
        self.set_all_tracers()

        event = CEventBreakpoint(None, CEventBreakpoint.DISABLE, id_list, fAll)
        self.m_event_dispatcher.fire_event(event)

        
    def enable_breakpoint(self, id_list, fAll):
        self.m_bp_manager.enable_breakpoint(id_list, fAll)
        self.set_all_tracers()

        event = CEventBreakpoint(None, CEventBreakpoint.ENABLE, id_list, fAll)
        self.m_event_dispatcher.fire_event(event)

        
    def delete_breakpoint(self, id_list, fAll):
        self.m_bp_manager.delete_breakpoint(id_list, fAll)
        self.set_all_tracers()

        event = CEventBreakpoint(None, CEventBreakpoint.REMOVE, id_list, fAll)
        self.m_event_dispatcher.fire_event(event)

        
    def get_breakpoints(self):
        """
        return id->breakpoint dictionary.
        """
        
        bpl = self.m_bp_manager.get_breakpoints()
        _items = [(id, copy.copy(bp)) for (id, bp) in bpl.items()]
        for (id, bp) in _items:
            bp.m_code = None
            
        _bpl = dict(_items)
        
        return _bpl        


    def send_events(self, event):
        """
        Send series of events that define the debugger state.
        """
        
        if isinstance(event, CEventSync):
            fException = event.m_fException
            fSendUnhandled = event.m_fSendUnhandled
        else:
            fException = False
            fSendUnhandled = False

        try:
            if isinstance(event, CEventSync) and not fException:
                self.m_state_manager.set_state()
                
            self.send_stack_depth()
            self.send_threads_event(fException)
            self.send_stack_event(fException)
            self.send_namespace_event()

            if fSendUnhandled and self.m_fUnhandledException:
                self.send_unhandled_exception_event()
            
        except NoThreads:
            self.send_no_threads_event()
            
        except:
            print_debug_exception()
            raise

       
    def send_unhandled_exception_event(self):
        event = CEventUnhandledException()
        self.m_event_dispatcher.fire_event(event)

        
    def send_stack_depth(self):
        """
        Send event with stack depth and exception stack depth.
        """
        
        ctx = self.get_current_ctx()
        
        try:
            try:
                f = None
                f = ctx.frame_acquire()
            except ThreadDone:
                return

            try:
                g_traceback_lock.acquire()
                s = traceback.extract_stack(f)
                
            finally:    
                g_traceback_lock.release()

            stack_depth = len(s)

            if f.f_exc_traceback is None:
                stack_depth_exception = None
            else:    
                try:
                    g_traceback_lock.acquire()
                    _s = traceback.extract_tb(f.f_exc_traceback)
                    
                finally:    
                    g_traceback_lock.release()

                stack_depth_exception = stack_depth + len(_s) - 1

            event = CEventStackDepth(stack_depth, stack_depth_exception)
            self.m_event_dispatcher.fire_event(event)
            
        finally:
            f = None
            ctx.frame_release()

            
    def send_threads_event(self, fException):
        """
        Send event with current thread list.
        In case of exception, send only the current thread.
        """
        
        tl = self.get_thread_list()
            
        if fException:
            ctid = tl[0]
            itl = tl[1]
            _itl = [a for a in itl if a[DICT_KEY_TID] == ctid]
            _tl = (ctid, _itl)
        else:
            _tl = tl

        event = CEventThreads(*_tl)
        self.m_event_dispatcher.fire_event(event)


    def send_stack_event(self, fException):
        sl = self.get_stack([], False, fException)

        if len(sl) == 0:
            return
            
        event = CEventStack(sl[0])
        self.m_event_dispatcher.fire_event(event)

        
    def send_namespace_event(self):
        """
        Send event notifying namespace should be queried again.
        """
        
        event = CEventNamespace()
        self.m_event_dispatcher.fire_event(event)


    def send_no_threads_event(self):
        _event = CEventNoThreads()
        self.m_event_dispatcher.fire_event(_event)

        
    def __get_stack(self, ctx, ctid, fException):
        tid = ctx.m_thread_id    

        try:
            try:
                f = None
                f = ctx.frame_acquire()
            except ThreadDone:
                return None

            _f = f

            try:
                g_traceback_lock.acquire()
                s = traceback.extract_stack(f)
                
            finally:    
                g_traceback_lock.release()

            if fException: 
                if f.f_exc_traceback is None:
                    raise NoExceptionFound

                _tb = f.f_exc_traceback
                while _tb.tb_next is not None:
                    _tb = _tb.tb_next

                _f = _tb.tb_frame    
                    
                try:
                    g_traceback_lock.acquire()
                    _s = traceback.extract_tb(f.f_exc_traceback)
                    
                finally:    
                    g_traceback_lock.release()

                s = s[:-1] + _s

            code_list = []
            while _f is not None:
                rc = repr(_f.f_code).split(',')[0].split()[-1]
                code_list.insert(0, rc)
                _f = _f.f_back
                
        finally:
            f = None
            _f = None
            ctx.frame_release()

        #print code_list

        path_dict = {}
        for e in s:
            path = e[0]
            if path in path_dict:
                continue

            try:
                expanded_path = FindFile(path, fModules = True)
            except IOError:
                expanded_path = path

            path_dict[path] = winlower(expanded_path)                   
        
            #print >> sys.__stderr__, path, path_dict[path]
                
        __s = [(path_dict[a], b, c, d) for (a, b, c, d) in s]

        if (ctx.m_uef_lineno is not None) and (len(__s) > 0):
            (a, b, c, d) = __s[0]
            __s = [(a, ctx.m_uef_lineno, c, d)] + __s[1:] 
            
        r = {}
        r[DICT_KEY_STACK] = __s
        r[DICT_KEY_CODE_LIST] = code_list
        r[DICT_KEY_TID] = tid
        r[DICT_KEY_BROKEN] = ctx.m_fBroken
        r[DICT_KEY_EVENT] = ctx.m_event
        
        if tid == ctid:
            r[DICT_KEY_CURRENT_TID] = True
            
        return r

    
    def get_stack(self, tid_list, fAll, fException):
        if fException and (fAll or (len(tid_list) != 0)):
            raise BadArgument

        ctx = self.get_current_ctx()       
        ctid = ctx.m_thread_id

        if fAll:
            ctx_list = self.get_threads().values()
        elif fException or (len(tid_list) == 0):
            ctx_list = [ctx]
        else:
            ctx_list = [self.get_threads().get(t, None) for t in tid_list]

        _sl = [self.__get_stack(ctx, ctid, fException) for ctx in ctx_list if ctx is not None]
        sl = [s for s in _sl if s is not None] 
        
        return sl


    def get_source_file(self, filename, lineno, nlines, frame_index, fException):  
        if lineno < 1:
            lineno = 1
            nlines = -1

        _lineno = lineno
        r = {}
        frame_filename = None
        
        try:
            ctx = self.get_current_ctx()

            try:
                f = None
                base_frame = None
                
                base_frame = ctx.frame_acquire()
                (f, frame_lineno) = ctx.get_frame(base_frame, frame_index, fException)
                frame_filename = calc_frame_path(f)

            finally:
                f = None
                base_frame = None            
                ctx.frame_release()

            frame_event = [[ctx.m_event, 'call'][frame_index > 0], 'exception'][fException]
            
        except NoThreads:
            if filename in [None, '']:
                raise

        fBlender = False
        
        if filename in [None, '']:
            __filename = frame_filename
            r[DICT_KEY_TID] = ctx.m_thread_id
        elif is_blender_file(filename):
            fBlender = True
            __filename = filename
        else:    
            __filename = FindFile(filename, fModules = True)
            if not IsPythonSourceFile(__filename):
                raise NotPythonSource

        _filename = winlower(__filename)    

        lines = []
        breakpoints = {}
        fhide_pwd_mode = False

        while nlines != 0:
            try:
                g_traceback_lock.acquire()
                line = get_source_line(_filename, _lineno, fBlender)
                
            finally:    
                g_traceback_lock.release()

            if line == '':
                break

            #
            # Remove any trace of session password from data structures that 
            # go over the network.
            #

            if fhide_pwd_mode:
                if not ')' in line:
                    line = '...\n'
                else:
                    line = '...""")' + line.split(')', 1)[1]
                    fhide_pwd_mode = False

            elif 'start_embedded_debugger(' in line:
                ls = line.split('start_embedded_debugger(', 1)
                line = ls[0] + 'start_embedded_debugger("""...Removed-password-from-output...'
                
                if ')' in ls[1]:
                    line += '""")' + ls[1].split(')', 1)[1]
                else:
                    line += '\n'
                    fhide_pwd_mode = True

            lines.append(line)

            try:
                bp = self.m_bp_manager.get_breakpoint(_filename, _lineno)
                breakpoints[_lineno] = [STATE_DISABLED, STATE_ENABLED][bp.isEnabled()]
            except KeyError:
                pass
                
            _lineno += 1
            nlines -= 1

        if frame_filename == _filename:
            r[DICT_KEY_FRAME_LINENO] = frame_lineno
            r[DICT_KEY_EVENT] = frame_event
            r[DICT_KEY_BROKEN] = ctx.m_fBroken
            
        r[DICT_KEY_LINES] = lines
        r[DICT_KEY_FILENAME] = _filename
        r[DICT_KEY_BREAKPOINTS] = breakpoints
        r[DICT_KEY_FIRST_LINENO] = lineno
        
        return r

            
    def __get_source(self, ctx, nlines, frame_index, fException):
        tid = ctx.m_thread_id
        _frame_index = [0, frame_index][tid == self.m_current_ctx.m_thread_id]

        try:
            try:
                f = None
                base_frame = None
                
                base_frame = ctx.frame_acquire()
                (f, frame_lineno)  = ctx.get_frame(base_frame, _frame_index, fException)
                frame_filename = calc_frame_path(f)
                
            except (ThreadDone, InvalidFrame):
                return None

        finally:
            f = None
            base_frame = None            
            ctx.frame_release()
            
        frame_event = [[ctx.m_event, 'call'][frame_index > 0], 'exception'][fException]

        first_line = max(1, frame_lineno - nlines / 2)     
        _lineno = first_line

        fBlender = is_blender_file(frame_filename)
        lines = []
        breakpoints = {}
        fhide_pwd_mode = False
        
        while nlines != 0:
            try:
                g_traceback_lock.acquire()
                line = get_source_line(frame_filename, _lineno, fBlender)
                
            finally:    
                g_traceback_lock.release()

            if line == '':
                break

            #
            # Remove any trace of session password from data structures that 
            # go over the network.
            #

            if fhide_pwd_mode:
                if not ')' in line:
                    line = '...\n'
                else:
                    line = '...""")' + line.split(')', 1)[1]
                    fhide_pwd_mode = False

            elif 'start_embedded_debugger(' in line:
                ls = line.split('start_embedded_debugger(', 1)
                line = ls[0] + 'start_embedded_debugger("""...Removed-password-from-output...'
                
                if ')' in ls[1]:
                    line += '""")' + ls[1].split(')', 1)[1]
                else:
                    line += '\n'
                    fhide_pwd_mode = True

            lines.append(line)

            try:
                bp = self.m_bp_manager.get_breakpoint(frame_filename, _lineno)
                breakpoints[_lineno] = [STATE_DISABLED, STATE_ENABLED][bp.isEnabled()]
            except KeyError:
                pass
                
            _lineno += 1
            nlines -= 1

        r = {}
        
        r[DICT_KEY_FRAME_LINENO] = frame_lineno
        r[DICT_KEY_EVENT] = frame_event
        r[DICT_KEY_BROKEN] = ctx.m_fBroken
        r[DICT_KEY_TID] = tid
        r[DICT_KEY_LINES] = lines
        r[DICT_KEY_FILENAME] = frame_filename
        r[DICT_KEY_BREAKPOINTS] = breakpoints
        r[DICT_KEY_FIRST_LINENO] = first_line
        
        return r

     
    def get_source_lines(self, nlines, fAll, frame_index, fException):
        if fException and fAll:
            raise BadArgument
            
        if fAll:
            ctx_list = self.get_threads().values()
        else:
            ctx = self.get_current_ctx()
            ctx_list = [ctx]

        _sl = [self.__get_source(ctx, nlines, frame_index, fException) for ctx in ctx_list]
        sl = [s for s in _sl if s is not None]    

        return sl


    def __get_locals_globals(self, frame_index, fException, fReadOnly = False):
        ctx = self.get_current_ctx()
        (_globals, _locals, _original_locals_copy) = ctx.get_locals_copy(frame_index, fException, fReadOnly)

        return (_globals, _locals, _original_locals_copy)


    def __calc_attribute_list(self, r, fFilter):
        al = CalcDictKeys(r, fFilter)    
                
        if hasattr(r, '__class__') and not '__class__' in al:
            al = ['__class__'] + al

        if hasattr(r, '__bases__') and not '__bases__' in al:
            al = ['__bases__'] + al

        _al = [a for a in al if hasattr(r, a)] 
  
        return _al

    
    def __calc_number_of_subnodes(self, r):
        if self.__parse_type(type(r)) in BASIC_TYPES_LIST:
            return 0
       
        try:
            try:
                if isinstance(r, set) or isinstance(r, frozenset):
                    return len(r)

            except NameError:
                pass

            if isinstance(r, sets.BaseSet):
                return len(r)

            if isinstance(r, dict):
                return len(r)

            if isinstance(r, list):
                return len(r)

            if isinstance(r, tuple):
                return len(r)

            if hasattr(r, '__class__') or hasattr(r, '__bases__'):
                return 1

        except AttributeError:
            return 0

        return 0


    def __parse_type(self, t):
        rt = repr(t)
        st = rt.split("'")[1]
        return st


    def __calc_subnodes(self, expr, r, fForceNames, fFilter, repr_limit):
        snl = []
        
        try:
            if isinstance(r, set) or isinstance(r, frozenset):
                if len(r) > MAX_SORTABLE_LENGTH:
                    g = r
                else:
                    g = [i for i in r]
                    g.sort(SafeCmp)

                for i in g:
                    if len(snl) >= MAX_NAMESPACE_ITEMS:
                        snl.append(MAX_NAMESPACE_WARNING)
                        break
                    
                    is_valid = [True]
                    rk = repr_ltd(i, REPR_ID_LENGTH, fraw = True)

                    e = {}
                    e[DICT_KEY_EXPR] = '_RPDB2_FindRepr((%s), %d)["%s"]' % (expr, REPR_ID_LENGTH, rk.replace('"', '&quot'))
                    e[DICT_KEY_NAME] = repr_ltd(i, repr_limit)
                    e[DICT_KEY_REPR] = repr_ltd(i, repr_limit, is_valid)
                    e[DICT_KEY_IS_VALID] = is_valid[0]
                    e[DICT_KEY_TYPE] = self.__parse_type(type(i))
                    e[DICT_KEY_N_SUBNODES] = self.__calc_number_of_subnodes(i)

                    snl.append(e)
                
                return snl

        except NameError:
            pass
        
        if isinstance(r, sets.BaseSet):
            if len(r) > MAX_SORTABLE_LENGTH:
                g = r
            else:
                g = [i for i in r]
                g.sort(SafeCmp)

            for i in g:
                if len(snl) >= MAX_NAMESPACE_ITEMS:
                    snl.append(MAX_NAMESPACE_WARNING)
                    break

                is_valid = [True]
                rk = repr_ltd(i, REPR_ID_LENGTH, fraw = True)

                e = {}
                e[DICT_KEY_EXPR] = '_RPDB2_FindRepr((%s), %d)["%s"]' % (expr, REPR_ID_LENGTH, rk.replace('"', '&quot'))
                e[DICT_KEY_NAME] = repr_ltd(i, repr_limit)
                e[DICT_KEY_REPR] = repr_ltd(i, repr_limit, is_valid)
                e[DICT_KEY_IS_VALID] = is_valid[0]
                e[DICT_KEY_TYPE] = self.__parse_type(type(i))
                e[DICT_KEY_N_SUBNODES] = self.__calc_number_of_subnodes(i)

                snl.append(e)
            
            return snl

        if isinstance(r, list) or isinstance(r, tuple):
            for i, v in enumerate(r[0: MAX_NAMESPACE_ITEMS]):
                is_valid = [True]
                e = {}
                e[DICT_KEY_EXPR] = '(%s)[%d]' % (expr, i)
                e[DICT_KEY_NAME] = repr(i)
                e[DICT_KEY_REPR] = repr_ltd(v, repr_limit, is_valid)
                e[DICT_KEY_IS_VALID] = is_valid[0]
                e[DICT_KEY_TYPE] = self.__parse_type(type(v))
                e[DICT_KEY_N_SUBNODES] = self.__calc_number_of_subnodes(v)

                snl.append(e)

            if len(r) > MAX_NAMESPACE_ITEMS:
                snl.append(MAX_NAMESPACE_WARNING)

            return snl

        if isinstance(r, dict):
            if len(r) > MAX_SORTABLE_LENGTH:
                kl = r
            else:
                kl = r.keys()
                kl.sort(SafeCmp)

            for k in kl:
                #
                # Remove any trace of session password from data structures that 
                # go over the network.
                #
                if k in ['_RPDB2_FindRepr', '_rpdb2_args', '_rpdb2_pwd', 'm_rpdb2_pwd']:
                    continue

                v = r[k]

                if len(snl) >= MAX_NAMESPACE_ITEMS:
                    snl.append(MAX_NAMESPACE_WARNING)
                    break

                is_valid = [True]
                e = {}

                if type(k) in [bool, int, float, str, unicode, type(None)]:
                    rk = repr(k)
                    if len(rk) < REPR_ID_LENGTH:
                        e[DICT_KEY_EXPR] = '(%s)[%s]' % (expr, rk)

                if not DICT_KEY_EXPR in e:
                    rk = repr_ltd(k, REPR_ID_LENGTH, fraw = True)
                    e[DICT_KEY_EXPR] = '_RPDB2_FindRepr((%s), %d)["%s"]' % (expr, REPR_ID_LENGTH, rk.replace('"', '&quot'))

                e[DICT_KEY_NAME] = [repr_ltd(k, repr_limit), k][fForceNames]
                e[DICT_KEY_REPR] = repr_ltd(v, repr_limit, is_valid)
                e[DICT_KEY_IS_VALID] = is_valid[0]
                e[DICT_KEY_TYPE] = self.__parse_type(type(v))
                e[DICT_KEY_N_SUBNODES] = self.__calc_number_of_subnodes(v)

                snl.append(e)

            return snl            

        al = self.__calc_attribute_list(r, fFilter)
        al.sort(SafeCmp)

        for a in al:
            if a == 'm_rpdb2_pwd':
                continue

            try:
                v = getattr(r, a)
            except AttributeError:
                continue
            
            if len(snl) >= MAX_NAMESPACE_ITEMS:
                snl.append(MAX_NAMESPACE_WARNING)
                break

            is_valid = [True]
            e = {}
            e[DICT_KEY_EXPR] = '(%s).%s' % (expr, a)
            e[DICT_KEY_NAME] = a
            e[DICT_KEY_REPR] = repr_ltd(v, repr_limit, is_valid)
            e[DICT_KEY_IS_VALID] = is_valid[0]
            e[DICT_KEY_TYPE] = self.__parse_type(type(v))
            e[DICT_KEY_N_SUBNODES] = self.__calc_number_of_subnodes(v)

            snl.append(e)

        return snl                


    def get_exception(self, frame_index, fException):
        ctx = self.get_current_ctx()

        try:
            f = None
            base_frame = None
            
            base_frame = ctx.frame_acquire()
            (f, frame_lineno) = ctx.get_frame(base_frame, frame_index, fException)

            e = {'type': f.f_exc_type, 'value': f.f_exc_value, 'traceback': f.f_exc_traceback}

            return e
            
        finally:
            f = None
            base_frame = None            
            ctx.frame_release()


    def is_child_of_failure(self, failed_expr_list, expr):
        for failed_expr in failed_expr_list:
            if expr.startswith(failed_expr):
                return True

        return False        


    def calc_expr(self, expr, fExpand, fFilter, frame_index, fException, _globals, _locals, lock, rl, index, repr_limit):
        e = {}

        try:
            __globals = _globals
            __locals = _locals
            
            if RPDB_EXEC_INFO in expr:
                rpdb_exception_info = self.get_exception(frame_index, fException)
                __globals = globals()
                __locals = locals()

            __locals['_RPDB2_FindRepr'] = _RPDB2_FindRepr

            is_valid = [True]
            r = eval(expr, __globals, __locals)

            e[DICT_KEY_EXPR] = expr
            e[DICT_KEY_REPR] = repr_ltd(r, repr_limit, is_valid)
            e[DICT_KEY_IS_VALID] = is_valid[0]
            e[DICT_KEY_TYPE] = self.__parse_type(type(r))
            e[DICT_KEY_N_SUBNODES] = self.__calc_number_of_subnodes(r)
            
            if fExpand and (e[DICT_KEY_N_SUBNODES] > 0):
                fForceNames = (expr in ['globals()', 'locals()']) or (RPDB_EXEC_INFO in expr)
                e[DICT_KEY_SUBNODES] = self.__calc_subnodes(expr, r, fForceNames, fFilter, repr_limit)
                e[DICT_KEY_N_SUBNODES] = len(e[DICT_KEY_SUBNODES])
                
        except:
            print_debug_exception()
            e[DICT_KEY_ERROR] = repr(sys.exc_info())
        
        lock.acquire()
        if len(rl) == index:    
            rl.append(e)
        lock.release()    

        
    def get_namespace(self, nl, fFilter, frame_index, fException, repr_limit):
        try:
            (_globals, _locals, x) = self.__get_locals_globals(frame_index, fException, fReadOnly = True)
        except:    
            print_debug_exception()
            raise

        failed_expr_list = []
        rl = []
        index = 0
        lock = threading.Condition()
        
        for (expr, fExpand) in nl:
            if self.is_child_of_failure(failed_expr_list, expr):
                continue

            args = (expr, fExpand, fFilter, frame_index, fException, _globals, _locals, lock, rl, index, repr_limit)
            t = CThread(name = 'calc_expr %s' % (expr, ), target = self.calc_expr, args = args)
            t.start()
            t.join(2)
            t = None
            
            lock.acquire()
            if len(rl) == index:
                rl.append('error')
                failed_expr_list.append(expr)
            index += 1    
            lock.release()

            if len(failed_expr_list) > 3:
                break
            
        _rl = [r for r in rl if r != 'error']
        
        return _rl 

            
    def evaluate(self, expr, frame_index, fException):
        """
        Evaluate expression in context of frame at depth 'frame-index'.
        """
        
        (_globals, _locals, x) = self.__get_locals_globals(frame_index, fException)

        v = ''
        w = ''
        e = ''

        try:
            if '_rpdb2_pwd' in expr or '_rpdb2_args' in expr:
                r = '...Removed-password-from-output...'
            
            else:
                r = eval(expr, _globals, _locals)

            v = repr_ltd(r, MAX_EVALUATE_LENGTH)
            
            if len(v) > MAX_EVALUATE_LENGTH:
                v += '... *** %s ***' % STR_MAX_EVALUATE_LENGTH_WARNING 
                w = STR_MAX_EVALUATE_LENGTH_WARNING

        except:
            exc_info = sys.exc_info()
            e = "%s, %s" % (str(exc_info[0]), str(exc_info[1]))

        self.notify_namespace()

        return (v, w, e)

        
    def execute(self, suite, frame_index, fException):
        """
        Execute suite (Python statement) in context of frame at 
        depth 'frame-index'.
        """
       
        print_debug('exec called with: ' + repr(suite))

        (_globals, _locals, _original_locals_copy) = self.__get_locals_globals(frame_index, fException)

        if frame_index > 0 and not _globals is _locals:
            _locals_copy = copy.copy(_locals)
        
        w = ''
        e = ''

        try:
            if '_RPDB2_FindRepr' in suite and not '_RPDB2_FindRepr' in _original_locals_copy:
                _locals['_RPDB2_FindRepr'] = _RPDB2_FindRepr

            try:
                exec suite in _globals, _locals
            finally:
                if '_RPDB2_FindRepr' in suite and not '_RPDB2_FindRepr' in _original_locals_copy:
                    del _locals['_RPDB2_FindRepr']

        except:    
            exc_info = sys.exc_info()
            e = "%s, %s" % (str(exc_info[0]), str(exc_info[1]))

        if frame_index > 0 and (not _globals is _locals) and _locals != _locals_copy:
            l = [(k, repr(v)) for k, v in _locals.items()]
            sl = sets.Set(l)

            lc = [(k, repr(v)) for k, v in _locals_copy.items()]
            slc = sets.Set(lc)

            nsc = [k for (k, v) in sl - slc if k in _original_locals_copy]
            if len(nsc) != 0:
                w = STR_LOCAL_NAMESPACE_WARNING
        
        self.notify_namespace()
        
        return (w, e)


    def get_thread_list(self):
        """
        Return thread list with tid, state, and last event of each thread.
        """
        
        ctx = self.get_current_ctx()
        
        if ctx is None:
            current_thread_id = -1
        else:
            current_thread_id = ctx.m_thread_id  
            
        ctx_list = self.get_threads().values()
        tl = [{DICT_KEY_TID: c.m_thread_id, DICT_KEY_NAME: c.m_thread_name, DICT_KEY_BROKEN: c.m_fBroken, DICT_KEY_EVENT: c.m_event} for c in ctx_list]

        return (current_thread_id, tl)


    def stop_debuggee(self):
        """
        Notify the client and terminate this proccess.
        """

        CThread(name = '_atexit', target = _atexit, args = (True, )).start()


    def set_trap_unhandled_exceptions(self, ftrap):
        self.m_ftrap = ftrap

        event = CEventTrap(ftrap)
        self.m_event_dispatcher.fire_event(event)


    def set_fork_mode(self, ffork_into_child, ffork_auto):
        self.m_ffork_into_child = ffork_into_child
        self.m_ffork_auto = ffork_auto

        event = CEventForkMode(ffork_into_child, ffork_auto)
        self.m_event_dispatcher.fire_event(event)


    
#
# ------------------------------------- RPC Server --------------------------------------------
#



class CWorkQueue:
    """
    Worker threads pool mechanism for RPC server.    
    """
    
    def __init__(self, size = N_WORK_QUEUE_THREADS):
        self.m_lock = threading.Condition()
        self.m_work_items = []
        self.m_f_shutdown = False

        self.m_size = size
        self.m_n_threads = 0
        self.m_n_available = 0

        self.__create_thread()
        

    def __create_thread(self): 
        t = CThread(name = '__worker_target', target = self.__worker_target, shutdown = self.shutdown)
        #t.setDaemon(True)
        t.start()


    def shutdown(self):
        """
        Signal worker threads to exit, and wait until they do.
        """
       
        if self.m_f_shutdown:
            return

        print_debug('Shutting down worker queue...')

        self.m_lock.acquire()
        self.m_f_shutdown = True
        self.m_lock.notifyAll()

        while self.m_n_threads > 0:
            self.m_lock.wait()
            
        self.m_lock.release()

        print_debug('Shutting down worker queue, done.')


    def __worker_target(self): 
        try:
            self.m_lock.acquire()
            
            self.m_n_threads += 1
            self.m_n_available += 1
            fcreate_thread = not self.m_f_shutdown and self.m_n_threads < self.m_size            
            
            self.m_lock.release()
            
            if fcreate_thread:
                self.__create_thread()
                
            self.m_lock.acquire()

            while not self.m_f_shutdown:
                self.m_lock.wait()

                if self.m_f_shutdown:
                    break
                    
                if len(self.m_work_items) == 0:
                    continue
                    
                fcreate_thread = self.m_n_available == 1

                (target, args) = self.m_work_items.pop()

                self.m_n_available -= 1                
                self.m_lock.release()

                if fcreate_thread:
                    self.__create_thread()
                    
                try:
                    target(*args)
                except:
                    print_debug_exception()

                self.m_lock.acquire()
                self.m_n_available += 1

                if self.m_n_available > self.m_size:
                    break
                    
            self.m_n_threads -= 1
            self.m_n_available -= 1 
            self.m_lock.notifyAll()
            
        finally:
            self.m_lock.release()


    def post_work_item(self, target, args):
        if self.m_f_shutdown:
            return
            
        try:
            self.m_lock.acquire()

            if self.m_f_shutdown:
                return
            
            self.m_work_items.append((target, args))

            self.m_lock.notify()
            
        finally:
            self.m_lock.release()
                
        
            
class CUnTracedThreadingMixIn(SocketServer.ThreadingMixIn):
    """
    Modification of SocketServer.ThreadingMixIn that uses a worker thread
    queue instead of spawning threads to process requests.
    This mod was needed to resolve deadlocks that were generated in some 
    circumstances.
    """
    
    def init_work_queue(self):
        self.m_work_queue = CWorkQueue()
    
    def shutdown_work_queue(self):
        self.m_work_queue.shutdown()

    def process_request(self, request, client_address):
        self.m_work_queue.post_work_item(target = SocketServer.ThreadingMixIn.process_request_thread, args = (self, request, client_address))



def my_xmlrpclib_loads(data):
    """
    Modification of Python 2.3 xmlrpclib.loads() that does not do an 
    import. Needed to prevent deadlocks.
    """
    
    p, u = xmlrpclib.getparser()
    p.feed(data)
    p.close()
    return u.close(), u.getmethodname()



class CXMLRPCServer(CUnTracedThreadingMixIn, SimpleXMLRPCServer.SimpleXMLRPCServer):
    allow_reuse_address = False
    
    """
    Modification of Python 2.3 SimpleXMLRPCServer.SimpleXMLRPCDispatcher 
    that uses my_xmlrpclib_loads(). Needed to prevent deadlocks.
    """

    def __marshaled_dispatch(self, data, dispatch_method = None):
        params, method = my_xmlrpclib_loads(data)

        # generate response
        try:
            if dispatch_method is not None:
                response = dispatch_method(method, params)
            else:
                response = self._dispatch(method, params)
            # wrap response in a singleton tuple
            response = (response,)
            response = xmlrpclib.dumps(response, methodresponse=1)
        except xmlrpclib.Fault, fault:
            response = xmlrpclib.dumps(fault)
        except:
            # report exception back to server
            response = xmlrpclib.dumps(
                xmlrpclib.Fault(1, "%s:%s" % (sys.exc_type, sys.exc_value))
                )
            print_debug_exception()

        return response

    if sys.version_info[:2] <= (2, 3):
        _marshaled_dispatch = __marshaled_dispatch


    def handle_error(self, request, client_address):
        print_debug("handle_error() in pid %d" % _getpid())

        if g_ignore_broken_pipe + 5 > time.time():
            return

        return SimpleXMLRPCServer.SimpleXMLRPCServer.handle_error(self, request, client_address)



class CPwdServerProxy:
    """
    Encrypted proxy to the debuggee.
    Works by wrapping a xmlrpclib.ServerProxy object.
    """
    
    def __init__(self, crypto, uri, transport = None, target_rid = 0):
        self.m_crypto = crypto       
        self.m_proxy = xmlrpclib.ServerProxy(uri, transport)

        self.m_fEncryption = is_encryption_supported()
        self.m_target_rid = target_rid

        self.m_method = getattr(self.m_proxy, DISPACHER_METHOD)

 
    def __set_encryption(self, fEncryption):
        self.m_fEncryption = fEncryption


    def get_encryption(self):
        return self.m_fEncryption


    def __request(self, name, params):
        """
        Call debuggee method 'name' with parameters 'params'.
        """
    
        while True:
            try:
                #
                # Encrypt method and params.
                #
                _params = self.m_crypto.do_crypto((name, params, self.m_target_rid), self.get_encryption())

                rpdb_version = get_interface_compatibility_version()

                r = self.m_method(rpdb_version + _params)
                
                #
                # Decrypt response.
                #
                ((max_index, _r, _e), id, fe)= self.m_crypto.undo_crypto(r, fVerifyIndex = False)
                
                if _e is not None:
                    raise _e

            except AuthenticationBadIndex, e:
                self.m_crypto.set_index(e.m_max_index, e.m_anchor)
                continue

            except xmlrpclib.Fault, fault:
                if class_name(BadVersion) in fault.faultString:
                    s = fault.faultString.split("'")
                    version = ['', s[1]][len(s) > 0]
                    raise BadVersion(version)
                    
                if class_name(EncryptionExpected) in fault.faultString:
                    raise EncryptionExpected
                    
                elif class_name(EncryptionNotSupported) in fault.faultString:
                    if self.m_crypto.m_fAllowUnencrypted:
                        self.__set_encryption(False)
                        continue
                        
                    raise EncryptionNotSupported
                    
                elif class_name(DecryptionFailure) in fault.faultString:
                    raise DecryptionFailure
                    
                elif class_name(AuthenticationBadData) in fault.faultString:
                    raise AuthenticationBadData
                    
                elif class_name(AuthenticationFailure) in fault.faultString:
                    raise AuthenticationFailure
                    
                else:
                    print_debug_exception()
                    assert False 

            except xmlrpclib.ProtocolError:
                print_debug("Caught ProtocolError for %s" % name)
                #print_debug_exception()
                raise CConnectionException
                
            return _r


    def __getattr__(self, name):
        return xmlrpclib._Method(self.__request, name)


    
class CIOServer:
    """
    Base class for debuggee server.
    """
    
    def __init__(self, _rpdb2_pwd, fAllowUnencrypted, fAllowRemote, rid):
        self.m_thread = None

        self.m_crypto = CCrypto(_rpdb2_pwd, fAllowUnencrypted, rid)
        
        self.m_fAllowRemote = fAllowRemote
        self.m_rid = rid
        
        self.m_port = None
        self.m_stop = False
        self.m_server = None
        

    def shutdown(self):
        self.stop()
        
    
    def start(self):
        self.m_thread = CThread(name = 'ioserver', target = self.run, shutdown = self.shutdown)
        self.m_thread.setDaemon(True)
        self.m_thread.start()


    def jumpstart(self):
        self.m_stop = False
        self.start()


    def stop(self):
        if self.m_stop:
            return
        
        print_debug('Stopping IO server... (pid = %d)' % _getpid())

        self.m_stop = True

        while self.m_thread.isAlive():
            try:
                proxy = CPwdServerProxy(self.m_crypto, calcURL(LOOPBACK, self.m_port), CLocalTimeoutTransport())
                proxy.null()
            except (socket.error, CException):
                pass
            
            self.m_thread.join(0.5)

        self.m_thread = None

        self.m_server.shutdown_work_queue()

        print_debug('Stopping IO server, done.')

        
    def export_null(self):
        return 0


    def run(self):
        if self.m_server == None:
            (self.m_port, self.m_server) = self.__StartXMLRPCServer()

        self.m_server.init_work_queue()
        self.m_server.register_function(self.dispatcher_method)        
        
        while not self.m_stop:
            self.m_server.handle_request()
            
        
    def dispatcher_method(self, params):
        """
        Process RPC call.
        """
        
        rpdb_version = get_interface_compatibility_version()

        if params[: len(rpdb_version)] != rpdb_version:
            raise BadVersion(get_version())

        _params = params[len(rpdb_version):]

        try:
            #
            # Decrypt parameters.
            #
            ((name, _params, target_rid), client_id, fEncryption) = self.m_crypto.undo_crypto(_params)
        except AuthenticationBadIndex, e:
            #print_debug_exception()

            #
            # Notify the caller on the expected index.
            #
            fEncryption = self.m_crypto.is_encrypted(_params)                           
            max_index = self.m_crypto.get_max_index()
            _r = self.m_crypto.do_crypto((max_index, None, e), fEncryption)
            return _r
            
        r = None
        e = None

        try:
            #
            # We are forcing the 'export_' prefix on methods that are
            # callable through XML-RPC to prevent potential security
            # problems
            #
            func = getattr(self, 'export_' + name)
        except AttributeError:
            raise Exception('method "%s" is not supported' % ('export_' + name, ))

        try:
            if (target_rid != 0) and (target_rid != self.m_rid):
                raise NotAttached
            
            #
            # Record that client id is still attached. 
            #
            self.record_client_heartbeat(client_id, name, _params)

            r = func(*_params)

        except Exception, _e:
            print_debug_exception()
            e = _e            

        #
        # Send the encrypted result.
        #
        max_index = self.m_crypto.get_max_index()
        _r = self.m_crypto.do_crypto((max_index, r, e), fEncryption)
        return _r


    def __StartXMLRPCServer(self):
        """
        As the name says, start the XML RPC server.
        Looks for an available tcp port to listen on.
        """
        
        host = [LOOPBACK, ""][self.m_fAllowRemote]
        port = SERVER_PORT_RANGE_START

        while True:
            try:
                server = CXMLRPCServer((host, port), logRequests = 0)
                return (port, server)
                
            except socket.error, e:
                if GetSocketError(e) != errno.EADDRINUSE:
                    raise
                    
                if port >= SERVER_PORT_RANGE_START + SERVER_PORT_RANGE_LENGTH - 1:
                    raise

                port += 1
                continue


    def record_client_heartbeat(self, id, name, params):
        pass



class CServerInfo:
    def __init__(self, age, port, pid, filename, rid, state, fembedded):
        self.m_age = age 
        self.m_port = port
        self.m_pid = pid
        self.m_filename = filename
        self.m_module_name = CalcModuleName(filename)
        self.m_rid = rid
        self.m_state = state
        self.m_fembedded = fembedded

    def __str__(self):
        return 'age: %d, port: %d, pid: %d, filename: %s, rid: %s' % (self.m_age, self.m_port, self.m_pid, self.m_filename, self.m_rid)


        
class CDebuggeeServer(CIOServer):
    """
    The debuggee XML RPC server class.
    """
    
    def __init__(self, filename, debugger, _rpdb2_pwd, fAllowUnencrypted, fAllowRemote, rid = None):
        if rid is None:
            rid = generate_rid()
            
        CIOServer.__init__(self, _rpdb2_pwd, fAllowUnencrypted, fAllowRemote, rid)
        
        self.m_filename = filename
        self.m_pid = _getpid()
        self.m_time = time.time()
        self.m_debugger = debugger
        self.m_rid = rid

                
    def shutdown(self):
        CIOServer.shutdown(self)

        
    def record_client_heartbeat(self, id, name, params):
        finit = (name == 'request_break')
        fdetach = (name == 'request_go' and True in params)

        self.m_debugger.record_client_heartbeat(id, finit, fdetach)


    def export_server_info(self):
        age = time.time() - self.m_time
        state = self.m_debugger.get_state()
        fembedded = self.m_debugger.is_embedded()
        
        si = CServerInfo(age, self.m_port, self.m_pid, self.m_filename, self.m_rid, state, fembedded)
        return si


    def export_sync_with_events(self, fException, fSendUnhandled):
        ei = self.m_debugger.sync_with_events(fException, fSendUnhandled)
        return ei


    def export_wait_for_event(self, timeout, event_index):
        (new_event_index, s) = self.m_debugger.wait_for_event(timeout, event_index)
        return (new_event_index, s)

                
    def export_set_breakpoint(self, filename, scope, lineno, fEnabled, expr, frame_index, fException):
        self.m_debugger.set_breakpoint(filename, scope, lineno, fEnabled, expr, frame_index, fException)
        return 0

        
    def export_disable_breakpoint(self, id_list, fAll):
        self.m_debugger.disable_breakpoint(id_list, fAll)
        return 0

        
    def export_enable_breakpoint(self, id_list, fAll):
        self.m_debugger.enable_breakpoint(id_list, fAll)
        return 0

        
    def export_delete_breakpoint(self, id_list, fAll):
        self.m_debugger.delete_breakpoint(id_list, fAll)
        return 0

        
    def export_get_breakpoints(self):
        bpl = self.m_debugger.get_breakpoints()
        return bpl

        
    def export_request_break(self):
        self.m_debugger.request_break()
        return 0


    def export_request_go(self, fdetach = False):
        self.m_debugger.request_go()
        return 0


    def export_request_go_breakpoint(self, filename, scope, lineno, frame_index, fException):
        self.m_debugger.request_go_breakpoint(filename, scope, lineno, frame_index, fException)
        return 0


    def export_request_step(self):
        self.m_debugger.request_step()
        return 0


    def export_request_next(self):
        self.m_debugger.request_next()
        return 0


    def export_request_return(self):
        self.m_debugger.request_return()
        return 0


    def export_request_jump(self, lineno):
        self.m_debugger.request_jump(lineno)
        return 0


    def export_get_stack(self, tid_list, fAll, fException):
        r = self.m_debugger.get_stack(tid_list, fAll, fException)                 
        return r
    

    def export_get_source_file(self, filename, lineno, nlines, frame_index, fException): 
        r = self.m_debugger.get_source_file(filename, lineno, nlines, frame_index, fException)
        return r


    def export_get_source_lines(self, nlines, fAll, frame_index, fException): 
        r = self.m_debugger.get_source_lines(nlines, fAll, frame_index, fException)
        return r

        
    def export_get_thread_list(self):
        r = self.m_debugger.get_thread_list()
        return r


    def export_set_thread(self, tid):
        self.m_debugger.set_thread(tid)   
        return 0


    def export_get_namespace(self, nl, fFilter, frame_index, fException, repr_limit):
        r = self.m_debugger.get_namespace(nl, fFilter, frame_index, fException, repr_limit)
        return r

        
    def export_evaluate(self, expr, frame_index, fException):
        (v, w, e) = self.m_debugger.evaluate(expr, frame_index, fException)
        return (v, w, e)

        
    def export_execute(self, suite, frame_index, fException):
        (w, e) = self.m_debugger.execute(suite, frame_index, fException)
        return (w, e)

        
    def export_stop_debuggee(self):
        self.m_debugger.stop_debuggee()
        return 0


    def export_set_trap_unhandled_exceptions(self, ftrap):
        self.m_debugger.set_trap_unhandled_exceptions(ftrap)
        return 0


    def export_set_fork_mode(self, ffork_into_child, ffork_auto):
        self.m_debugger.set_fork_mode(ffork_into_child, ffork_auto)
        return 0


        
#
# ------------------------------------- RPC Client --------------------------------------------
#



class CTimeoutHTTPConnection(httplib.HTTPConnection):
    """
    Modification of httplib.HTTPConnection with timeout for sockets.
    """

    _rpdb2_timeout = PING_TIMEOUT
    
    def connect(self):
        """Connect to the host and port specified in __init__."""
        msg = "getaddrinfo returns an empty list"
        for res in socket.getaddrinfo(self.host, self.port, 0,
                                      socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                self.sock = socket.socket(af, socktype, proto)
                self.sock.settimeout(self._rpdb2_timeout)
                if self.debuglevel > 0:
                    print_debug("connect: (%s, %s)" % (self.host, self.port))
                self.sock.connect(sa)
            except socket.error, msg:
                if self.debuglevel > 0:
                    print_debug('connect fail: ' + repr((self.host, self.port)))
                if self.sock:
                    self.sock.close()
                self.sock = None
                continue
            break
        if not self.sock:
            raise socket.error, msg



class CLocalTimeoutHTTPConnection(CTimeoutHTTPConnection):
    """
    Modification of httplib.HTTPConnection with timeout for sockets.
    """

    _rpdb2_timeout = LOCAL_TIMEOUT



class CTimeoutHTTP(httplib.HTTP):
    """
    Modification of httplib.HTTP with timeout for sockets.
    """
    
    _connection_class = CTimeoutHTTPConnection

    
        
class CLocalTimeoutHTTP(httplib.HTTP):
    """
    Modification of httplib.HTTP with timeout for sockets.
    """
    
    _connection_class = CLocalTimeoutHTTPConnection

    
        
class CTimeoutTransport(xmlrpclib.Transport):
    """
    Modification of xmlrpclib.Transport with timeout for sockets.
    """
    
    def make_connection(self, host):
        # create a HTTP connection object from a host descriptor
        host, extra_headers, x509 = self.get_host_info(host)
        return CTimeoutHTTP(host)

    
    
class CLocalTimeoutTransport(xmlrpclib.Transport):
    """
    Modification of xmlrpclib.Transport with timeout for sockets.
    """
    
    def make_connection(self, host):
        # create a HTTP connection object from a host descriptor
        host, extra_headers, x509 = self.get_host_info(host)
        return CLocalTimeoutHTTP(host)

    
    
class CSession:
    """
    Basic class that communicates with the debuggee server.
    """
    
    def __init__(self, host, port, _rpdb2_pwd, fAllowUnencrypted, rid):
        self.m_crypto = CCrypto(_rpdb2_pwd, fAllowUnencrypted, rid)

        self.m_host = host
        self.m_port = port
        self.m_proxy = None
        self.m_server_info = None
        self.m_exc_info = None

        self.m_fShutDown = False
        self.m_fRestart = False


    def get_encryption(self):
        return self.m_proxy.get_encryption()

        
    def getServerInfo(self):
        return self.m_server_info


    def pause(self):
        self.m_fRestart = True


    def restart(self, sleep = 0, timeout = 10):
        self.m_fRestart = True

        time.sleep(sleep)

        t0 = time.time()

        try:
            try:
                while time.time() < t0 + timeout:
                    try:
                        self.Connect()
                        return

                    except socket.error:
                        continue

                raise CConnectionException

            except:
                self.m_fShutDown = True
                raise

        finally:
            self.m_fRestart = False


    def shut_down(self):
        self.m_fShutDown = True

        
    def getProxy(self):
        """
        Return the proxy object.
        With this object you can invoke methods on the server.
        """
        
        while self.m_fRestart:
            time.sleep(0.1)

        if self.m_fShutDown:
            raise NotAttached
        
        return self.m_proxy


    def ConnectAsync(self):
        t = threading.Thread(target = self.ConnectNoThrow)
        #t.setDaemon(True)
        t.start()
        return t


    def ConnectNoThrow(self):
        try:
            self.Connect()
        except:
            self.m_exc_info = sys.exc_info() 


    def Connect(self):
        host = self.m_host
        if host.lower() == LOCALHOST:
            host = LOOPBACK
        
        server = CPwdServerProxy(self.m_crypto, calcURL(host, self.m_port), CTimeoutTransport())
        server_info = server.server_info()

        self.m_proxy = CPwdServerProxy(self.m_crypto, calcURL(host, self.m_port), target_rid = server_info.m_rid)
        self.m_server_info = server_info

                
    def isConnected(self):
        return self.m_proxy is not None

    

class CServerList:
    def __init__(self, host):
        self.m_host = host
        self.m_list = []
        self.m_errors = {}


    def calcList(self, _rpdb2_pwd, rid):
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
        return self.m_list 


    def get_errors(self):
        return self.m_errors


    def findServers(self, key):
        try:
            n = int(key)
            _s = [s for s in self.m_list if (s.m_pid == n) or (s.m_rid == key)]

        except ValueError: 
            if type(key) == unicode:
                fse = sys.getfilesystemencoding()
                key = key.encode(fse)

            _s = [s for s in self.m_list if key in s.m_filename]

        if _s == []:
            raise UnknownServer

        return _s    



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

        event_type_dict = {CEventPsycoWarning: {}}
        self.register_callback(self.on_event_psyco, event_type_dict, fSingleUse = False)
        
        event_type_dict = {CEventTrap: {}}
        self.m_event_dispatcher_proxy.register_callback(self.on_event_trap, event_type_dict, fSingleUse = False)
        self.m_event_dispatcher.register_chain_override(event_type_dict)

        event_type_dict = {CEventForkMode: {}}
        self.m_event_dispatcher_proxy.register_callback(self.on_event_fork_mode, event_type_dict, fSingleUse = False)
        self.m_event_dispatcher.register_chain_override(event_type_dict)

        self.m_printer = self.__nul_printer

        self.m_last_command_line = None
        self.m_last_fchdir = None

        self.m_ftrap = True

        self.m_ffork_into_child = False
        self.m_ffork_auto = False
        
    
    def __del__(self):
        self.m_event_dispatcher_proxy.shutdown()
        self.m_event_dispatcher.shutdown()
        self.m_state_manager.shutdown()

        
    def __nul_printer(self, str):
        pass

        
    def set_printer(self, printer):
        self.m_printer = printer


    def register_callback(self, callback, event_type_dict, fSingleUse):
        return self.m_event_dispatcher.register_callback(callback, event_type_dict, fSingleUse)

        
    def remove_callback(self, callback):
        return self.m_event_dispatcher.remove_callback(callback)


    def __wait_for_debuggee(self, rid):
        try:
            for i in range(0,STARTUP_RETRIES):
                try:
                    self.m_server_list_object.calcList(self.m_rpdb2_pwd, self.m_rid)
                    return self.m_server_list_object.findServers(rid)[0]
                except UnknownServer:
                    time.sleep(STARTUP_TIMEOUT)
                    continue
                    
            self.m_server_list_object.calcList(self.m_rpdb2_pwd, self.m_rid)
            return self.m_server_list_object.findServers(rid)[0]

        finally:
            errors = self.m_server_list_object.get_errors()
            self.__report_server_errors(errors, fsupress_pwd_warning = True)
                        

    def get_encryption(self):
        return self.getSession().get_encryption()

    
    def launch(self, fchdir, command_line, fload_breakpoints = True):
        self.__verify_unattached()

        if not os.name in [POSIX, 'nt']:
            self.m_printer(STR_SPAWN_UNSUPPORTED)
            raise SpawnUnsupported
            
        if self.m_rpdb2_pwd is None:
            self.set_random_password()
            
        if command_line == '':
            raise BadArgument

        (path, filename, args) = split_command_line_path_filename_args(command_line)

        #if not IsPythonSourceFile(filename):
        #    raise NotPythonSource

        _filename = os.path.join(path, filename) 
           
        ExpandedFilename = FindFile(_filename)
        self.set_host(LOCALHOST)

        self.m_printer(STR_STARTUP_SPAWN_NOTICE)

        rid = generate_rid()

        create_pwd_file(rid, self.m_rpdb2_pwd)
        
        self.m_state_manager.set_state(STATE_SPAWNING)

        try:
            try:
                self._spawn_server(fchdir, ExpandedFilename, args, rid)            
                server = self.__wait_for_debuggee(rid)
                self.attach(server.m_rid, server.m_filename, fsupress_pwd_warning = True)

                self.m_last_command_line = command_line
                self.m_last_fchdir = fchdir
                
            except:
                if self.m_state_manager.get_state() != STATE_DETACHED:
                    self.m_state_manager.set_state(STATE_DETACHED)

                raise

            try:
                if fload_breakpoints:
                    self.load_breakpoints()
            except:
                pass

        finally:
            delete_pwd_file(rid)


    def restart(self):
        """
        Restart debug session with same command_line and fchdir arguments
        which were used in last launch.
        """

        if None in (self.m_last_fchdir, self.m_last_command_line):
            return

        if self.m_state_manager.get_state() != STATE_DETACHED:
            self.stop_debuggee()

        self.launch(self.m_last_fchdir, self.m_last_command_line)


    def get_launch_args(self):    
        """
        Return command_line and fchdir arguments which were used in last 
        launch as (last_fchdir, last_command_line).
        Returns None if there is no info.
        """

        if None in (self.m_last_fchdir, self.m_last_command_line):
            return (None, None)
            
        return (self.m_last_fchdir, self.m_last_command_line)


    def _spawn_server(self, fchdir, ExpandedFilename, args, rid):
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
        p = ['', ' --pwd="%s"' % (self.m_rpdb2_pwd, )][os.name == 'nt']
       
        b = ''
        if ExpandedFilename in g_found_unicode_files:
            u = g_found_unicode_files[ExpandedFilename]
            _u = u.encode('utf8')
            _b = base64.encodestring(_u).strip('\n').translate(g_safe_base64_to)
            b = ' --base64=%s' % _b

        debugger = os.path.abspath(__file__)
        if debugger[-1:] == 'c':
            debugger = debugger[:-1]

        debug_prints = ['', ' --debug'][g_fDebug]    
            
        options = '"%s"%s --debugee%s%s%s%s%s --rid=%s "%s" %s' % (debugger, debug_prints, p, e, r, c, b, rid, ExpandedFilename, args)

        python_exec = sys.executable
        if python_exec.endswith('w.exe'):
            python_exec = python_exec[:-5] + '.exe'

        if '?' in python_exec or '?' in debugger:
            raise BadMBCSPath

        if name == POSIX:
            shell = CalcUserShell()
            terminal_command = CalcTerminalCommand()

            if terminal_command == GNOME_DEFAULT_TERM:
                command = osSpawn[GNOME_DEFAULT_TERM] % {'shell': shell, 'exec': python_exec, 'options': options}
            else:    
                command = osSpawn[name] % {'term': terminal_command, 'shell': shell, 'exec': python_exec, 'options': options}
        else:    
            command = osSpawn[name] % {'exec': python_exec, 'options': options}

        if name == DARWIN:
            s = 'cd "%s" ; %s' % (os.getcwdu(), command)
            command = CalcMacTerminalCommand(s)

        print_debug('Terminal open string: %s' % repr(command))

        if type(command) == unicode:
            fse = sys.getfilesystemencoding()
            command = command.encode(fse)
        
        if name == MAC:
            terminalcommand.run(command)
        else:
            os.popen(command)

    
    def attach(self, key, name = None, fsupress_pwd_warning = False):
        self.__verify_unattached()

        if key == '':
            raise BadArgument

        if self.m_rpdb2_pwd is None:
            self.m_printer(STR_PASSWORD_MUST_BE_SET)
            raise UnsetPassword
        
        if name is None:
            name = key

        _name = name
        
        self.m_printer(STR_STARTUP_NOTICE)
        self.m_state_manager.set_state(STATE_ATTACHING)

        try:
            self.m_server_list_object.calcList(self.m_rpdb2_pwd, self.m_rid)                
            servers = self.m_server_list_object.findServers(key)
            server = servers[0] 

            _name = server.m_filename
            
            errors = self.m_server_list_object.get_errors()
            if not key in [server.m_rid, str(server.m_pid)]:
                self.__report_server_errors(errors, fsupress_pwd_warning)

            self.__attach(server)
            if len(servers) > 1:
                self.m_printer(STR_MULTIPLE_DEBUGGEES % (key, ))
            self.m_printer(STR_ATTACH_CRYPTO_MODE % ([' ' + STR_ATTACH_CRYPTO_MODE_NOT, ''][self.get_encryption()], ))    
            self.m_printer(STR_ATTACH_SUCCEEDED % (server.m_filename, ))
            return

        except (socket.error, CConnectionException):
            self.m_printer(STR_ATTACH_FAILED_NAME % (_name, ))
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

        
    def __attach(self, server):
        self.__verify_unattached()

        session = CSession(self.m_host, server.m_port, self.m_rpdb2_pwd, self.m_fAllowUnencrypted, self.m_rid)
        session.Connect()

        if (session.getServerInfo().m_pid != server.m_pid) or (session.getServerInfo().m_filename != server.m_filename):
            raise UnexpectedData

        self.m_session = session
        
        self.m_server_info = self.get_server_info()

        self.getSession().getProxy().set_trap_unhandled_exceptions(self.m_ftrap)
        self.getSession().getProxy().set_fork_mode(self.m_ffork_into_child, self.m_ffork_auto)

        self.request_break()
        self.refresh(True)
        
        self.__start_event_monitor()

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
        #self.m_worker_thread.setDaemon(True)
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


    def on_event_psyco(self, event):
        self.m_printer(STR_PSYCO_WARNING)


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

    
    def set_breakpoint(self, filename, scope, lineno, fEnabled, expr):
        frame_index = self.get_frame_index()
        fAnalyzeMode = (self.m_state_manager.get_state() == STATE_ANALYZE) 

        self.getSession().getProxy().set_breakpoint(filename, scope, lineno, fEnabled, expr, frame_index, fAnalyzeMode)

        
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

        path = calc_bpl_filename(module_name + filename)            
        file = open(path, 'wb')

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

        path = calc_bpl_filename(module_name + filename)                            
        file = open(path, 'rb')

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
                    self.set_breakpoint(bp.m_filename, bp.m_scope_fqn, bp.m_scope_offset, bp.m_fEnabled, bp.m_expr)
                except:
                    print_debug_exception()
                    ferror = True

            if ferror:
                raise CException
                
        finally:
            file.close()


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

        
    def get_namespace(self, nl, fFilter, repr_limit):
        frame_index = self.get_frame_index()
        fAnalyzeMode = (self.m_state_manager.get_state() == STATE_ANALYZE) 

        r = self.getSession().getProxy().get_namespace(nl, fFilter, frame_index, fAnalyzeMode, repr_limit)
        return r


    def evaluate(self, expr):
        self.__verify_attached()
        self.__verify_broken()

        frame_index = self.get_frame_index()
        fAnalyzeMode = (self.m_state_manager.get_state() == STATE_ANALYZE) 

        (value, warning, error) = self.getSession().getProxy().evaluate(expr, frame_index, fAnalyzeMode)
        return (value, warning, error)

        
    def execute(self, suite):
        self.__verify_attached()
        self.__verify_broken()

        frame_index = self.get_frame_index()
        fAnalyzeMode = (self.m_state_manager.get_state() == STATE_ANALYZE)

        (warning, error) = self.getSession().getProxy().execute(suite, frame_index, fAnalyzeMode)
        return (warning, error)


    def set_host(self, host):
        self.__verify_unattached()
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
        return self.m_host


    def calc_server_list(self):
        if self.m_rpdb2_pwd is None:
            raise UnsetPassword
        
        server_list = self.m_server_list_object.calcList(self.m_rpdb2_pwd, self.m_rid)
        errors = self.m_server_list_object.get_errors()
        self.__report_server_errors(errors)
        
        return (server_list, errors)


    def get_server_info(self): 
        return self.getSession().getServerInfo()


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
        return self.m_state_manager.get_state()


    def set_password(self, _rpdb2_pwd):    
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



class CConsoleInternal(cmd.Cmd, threading.Thread):
    def __init__(self, session_manager, stdin = None, stdout = None, fSplit = False):
        global g_fDefaultStd

        cmd.Cmd.__init__(self, stdin = stdin, stdout = stdout)
        threading.Thread.__init__(self)
        
        self.fAnalyzeMode = False
        self.fPrintBroken = True

        self.m_filename = None
        
        self.use_rawinput = [1, 0][fSplit]
        self.m_fSplit = fSplit
        self.prompt = [[CONSOLE_PROMPT, CONSOLE_PROMPT_ANALYZE][self.fAnalyzeMode], ""][fSplit]
        self.intro = CONSOLE_INTRO
        #self.setDaemon(True)
        
        self.m_session_manager = session_manager
        self.m_session_manager.set_printer(self.printer)

        event_type_dict = {CEventState: {}}
        self.m_session_manager.register_callback(self.event_handler, event_type_dict, fSingleUse = False)

        event_type_dict = {CEventTrap: {}}
        self.m_session_manager.register_callback(self.trap_handler, event_type_dict, fSingleUse = False)

        event_type_dict = {CEventForkMode: {}}
        self.m_session_manager.register_callback(self.fork_mode_handler, event_type_dict, fSingleUse = False)

        self.m_last_source_line = None
        self.m_last_nlines = DEFAULT_NUMBER_OF_LINES
        
        self.m_fAddPromptBeforeMsg = False
        self.m_eInLoop = threading.Event()
        self.cmdqueue.insert(0, '')

        g_fDefaultStd = (stdin == None)

        try:
            self.m_encoding = self.stdin.encoding
        except:
            self.m_encoding = locale.getdefaultlocale()[1]
            if self.m_encoding == None:
                self.m_encoding = 'ascii'


    def set_filename(self, filename):
        self.m_filename = filename


    def precmd(self, line):
        if type(line) == str:
            line = line.decode(self.m_encoding, 'replace')

        self.m_fAddPromptBeforeMsg = True
        if not self.m_eInLoop.isSet():
            self.m_eInLoop.set()
            time.sleep(0.01)

        if not line.strip():
            return line
            
        command = line.split(' ', 1)[0].split(SOURCE_MORE, 1)[0].split(SOURCE_LESS, 1)[0]
        if command not in ['list', 'l']:
            self.m_last_source_line = None
            self.m_last_nlines = DEFAULT_NUMBER_OF_LINES

        return line    

            
    def postcmd(self, stop, line):
        self.m_fAddPromptBeforeMsg = False

        return stop


    def onecmd(self, line):
        """
        Default Error handling and reporting of session manager errors.
        """
        
        try:
            return cmd.Cmd.onecmd(self, line)
            
        except (socket.error, CConnectionException):
            self.m_session_manager.report_exception(*sys.exc_info())
        except CException:
            self.m_session_manager.report_exception(*sys.exc_info())
        except:
            self.m_session_manager.report_exception(*sys.exc_info())
            print_debug_exception(True)

        return False
        
        
    def emptyline(self):
        pass

        
    def run(self):
        self.cmdloop()


    def __get_str_wrap(self, _str, max_len):
        if len(_str) <= max_len and not '\n' in _str:
            return (_str, '')

        s = _str[: max_len]

        i = s.find('\n')

        if i == -1:
            i = s.rfind(' ')

        if i == -1:
            return (s, _str[max_len:])

        return (_str[: i], _str[i + 1:])    

            
    def printer(self, _str):
        if not self.m_eInLoop.isSet():
            self.m_eInLoop.wait()

        fAPBM = self.m_fAddPromptBeforeMsg    
        prefix = ['', self.prompt.strip('\n')][fAPBM] + CONSOLE_PRINTER
        suffix = '\n' + [self.prompt.strip('\n'), ''][fAPBM]

        s = _str
        while s != '':
            s, _s = self.__get_str_wrap(s, CONSOLE_WRAP_INDEX - len(prefix + suffix))
            self.stdout.write(prefix + s + suffix)
            s = _s 

        self.stdout.flush()
        

    def print_notice(self, notice):
        nl = notice.split('\n')

        i = 0
        for l in nl:
            print >> self.stdout, l
            i += 1
            if i % PRINT_NOTICE_LINES_PER_SECTION == 0:
                print >> self.stdout, "\n" + PRINT_NOTICE_PROMPT,
                response = self.stdin.readline()
                if response != '\n':
                    break

                print >> self.stdout

        
    def event_handler(self, event): 
        state = event.m_state
        if (state == STATE_BROKEN) and self.fPrintBroken:
            self.fPrintBroken = False
            self.printer(STR_DEBUGGER_HAS_BROKEN)
            return

        if (state != STATE_ANALYZE) and self.fAnalyzeMode:
            self.fAnalyzeMode = False
            self.prompt = [CONSOLE_PROMPT, ""][self.m_fSplit]
            self.printer(STR_ANALYZE_MODE_TOGGLE % (MODE_OFF, ))
            return
        
        if (state == STATE_ANALYZE) and not self.fAnalyzeMode:
            self.fAnalyzeMode = True
            self.prompt = [CONSOLE_PROMPT_ANALYZE, ""][self.m_fSplit]
            self.printer(STR_ANALYZE_MODE_TOGGLE % (MODE_ON, ))
            return


    def trap_handler(self, event):
        self.printer(STR_TRAP_MODE_SET % (str(event.m_ftrap), ))

        
    def fork_mode_handler(self, event):
        x = [FORK_PARENT, FORK_CHILD][event.m_ffork_into_child]
        y = [FORK_MANUAL, FORK_AUTO][event.m_ffork_auto]

        self.printer(STR_FORK_MODE_SET % (x, y))

        
    def do_launch(self, arg):
        if arg == '':
            self.printer(STR_BAD_ARGUMENT)
            return

        if arg[:2] == '-k':
            fchdir = False
            _arg = arg[2:].strip()
        else:
            fchdir = True
            _arg = arg

        self.fPrintBroken = True

        try:
            self.m_session_manager.launch(fchdir, _arg)
            return
            
        except BadArgument:
            self.printer(STR_BAD_ARGUMENT)            
        except IOError:
            self.printer(STR_FILE_NOT_FOUND % (arg, ))
        except:
            self.fPrintBroken = False
            raise
                    
        self.fPrintBroken = False


    def do_restart(self, arg):
        if arg != '':
            self.printer(STR_BAD_ARGUMENT)
            return
            
        try:
            self.m_session_manager.restart()
            return
            
        except BadArgument:
            self.printer(STR_BAD_ARGUMENT)
        except IOError:
            self.printer(STR_FILE_NOT_FOUND % (arg, ))
        except:
            self.fPrintBroken = False
            raise

        self.fPrintBroken = False

    
    def do_attach(self, arg):
        if arg == '':
            return self.__scripts(arg)
            
        self.fPrintBroken = True

        try:
            self.m_session_manager.attach(arg)
            return
            
        except BadArgument:
            self.printer(STR_BAD_ARGUMENT)
        except:
            self.fPrintBroken = False
            raise

        self.fPrintBroken = False


    def __scripts(self, arg):
        if self.m_session_manager.get_password() is None:
            print >> self.stdout, STR_PASSWORD_MUST_BE_SET
            return

        host = self.m_session_manager.get_host()
        print >> self.stdout, STR_SCRIPTS_CONNECTING % (host, )

        (server_list, errors) = self.m_session_manager.calc_server_list()

        if server_list == []:
            print >> self.stdout, STR_SCRIPTS_NO_SCRIPTS % (host, )
            return

        try:
            spid = self.m_session_manager.get_server_info().m_pid
        except NotAttached:
            spid = None

        print >> self.stdout, STR_SCRIPTS_TO_DEBUG % (host, )    
        for s in server_list:
            m = ['', SYMBOL_MARKER][spid == s.m_pid]
            print >> self.stdout, ' %1s %-5d  %s' % (m, s.m_pid, s.m_filename)


    def do_detach(self, arg):
        if not arg == '':
            self.printer(STR_BAD_ARGUMENT)
            return

        self.m_session_manager.detach()


    def do_host(self, arg):
        if arg == '':
            host = self.m_session_manager.get_host()
            print >> self.stdout, host
            return

        try:
            self.m_session_manager.set_host(arg)

        except socket.gaierror, e:
            self.printer(MSG_ERROR_HOST_TEXT % (arg, e))

        
    def do_break(self, arg):
        if arg != '':
            self.printer(STR_BAD_ARGUMENT)
            return
            
        self.m_session_manager.request_break()

    do_b = do_break

    
    def __parse_bp_arg(self, arg, fAllowExpr = True):
        _args = arg.split(BP_EVAL_SEP)

        if (len(_args) > 1) and (not fAllowExpr):
            raise BadArgument
            
        if len(_args) > 1:
            expr = _args[1].strip()
        else:
            expr = ''

        rf = _args[0].rfind(BP_FILENAME_SEP)
        if rf == -1:
            args = [_args[0]]
        else:
            args = [_args[0][:rf], _args[0][rf + 1:]]

        filename = ['', args[0]][len(args) > 1]

        if filename in [None, '']:
            filename = self.m_filename

        try:
            lineno = int(args[-1])
            scope = ''
        except ValueError:
            lineno = 0
            scope = args[-1].strip()

        return (filename, scope, lineno, expr)

    
    def do_go(self, arg):
        if self.fAnalyzeMode:
            self.printer(STR_ILEGAL_ANALYZE_MODE_CMD)
            return

        try:
            if arg != '':
                (filename, scope, lineno, expr) = self.__parse_bp_arg(arg, fAllowExpr = False)
                self.fPrintBroken = True
                self.m_session_manager.request_go_breakpoint(filename, scope, lineno)
                return
            
            self.fPrintBroken = True
            self.m_session_manager.request_go()
            return

        except BadArgument:    
            self.printer(STR_BAD_ARGUMENT)
        except IOError:
            self.printer(STR_FILE_NOT_FOUND % (filename, ))
        except InvalidScopeName:
            self.printer(STR_SCOPE_NOT_FOUND % (scope, ))
        except DebuggerNotBroken:
            self.m_session_manager.report_exception(*sys.exc_info())
        except:
            self.fPrintBroken = False
            raise

        self.fPrintBroken = False

    do_g = do_go


    def do_step(self, arg):
        if arg != '':
            self.printer(STR_BAD_ARGUMENT)
            return
            
        if self.fAnalyzeMode:
            self.printer(STR_ILEGAL_ANALYZE_MODE_CMD)
            return

        try:
            self.m_session_manager.request_step()

        except DebuggerNotBroken:
            self.m_session_manager.report_exception(*sys.exc_info())

    do_s = do_step


    def do_next(self, arg):
        if arg != '':
            self.printer(STR_BAD_ARGUMENT)
            return
            
        if self.fAnalyzeMode:
            self.printer(STR_ILEGAL_ANALYZE_MODE_CMD)
            return

        try:
            self.m_session_manager.request_next()

        except DebuggerNotBroken:
            self.m_session_manager.report_exception(*sys.exc_info())

    do_n = do_next

    
    def do_return(self, arg):
        if arg != '':
            self.printer(STR_BAD_ARGUMENT)
            return
            
        if self.fAnalyzeMode:
            self.printer(STR_ILEGAL_ANALYZE_MODE_CMD)
            return

        try:
            self.m_session_manager.request_return()

        except DebuggerNotBroken:
            self.m_session_manager.report_exception(*sys.exc_info())

    do_r = do_return

    
    def do_jump(self, arg):
        try:
            lineno = int(arg)
        except ValueError:
            self.printer(STR_BAD_ARGUMENT)
            return

        try:
            self.m_session_manager.request_jump(lineno)

        except DebuggerNotBroken:
            self.m_session_manager.report_exception(*sys.exc_info())

    do_j = do_jump

    
    def do_bp(self, arg):
        if arg == '':
            self.printer(STR_BAD_ARGUMENT)
            return
        
        try:
            (filename, scope, lineno, expr) = self.__parse_bp_arg(arg, fAllowExpr = True)
            self.m_session_manager.set_breakpoint(filename, scope, lineno, True, expr)

        except BadArgument:    
            self.printer(STR_BAD_ARGUMENT)
        except IOError:
            self.printer(STR_FILE_NOT_FOUND % (filename, ))
        except InvalidScopeName:
            self.printer(STR_SCOPE_NOT_FOUND % (scope, ))
        except SyntaxError:
            self.printer(STR_BAD_EXPRESSION % (expr, ))
        except DebuggerNotBroken:
            self.m_session_manager.report_exception(*sys.exc_info())


    def do_be(self, arg):
        if arg == '':
            self.printer(STR_BAD_ARGUMENT)
            return
            
        try:
            id_list = []
            fAll = (arg == SYMBOL_ALL)
            
            if not fAll:
                sid_list = arg.split()
                id_list = [int(sid) for sid in sid_list]

            self.m_session_manager.enable_breakpoint(id_list, fAll)

        except ValueError:
            self.printer(STR_BAD_ARGUMENT)


    def do_bd(self, arg):
        if arg == '':
            self.printer(STR_BAD_ARGUMENT)
            return
            
        try:
            id_list = []
            fAll = (arg == SYMBOL_ALL)
            
            if not fAll:
                sid_list = arg.split()
                id_list = [int(sid) for sid in sid_list]

            self.m_session_manager.disable_breakpoint(id_list, fAll)

        except ValueError:
            self.printer(STR_BAD_ARGUMENT)


    def do_bc(self, arg):
        if arg == '':
            self.printer(STR_BAD_ARGUMENT)
            return
            
        try:
            id_list = []
            fAll = (arg == SYMBOL_ALL)
            
            if not fAll:
                sid_list = arg.split()
                id_list = [int(sid) for sid in sid_list]

            self.m_session_manager.delete_breakpoint(id_list, fAll)

        except ValueError:
            self.printer(STR_BAD_ARGUMENT)


    def do_bl(self, arg):
        bpl = self.m_session_manager.get_breakpoints()
            
        bplk = bpl.keys()
        bplk.sort()
        
        print >> self.stdout, STR_BREAKPOINTS_LIST    
        for id in bplk:
            bp = bpl[id]

            if bp.m_expr:
                expr = bp.m_expr + '\n'
            else:
                expr = ''

            scope = bp.m_scope_fqn

            if scope.startswith(MODULE_SCOPE + '.'):
                scope = scope[len(MODULE_SCOPE) + 1:]

            elif scope.startswith(MODULE_SCOPE2 + '.'):
                scope = scope[len(MODULE_SCOPE2) + 1:]   
                
            state = [STATE_DISABLED, STATE_ENABLED][bp.isEnabled()]
            print >> self.stdout, STR_BREAKPOINTS_TEMPLATE % (id, state, bp.m_lineno, clip_filename(bp.m_filename, 45), calc_suffix(scope, 45), calc_prefix(expr, 50))
            

    def do_save(self, arg):
        self.m_session_manager.save_breakpoints(arg)
        print >> self.stdout, STR_BREAKPOINTS_SAVED    
        return
            
        
    def do_load(self, arg):
        try:
            self.m_session_manager.load_breakpoints(arg)
            print >> self.stdout, STR_BREAKPOINTS_LOADED    
            return

        except IOError:
            error = [STR_BREAKPOINTS_FILE_NOT_FOUND, STR_BREAKPOINTS_NOT_FOUND][arg == '']
            self.printer(error)


    def do_stack(self, arg):
        if self.fAnalyzeMode and (arg != ''):
            self.printer(STR_ILEGAL_ANALYZE_MODE_ARG)
            return

        try:
            tid_list = []
            fAll = (arg == SYMBOL_ALL)
            
            if not fAll:
                sid_list = arg.split()
                tid_list = [int(sid) for sid in sid_list]
                
            sl = self.m_session_manager.get_stack(tid_list, fAll)

            if len(sl) == 0:
                self.printer(STR_NO_THREADS_FOUND)
                return

            frame_index = self.m_session_manager.get_frame_index()

            m = None    
            for st in sl:
                s = st.get(DICT_KEY_STACK, [])
                tid = st.get(DICT_KEY_TID, 0)
                fBroken = st.get(DICT_KEY_BROKEN, False)
                fCurrent = st.get(DICT_KEY_CURRENT_TID, False)

                if m is not None:
                    print >> self.stdout
                    
                print >> self.stdout, STR_STACK_TRACE % (tid, )    
                i = 0
                while i < len(s):
                    e = s[-(1 + i)]

                    marker = [SOURCE_STATE_UNBROKEN, SYMBOL_MARKER][fBroken]
                    
                    if fCurrent:
                        m = ['', marker][i == frame_index]
                    else:
                        m = ['', marker][i == 0]
                        
                    print >> self.stdout, ' %1s %5d  %-28s  %4d  %s' % (m, i, calc_suffix(e[0], 28), e[1], calc_prefix(e[2], 20))
                    i += 1
                    
        except ValueError:
            self.printer(STR_BAD_ARGUMENT)
        except (NoExceptionFound, NoThreads):
            self.m_session_manager.report_exception(*sys.exc_info())

    do_k = do_stack

    
    def do_list(self, arg):
        rf = arg.rfind(BP_FILENAME_SEP)
        if rf == -1:
            _filename = ''
            __args2 = arg
        else:
            _filename = arg[:rf]
            __args2 = arg[rf + 1:]
            
        _args = __args2.split(BP_EVAL_SEP)
        
        fAll = (_args[0] == SYMBOL_ALL)
        fMore = (_args[0] == SOURCE_MORE)
        fLess = (_args[0] == SOURCE_LESS)
        fEntire = (_args[0] == SOURCE_ENTIRE_FILE)
        fCurrent = (_args[0] == '')
        fLine = False
        l = 1
        
        try:
            if len(_args) > 1:
                nlines = int(_args[1])
            else:
                nlines = self.m_last_nlines

            if not (fAll or fMore or fLess or fEntire or fCurrent):     
                l = int(_args[0])
                fLine = True

        except ValueError:
            self.printer(STR_BAD_ARGUMENT)
            return

        if self.fAnalyzeMode and fAll:
            self.printer(STR_ILEGAL_ANALYZE_MODE_ARG)
            return

        if fMore and self.m_last_source_line:
            l = max(1, self.m_last_source_line + self.m_last_nlines / 2 + 1)
            fLine = True
        elif fLess and self.m_last_source_line:
            l = max(1, self.m_last_source_line - (self.m_last_nlines - 1) / 2 - nlines)
            fLine = True
            
        try:
            if fEntire:
                r = [self.m_session_manager.get_source_file(_filename, -1, -1)]
            elif fLine:
                r = [self.m_session_manager.get_source_file(_filename, l, nlines)]
            elif _filename != '':
                r = [self.m_session_manager.get_source_file(_filename, l, nlines)]
            else:
                r = self.m_session_manager.get_source_lines(nlines, fAll)

            if len(r) == 0:
                self.printer(STR_NO_THREADS_FOUND)
                return

            m = None    
            for d in r:
                tid = d.get(DICT_KEY_TID, 0)
                filename = d.get(DICT_KEY_FILENAME, '')
                breakpoints = d.get(DICT_KEY_BREAKPOINTS, {})
                source_lines = d.get(DICT_KEY_LINES, [])
                first_lineno = d.get(DICT_KEY_FIRST_LINENO, 0)

                if len(r) == 1 and first_lineno != 0:
                    l = first_lineno
                    
                fBroken = d.get(DICT_KEY_BROKEN, False)
                frame_event = d.get(DICT_KEY_EVENT, '')
                frame_lineno = d.get(DICT_KEY_FRAME_LINENO, 0)
                
                if m is not None:
                    print >> self.stdout
                    
                print >> self.stdout, STR_SOURCE_LINES % (tid, filename)    
                for i, line in enumerate(source_lines):
                    lineno = first_lineno + i
                    if lineno != frame_lineno:
                        m = ''
                    elif not fBroken:
                        m = SOURCE_STATE_UNBROKEN + SYMBOL_MARKER
                    elif frame_event == 'call':
                        m = SOURCE_EVENT_CALL + SYMBOL_MARKER
                    elif frame_event == 'line':
                        m = SOURCE_EVENT_LINE + SYMBOL_MARKER
                    elif frame_event == 'return':
                        m = SOURCE_EVENT_RETURN + SYMBOL_MARKER
                    elif frame_event == 'exception':
                        m = SOURCE_EVENT_EXCEPTION + SYMBOL_MARKER

                    if breakpoints.get(lineno, None) == STATE_ENABLED:
                        b = SOURCE_BP_ENABLED
                    elif breakpoints.get(lineno, None) == STATE_DISABLED:
                        b = SOURCE_BP_DISABLED
                    else:
                        b = ''
                        
                    print >> self.stdout, ' %2s %1s %5d  %s' % (m, b, lineno, calc_prefix(line[:-1], 60))

            if fAll or fEntire:
                self.m_last_source_line = None        
            elif len(source_lines) != 0:
                self.m_last_source_line = [l + (nlines - 1) / 2, frame_lineno][l == -1]

            self.m_last_nlines = nlines
                
        except (InvalidFrame, IOError):
            self.printer(STR_SOURCE_NOT_FOUND)
        except (NoExceptionFound, NoThreads):
            self.m_session_manager.report_exception(*sys.exc_info())

    do_l = do_list


    def do_up(self, arg):
        if arg != '':
            self.printer(STR_BAD_ARGUMENT)
            return

        try:
            fi = self.m_session_manager.get_frame_index()
            self.m_session_manager.set_frame_index(fi - 1)
            
        except DebuggerNotBroken:
            self.m_session_manager.report_exception(*sys.exc_info())


    def do_down(self, arg):
        if arg != '':
            self.printer(STR_BAD_ARGUMENT)
            return
            
        try:
            fi = self.m_session_manager.get_frame_index()
            self.m_session_manager.set_frame_index(fi + 1)
            
        except DebuggerNotBroken:
            self.m_session_manager.report_exception(*sys.exc_info())


    def evaluate_job(self, sync_event, expr):
        try:
            (value, warning, error) = self.m_session_manager.evaluate(expr)

            if warning:
                self.printer(STR_WARNING % (warning, ))

            if error:
                print >> self.stdout, error + '\n'

            print >> self.stdout, value

            if sync_event.isSet():
                print >> self.stdout, self.prompt, 

            return
                
        except (NoExceptionFound, DebuggerNotBroken):
            self.m_session_manager.report_exception(*sys.exc_info())
                    
        except (socket.error, CConnectionException):
            self.m_session_manager.report_exception(*sys.exc_info())
        except CException:
            self.m_session_manager.report_exception(*sys.exc_info())
        except:
            self.m_session_manager.report_exception(*sys.exc_info())
            print_debug_exception(True)
        

    def do_eval(self, arg):
        if arg == '':
            self.printer(STR_BAD_ARGUMENT)
            return
            
        sync_event = threading.Event()
        t = threading.Thread(target = self.evaluate_job, args = (sync_event, arg))
        t.start()
        t.join(WAIT_FOR_BREAK_TIMEOUT)

        if t.isAlive():
            print >> self.stdout, STR_OUTPUT_WARNING_ASYNC
            sync_event.set()
                        
    do_v = do_eval

    
    def execute_job(self, sync_event, suite):
        try:
            (warning, error) = self.m_session_manager.execute(suite)

            if warning:
                self.printer(STR_WARNING % (warning, ))

            if error:
                print >> self.stdout, error + '\n'

            if sync_event.isSet():
                print >> self.stdout, self.prompt, 

            return    
                
        except (NoExceptionFound, DebuggerNotBroken):
            self.m_session_manager.report_exception(*sys.exc_info())
                    
        except (socket.error, CConnectionException):
            self.m_session_manager.report_exception(*sys.exc_info())
        except CException:
            self.m_session_manager.report_exception(*sys.exc_info())
        except:
            self.m_session_manager.report_exception(*sys.exc_info())
            print_debug_exception(True)
        

    def do_exec(self, arg):
        if arg == '':
            self.printer(STR_BAD_ARGUMENT)
            return
            
        print >> self.stdout, STR_OUTPUT_WARNING

        sync_event = threading.Event()
        t = threading.Thread(target = self.execute_job, args = (sync_event, arg))
        t.start()
        t.join(WAIT_FOR_BREAK_TIMEOUT)

        if t.isAlive():
            print >> self.stdout, STR_OUTPUT_WARNING_ASYNC
            sync_event.set()
        
    do_x = do_exec

    
    def do_thread(self, arg):
        if self.fAnalyzeMode and (arg != ''):
            self.printer(STR_ILEGAL_ANALYZE_MODE_ARG)
            return

        try:
            if arg != '':
                tid = int(arg)
                self.m_session_manager.set_thread(tid)

                print >> self.stdout, STR_THREAD_FOCUS_SET
                return

            (current_thread_id, tl) = self.m_session_manager.get_thread_list()

            print >> self.stdout, STR_ACTIVE_THREADS    
            for i, t in enumerate(tl):
                m = ['', SYMBOL_MARKER][t[DICT_KEY_TID] == current_thread_id]
                state = [STATE_RUNNING, STR_STATE_BROKEN][t[DICT_KEY_BROKEN]]
                print >> self.stdout, ' %1s %3d  %5d  %-15s  %s' % (m, i, t[DICT_KEY_TID], t[DICT_KEY_NAME], state[:25])
                
        except ValueError:
            self.printer(STR_BAD_ARGUMENT)
        except ThreadNotFound:
            self.printer(STR_THREAD_NOT_FOUND)
        except DebuggerNotBroken:
            self.m_session_manager.report_exception(*sys.exc_info())

    do_t = do_thread


    def do_analyze(self, arg):
        if arg != '':
            self.printer(STR_BAD_ARGUMENT)
            return

        try:
            self.m_session_manager.set_analyze(not self.fAnalyzeMode)

        except DebuggerNotBroken:
            self.m_session_manager.report_exception(*sys.exc_info())

    do_a = do_analyze

   
    def do_trap(self, arg):
        if arg == '':
            ftrap = self.m_session_manager.get_trap_unhandled_exceptions()
            print >> self.stdout, STR_TRAP_MODE % (str(ftrap), )
            return

        if arg == str(True):
            ftrap = True
        elif arg == str(False):
            ftrap = False
        else:
            print >> self.stdout, STR_BAD_ARGUMENT
            return

        self.m_session_manager.set_trap_unhandled_exceptions(ftrap)

   
    def do_fork(self, arg):
        (ffork_into_child, ffork_auto) = self.m_session_manager.get_fork_mode()

        if arg == '':
            x = [FORK_PARENT, FORK_CHILD][ffork_into_child]
            y = [FORK_MANUAL, FORK_AUTO][ffork_auto]

            print >> self.stdout, STR_FORK_MODE % (x, y)
            return 

        arg = arg.lower()

        if FORK_PARENT in arg:
            ffork_into_child = False
        elif FORK_CHILD in arg:
            ffork_into_child = True

        if FORK_AUTO in arg:
            ffork_auto = True
        elif FORK_MANUAL in arg:
            ffork_auto = False

        self.m_session_manager.set_fork_mode(ffork_into_child, ffork_auto)
 

    def do_password(self, arg):
        if arg == '':
            _rpdb2_pwd = self.m_session_manager.get_password()
            if _rpdb2_pwd is None:
                print >> self.stdout, STR_PASSWORD_NOT_SET
            else:    
                print >> self.stdout, STR_PASSWORD_SET % (_rpdb2_pwd, )
            return

        _rpdb2_pwd = arg.strip('"\'')
        
        self.m_session_manager.set_password(_rpdb2_pwd)
        print >> self.stdout, STR_PASSWORD_SET % (_rpdb2_pwd, )

            
    def do_remote(self, arg):
        if arg == '':
            fAllowRemote = self.m_session_manager.get_remote()
            print >> self.stdout, STR_REMOTE_MODE % (str(fAllowRemote), )
            return

        if arg == str(True):
            fAllowRemote = True
        elif arg == str(False):
            fAllowRemote = False
        else:
            print >> self.stdout, STR_BAD_ARGUMENT
            return

        self.m_session_manager.set_remote(fAllowRemote)
        print >> self.stdout, STR_REMOTE_MODE % (str(fAllowRemote), )


    def do_stop(self, arg):        
        self.m_session_manager.stop_debuggee()
            
        
    def do_exit(self, arg):
        if arg != '':
            self.printer(STR_BAD_ARGUMENT)
            return

        if self.m_session_manager.get_state() != STATE_DETACHED:    
            try:
                self.do_stop('')
                
            except (socket.error, CConnectionException):
                self.m_session_manager.report_exception(*sys.exc_info())
            except CException:
                self.m_session_manager.report_exception(*sys.exc_info())
            except:
                self.m_session_manager.report_exception(*sys.exc_info())
                print_debug_exception(True)

        print >> self.stdout, ''

        return True 

    do_EOF = do_exit    


    def do_copyright(self, arg):
        self.print_notice(COPYRIGHT_NOTICE)


    def do_license(self, arg):
        self.print_notice(LICENSE_NOTICE + COPY_OF_THE_GPL_LICENSE)


    def do_credits(self, arg):
        self.print_notice(CREDITS_NOTICE)


    def do_help(self, arg):
        cmd.Cmd.do_help(self, arg)

        if arg == '':
            help_notice = """Security:
----------------

password    - Get or set the channel password.
remote      - Get or set "allow connections from remote machines" mode.

Session Control:
-----------------

host        - Display or change host.
attach      - Display scripts or attach to a script on host.
detach      - Detach from script.
launch      - Start a script and attach to it.
restart     - Restart a script.
stop        - Shutdown the debugged script.
exit        - Exit from debugger.

Debuggee Control:
-----------------

break       - Request an immediate break.
step        - Continue to the next execution line.
next        - Continue to the next execution line in the current frame.
return      - Continue until the debugger is about to return from the frame.
jump        - Jump to a line in the current scope.
go          - Continue execution.

Breakpoints Control:
--------------------

bp          - Set a break point.
bd          - Disable a breakpoint.
be          - Enable a breakpoint.
bc          - Clear (delete) a breakpoint.
bl          - List all breakpoints.
load        - Load session breakpoints.
save        - save session breakpoints.

Misc:
-----

thread      - Display threads or switch to a particular thread.
list        - List source code.
stack       - Display stack trace.
up          - Go up one frame in stack.
down        - Go down one frame in stack.
eval        - Evaluate expression in the context of the current frame.
exec        - Execute suite in the context of the current frame.
analyze     - Toggle analyze last exception mode.
trap        - Get or set "trap unhandled exceptions" mode.
fork        - Get or set fork handling mode.

License:
----------------

copyright   - Print copyright notice.
license     - Print license.
credits     - Print credits information.


type help <topic> for futher information."""

            self.print_notice(help_notice)

        
    def help_copyright(self):
        print >> self.stdout, """copyright

Print copyright notice."""  


    def help_license(self):
        print >> self.stdout, """license

Print license."""  


    def help_credits(self):
        print >> self.stdout, """credits

Print credits information."""  


    def help_help(self):
        print >> self.stdout, """help <cmd>

Print help for command <cmd>.
On the other hand I guess that you already know that, don't you?"""  


    def help_analyze(self):
        print >> self.stdout, """analyze

(shorthand - a)

Toggle analyze last exception mode.

The following changes to the debugger behavior apply in analyze mode:
The debugger prompt changes to 'Analyze>'.
'go', 'step', 'next', and 'return' are not allowed.
'thread' does not allow to change the thread focus.
'stack' allows no arguments.
'list' does not accept the '*' (all threads) argument
'stack', 'list', 'eval', 'exec', 'up', and 'down' operate on the thrown 
exception."""

    help_a = help_analyze    


    def help_password(self):
        print >> self.stdout, """password <password>

Get or set the channel password.

Communication between the console and the debuggee is always authenticated and
optionally encrypted. The password (A secret known to the console and the
debuggee alone) governs both security methods. The password is never 
communicated between the two components on the communication channel.

A password is always required since unsecured communication between the 
console and the debuggee may expose your machine to attacks."""


    def help_remote(self):
        print >> self.stdout, """remote [True | False]

Get or set "allow connections from remote machines" mode.

When set to False: 
Newly launched debuggees will listen on localhost only. In this mode, debugger
consoles on remote machines will NOT BE able to see or attach to the debuggee.

When set to True: 
Newly launched debuggees will listen on INADDR_ANY. In this mode, debugger 
consoles on remote machines will BE able to see and attach to the debuggee."""


    def help_trap(self):
        print >> self.stdout, """trap [True | False]

Get or set "trap unhandled exceptions" mode.

When set to False: 
Debuggee will ignore unhandled exceptions.

When set to True: 
Debuggee will pause on unhandled exceptions for inspection."""


    def help_fork(self):
        print >> self.stdout, """fork [parent | child] [manual | auto]

Get or set fork handling mode.

Without arguments returns the current mode.

When 'parent' is specified the debugger will continue to debug the original
parent process after a fork.

When 'child' is specified the debugger will switch to debug the forked 
child process after a fork.

When 'manual' is specified the debugger will pause before doing a fork.

When 'auto' is specified the debugger will go through the fork without 
pausing and will make the forking decision based on the parent/child 
setting.

WARNING:
On some Posix OS such as FreeBSD, Stepping into the child fork 
can result in termination of the child process since the debugger
uses threading for its operation and on these systems threading and 
forking can conflict.
"""


    def help_stop(self):
        print >> self.stdout, """stop

Shutdown the debugged script."""


    def help_launch(self):
        print >> self.stdout, """launch [-k] <script_name> [<script_args>]

Start script <script_name> and attach to it.

-k  Don't change the current working directory. By default the working
    directory of the launched script is set to its folder."""


    def help_restart(self):
        print >> self.stdout, """restart

Restart a script with same arguments from last launch."""



    def help_attach(self):
        print >> self.stdout, """attach [<arg>]

Without an argument, 'attach' prints the scripts available for debugging
on the selected host. To select a host use the 'host' command. A script is
considered available for debugging only if it is using the rpdb2 module or
has been executed by the debugger.
If the debugger is already attached to a script, a special character will
mark that script in the list.

When <arg> is an integer the debugger will try to attach to a script with
that pid. 
When <arg> is a string the debugger will try to attach to a script
with that name in the list."""  


    def help_detach(self):
        print >> self.stdout, """detach

Detach from the script the debugger is currently attached to. The detached
script will continue execution."""  


    def help_break(self):
        print >> self.stdout, """break 

(shorthand - b)

Request script to break (pause execution as if it hit a breakpoint). 
The 'break' command returns immdeiately but the break is only established 
when an active thread submits to the debugger control. If a thread is 
doing a system call or executing C code, this will happen only when 
it returns to do python code."""  

    help_b = help_break
    

    def help_bp(self):
        print >> self.stdout, """bp [<filename>':'] (<line> | <scope>) [',' <expr>]

Set a breakpoint.

<filename> - either the filename or the module name. 
<line>     - is the line number to assign the breakpoint to.
<scope>    - is a "fully qualified" function name. That is, not only the 
             function name but also the class name (in case of a member 
             function), such as MyClass.MyMemberFunction.
<expr>     - condition to evaluate in the context of the frame. If it
             evaluates to 'True' the break point will break into the debugger.

In case the <filemame> is omitted, the current file is assumed. In this case 
the debuggee has to be waiting at break point.

Examples:

    bp test_file.py:20
    bp test_file.py:MyClass.Foo
    bp 304

Type 'help break' for more information on breakpoints and threads."""


    def help_be(self):
        print >> self.stdout, """be (<id_list> | '*')
        
Enable breakpoints.

<id_list> - is a space delimited list of at least one breakpoint id
'*' - Enable all breakpoints."""


    def help_bd(self):
        print >> self.stdout, """bd (<id_list> | '*')
        
Disable breakpoints.

<id_list> - is a space delimited list of at least one breakpoint id
'*' - disable all breakpoints."""


    def help_bc(self):
        print >> self.stdout, """bc (<id_list> | '*')
        
Clear (delete) breakpoints.

<id_list> - is a space delimited list of at least one breakpoint id
'*' - clear all breakpoints."""


    def help_bl(self):
        print >> self.stdout, """bl

List all breakpoints, sorted by their id."""


    def help_load(self):
        print >> self.stdout, """load [<filename>]
        
Load breakpoints.

<filename> - optional breakpoints filename. The filename should not include
             a file extension."""


    def help_save(self):
        print >> self.stdout, """save [<filename>]
        
save breakpoints.

<filename> - optional breakpoints filename. The filename should not include
             a file extension."""


    def help_go(self):
        print >> self.stdout, """go [[<filename>':'] (<line> | <scope>)]

(shorthand - g)

Resume execution of a script that is waiting at break point. 
If an argument is present, continue execution until that argument is reached.

<filename> - is the file name which basically is the script's name without
             the '.py' extension. 
<line>   - is the line number to assign the breakpoint to.
<scope>  - is a "fully qualified" function name. That is, not only the 
           function name but also the class name (in case of a member 
           function), such as MyClass.MyMemberFunction."""

    help_g = help_go
    

    def help_exit(self):
        print >> self.stdout, """exit

Exit the debugger. If the debugger is attached to a script, the debugger
will attempt to detach from the script first."""  

    help_EOF = help_exit
    

    def help_host(self):
        print >> self.stdout, """host [<arg>]

Without an argument, 'host' prints the current selected host.
With an argument <arg>, 'host' attempts to resolve <arg> to a known ip 
address or a domain name. If it is successful, that host will become the
selected host. 
The default selected host is the local host.
Subsequent 'attach' commands will be done on the selected host. 

Type 'help attach' for more information."""  

    def help_stack(self):
        print >> self.stdout, """stack [<tid> | '*']

(shorthand - k)

Without an argument, 'stack' prints the stack trace of the focused thread.
If the thread is waiting at break point a special character will mark the 
focused frame.

<tid> - print the stack of thread <tid> 
'*'   - print the stacks of all active threads.

Type 'help break' for more information on breakpoints and threads.
Type 'help up' or 'help down' for more information on focused frames."""  

    help_k = help_stack
    

    def help_list(self):
        print >> self.stdout, """list [<file_name>:][<line_no> | '+' | '-' | '^' | '*'] [',' <nlines>]

(shorthand - l)

Without an argument, 'list' prints the source lines around the current line
of the focused thread in the focused frame. A special character sequence will 
mark the current line according to the event:

    'C>' - call - A function is called.
    'L>' - line - The interpreter is about to execute a new line of code.
    'R>' - return - A function is about to return.
    'E>' - exception - An exception has been thrown.
    '*>' - running - The thread is running.

If a breakpoint is assigned to a line, that line will be marked with:

    'B' - if the breakpoint is enabled
    'D' - if the breakpoint is disabled

<file_name> - List source from filename    
<line_no>   - Print the source lines around that line number in the same file 
              of the current line.
'+'         - Print the next lines in the file.
'-'         - Print the previous lines in the file.
'^'         - Print the entire file.
'*'         - Print the source lines for each of the active threads.
<nlines>    - Print <nlines> of source

Type 'help break' for more information on breakpoints and threads.
Type 'help up' or 'help down' for more information on focused frames."""  

    help_l = help_list
    

    def help_thread(self):
        print >> self.stdout, """thread [<no> | <tid>]

(shorthand - t)

Without an argument, 'thread' prints the list of known active threads, with
their corresponding state, which can be either 'running' or 
'waiting at break point'. A special character will mark the focused thread.

With an argument <tid>, 'thread' will attempt to set the debugger focus to
the thread of that tid.
With an argument <no>, 'thread' will attempt to set the debugger focus to 
the thread of that order in the thread list.

Type 'help break' for more information on breakpoints and threads."""

    help_t = help_thread


    def help_jump(self):
        print >> self.stdout, """jump <lineno>

(shorthand - j)

Jump to line <lineno> in the current scope."""

    help_j = help_jump
    

    def help_next(self):
        print >> self.stdout, """next

(shorthand - n)

Continue execution until the next line in the current function
is reached or it returns."""

    help_n = help_next
    

    def help_step(self):
        print >> self.stdout, """next

(shorthand - s)

Execute the current line, stop at the first possible occasion
(either in a function that is called or in the current function)."""

    help_s = help_step    


    def help_return(self):
        print >> self.stdout, """next

(shorthand - r)

Continue execution until the current function returns."""

    help_r = help_return    


    def help_up(self):
        print >> self.stdout, """up

move the debugger focus one frame up the stack of the debugged thread 
(closer to the current, most recently executed frame). Evaluation of 
expressions or execution of statements will be done at the local and global 
name spaces of the focused frame.

Type 'help eval' for more information on evaluation of expressions.
Type 'help exec' for more information on execution of statements."""


    def help_down(self):
        print >> self.stdout, """down

move the debugger focus one frame down the stack of the debugged thread 
(closer to the current, most recently executed frame). Evaluation of 
expressions or execution of statements will be done at the local and global 
name spaces of the focused frame.

Type 'help eval' for more information on evaluation of expressions.
Type 'help exec' for more information on execution of statements."""


    def help_eval(self):
        print >> self.stdout, """eval <expr>

(shorthand - v)

Evaluate the python expression <expr> under the global and local name spaces
of the currently focused frame.

Example:
'eval locals()' - will display the dictionary of the local variables.

IMPORTANT: Any changes to the global name space will be discarded unless the
focused stack frame is the top most frame.

Type 'help up' or 'help down' for more information on focused frames."""  

    help_v = help_eval


    def help_exec(self):
        print >> self.stdout, """exec <stmt>

(shorthand - x)

Execute the python suite <stmt> under the global and local name spaces
of the currently focused frame.

Example:
'exec i += 1'

IMPORTANT: Any changes to the global name space will be discarded unless the
focused stack frame is the top most frame.

Type 'help up' or 'help down' for more information on focused frames."""  

    help_x = help_exec

    

#
# ---------------------------------------- Replacement Functions ------------------------------------
#



def __fork():
    global g_forktid
    g_forktid = setbreak()

    #
    # os.fork() has been called. 
    #
    # You can choose if you would like the debugger
    # to continue with the parent or child fork with
    # the 'fork' console command.
    # 
    # For example: 'fork child' or 'fork parent'
    # Type: 'help fork' for more information.
    #
    # WARNING: 
    # On some Posix OS such as FreeBSD, 
    # Stepping into the child fork can result in 
    # termination of the child process.
    #
    # *** RPDB2 SAYS: Read the entire comment! ***
    #
    return g_os_fork()



g_os_fork = None

if __name__ == 'rpdb2' and 'fork' in dir(os) and os.fork != __fork:
    g_os_fork = os.fork
    os.fork = __fork



def __exit(n):
    global g_fos_exit

    if type(n) == int:
        g_fos_exit = (setbreak() != None)

    #
    # os._exit(n) has been called.
    #
    # Stepping on from this point will result 
    # in program termination.
    #
    return g_os_exit(n)



g_os_exit = None

if __name__ == 'rpdb2' and '_exit' in dir(os) and os._exit != __exit:
    g_os_exit = os._exit
    os._exit = __exit



def __execv(path, args):
    global g_exectid
    
    if os.path.isfile(path):
        g_exectid = setbreak()

    #
    # os.execv() has been called. 
    #
    # Stepping on from this point will result 
    # in termination of the debug session if
    # the exec operation completes successfully.
    #
    return g_os_execv(path, args)



g_os_execv = None

if __name__ == 'rpdb2' and 'execv' in dir(os) and os.execv != __execv:
    g_os_execv = os.execv
    os.execv = __execv



def __execve(path, args, env):
    global g_exectid

    if os.path.isfile(path):
        g_exectid = setbreak()

    #
    # os.execve() has been called. 
    #
    # Stepping on from this point will result 
    # in termination of the debug session if
    # the exec operation completes successfully.
    #
    return g_os_execve(path, args, env)



g_os_execve = None

if __name__ == 'rpdb2' and 'execve' in dir(os) and os.execve != __execve:
    g_os_execve = os.execve
    os.execve = __execve



def __function_wrapper(function, args, kwargs):
    __settrace(depth = 1)

    #
    # Debuggee breaks (pauses) here
    # on unhandled exceptions.
    # Use analyze mode for post mortem.
    # type 'help analyze' for more information.
    #
    return function(*args, **kwargs)



def __start_new_thread(function, args, kwargs = {}):
    return g_thread_start_new_thread(__function_wrapper, (function, args, kwargs))



g_thread_start_new_thread = None

if __name__ == 'rpdb2' and 'start_new_thread' in dir(thread) and thread.start_new_thread != __start_new_thread:
    g_thread_start_new_thread = thread.start_new_thread
    thread.start_new_thread = __start_new_thread



#
# ---------------------------------------- main ------------------------------------
#



def __settrace(depth = 2):
    if g_debugger is None:
        return
        
    f = sys._getframe(depth)
    g_debugger.settrace(f, f_break_on_init = False)

    

def __setbreak():
    if g_debugger is None:
        return
        
    f = sys._getframe(2)
    g_debugger.setbreak(f)

    return thread.get_ident()

    

def _atexit(fabort = False):
    if g_fignore_atexit:
        return

    print_debug("Entered _atexit() in pid %d" % _getpid())

    if g_debugger is None:
        return

    if not fabort:
        g_debugger.stoptrace()
        
    g_debugger.send_event_exit()

    time.sleep(1.0)

    g_server.shutdown()
    g_debugger.shutdown()

    if fabort:
        os.abort()
        


def myimport(*args, **kwargs):
    if len(args) != 1 or len(kwargs) != 0:
        return __import__(*args, **kwargs)

    name = args[0]
    if name in sys.modules:
        return

    return __import__(name)



def workaround_import_deadlock():
    xmlrpclib.loads(XML_DATA)    
    pickle.loads('(S\'\\xb3\\x95\\xf9\\x1d\\x105c\\xc6\\xe2t\\x9a\\xa5_`\\xa59\'\np0\nS"(I0\\nI1\\nS\'5657827\'\\np0\\n(S\'server_info\'\\np1\\n(tI0\\ntp2\\ntp3\\n."\np1\ntp2\n.0000000')
    pickle.__import__ = myimport



def __start_embedded_debugger(_rpdb2_pwd, fAllowUnencrypted, fAllowRemote, timeout, fDebug):
    global g_server
    global g_debugger
    global g_fDebug
    global g_initial_cwd

    try:
        g_server_lock.acquire()
        
        if g_debugger is not None:
            f = sys._getframe(2)
            g_debugger.setbreak(f)
            return

        g_fDebug = fDebug
       
        workaround_import_deadlock()

        if (not fAllowUnencrypted) and not is_encryption_supported():
            raise EncryptionNotSupported
        
        f = sys._getframe(2)
        filename = calc_frame_path(f)

        #
        # This is an attempt to address the Python problem of recording only
        # relative paths in __file__ members of modules in the following case.
        #
        if sys.path[0] == '':
            g_initial_cwd = [os.getcwd(), os.getcwdu()]
            
        atexit.register(_atexit)
        
        g_debugger = CDebuggerEngine(fembedded = True)

        g_server = CDebuggeeServer(filename, g_debugger, _rpdb2_pwd, fAllowUnencrypted, fAllowRemote)
        g_server.start()

        g_debugger.settrace(f, timeout = timeout)

    finally:
        g_server_lock.release()


    
def StartServer(args, fchdir, _rpdb2_pwd, fAllowUnencrypted, fAllowRemote, rid): 
    global g_server
    global g_debugger
    global g_module_main
   
    try:
        ExpandedFilename = FindFile(args[0])
        _path = g_found_unicode_files.get(ExpandedFilename, ExpandedFilename)
        
        if fchdir:   
            os.chdir(os.path.dirname(_path))

        if type(_path) == unicode:
            prefix = os.path.join(os.getcwdu(), '')
            _path = _path.replace(winlower(prefix), '')
        
    except IOError:
        print 'File', args[0], ' not found.'
        return

    print_debug('Starting server with: %s' % ExpandedFilename)

    #
    # Replace the rpdb2.py directory with the script directory in 
    # the search path
    #

    spe = ExpandedFilename
    if os.path.islink(ExpandedFilename):
        spe = os.path.realpath(ExpandedFilename)

    sys.path[0] = os.path.dirname(spe)

    sys.argv = args

    atexit.register(_atexit)

    g_debugger = CDebuggerEngine()

    g_server = CDebuggeeServer(ExpandedFilename, g_debugger, _rpdb2_pwd, fAllowUnencrypted, fAllowRemote, rid)
    g_server.start()

    try:
        g_debugger.m_bp_manager.set_temp_breakpoint(ExpandedFilename, '', 1, fhard = True)
    except:
        pass

    f = sys._getframe(0)
    g_debugger.settrace(f, f_break_on_init = False, builtins_hack = ExpandedFilename)

    g_module_main = -1
    del sys.modules['__main__']

    #
    # An exception in this line occurs if
    # there is a syntax error in the debugged script or if
    # there was a problem loading the debugged script.
    #
    imp.load_source('__main__', _path)    
        


def StartClient(command_line, fAttach, fchdir, _rpdb2_pwd, fAllowUnencrypted, fAllowRemote, host):
    if (not fAllowUnencrypted) and not is_encryption_supported():
        print STR_ENCRYPTION_SUPPORT_ERROR
        return 2
        
    sm = CSessionManager(_rpdb2_pwd, fAllowUnencrypted, fAllowRemote, host)
    c = CConsole(sm)
    c.start()

    time.sleep(1.0)

    try:
        if fAttach:
            sm.attach(command_line)
        elif command_line != '':
            sm.launch(fchdir, command_line)
            
    except (socket.error, CConnectionException):
        sm.report_exception(*sys.exc_info())
    except CException:
        sm.report_exception(*sys.exc_info())
    except:
        sm.report_exception(*sys.exc_info())
        print_debug_exception(True)
        
    c.join()



def PrintUsage(fExtended = False):
    scriptName = os.path.basename(sys.argv[0])
    print """ %(rpdb)s [options] [<script-name> [<script-args>...]]

    Where the options can be a combination of the following:
    -h, --help      print this help.
    -d, --debuggee  start debuggee and break into it, without starting a 
                    debugger console. 
    -a, --attach    Attach to an already started debuggee.
    -o, --host      Specify host for attachment.
    -r, --remote    Allow debuggees to accept connections from remote machines.
    -e, --encrypt   Force encrypted connections between debugger and debuggees.
    -p, --pwd       Password. This flag is available only on NT systems. 
                    On other systems the password will be queried interactively 
                    if it is needed.
    -s, --screen    Use the Unix screen utility when starting the debuggee.
                    Note that the debugger should be started as follows:
                    screen rpdb2 -s [options] [<script-name> [<script-args>...]]
    -c, --chdir     Change the working directory to that of the launched 
                    script.
    --debug         Debug prints.
""" % {"rpdb": scriptName}
    
    if not fExtended:
        return
        
    print __doc__



def main(StartClient_func = StartClient):
    global g_fScreen
    global g_fDebug
    
    create_rpdb_settings_folder()

    try:
        options, _rpdb2_args = getopt.getopt(
                            sys.argv[1:], 
                            'hdao:rtep:sc', 
                            ['help', 'debugee', 'debuggee', 'attach', 'host=', 'remote', 'plaintext', 'encrypt', 'pwd=', 'rid=', 'screen', 'chdir', 'base64=', 'debug']
                            )

    except getopt.GetoptError, e:
        print e
        return 2
        
    fWrap = False
    fAttach = False
    fSpawn = False
    fStart = False
    
    encoded_path = None
    secret = None
    host = None
    _rpdb2_pwd = None
    fchdir = False
    fAllowRemote = False
    fAllowUnencrypted = True
    
    for o, a in options:
        if o in ['-h', '--help']:
            PrintUsage()
            return 0
        if o in ['--debug']:
            g_fDebug = True 
        if o in ['-d', '--debugee', '--debuggee']:
            fWrap = True
        if o in ['-a', '--attach']:
            fAttach = True
        if o in ['-o', '--host']:
            host = a
        if o in ['-r', '--remote']:
            fAllowRemote = True
        if o in ['-t', '--plaintext']:
            fAllowUnencrypted = True
        if o in ['-e', '--encrypt']:
            fAllowUnencrypted = False
        if o in ['-p', '--pwd']:
            _rpdb2_pwd = a
        if o in ['--rid']:
            secret = a
        if o in ['-s', '--screen']:
            g_fScreen = True
        if o in ['-c', '--chdir']:
            fchdir = True
        if o in ['--base64']:
            encoded_path = a
    
    options = None
    o = None
    a = None

    if (_rpdb2_pwd is not None) and (os.name != 'nt'):
        print STR_PASSWORD_NOT_SUPPORTED
        return 2

    if fWrap and (len(_rpdb2_args) == 0):
        print "--debuggee option requires a script name with optional <script-arg> arguments"
        return 2
        
    if fWrap and fAttach:
        print "--debuggee and --attach can not be used together."
        return 2
        
    if fAttach and (len(_rpdb2_args) == 0):
        print "--attach option requires a script name to attach to."
        return 2
        
    if fAttach and (len(_rpdb2_args) > 1):
        print "--attach option does not accept <script-arg> arguments."
        return 2

    if fAttach and fAllowRemote:
        print "--attach and --remote can not be used together."
        return 2
        
    if (host is not None) and not fAttach:
        print "--host can only be used together with --attach."
        return 2

    if host is None:
        host = LOCALHOST    

    fSpawn = (len(_rpdb2_args) != 0) and (not fWrap) and (not fAttach)
    fStart = (len(_rpdb2_args) == 0)
    
    if fchdir and not (fWrap or fSpawn):
        print "-c can only be used when launching or starting a script from command line."
        return 2

    assert (fWrap + fAttach + fSpawn + fStart) == 1

    if fAttach and (os.name == POSIX):
        try:
            int(_rpdb2_args[0])

            _rpdb2_pwd = read_pwd_file(_rpdb2_args[0])
            delete_pwd_file(_rpdb2_args[0])

        except (ValueError, IOError):
            pass
            
    if (secret is not None) and (os.name == POSIX):
        _rpdb2_pwd = read_pwd_file(secret)
        
    if (fWrap or fAttach) and (_rpdb2_pwd in [None, '']):
        print STR_PASSWORD_MUST_BE_SET
        
        while True:
            _rpdb2_pwd = raw_input(STR_PASSWORD_INPUT)
            _rpdb2_pwd = _rpdb2_pwd.rstrip('\n')
            if _rpdb2_pwd != '':
                break

        print STR_PASSWORD_CONFIRM       
                
    if fWrap or fSpawn:
        try:
            if encoded_path != None:
                _u = base64.decodestring(encoded_path.translate(g_safe_base64_from))
                _path = _u.decode('utf8')
                _rpdb2_args[0] = _path

            FindFile(_rpdb2_args[0])
        except IOError:
            print STR_FILE_NOT_FOUND % (_rpdb2_args[0], )
            return 2
            
    if fWrap:
        if (not fAllowUnencrypted) and not is_encryption_supported():
            print STR_ENCRYPTION_SUPPORT_ERROR
            return 2

        StartServer(_rpdb2_args, fchdir, _rpdb2_pwd, fAllowUnencrypted, fAllowRemote, secret)
        
    elif fAttach:
        StartClient_func(_rpdb2_args[0], fAttach, fchdir, _rpdb2_pwd, fAllowUnencrypted, fAllowRemote, host)
        
    elif fStart:
        StartClient_func('', fAttach, fchdir, _rpdb2_pwd, fAllowUnencrypted, fAllowRemote, host)
        
    else:
        if len(_rpdb2_args) == 0:
            _rpdb2_args = ''
        else:
            _rpdb2_args = '"' + '" "'.join(_rpdb2_args) + '"'

        StartClient_func(_rpdb2_args, fAttach, fchdir, _rpdb2_pwd, fAllowUnencrypted, fAllowRemote, host)
   
    return 0



if __name__ == '__main__':
    import rpdb2

    #
    # Debuggee breaks (pauses) here
    # on unhandled exceptions.
    # Use analyze mode for post mortem.
    # type 'help analyze' for more information.
    #
    ret = rpdb2.main()

    #
    # Debuggee breaks (pauses) here 
    # before program termination. 
    #
    # You can step to debug any exit handlers.
    #
    rpdb2.setbreak()



