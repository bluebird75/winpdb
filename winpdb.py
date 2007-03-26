#! /usr/bin/env python

"""
    winpdb.py

    A GUI for rpdb2.py

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
    59 Temple Place, Suite 330, Boston, MA 02111-1307 USA    
"""

ABOUT_NOTICE = """winpdb.py

A GUI for rpdb2.py

Copyright (C) 2005-2007 Nir Aides

This program is free software; you can redistribute it and/or modify it 
under the terms of the GNU General Public License as published by the 
Free Software Foundation; either version 2 of the License, or any later 
version.

This program is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 

See the GNU General Public License for more details.

Credits:
Jurjen N.E. Bos - Compatibility with OS X."""

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



import sys



WXVER = "2.6"

STR_WXPYTHON_ERROR = """wxPython was not found.
wxPython 2.6 or higher is required to run the winpdb GUI.
You can get more information on wxPython in http://www.wxpython.org/
To use the debugger without a GUI, run rpdb2.py or _rpdb2.py"""



if 'wx' not in sys.modules:
    try:
        import wxversion   
        wxversion.ensureMinimal(WXVER)
    except ImportError:
        print STR_WXPYTHON_ERROR
        sys.exit(1)

import wx

assert wx.VERSION_STRING >= WXVER
        
import wx.lib.wxpTag
import wx.gizmos
import wx.html

import wx.lib.mixins.listctrl  as  listmix
import wx.stc as stc



import webbrowser
import traceback
import cStringIO
import threading
import xmlrpclib
import tempfile
import cPickle
import keyword
import weakref
import base64
import socket
import string
import Queue
import rpdb2
import time
import os



MARKER_BREAKPOINT_ENABLED = 5
MARKER_BREAKPOINT_DISABLED = 6
MARKER_CURRENT_LINE = 7
MARKER_CURRENT_LINE_HIT = 8

MARKER_CALL = 0
MARKER_LINE = 1
MARKER_RETURN = 2
MARKER_EXCEPTION = 3
MARKER_RUNNING = 4

MARKER_LIST = [MARKER_BREAKPOINT_ENABLED, MARKER_BREAKPOINT_DISABLED, MARKER_CURRENT_LINE, MARKER_CURRENT_LINE_HIT, MARKER_CALL, MARKER_LINE, MARKER_RETURN, MARKER_EXCEPTION, MARKER_RUNNING]

CAPTION_SOURCE = "Source"
CAPTION_CONSOLE = "Console"
CAPTION_THREADS = "Threads"
CAPTION_STACK = "Stack"
CAPTION_NAMESPACE = "Namespace"

CONSOLE_PROMPT = "\n> "

ENABLED = True
DISABLED = False

WINPDB_WILDCARD = "Python source (*.py)|*.py|All files (*.*)|*.*"

MSG_WARNING_TRAP = "Are you sure that you want to disable the trapping of unhandled exceptions? If you click Yes unhandled exceptions will not be caught."
MSG_WARNING_UNHANDLED_EXCEPTION = "An unhandled exception was caught. Would you like to analyze it?"
MSG_WARNING_TITLE = "Warning"
MSG_WARNING_TEMPLATE = "%s\n\nClick 'Cancel' to ignore this warning in the future."
MSG_ERROR_TITLE = "Error"
MSG_ERROR_HOST_TEXT = "Host '%s' not found."
MSG_ERROR_FILE_NOT_FOUND = "File not found."
MSG_ERROR_FILE_NOT_PYTHON = "Only Python files that end with '.py' are accepted."

STR_FILE_LOAD_ERROR = "Failed to load source file '%s' from debuggee."
STR_FILE_LOAD_ERROR2 = """Failed to load source file '%s' from debuggee.
You may continue to debug, but you will not see 
source lines from this file."""
STR_BLENDER_SOURCE_WARNING = "To debug Blender Python scripts you need to load them into the Blender text window and launch them from there."

DLG_EXPR_TITLE = "Enter Expression"
DLG_PWD_TITLE = "Password"
DLG_OPEN_TITLE = "Open Source"
DLG_LAUNCH_TITLE = "Launch"
DLG_ATTACH_TITLE = "Attach"
STATIC_EXPR = """The new expression will be evaluated at the debuggee
and its value will be set to the item."""
STATIC_PWD = """The password is used to secure communitcation between
the debugger console and the debuggee. Debuggees with
unmatching passwords will not appear in the attach
query list."""
STATIC_OPEN = """The source file entered will be fetched from the debugee."""
LABEL_EXPR = "New Expression:"
LABEL_PWD = "Set password:"
LABEL_OPEN = "File name:"
LABEL_LAUNCH_COMMAND_LINE = "Command line:"
LABEL_ATTACH_HOST = "Host:"
LABEL_CONSOLE = "Command:"
BUTTON_LAUNCH_BROWSE = "Browse"
BUTTON_ATTACH_REFRESH = "Refresh"
CHECKBOX_LAUNCH = "Set working directory to the script folder."

HLIST_HEADER_PID = "PID"
HLIST_HEADER_FILENAME = "Filename"

HLIST_HEADER_TID = "TID"
HLIST_HEADER_NAME = "Name"
HLIST_HEADER_STATE = "State"

HLIST_HEADER_FRAME = "Frame"
HLIST_HEADER_LINENO = "Line"
HLIST_HEADER_FUNCTION = "Function"
HLIST_HEADER_PATH = "Path"

TLC_HEADER_NAME = "Name"
TLC_HEADER_REPR = "Repr"
TLC_HEADER_TYPE = "Type"

WINPDB_TITLE = "Winpdb 1.1.1"
WINPDB_VERSION = "WINPDB_1_1_1"

WINPDB_SIZE = "winpdb_size"
WINPDB_MAXIMIZE = "winpdb_maximize"
SPLITTER_1_POS = "splitter_1_pos"
SPLITTER_2_POS = "splitter_2_pos"
SPLITTER_3_POS = "splitter_3_pos"
SPLITTER_4_POS = "splitter_4_pos"

WINPDB_SIZE_MIN = (640, 480)

WINPDB_SETTINGS_FILENAME = "winpdb_settings.cfg"

WINPDB_SETTINGS_DEFAULT = {
    WINPDB_SIZE: (800, 600),
    WINPDB_MAXIMIZE: False,
    SPLITTER_1_POS: 190,
    SPLITTER_2_POS: 294,
    SPLITTER_3_POS: 382,
    SPLITTER_4_POS: 305
}

AC_CHAR = "\t"
AC_EXIT = "Alt-X"
AC_ANALYZE = "F3"
AC_BREAK = "F4"
AC_GO = "F5"
AC_NEXT = "F6"
AC_STEP = "F7"
AC_GOTO = "F8"
AC_TOOGLE = "F9"
AC_RETURN = "F12"

ML_EMPTY = "<empty>"
ML_SEPARATOR = "<separator>"
ML_ROOT = "<root>"

ML_FILE = "&File"
ML_PWD = "&Password"
ML_LAUNCH = "&Launch"
ML_ATTACH = "&Attach"
ML_DETACH = "&Detach"
ML_STOP = "&Stop"
ML_RESTART = "&Restart"
ML_OPEN = "&Open Source"
ML_EXIT = "E&xit" + AC_CHAR + AC_EXIT

ML_BREAKPOINTS = "&Breakpoints"
ML_TOGGLE = "&Toggle" + AC_CHAR + AC_TOOGLE
ML_DISABLE = "&Disable All"
ML_ENABLE = "&Enable All"
ML_CLEAR = "&Clear All"
ML_LOAD = "&Load"
ML_SAVE = "&Save"

ML_CONTROL = "&Control"
ML_ANALYZE = "&Toggle Analyze" + AC_CHAR + AC_ANALYZE 
ML_GO = "&Go" + AC_CHAR + AC_GO
ML_BREAK = "&Break" + AC_CHAR + AC_BREAK
ML_STEP = "&Step" + AC_CHAR + AC_STEP
ML_NEXT = "&Next" + AC_CHAR + AC_NEXT
ML_RETURN = "&Return" + AC_CHAR + AC_RETURN
ML_GOTO = "&Run to Cursor" + AC_CHAR + AC_GOTO

ML_WINDOW = "&Window"

ML_HELP = "&Help"
ML_WEBSITE = "&Website"
ML_SUPPORT = "&Support"
ML_DOCS = "&Online Docs"
ML_UPDATES = "&Check for Updates"
ML_LICENSE = "&License"
ML_ABOUT = "&About"

TB_GO = "Go"
TB_BREAK = "Break"
TB_STEP = "Step"
TB_NEXT = "Next"
TB_RETURN = "Return"
TB_GOTO = "Run to cursor"
TB_TOGGLE_BP = "Toggle breakpoint."
TB_FILTER = "Filter modules, classes, and functions from the global and local namespaces."
TB_EXCEPTION = "Toggle 'analyze exception' mode."
TB_TRAP = "Trap unhandled exceptions."

COMMAND = "command"
TOOLTIP = "tooltip"
DATA = "data"
DATA2 = "data2"
ID = "id"
LABEL = "label"
FORMAT = "format"
KEYS = "keys"
WIDTH = "width"

PWD_TIP = "Set connection password."
LAUNCH_TIP = "Launch a new debugged script."
ATTACH_TIP = "Attach to a debugged script."
DETACH_TIP = "Detach from debugged sctipt."
STOP_TIP = "Shutdown the debugged script."
RESTART_TIP = "Restart the debugged script."
OPEN_TIP = "Open source file in the source viewer."
WEBSITE_TIP = "Open the Winpdb homepage."
SUPPORT_TIP = "Open the Winpdb support web page."
DOCS_TIP = "Open the Winpdb online documentation web page."
UPDATES_TIP = "Check for updates in the Winpdb website."
TOGGLE_TIP = "Toggle breakpoint at cursor location."
DISABLE_TIP = "Disable all breakpoints."
ENABLE_TIP = "Enable all breakpoints."
CLEAR_TIP = "Clear all breakpoints."
LOAD_TIP = "Load breakpoints from file."
SAVE_TIP = "Save breakpoints to file."

TOOLTIP_UNLOCKED = "Communication channel is authenticated but NOT encrypted."
TOOLTIP_LOCKED = "Communication channel is authenticated AND encrypted."

TOOLBAR_BITMAP_SIZE = (23, 21)

BASE64_BREAK = "iVBORw0KGgoAAAANSUhEUgAAABcAAAAVBAMAAABfzGiYAAAAElBMVEUABwAAAIAAScCsqJn///8BAQEretZKAAAAAXRSTlMAQObYZgAAAAFiS0dEAIgFHUgAAAAJcEhZcwAACxMAAAsTAQCanBgAAAAHdElNRQfVBQ0LNTlFzNXOAAABHElEQVR4AQERAe7+AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADMzMzMzMAAAAAAAAAA0RERERDAAAAAAAAAANEREREQwAAAAAAAAADRVVEREMAAAAAAAAAA0RERERDAAAAAAAAAANEVVVVQwAAAAAAAAADREREREMSASAAAAAAA0RVVVVDIQIQAAAAAANEREREQxIBIAAAAAADREVVVEMhAhAAAAAAA0RERERDEgEgAAAAAANEVVVVQyECEAAAAAADREREREMSASAAAAAAA0RERERDAAAAAAAAAAMzMzMzMwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAdU4VleIq9nkAAAAASUVORK5CYII="
BASE64_GO = "iVBORw0KGgoAAAANSUhEUgAAABcAAAAVBAMAAABfzGiYAAAAD1BMVEUDAAAAAICsqJn///8BAQEmZTuKAAAAAXRSTlMAQObYZgAAAAFiS0dEAIgFHUgAAAAJcEhZcwAACxMAAAsTAQCanBgAAAAHdElNRQfVBQ0MJDaD5f3KAAABHElEQVR4AQERAe7+AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACIiIiIiIAAAAAAAAAAjMzMzMyAAAAAAAAAAIzMzMzMgAQAAAAAAACNEQzMzIAEAAAAAAAAjMzMzMyABAAAAAAAAIzREREMgAQAAAAAAACMzMzMzIAEAAAAAAAAjNEREQyABAAAAAAAAIzMzMzMgAQAAAAAAACMzREQzIAEAAAAAAAAjMzMzMyABAAAAAAAAIzREREMhEREAAAAAACMzMzMzIBEQAAAAAAAjMzMzMyABAAAAAAAAIiIiIiIgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAkgkQCtNT0YAAAAAASUVORK5CYII="
BASE64_STEP = "iVBORw0KGgoAAAANSUhEUgAAABcAAAAVAgMAAADQjJ04AAAACVBMVEWzAAIAAIABAQHnktlqAAAAAXRSTlMAQObYZgAAAAFiS0dEAIgFHUgAAAAJcEhZcwAACxMAAAsTAQCanBgAAAAHdElNRQfVBQ0MKBtqj+6zAAAAnklEQVR4AQGTAGz/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFVUAAAAAAAAAQAAAAAAAABAAAAAAACgQoAAAAACgECgAAAAAoBAoAAAAAKFVKAAAAACgVCgAAAACgBAKAAAAAKAAKAAAAACgACgAAAAAoAAoAAAAAKAAKAAAAAAoAKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIZYHmtBlz3kAAAAASUVORK5CYII="
BASE64_NEXT = "iVBORw0KGgoAAAANSUhEUgAAABcAAAAVAgMAAADQjJ04AAAACVBMVEWzAAIAAIABAQHnktlqAAAAAXRSTlMAQObYZgAAAAFiS0dEAIgFHUgAAAAJcEhZcwAACxMAAAsTAQCanBgAAAAHdElNRQfVBQ0MKTIxJkeeAAAAnklEQVR4AQGTAGz/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAABVVVAAAAABAAAEAAAAAAAAAQAAAAAKKAEAAAAAKAoBAAAAACgKAQAAAAAoChVQAAAAKAoFQAAAAKACgQAAAAAoCgAAAAAAKAoAAAAAACgKAAAAAAAoCgAAAAAACigAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAf7IExY7m3XoAAAAASUVORK5CYII="
BASE64_RETURN = "iVBORw0KGgoAAAANSUhEUgAAABcAAAAVAgMAAADQjJ04AAAACVBMVEWzAAIAAIABAQHnktlqAAAAAXRSTlMAQObYZgAAAAFiS0dEAIgFHUgAAAAJcEhZcwAACxMAAAsTAQCanBgAAAAHdElNRQfVBQ0MKjYdZtBEAAAAnklEQVR4AQGTAGz/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABVQAAAAAABABAAAAAABAAEAAAAAoSgBAAAAAoEKAQAAAAKBCgEAAAACgAoVUAAAAoAKBUAAAAoAAoEAAAACgAoAAAAAAoAKAAAAAAKACgAAAAACgAoAAAAAAKAoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA/t0N65RYePoAAAAASUVORK5CYII="
BASE64_GOTO = "iVBORw0KGgoAAAANSUhEUgAAABcAAAAVAgMAAADQjJ04AAAACVBMVEWzAAIAAIABAQHnktlqAAAAAXRSTlMAQObYZgAAAAFiS0dEAIgFHUgAAAAJcEhZcwAACxMAAAsTAQCanBgAAAAHdElNRQfVBQ0MKzoNy60uAAAAnklEQVR4AQGTAGz/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAECgKAAAAABSgAoAAAAVVoAKAAAAAFKACgAAAABCgAoAAAAACgACgAAAAAKACgAAAAACgAoAAAAAAoAKAAAAAAKACgAAAAAAoCgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATuYIySxPH7cAAAAASUVORK5CYII="
BASE64_TOGGLE_BP = "iVBORw0KGgoAAAANSUhEUgAAABcAAAAVCAYAAACt4nWrAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAbklEQVR42u2TwQrAMAhDjez/f9ldpGxjpGnRWwO9FPo00ZodFSjySPJFsEWEXESFR0KfFzYr4EVR9cCZA++c/iVYxS7cmV1laExQNgSAfbflBQF+WSxz5CMK7l7Fbfjovjpz+kNneS/Bi5o8atYN5nssA5y02NcAAAAASUVORK5CYII="
BASE64_LOCKED = "iVBORw0KGgoAAAANSUhEUgAAABcAAAAVCAYAAACt4nWrAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAhUlEQVR42u2UQRLAEAxFP+NguRm5WW6WbrRjOkqorurvmHiR5ANsVeQsQSlBb2u3JHtKUBFRAApAcyK1nPU9MJGAiM4qXd6HJYHvBRTg4Zb4LwcaZgZa7rcqcaPASpzZdRfYop5zwoJnMNdz5paLBADNw2NsmhQiv7s58/u/6YmgCxhbdR19GFJ+yzjAWQAAAABJRU5ErkJggg=="
BASE64_UNLOCKED = "iVBORw0KGgoAAAANSUhEUgAAABcAAAAVCAYAAACt4nWrAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAjklEQVR42u1TQQ7DIAyzUR8WXkb4WX7mnSqtFetCxU6rb0jYJLYBHgzAOyR36HTmkmncoYgQSZGUO0RSo7tlVtgsUGuFJEoiALQmjB4os5PvwhlLyi8D3TKBLWtLVrh3HuxJBZbBVUO+2oJFtd3GK38mmAUAuy/e2hXFEPF3k/fOZZ/ooJSp146pjj94xwuYKl+HgD9iOwAAAABJRU5ErkJggg=="

BASE64_FILTER = "iVBORw0KGgoAAAANSUhEUgAAABcAAAAVCAYAAACt4nWrAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAZElEQVR42u3UsQlAIQwE0Is4kvtv4Ez5hY2KmDN8xCLXiATeWQSByO3IdNc/vTxP9ZCvtZ2l2C9vvrpgYXCqwIJ3+LaAgS18WcDCDD4UnMAAkJj1ko5hYRZ3J3D3tqz+HEHkyXxoxx+Czcym0QAAAABJRU5ErkJggg=="
BASE64_EXCEPTION = "iVBORw0KGgoAAAANSUhEUgAAABcAAAAVCAYAAACt4nWrAAAACXBIWXMAAAsTAAALEwEAmpwYAAABZklEQVR42u2UsWrCQBzGv+RKRaMgXmzPXbqESBbXUskTqIODm4/hU7j4BA4+hEhKQVyFEJDiXtsqpjWgWDQdLFdbLiTSli5+U+6f//3ug/v+B5wkkBSlSdP6/vea45jSj+C6bvmEEDCWQzKZ4nXPW2I6fcB2u4Vtl6Sj4bp+66tqFpTSwMPn8zlms2fY9o2QIwc5DgMDAKUUqpqFrlu+6P+ZqEgI4WBZBmq1JEwzjkRCguNs0G6/wnV3/IDFYo5IzjWt7zOW4+tyWUGloqDTWaLVeoFhxNBopL7sYSwnvHSh88PLM804AGAwWEP+sFIonAf2h8IPlcnsid3uJa8pihwp56Fw192BUoJ6/RGbzXFDJLTgeUv+bVkrAECxGAMhAGMEzWY6sD8054Zx5+fzVzwt1aqCUimOdFrGePyG4XCNXm/F+yeTe4xG11Ik+D7nF6E5/xykJ+Gk/umE/s/b8huv4klCvQMz8oLsLpAhfwAAAABJRU5ErkJggg=="
BASE64_TRAP = "iVBORw0KGgoAAAANSUhEUgAAABcAAAAVCAYAAACt4nWrAAAACXBIWXMAAAsTAAALEwEAmpwYAAAA\nB3RJTUUH1wMWBzIMELT6ewAAAixJREFUeNrNlVtIkwEUx39z35zOteU252X6hbNpEeZW5oUyejC7\naEEIERhRPVTMhx6rh3rLqCB8iaSHejGiqF588QJFD3bZg4HQCsNLuE2deNk3v29urtV7N9RvQef1\nnPPjcPif/4F/GFrVBEdOFUm7jmRU+jmVoY7c1EIw7zCajNTvsuuGl3DVa8TalkNFEGUylBZ4B1fK\nPVRdg6mmbAqXTzi6P6Rl50fZ7HlPb1uuJWSOxMyCicon/dGDg3+q16wW3FBEvcHG5XoX04qE/vmA\neXmUyAXVanFS3crG0JmLl9Dt8GAaHWOLaIw/TQZNcj4Oayk1FnBbJT7NrwlewLH2JeabHZZpf2UV\nzlIRo82OYTzBAckQPzT3fWHviDSzTyZel0WDlODz+KrgG6g7KRNs0RCRY7JUkJTILRaxlXuw2woJ\nGc34ZQVhbjah6OKuzkUG3q568gSB4eraxsBU8OuLPamKNxOTS8VlrnjBVjeZgS8MPbxH5sQwvjJl\nZ9dHfP51n4uYxblGJw9edXCj5xYDrW5e70I83ld936lKLdnk7naIC+e9pwjPjlA2NsiiEsx53IPc\nr0otetyub0TPxldi7wJhtgfCzNgi3HmmrPhUOUdzzc1KHY67AoXXBUydwOm19P91LTo2eVMs12vQ\nhCD1Mkm4Ly1erCf/iBZrr0DRbT21rrSZvIC4X4u1W0dJuxrOL66YxTYRojVgfOQyN3el9TUJ5DXo\nMTv53+MHY3Sxa+ko45EAAAAASUVORK5CYII=\n"

SB_LINE = "Line"
SB_COL = "Col"
SB_STATE = "State"
SB_ENCRYPTION = "Encryption"

SHOW = "Show"
VALUE = "Value"
BITMAP = "Bitmap"

STATE_SPAWNING_MENU = {ENABLED: [ML_STOP, ML_DETACH], DISABLED: [ML_ANALYZE, ML_GO, ML_BREAK, ML_STEP, ML_NEXT, ML_RETURN, ML_GOTO, ML_TOGGLE, ML_DISABLE, ML_ENABLE, ML_CLEAR, ML_LOAD, ML_SAVE, ML_OPEN, ML_PWD, ML_LAUNCH, ML_ATTACH, ML_RESTART]}
STATE_ATTACHING_MENU = {ENABLED: [ML_STOP, ML_DETACH], DISABLED: [ML_ANALYZE, ML_GO, ML_BREAK, ML_STEP, ML_NEXT, ML_RETURN, ML_GOTO, ML_TOGGLE, ML_DISABLE, ML_ENABLE, ML_CLEAR, ML_LOAD, ML_SAVE, ML_OPEN, ML_PWD, ML_LAUNCH, ML_ATTACH, ML_RESTART]}
STATE_BROKEN_MENU = {ENABLED: [ML_ANALYZE, ML_GO, ML_STEP, ML_NEXT, ML_RETURN, ML_GOTO, ML_TOGGLE, ML_DISABLE, ML_ENABLE, ML_CLEAR, ML_LOAD, ML_SAVE, ML_OPEN, ML_STOP, ML_DETACH, ML_RESTART], DISABLED: [ML_PWD, ML_LAUNCH, ML_ATTACH, ML_BREAK]}
STATE_ANALYZE_MENU = {ENABLED: [ML_ANALYZE, ML_TOGGLE, ML_DISABLE, ML_ENABLE, ML_CLEAR, ML_LOAD, ML_SAVE, ML_OPEN, ML_STOP, ML_DETACH, ML_RESTART], DISABLED: [ML_PWD, ML_LAUNCH, ML_ATTACH, ML_BREAK, ML_GO, ML_STEP, ML_NEXT, ML_RETURN, ML_GOTO]}
STATE_RUNNING_MENU = {ENABLED: [ML_BREAK, ML_TOGGLE, ML_DISABLE, ML_ENABLE, ML_CLEAR, ML_LOAD, ML_SAVE, ML_OPEN, ML_STOP, ML_DETACH, ML_RESTART], DISABLED: [ML_ANALYZE, ML_PWD, ML_LAUNCH, ML_ATTACH, ML_GO, ML_STEP, ML_NEXT, ML_RETURN, ML_GOTO]}
STATE_DETACHED_MENU = {ENABLED: [ML_PWD, ML_LAUNCH, ML_ATTACH], DISABLED: [ML_ANALYZE, ML_GO, ML_BREAK, ML_STEP, ML_NEXT, ML_RETURN, ML_GOTO, ML_TOGGLE, ML_DISABLE, ML_ENABLE, ML_CLEAR, ML_LOAD, ML_SAVE, ML_OPEN, ML_STOP, ML_DETACH, ML_RESTART]}
STATE_DETACHING_MENU = {ENABLED: [ML_STOP, ML_DETACH], DISABLED: [ML_ANALYZE, ML_GO, ML_BREAK, ML_STEP, ML_NEXT, ML_RETURN, ML_GOTO, ML_TOGGLE, ML_DISABLE, ML_ENABLE, ML_CLEAR, ML_LOAD, ML_SAVE, ML_OPEN, ML_PWD, ML_LAUNCH, ML_ATTACH, ML_RESTART]}

STATE_BROKEN_TOOLBAR = {ENABLED: [TB_EXCEPTION, TB_FILTER, TB_TOGGLE_BP, TB_GO, TB_STEP, TB_NEXT, TB_RETURN, TB_GOTO], DISABLED: [TB_BREAK]}
STATE_ANALYZE_TOOLBAR = {ENABLED: [TB_EXCEPTION, TB_FILTER, TB_TOGGLE_BP], DISABLED: [TB_BREAK, TB_GO, TB_STEP, TB_NEXT, TB_RETURN, TB_GOTO]}
STATE_RUNNING_TOOLBAR = {ENABLED: [TB_TOGGLE_BP, TB_BREAK], DISABLED: [TB_EXCEPTION, TB_FILTER, TB_GO, TB_STEP, TB_NEXT, TB_RETURN, TB_GOTO]}
STATE_SPAWNING_TOOLBAR = {ENABLED: [], DISABLED: [TB_EXCEPTION, TB_FILTER, TB_TOGGLE_BP, TB_BREAK, TB_GO, TB_STEP, TB_NEXT, TB_RETURN, TB_GOTO]}
STATE_ATTACHING_TOOLBAR = {ENABLED: [], DISABLED: [TB_EXCEPTION, TB_FILTER, TB_TOGGLE_BP, TB_BREAK, TB_GO, TB_STEP, TB_NEXT, TB_RETURN, TB_GOTO]}
STATE_DETACHED_TOOLBAR = {ENABLED: [], DISABLED: [TB_EXCEPTION, TB_FILTER, TB_TOGGLE_BP, TB_BREAK, TB_GO, TB_STEP, TB_NEXT, TB_RETURN, TB_GOTO]}
STATE_DETACHING_TOOLBAR = {ENABLED: [], DISABLED: [TB_EXCEPTION, TB_FILTER, TB_TOGGLE_BP, TB_BREAK, TB_GO, TB_STEP, TB_NEXT, TB_RETURN, TB_GOTO]}

STATE_MAP = {
    rpdb2.STATE_SPAWNING: (STATE_SPAWNING_MENU, STATE_SPAWNING_TOOLBAR),
    rpdb2.STATE_ATTACHING: (STATE_ATTACHING_MENU, STATE_ATTACHING_TOOLBAR),
    rpdb2.STATE_BROKEN: (STATE_BROKEN_MENU, STATE_BROKEN_TOOLBAR),
    rpdb2.STATE_ANALYZE: (STATE_ANALYZE_MENU, STATE_ANALYZE_TOOLBAR),
    rpdb2.STATE_RUNNING: (STATE_RUNNING_MENU, STATE_RUNNING_TOOLBAR),
    rpdb2.STATE_DETACHED: (STATE_DETACHED_MENU, STATE_DETACHED_TOOLBAR),    
    rpdb2.STATE_DETACHING: (STATE_DETACHING_MENU, STATE_DETACHING_TOOLBAR)    
}

LICENSE_TITLE = 'License.'

ABOUT_TITLE = 'About ' + WINPDB_TITLE

ABOUT_HTML_PREFIX = """
<html>
<body>
<p>
"""

ABOUT_HTML_SUFFIX = """
</p>
</body>
</html>
"""

WEBSITE_URL = "http://www.digitalpeers.com/pythondebugger/"
SUPPORT_URL = "http://www.digitalpeers.com/pythondebugger/support.htm"
DOCS_URL = "http://www.digitalpeers.com/pythondebugger/docs.htm"
UPDATES_URL = "http://www.digitalpeers.com/pythondebugger/download.htm"

STR_ERROR_INTERFACE_COMPATIBILITY = "The rpdb2 module which was found by Winpdb is of unexpected version (version expected: %s, version found: %s). Please upgrade to the latest versions of winpdb.py and rpdb2.py."
STR_NAMESPACE_DEADLOCK = 'Data Not Available'

BAD_FILE_WARNING_TIMEOUT_SEC = 10.0
POSITION_TIMEOUT = 2.0



g_ignored_warnings = {'': True}



def image_from_base64(str_b64):
    s = base64.decodestring(str_b64)
    stream = cStringIO.StringIO(s)
    image = wx.ImageFromStream(stream)

    return image

    

class CSettings:
    def __init__(self, default_settings):
        self.m_dict = default_settings


    def calc_path(self):
        if os.name == rpdb2.POSIX:
            home = os.path.expanduser('~')
            path = os.path.join(home, '.' + WINPDB_SETTINGS_FILENAME)
            return path

        #
        # gettempdir() is used since it works with unicode user names on 
        # Windows.
        #
        
        tmpdir = tempfile.gettempdir()
        path = os.path.join(tmpdir, WINPDB_SETTINGS_FILENAME)
        return path


    def load_settings(self):
        try:
            path = self.calc_path()
            f = open(path, 'r')
            
        except IOError:
            return 
            
        try:
            d = cPickle.load(f)
            self.m_dict.update(d)
            
        finally:
            f.close()

            
    def save_settings(self):
        try:
            path = self.calc_path()
            f = open(path, 'w')
            
        except IOError:
            return 
            
        try:
            cPickle.dump(self.m_dict, f)
            
        finally:
            f.close()

        
    def __getitem__(self, key):
        return self.m_dict[key]


    def __setitem__(self, key, value):
        self.m_dict[key] = value
        

    
class CMenuBar:
    def __init__(self):
        self.m_menubar = None
        
        self.m_encapsulating_menu_items = {}
        self.m_cascades = {}
        
    def init_menubar(self, resource):
        if 'wxMac' in wx.PlatformInfo:
             wx.MenuBar.SetAutoWindowMenu(False)

        self.m_menubar = wx.MenuBar()

        self.SetMenuBar(self.m_menubar)

        self.m_cascades = {ML_ROOT: self.m_menubar}
        
        k = resource.keys()
        k.sort()

        for c in k:
            s = (ML_ROOT + c).split('/')
            sc = [e for e in s if not e.isdigit()]
            for i, e in enumerate(sc[:-1]):
                if not e in self.m_cascades:
                    parent_label = sc[i - 1]
                    parent = self.m_cascades[parent_label]
                    child = wx.Menu()
                    
                    if parent_label == ML_ROOT:
                        parent.Append(child, e)
                    else:
                        parent.AppendMenu(wx.NewId(), e, child)
                        self.m_encapsulating_menu_items[e] = parent

                    self.m_cascades[e] = child

            parent_label = sc[-2]
            parent = self.m_cascades[parent_label]
            item_label = sc[-1]

            if item_label == ML_EMPTY:
                continue
                
            if item_label == ML_SEPARATOR:
                parent.AppendSeparator()
                continue

            command = resource[c][COMMAND]
            tip = resource[c].get(TOOLTIP, wx.EmptyString)
            
            item = parent.Append(-1, item_label, tip)
            self.Bind(wx.EVT_MENU, command, item)

            self.m_encapsulating_menu_items[item_label] = parent 

    def set_menu_items_state(self, state_label_dict):
        for state, label_list in state_label_dict.items():
            for item_label in label_list:
                parent = self.m_encapsulating_menu_items[item_label]
                id = parent.FindItem(item_label)
                parent.Enable(id, [True, False][state == DISABLED])

    def add_menu_item(self, menu_label, item_label, command):
        parent = self.m_cascades[menu_label]
        item = parent.Append(-1, item_label)
        self.Bind(wx.EVT_MENU, command, item)

    def clear_menu_items(self, menu_label):    
        parent = self.m_cascades[menu_label]

        while parent.GetMenuItemCount() > 0:
            i = parent.FindItemByPosition(0)
            parent.DeleteItem(i)

        

class CToolBar:
    def __init__(self):
        self.m_toolbar = None
        self.m_items = {}

    def init_toolbar(self, resource):
        self.m_toolbar = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT)
        self.m_toolbar.SetToolBitmapSize(TOOLBAR_BITMAP_SIZE)
        
        for e in resource:
            item_label = e[LABEL]

            if item_label == ML_SEPARATOR:
                self.m_toolbar.AddSeparator()
                continue

            command = e[COMMAND]
            id = wx.NewId()
            image = image_from_base64(e[DATA])
            bitmap = wx.BitmapFromImage(image)

            if DATA2 in e:
                image2 = image_from_base64(e[DATA2])
                bitmap2 = wx.BitmapFromImage(image2)
                self.m_toolbar.AddSimpleTool(id, bitmap, item_label, isToggle = True)
                self.m_items[item_label] = {ID: id, DATA: bitmap, DATA2: bitmap2}
                self.Bind(wx.EVT_TOOL, command, id = id)
                self.Bind(wx.EVT_TOOL, self.OnToggleTool, id = id)

            else:
                self.m_toolbar.AddSimpleTool(id, bitmap, item_label)
                self.m_items[item_label] = {ID: id}
                self.Bind(wx.EVT_TOOL, command, id = id)
            
        self.m_toolbar.Realize()

    def set_toolbar_items_state(self, state_label_dict):
        for state, label_list in state_label_dict.items():
            for label in label_list:
                id = self.m_items[label][ID]

                if (wx.Platform == '__WXGTK__') and (state == ENABLED):
                    self.__gtk_enable_tool(id)
                else:    
                    self.m_toolbar.EnableTool(id, [True, False][state == DISABLED])

    def __gtk_enable_tool(self, id):
        p = self.m_toolbar.ScreenToClient(wx.GetMousePosition())
        (x, y) = self.m_toolbar.GetSize()
        r = wx.RectS((x, y))

        if r.Inside(p):
            self.m_toolbar.WarpPointer(p.x, p.y + 2 * y)

        self.m_toolbar.EnableTool(id, True)

        if r.Inside(p):
            self.m_toolbar.WarpPointer(p.x, p.y) 

    def set_toggle(self, label, fToggle):
        item = self.m_items[label]
        id = item[ID]
        bitmap = [item[DATA], item[DATA2]][fToggle]

        tool = self.m_toolbar.FindById(id)
        tool.SetNormalBitmap(bitmap)
        
        self.m_toolbar.ToggleTool(id, fToggle)
        
        if wx.Platform == '__WXMSW__':
            self.m_toolbar.Realize()
        else:    
            self.m_toolbar.ToggleTool(id, not fToggle);   
            self.m_toolbar.ToggleTool(id, fToggle);

    def OnToggleTool(self, event):
        tool = self.m_toolbar.FindById(event.GetId())
        if tool is None:
            event.Skip()
            return

        label = tool.GetShortHelp()
        f = event.IsChecked()
        
        self.set_toggle(label, f)

        event.Skip()   



class CStatusBar:
    def __init__(self):
        self.m_statusbar = None

        self.m_widths = []
        self.m_formats = []
        self.m_keys = []
        self.m_data = {}
        self.m_bitmaps = {}

        self.sizeChanged = False

        
    def init_statusbar(self, resource):
        self.m_widths = [e[WIDTH] for e in resource]
        self.m_formats = [e.get(FORMAT, "") for e in resource]
        self.m_keys = [e.get(KEYS, []) for e in resource]
        
        self.m_statusbar = self.CreateStatusBar(1, wx.ST_SIZEGRIP)
        self.m_statusbar.SetFieldsCount(len(self.m_widths))
        self.m_statusbar.SetStatusWidths(self.m_widths)
        
        self.m_statusbar.Bind(wx.EVT_SIZE, self.OnSize)
        self.m_statusbar.Bind(wx.EVT_IDLE, self.OnIdle)


    def set_statusbar_data(self, data):
        self.m_data.update(data)

        for i, e in enumerate(self.m_keys):
            for k in e:
                if k in data:
                    if self.m_formats[i] == BITMAP:
                        self.set_bitmap(i, data[k][0], data[k][1])
                    else:
                        self.m_statusbar.SetStatusText(self.m_formats[i] % self.m_data, i)
                        break


    def set_bitmap(self, i, data, tooltip):
        if not i in self.m_bitmaps:
            if data is None:
                return
                
            image = image_from_base64(data)
            bitmap = wx.BitmapFromImage(image)
            p = wx.Panel(self.m_statusbar)
            sb = wx.StaticBitmap(p, -1, bitmap)

            self.m_bitmaps[i] = (p, sb, tooltip)
            
        else:
            if data is None:
                self.m_bitmaps[i][0].Hide()
            else:
                image = image_from_base64(data)
                bitmap = wx.BitmapFromImage(image)
                
                self.m_bitmaps[i][1].SetBitmap(bitmap)
                self.m_bitmaps[i][0].Show()

        self.reposition()    


    def reposition(self):
        for i, (p, sb, tooltip) in self.m_bitmaps.items():
            rect = self.m_statusbar.GetFieldRect(i)
            p.SetPosition((rect.x + 2, rect.y + 2))
            s = sb.GetSize()
            sb.SetSize((s[0], rect.height - 4))
            sb.SetToolTipString(tooltip)
            p.SetToolTipString(tooltip)
            p.SetClientSize(sb.GetSize())
            
        self.sizeChanged = False


    def OnSize(self, event):
        self.reposition()
        self.sizeChanged = True


    def OnIdle(self, event):
        if self.sizeChanged:
            self.reposition()
            


class CJobs:
    def __init__(self):
        self.__m_jobs_lock = threading.RLock()
        self.__m_n_expected_jobs = 0
        self.__m_f_shutdown = False

        
    def init_jobs(self):
        pass


    def shutdown_jobs(self):    
        self.__m_f_shutdown = True

        while 1:
            try:
                self.__m_jobs_lock.acquire()

                if self.__m_n_expected_jobs == 0:
                    return

            finally:        
                self.__m_jobs_lock.release()

            time.sleep(0.1)    

        
    def job_post(self, job, args, callback = None):
        threading.Thread(target = self.job_do, args = (job, args, callback)).start()

        
    def job_do(self, job, args, callback):
        try:
            self.__m_jobs_lock.acquire()

            if self.__m_f_shutdown:
                return
            
            if self.__m_n_expected_jobs == 0:
                wx.CallAfter(self.set_cursor, wx.CURSOR_WAIT)

            self.__m_n_expected_jobs += 1

        finally:        
            self.__m_jobs_lock.release()

        r = None
        exc_info = (None, None, None)
        
        try:
            r = job(*args)
        except:
            exc_info = sys.exc_info()

            if callback == None:
                rpdb2.print_debug()

        if callback is not None:
            wx.CallAfter(callback, r, exc_info)
            
        try:
            self.__m_jobs_lock.acquire()
            
            self.__m_n_expected_jobs -= 1

            if self.__m_n_expected_jobs == 0:
                wx.CallAfter(self.set_cursor, wx.CURSOR_ARROW)

        finally:        
            self.__m_jobs_lock.release()


    def set_cursor(self, id):
        cursor = wx.StockCursor(id)
        self.SetCursor(cursor)        
        

    
class CMainWindow(CMenuBar, CToolBar, CStatusBar, CJobs):
    def __init__(self):
        CMenuBar.__init__(self)
        CToolBar.__init__(self)
        CStatusBar.__init__(self)
        CJobs.__init__(self)



class CAsyncSessionManagerCall:
    def __init__(self, session_manager, job_manager, f, callback):
        self.m_session_manager = session_manager
        self.m_job_manager = job_manager
        self.m_f = f
        self.m_callback = callback


    def __wrapper(self, *args):
        if self.m_callback != None:
            return self.m_f(*args)
            
        try:
            self.m_f(*args)
            
        except (socket.error, rpdb2.CConnectionException):
            self.m_session_manager.report_exception(*sys.exc_info())
        except rpdb2.CException:
            self.m_session_manager.report_exception(*sys.exc_info())
        except:
            self.m_session_manager.report_exception(*sys.exc_info())
            rpdb2.print_debug(True)

    
    def __call__(self, *args):
        if self.m_job_manager == None:
            return
            
        self.m_job_manager.job_post(self.__wrapper, args, self.m_callback)



class CAsyncSessionManager:
    def __init__(self, session_manager, job_manager, callback = None):
        self.m_session_manager = session_manager
        self.m_callback = callback

        self.m_weakref_job_manager = None
        
        if job_manager != None:
            self.m_weakref_job_manager = weakref.ref(job_manager)


    def with_callback(self, callback):
        if self.m_weakref_job_manager != None:
            job_manager = self.m_weakref_job_manager()
        else:
            job_manager = None
        
        asm = CAsyncSessionManager(self.m_session_manager, job_manager, callback)
        return asm


    def __getattr__(self, name):
        f = getattr(self.m_session_manager, name)
        if not hasattr(f, '__call__'):
            raise TypeError(repr(type(f)) + ' object is not callable')

        if self.m_weakref_job_manager != None:
            job_manager = self.m_weakref_job_manager()
        else:
            job_manager = None
        
        return CAsyncSessionManagerCall(self.m_session_manager, job_manager, f, self.m_callback)

    
        
class CWinpdbWindow(wx.Frame, CMainWindow):
    def __init__(self, session_manager, fchdir, command_line, fAttach, settings):
        CMainWindow.__init__(self)

        wx.Frame.__init__(self, None, -1, WINPDB_TITLE, size = settings[WINPDB_SIZE],
                          style = wx.DEFAULT_FRAME_STYLE | wx.NO_FULL_REPAINT_ON_RESIZE)

        #
        # Force 'Left to Right' as long as internationalization is not supported.
        # Not available on wxPython 2.6
        #
        if hasattr(self, 'SetLayoutDirection'):
            self.SetLayoutDirection(1)
        
        self.Maximize(settings[WINPDB_MAXIMIZE])
        
        self.m_session_manager = session_manager
        self.m_async_sm = CAsyncSessionManager(session_manager, self)
        
        self.m_source_manager = CSourceManager(self, session_manager)

        self.m_fchdir = fchdir
        self.m_command_line = command_line
        self.m_fAttach = fAttach
        self.m_settings = settings

        self.m_stack = None
        
        self.m_state = rpdb2.STATE_DETACHED
                
        self.SetMinSize(WINPDB_SIZE_MIN)
        self.Centre(wx.BOTH)

        self.init_jobs()
        
        menu_resource = { 
            "/0/" + ML_FILE +   "/0/" + ML_PWD: {COMMAND: self.do_password, TOOLTIP: PWD_TIP}, 
            "/0/" + ML_FILE +   "/1/" + ML_LAUNCH: {COMMAND: self.do_launch, TOOLTIP: LAUNCH_TIP}, 
            "/0/" + ML_FILE +   "/2/" + ML_ATTACH: {COMMAND: self.do_attach, TOOLTIP: ATTACH_TIP}, 
            "/0/" + ML_FILE +   "/3/" + ML_OPEN: {COMMAND: self.do_open, TOOLTIP: OPEN_TIP}, 
            "/0/" + ML_FILE +   "/4/" + ML_DETACH: {COMMAND: self.do_detach, TOOLTIP: DETACH_TIP}, 
            "/0/" + ML_FILE +   "/5/" + ML_STOP: {COMMAND: self.do_stop, TOOLTIP: STOP_TIP}, 
            "/0/" + ML_FILE +   "/6/" + ML_RESTART: {COMMAND: self.do_restart, TOOLTIP: RESTART_TIP}, 
            "/0/" + ML_FILE +   "/7/" + ML_SEPARATOR: None, 
            "/0/" + ML_FILE +   "/8/" + ML_EXIT: {COMMAND: self.do_exit}, 
            "/1/" + ML_BREAKPOINTS + "/0/" + ML_TOGGLE: {COMMAND: self.toggle_breakpoint, TOOLTIP: TOGGLE_TIP}, 
            "/1/" + ML_BREAKPOINTS + "/1/" + ML_DISABLE: {COMMAND: self.do_disable, TOOLTIP: DISABLE_TIP}, 
            "/1/" + ML_BREAKPOINTS + "/2/" + ML_ENABLE: {COMMAND: self.do_enable, TOOLTIP: ENABLE_TIP}, 
            "/1/" + ML_BREAKPOINTS + "/3/" + ML_CLEAR: {COMMAND: self.do_clear, TOOLTIP: CLEAR_TIP}, 
            "/1/" + ML_BREAKPOINTS + "/4/" + ML_LOAD: {COMMAND: self.do_load, TOOLTIP: LOAD_TIP}, 
            "/1/" + ML_BREAKPOINTS + "/5/" + ML_SAVE: {COMMAND: self.do_save, TOOLTIP: SAVE_TIP}, 
            "/2/" + ML_CONTROL + "/0/" + ML_ANALYZE: {COMMAND: self.do_analyze_menu}, 
            "/2/" + ML_CONTROL + "/1/" + ML_BREAK: {COMMAND: self.do_break}, 
            "/2/" + ML_CONTROL + "/2/" + ML_GO: {COMMAND: self.do_go}, 
            "/2/" + ML_CONTROL + "/3/" + ML_NEXT: {COMMAND: self.do_next}, 
            "/2/" + ML_CONTROL + "/4/" + ML_STEP: {COMMAND: self.do_step}, 
            "/2/" + ML_CONTROL + "/5/" + ML_GOTO: {COMMAND: self.do_goto}, 
            "/2/" + ML_CONTROL + "/6/" + ML_RETURN: {COMMAND: self.do_return}, 
            "/3/" + ML_WINDOW + "/0/" + ML_EMPTY: None,
            "/4/" + ML_HELP +   "/0/" + ML_WEBSITE: {COMMAND: self.do_website, TOOLTIP: WEBSITE_TIP}, 
            "/4/" + ML_HELP +   "/1/" + ML_SUPPORT: {COMMAND: self.do_support, TOOLTIP: SUPPORT_TIP}, 
            "/4/" + ML_HELP +   "/2/" + ML_DOCS: {COMMAND: self.do_docs, TOOLTIP: DOCS_TIP}, 
            "/4/" + ML_HELP +   "/3/" + ML_UPDATES: {COMMAND: self.do_updates, TOOLTIP: UPDATES_TIP}, 
            "/4/" + ML_HELP +   "/4/" + ML_ABOUT: {COMMAND: self.do_about}, 
            "/4/" + ML_HELP +   "/5/" + ML_LICENSE: {COMMAND: self.do_license}
        }
        
        self.init_menubar(menu_resource)
        
        toolbar_resource = [
            {LABEL: TB_GO,      DATA: BASE64_GO,    COMMAND: self.do_go},
            {LABEL: TB_BREAK,   DATA: BASE64_BREAK, COMMAND: self.do_break},
            {LABEL: ML_SEPARATOR},
            {LABEL: TB_STEP,    DATA: BASE64_STEP,  COMMAND: self.do_step},
            {LABEL: TB_NEXT,    DATA: BASE64_NEXT,  COMMAND: self.do_next},
            {LABEL: TB_RETURN,  DATA: BASE64_RETURN, COMMAND: self.do_return},
            {LABEL: TB_GOTO,    DATA: BASE64_GOTO,  COMMAND: self.do_goto},
            {LABEL: ML_SEPARATOR},
            {LABEL: TB_TOGGLE_BP, DATA: BASE64_TOGGLE_BP,  COMMAND: self.toggle_breakpoint},
            {LABEL: ML_SEPARATOR},
            {LABEL: TB_FILTER,  DATA: BASE64_FILTER, DATA2: BASE64_FILTER, COMMAND: self.do_filter},
            {LABEL: TB_EXCEPTION, DATA: BASE64_EXCEPTION, DATA2: BASE64_EXCEPTION, COMMAND: self.do_analyze},
            {LABEL: TB_TRAP, DATA: BASE64_TRAP, DATA2: BASE64_TRAP, COMMAND: self.do_trap}
        ]

        self.init_toolbar(toolbar_resource)

        ftrap = self.m_session_manager.get_trap_unhandled_exceptions()
        self.set_toggle(TB_TRAP, ftrap)
        
        statusbar_resource = [
            {WIDTH: -2},
            {WIDTH: -1, FORMAT: SB_STATE + ": %(" + SB_STATE + ")s", KEYS: [SB_STATE]},
            {WIDTH: -1, FORMAT: SB_LINE + ": %(" + SB_LINE + ")d " + SB_COL + ": %(" + SB_COL + ")d", KEYS: [SB_LINE, SB_COL]},
            {WIDTH: 50, FORMAT: BITMAP, KEYS: [SB_ENCRYPTION]}
        ]

        self.init_statusbar(statusbar_resource)

        self.m_splitterv = wx.SplitterWindow(self, -1, style = wx.SP_LIVE_UPDATE | wx.SP_3D)
        self.m_splitterv.SetMinimumPaneSize(100)
        self.m_splitterv.SetSashGravity(0.5)
        
        self.m_splitterh1 = wx.SplitterWindow(self.m_splitterv, -1, style = wx.SP_LIVE_UPDATE | wx.SP_3D)
        self.m_splitterh1.SetMinimumPaneSize(70)
        self.m_splitterh1.SetSashGravity(0.67)

        self.m_splitterh2 = wx.SplitterWindow(self.m_splitterh1, -1, style = wx.SP_LIVE_UPDATE | wx.SP_3D)
        self.m_splitterh2.SetMinimumPaneSize(70)
        self.m_splitterh2.SetSashGravity(0.5)
        
        self.m_namespace_viewer = CNamespaceViewer(self.m_splitterh2, style = wx.STATIC_BORDER, session_manager = self.m_session_manager)

        self.m_threads_viewer = CThreadsViewer(self.m_splitterh2, style = wx.STATIC_BORDER, select_command = self.OnThreadSelected)

        self.m_stack_viewer = CStackViewer(self.m_splitterh1, style = wx.STATIC_BORDER, select_command = self.OnFrameSelected)

        self.m_splitterh3 = wx.SplitterWindow(self.m_splitterv, -1, style = wx.SP_LIVE_UPDATE | wx.SP_3D)
        self.m_splitterh3.SetMinimumPaneSize(100)
        self.m_splitterh3.SetSashGravity(1.0)
        
        self.m_code_viewer = CCodeViewer(self.m_splitterh3, style = wx.STATIC_BORDER | wx.TAB_TRAVERSAL, session_manager = self.m_session_manager, source_manager = self.m_source_manager, notify_filename = self.do_notify_filename)
        
        self.m_console = CConsole(self.m_splitterh3, style = wx.STATIC_BORDER | wx.TAB_TRAVERSAL)
        self.job_post(self.m_console.start, (self, self.m_session_manager, self.m_fchdir, self.m_command_line, self.m_fAttach))
        
        self.m_splitterh2.SplitHorizontally(self.m_namespace_viewer, self.m_threads_viewer)
        self.m_splitterh1.SplitHorizontally(self.m_splitterh2, self.m_stack_viewer)
        self.m_splitterv.SplitVertically(self.m_splitterh1, self.m_splitterh3)
        self.m_splitterh3.SplitHorizontally(self.m_code_viewer, self.m_console)
        
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_SIZE, self.OnSizeWindow)

        state = self.m_session_manager.get_state()
        self.update_state(rpdb2.CEventState(state))

        event_type_dict = {rpdb2.CEventState: {}}
        self.m_session_manager.register_callback(self.update_state, event_type_dict, fSingleUse = False)

        event_type_dict = {rpdb2.CEventStackFrameChange: {}}
        self.m_session_manager.register_callback(self.update_frame, event_type_dict, fSingleUse = False)

        event_type_dict = {rpdb2.CEventThreads: {}}
        self.m_session_manager.register_callback(self.update_threads, event_type_dict, fSingleUse = False)

        event_type_dict = {rpdb2.CEventNoThreads: {}}
        self.m_session_manager.register_callback(self.update_no_threads, event_type_dict, fSingleUse = False)

        event_type_dict = {rpdb2.CEventNamespace: {}}
        self.m_session_manager.register_callback(self.update_namespace, event_type_dict, fSingleUse = False)

        event_type_dict = {rpdb2.CEventUnhandledException: {}}
        self.m_session_manager.register_callback(self.update_unhandled_exception, event_type_dict, fSingleUse = False)

        event_type_dict = {rpdb2.CEventThreadBroken: {}}
        self.m_session_manager.register_callback(self.update_thread_broken, event_type_dict, fSingleUse = False)

        event_type_dict = {rpdb2.CEventStack: {}}
        self.m_session_manager.register_callback(self.update_stack, event_type_dict, fSingleUse = False)

        event_type_dict = {rpdb2.CEventBreakpoint: {}}
        self.m_session_manager.register_callback(self.update_bp, event_type_dict, fSingleUse = False)

        event_type_dict = {rpdb2.CEventTrap: {}}
        self.m_session_manager.register_callback(self.update_trap, event_type_dict, fSingleUse = False)

        wx.CallAfter(self.__set_sash_positions)


    #
    #--------------------------------------------------
    #

    def __set_sash_positions(self):
        self.m_splitterh1.SetSashPosition(self.m_settings[SPLITTER_2_POS])
        self.m_splitterh2.SetSashPosition(self.m_settings[SPLITTER_1_POS])
        self.m_splitterv.SetSashPosition(self.m_settings[SPLITTER_3_POS])
        self.m_splitterh3.SetSashPosition(self.m_settings[SPLITTER_4_POS])


    #
    #----------------- Thread list logic --------------
    #


    def OnThreadSelected(self, tid):
        self.m_async_sm.set_thread(tid)
        

    def update_threads(self, event):
        wx.CallAfter(self.m_threads_viewer.update_threads_list, event.m_current_thread, event.m_thread_list)


    def update_no_threads(self, event):
        wx.CallAfter(self.clear_all)


    def clear_all(self):
        self.m_code_viewer._clear()
        self.m_namespace_viewer._clear()
        self.m_stack_viewer._clear()
        self.m_threads_viewer._clear()


    def update_thread_broken(self, event):
        wx.CallAfter(self.m_threads_viewer.update_thread, event.m_tid, event.m_name, True)


    #
    #----------------------------------------------------
    #

    def update_bp(self, event):
        wx.CallAfter(self.m_code_viewer.update_bp, event)


    def toggle_breakpoint(self, event):
        self.m_code_viewer.toggle_breakpoint()

        
    #
    #------------------- Frame Select Logic -------------
    #
    
    def OnFrameSelected(self, event):    
        self.m_async_sm.set_frame_index(event.m_itemIndex)
        

    def update_frame(self, event):
        wx.CallAfter(self.do_update_frame, event.m_frame_index)


    def do_update_frame(self, index):
        self.do_set_position(index)
        self.m_stack_viewer.select_frame(index)


    #
    #----------------------------------------------------------
    #
    
    def update_stack(self, event):
        self.m_stack = event.m_stack
        wx.CallAfter(self.do_update_stack, event.m_stack)


    def do_update_stack(self, _stack):
        self.m_stack = _stack

        self.do_set_position(0)
        self.m_stack_viewer.update_stack_list(self.m_stack)


    def do_set_position(self, index):
        s = self.m_stack[rpdb2.DICT_KEY_STACK]
        e = s[-(1 + index)]
        
        filename = e[0]
        lineno = e[1]

        fBroken = self.m_stack[rpdb2.DICT_KEY_BROKEN]
        _event = self.m_stack[rpdb2.DICT_KEY_EVENT]
        __event = ['running', ['call', _event][index == 0]][fBroken]

        self.m_code_viewer.set_position(filename, lineno, __event)

        
    #
    #----------------------------------------------------
    #

    def do_analyze_menu(self, event):
        state = self.m_session_manager.get_state()
        f = (state != rpdb2.STATE_ANALYZE)

        self.m_async_sm.set_analyze(f)


    def do_analyze(self, event):
        f = event.IsChecked()

        self.m_async_sm.set_analyze(f)


    def update_trap(self, event):
        wx.CallAfter(self.set_toggle, TB_TRAP, event.m_ftrap)

        
    def do_trap(self, event):
        f = event.IsChecked()

        if not f:
            dlg = wx.MessageDialog(self, MSG_WARNING_TRAP, MSG_WARNING_TITLE, wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
            res = dlg.ShowModal()
            dlg.Destroy()

            if res == wx.ID_NO:
                self.set_toggle(TB_TRAP, True)
                return

        self.m_async_sm.set_trap_unhandled_exceptions(f)


    def update_namespace(self, event):
        wx.CallAfter(self.m_namespace_viewer.update_namespace, self.m_stack)


    def update_unhandled_exception(self, event):
        wx.CallAfter(self.notify_unhandled_exception)


    def notify_unhandled_exception(self):
        dlg = wx.MessageDialog(self, MSG_WARNING_UNHANDLED_EXCEPTION, MSG_WARNING_TITLE, wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
        res = dlg.ShowModal()
        dlg.Destroy()

        if res != wx.ID_YES:
            return

        self.m_async_sm.set_analyze(True)
        
    
    def do_filter(self, event):
        f = event.IsChecked()
        self.m_namespace_viewer.set_filter(f)
        self.m_namespace_viewer.update_namespace(self.m_stack)

    
    def do_notify_filename(self, filename, command):
        if command is not None:
            self.add_menu_item(ML_WINDOW, filename, command)
            
        self.m_console.set_filename(filename)

    
    def OnSizeWindow(self, event):
        if not self.IsMaximized():
            #
            # On a Mac, the size is magically increased by 47; decrease it back.
            #

            (w, h) = self.GetSize()
            if sys.platform == 'darwin':
                h -= 47

            self.m_settings[WINPDB_SIZE] = (w, h)

        event.Skip()
        
        
    def OnCloseWindow(self, event):
        self.m_settings[WINPDB_MAXIMIZE] = self.IsMaximized()
        self.m_settings[SPLITTER_1_POS] = self.m_splitterh2.GetSashPosition()
        self.m_settings[SPLITTER_2_POS] = self.m_splitterh1.GetSashPosition()
        self.m_settings[SPLITTER_3_POS] = self.m_splitterv.GetSashPosition()
        self.m_settings[SPLITTER_4_POS] = self.m_splitterh3.GetSashPosition()

        #print self.m_settings[SPLITTER_1_POS], self.m_settings[SPLITTER_2_POS], self.m_settings[SPLITTER_3_POS], self.m_settings[SPLITTER_4_POS] 
        
        self.m_console.stop()
        self.shutdown_jobs()
        self.Destroy()

        event.Skip()


    def set_cursor(self, id):
        cursor = wx.StockCursor(id)
        self.SetCursor(cursor)        
        self.m_code_viewer.set_cursor(id)        
        self.m_threads_viewer.set_cursor(id)        
        self.m_stack_viewer.set_cursor(id)        


    def do_none(self, event):
        pass


    def update_state(self, event):
        wx.CallAfter(self.callback_state, event)


    def callback_state(self, event):
        old_state = self.m_state
        self.m_state = event.m_state

        (menu_update_dict, toolbar_update_dict) = STATE_MAP[self.m_state]
        self.set_menu_items_state(menu_update_dict)
        self.set_toolbar_items_state(toolbar_update_dict)

        try:
            index = STATE_DETACHED_MENU[DISABLED].index(ML_RESTART)
            del STATE_DETACHED_MENU[DISABLED][index]
            STATE_DETACHED_MENU[ENABLED].append(ML_RESTART)

        except ValueError:
            pass
            
        state_text = self.m_state
        if state_text == rpdb2.STATE_BROKEN:
            state_text = rpdb2.STR_STATE_BROKEN
            
        self.set_statusbar_data({SB_STATE: state_text.upper()}) 

        if self.m_state == rpdb2.STATE_DETACHED:
            self.set_statusbar_data({SB_ENCRYPTION: (None, None)})
            self.clear_menu_items(ML_WINDOW)
            self.m_source_manager._clear()
            self.m_code_viewer._clear()
            self.m_namespace_viewer._clear()
            self.m_stack_viewer._clear()
            self.m_threads_viewer._clear()
            self.m_console.set_focus()
            
        elif (old_state in [rpdb2.STATE_DETACHED, rpdb2.STATE_DETACHING, rpdb2.STATE_SPAWNING, rpdb2.STATE_ATTACHING]) and (self.m_state not in [rpdb2.STATE_DETACHED, rpdb2.STATE_DETACHING, rpdb2.STATE_SPAWNING, rpdb2.STATE_ATTACHING]):
            try:
                f = self.m_session_manager.get_encryption()
            except rpdb2.NotAttached:
                f = False
                
            data = [BASE64_UNLOCKED, BASE64_LOCKED][f] 
            tooltip = [TOOLTIP_UNLOCKED, TOOLTIP_LOCKED][f]
            self.set_statusbar_data({SB_ENCRYPTION: (data, tooltip)})

        if self.m_state == rpdb2.STATE_BROKEN:
            self.set_toggle(TB_EXCEPTION, False)
            
            #self.m_code_viewer._enable()
            self.m_namespace_viewer._enable()
            self.m_stack_viewer._enable()
            self.m_threads_viewer._enable()

            self.Raise()
            
        elif self.m_state == rpdb2.STATE_ANALYZE:
            self.set_toggle(TB_EXCEPTION, True)
            
            #self.m_code_viewer._enable()
            self.m_namespace_viewer._enable()
            self.m_stack_viewer._enable()
            self.m_threads_viewer._disable()
            self.m_console.set_focus()
            
        else:
            #self.m_code_viewer._disable()
            self.m_namespace_viewer._disable()
            self.m_stack_viewer._disable()
            self.m_threads_viewer._disable()
            self.m_console.set_focus()


    def do_website(self, event):
        self.job_post(webbrowser.open_new, (WEBSITE_URL, ))


    def do_support(self, event):
        self.job_post(webbrowser.open_new, (SUPPORT_URL, ))


    def do_docs(self, event):
        self.job_post(webbrowser.open_new, (DOCS_URL, ))


    def do_updates(self, event):
        self.job_post(webbrowser.open_new, (UPDATES_URL, ))


    def do_license(self, event):
        about = CHTMLDialog(self, LICENSE_TITLE, LICENSE_NOTICE + COPY_OF_THE_GPL_LICENSE)
        about.ShowModal()
        about.Destroy()


    def do_about(self, event):
        about = CHTMLDialog(self, ABOUT_TITLE, ABOUT_NOTICE)
        about.ShowModal()
        about.Destroy()


    def do_password(self, event):
        pwd = self.m_session_manager.get_password()
        pwd_dialog = CPwdDialog(self, pwd)
        r = pwd_dialog.ShowModal()
        if r == wx.ID_OK:
            pwd = pwd_dialog.get_password()

            try:
                self.m_session_manager.set_password(pwd)
            except rpdb2.AlreadyAttached:    
                assert(0)

        pwd_dialog.Destroy()


    def do_launch(self, event):
        (fchdir, command_line) = self.m_session_manager.get_launch_args()

        if None in (fchdir, command_line):
            (fchdir, command_line) = (True, '')
            
        launch_dialog = CLaunchDialog(self, fchdir, command_line)
        r = launch_dialog.ShowModal()
        if r == wx.ID_OK:
            (command_line, fchdir) = launch_dialog.get_command_line()
            self.m_async_sm.launch(fchdir, command_line)
            
        launch_dialog.Destroy()


    def do_open(self, event):
        host = self.m_session_manager.get_host()
        fLocal = (host == rpdb2.LOCAL_HOST)
        open_dialog = COpenDialog(self, fLocal = False)
        r = open_dialog.ShowModal()
        if r == wx.ID_OK:
            file_name = open_dialog.get_file_name()
            self.m_code_viewer.set_file(file_name, fComplain = True)
            
        open_dialog.Destroy()


    def do_attach(self, event):
        attach_dialog = CAttachDialog(self, self.m_session_manager)
        r = attach_dialog.ShowModal()
        if r == wx.ID_OK:
            server = attach_dialog.get_server()
            self.m_async_sm.attach(server.m_rid, server.m_filename)

        attach_dialog.Destroy()


    def do_detach(self, event):
        self.m_async_sm.detach()


    def do_stop(self, event):
        self.m_async_sm.stop_debuggee()

        
    def do_restart(self, event):
        self.m_async_sm.restart()

        
    def do_disable(self, event):
        self.m_async_sm.disable_breakpoint([], fAll = True)

        
    def do_enable(self, event):
        self.m_async_sm.enable_breakpoint([], fAll = True)

        
    def do_clear(self, event):
        self.m_async_sm.delete_breakpoint([], fAll = True)

        
    def do_load(self, event):
        self.m_async_sm.with_callback(self.callback_load).load_breakpoints()


    def callback_load(self, r, exc_info):
        (t, v, tb) = exc_info
           
        if t in (socket.error, rpdb2.CException):    
            error = rpdb2.STR_BREAKPOINTS_LOAD_PROBLEM
        elif t == IOError:     
            error = rpdb2.STR_BREAKPOINTS_NOT_FOUND
        else:
            return

        dlg = wx.MessageDialog(self, error, MSG_ERROR_TITLE, wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()

        
    def do_save(self, event):
        self.m_async_sm.with_callback(self.callback_save).load_breakpoints()


    def callback_save(self, r, exc_info):
        (t, v, tb) = exc_info
           
        if t in (socket.error, rpdb2.CException, IOError):    
            error = rpdb2.STR_BREAKPOINTS_SAVE_PROBLEM
        else:
            return
            
        dlg = wx.MessageDialog(self, error, MSG_ERROR_TITLE, wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()

        
    def do_go(self, event):
        self.m_async_sm.request_go()

        
    def do_break(self, event):
        self.m_async_sm.request_break()

        
    def do_step(self, event):
        self.m_async_sm.request_step()

        
    def do_next(self, event):
        self.m_async_sm.request_next()

        
    def do_return(self, event):
        self.m_async_sm.request_return()

            
    def do_goto(self, event):
        (filename, lineno) = self.m_code_viewer.get_file_lineno()
        self.m_async_sm.request_go_breakpoint(filename, '', lineno)

            
    def do_exit(self, event = None):
        self.Close()



class CWinpdbApp(wx.App):
    def __init__(self, session_manager, fchdir, command_line, fAttach, fAllowUnencrypted):
        self.m_frame = None
        self.m_session_manager = session_manager
        self.m_fchdir = fchdir
        self.m_command_line = command_line
        self.m_fAttach = fAttach
        self.m_fAllowUnencrypted = fAllowUnencrypted
        
        self.m_settings = CSettings(WINPDB_SETTINGS_DEFAULT)

        wx.App.__init__(self, redirect = False)


    def OnInit(self):
        wx.SystemOptions.SetOptionInt("mac.window-plain-transition", 1)

        self.m_settings.load_settings()
        
        if (not self.m_fAllowUnencrypted) and not rpdb2.is_encryption_supported():
            dlg = wx.MessageDialog(None, rpdb2.STR_ENCRYPTION_SUPPORT_ERROR, MSG_ERROR_TITLE, wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return True
        
        self.m_frame = CWinpdbWindow(self.m_session_manager, self.m_fchdir, self.m_command_line, self.m_fAttach, self.m_settings)
        self.m_frame.Show()

        self.SetTopWindow(self.m_frame)

        return True


    def OnExit(self):
        self.m_settings.save_settings()
        


class CCaption(wx.Panel):
    def __init__(self, *args, **kwargs):
        label = kwargs.pop("label", "")
        
        wx.Panel.__init__(self, *args, **kwargs)

        self.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_INACTIVECAPTION))
        self.SetForegroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_CAPTIONTEXT))
        
        sizerv = wx.BoxSizer(wx.VERTICAL)

        self.m_static_text = wx.StaticText(self, -1, label)
        sizerv.Add(self.m_static_text, 0, wx.EXPAND | wx.ALL, 2)

        font = self.m_static_text.GetFont()
        new_font = wx.Font(pointSize = font.GetPointSize(), family = font.GetFamily(), style = font.GetStyle(), weight = wx.BOLD, face = font.GetFaceName())
        self.m_static_text.SetFont(new_font)

        self.SetSizer(sizerv)
        sizerv.Fit(self)



class CCaptionManager:
    def bind_caption(self, widget):
        widget.Bind(wx.EVT_SET_FOCUS, self.OnGainFocus)
        widget.Bind(wx.EVT_KILL_FOCUS, self.OnLoseFocus)

        self.m_n_focus = 0

    def OnGainFocus(self, event):        
        self.m_n_focus += 1
        
        self.m_caption.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_ACTIVECAPTION))
        self.m_caption.Refresh()
        event.Skip()

    def OnLoseFocus(self, event):
        self.m_n_focus -= 1
        if self.m_n_focus > 0:
            return
            
        self.m_caption.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_INACTIVECAPTION))
        self.m_caption.Refresh()
        event.Skip()

        
    
class CStyledViewer(stc.StyledTextCtrl):
    def __init__(self, *args, **kwargs):
        self.m_margin_command = kwargs.pop('margin_command', None)

        stc.StyledTextCtrl.__init__(self, *args, **kwargs)

        #
        # Force Left to Right since CStyledViewer is broken for Right to Left.
        # Not available on wxPython 2.6
        #
        if hasattr(self, 'SetLayoutDirection'):
            self.SetLayoutDirection(1)

        self.SetLexer(stc.STC_LEX_PYTHON)
        self.SetKeyWords(0, " ".join(keyword.kwlist))

        self.SetReadOnly(True)

        self.SetVisiblePolicy(wx.stc.STC_VISIBLE_SLOP, 7)
        self.SetViewWhiteSpace(False)
        self.SetIndentationGuides(True)
        self.SetEOLMode(stc.STC_EOL_LF)
        self.SetViewEOL(False)
        self.SetProperty("fold", "0")
        
        self.SetMarginType(0, stc.STC_MARGIN_NUMBER)
        self.SetMarginMask(0, 0x0)
        self.SetMarginWidth(0, 40)

        self.SetMarginType(1, stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(1, 0x1F)
        self.SetMarginWidth(1, 16)
        self.SetMarginSensitive(1, True)

        if self.m_margin_command is not None:
            self.Bind(stc.EVT_STC_MARGINCLICK, self.m_margin_command)

        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyPressed)
        self.Bind(wx.EVT_KEY_UP, self.OnKeyReleased)

        if wx.Platform == '__WXMSW__':
            self.StyleSetSpec(stc.STC_STYLE_DEFAULT, 'fore:#000000,back:#FFFFFF,face:Courier New,size:9')
        else:
            self.StyleSetSpec(stc.STC_STYLE_DEFAULT, 'fore:#000000,back:#FFFFFF,face:Courier')

        self.StyleClearAll()
        self.SetTabWidth(4)
        
        self.StyleSetSpec(stc.STC_STYLE_LINENUMBER, 'fore:#000000,back:#99A9C2')    
        self.StyleSetSpec(stc.STC_STYLE_BRACELIGHT, 'fore:#00009D,back:#FFFF00')
        self.StyleSetSpec(stc.STC_STYLE_BRACEBAD, 'fore:#00009D,back:#FF0000')
        self.StyleSetSpec(stc.STC_STYLE_INDENTGUIDE, "fore:#CDCDCD")
        self.StyleSetSpec(stc.STC_P_DEFAULT, 'fore:#000000')
        self.StyleSetSpec(stc.STC_P_COMMENTLINE, 'fore:#008000,back:#F0FFF0')
        self.StyleSetSpec(stc.STC_P_COMMENTBLOCK, 'fore:#008000,back:#F0FFF0')
        self.StyleSetSpec(stc.STC_P_NUMBER, 'fore:#008050')
        self.StyleSetSpec(stc.STC_P_STRING, 'fore:#800080')
        self.StyleSetSpec(stc.STC_P_CHARACTER, 'fore:#800080')
        self.StyleSetSpec(stc.STC_P_WORD, 'fore:#000080,bold')
        self.StyleSetSpec(stc.STC_P_TRIPLE, 'fore:#800080,back:#FFFFEA')
        self.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, 'fore:#800080,back:#FFFFEA')
        self.StyleSetSpec(stc.STC_P_CLASSNAME, 'fore:#0000FF,bold')
        self.StyleSetSpec(stc.STC_P_DEFNAME, 'fore:#008050,bold')
        self.StyleSetSpec(stc.STC_P_OPERATOR, 'fore:#800000,bold')
        self.StyleSetSpec(stc.STC_P_IDENTIFIER, 'fore:#000000')

        self.SetSelBackground(True, '#316ac5')
        self.SetSelForeground(True, wx.WHITE)

        self.MarkerDefine(MARKER_BREAKPOINT_ENABLED, stc.STC_MARKER_MAX, wx.BLACK, (255, 0, 0))
        self.MarkerDefine(MARKER_BREAKPOINT_DISABLED, stc.STC_MARKER_MAX, wx.BLACK, (255, 255, 128))
        self.MarkerDefine(MARKER_CURRENT_LINE, stc.STC_MARKER_MAX, wx.WHITE, (150, 150, 255))
        self.MarkerDefine(MARKER_CURRENT_LINE_HIT, stc.STC_MARKER_MAX, wx.BLACK, (215, 215, 255))

        self.MarkerDefine(MARKER_CALL, stc.STC_MARK_CHARACTER + ord('C'), wx.WHITE, "#99A9C2")
        self.MarkerDefine(MARKER_LINE, stc.STC_MARK_CHARACTER + ord('L'), wx.WHITE, "#99A9C2")
        self.MarkerDefine(MARKER_RETURN, stc.STC_MARK_CHARACTER + ord('R'), wx.WHITE, "#99A9C2")
        self.MarkerDefine(MARKER_EXCEPTION, stc.STC_MARK_CHARACTER + ord('E'), wx.WHITE, "#99A9C2")
        self.MarkerDefine(MARKER_RUNNING, stc.STC_MARK_CHARACTER + ord('*'), wx.WHITE, "#99A9C2")

    def _clear(self):
        self.SetReadOnly(False)
        self.ClearAll()
        self.SetReadOnly(True)
        
    def load_source(self, value):
        self.SetReadOnly(False)
        self.ClearAll()
        self.SetText(value)
        self.SetReadOnly(True)
        self.GotoLine(0)
        self.EmptyUndoBuffer()
        self.SetSavePoint()
      
    def OnKeyReleased(self, event):
        key_code = event.GetKeyCode()

        if key_code == wx.WXK_CONTROL:
            self.GetParent().GetEventHandler().ProcessEvent(event)

        event.Skip()
            
    def OnKeyPressed(self, event):
        key_code = event.GetKeyCode()

        if key_code == wx.WXK_TAB:
            forward = not event.ShiftDown()
            switch = event.ControlDown()
            if switch:
                self.GetParent().GetEventHandler().ProcessEvent(event)
                return
            
            ne = wx.NavigationKeyEvent()
            ne.SetDirection(forward)
            ne.SetCurrentFocus(self)
            ne.SetEventObject(self)
            self.GetParent().GetEventHandler().ProcessEvent(ne)
            event.Skip()
            return
            
        event.Skip()



class CSourceManager:
    def __init__(self, job_manager, session_manager):
        self.m_job_manager = job_manager
        self.m_session_manager = session_manager
        self.m_async_sm = CAsyncSessionManager(session_manager, self.m_job_manager)

        self.m_files = {}

        self.m_lock = threading.RLock()


    def _clear(self):
        self.m_files = {}


    def is_in_files(self, filename):
        for k in self.m_files.keys():
            if filename in k:
                return True

        return False
        
    
    def get_source(self, filename):
        for k, v in self.m_files.items():
            if not filename in k:
                continue

            if v[0] == 0:        
                return (k, v[1])

            t = time.time()
            if t - v[0] < BAD_FILE_WARNING_TIMEOUT_SEC:
                return (k, v[1])    

            #del self.m_files[k]
            raise KeyError

        raise KeyError

        
    def load_source(self, filename, callback, args, fComplain): 
        f = lambda r, exc_info: self.callback_load_source(r, exc_info, filename, callback, args, fComplain)        

        self.m_async_sm.with_callback(f).get_source_file(filename, -1, -1)

        
    def callback_load_source(self, r, exc_info, filename, callback, args, fComplain):
        (t, v, tb) = exc_info

        if t == None:
            _filename = r[rpdb2.DICT_KEY_FILENAME]
            source_lines = r[rpdb2.DICT_KEY_LINES]
            _source = string.join(source_lines, '')

            de = wx.GetDefaultPyEncoding()
            se = rpdb2.ParseEncoding(_source)
            if se is None:
                se = de
                
            u = _source.decode(se, 'ignore')
            source = u.encode(de, 'ignore')
            _time = 0
            
        elif t in (IOError, socket.error, rpdb2.CConnectionException):
            if fComplain:
                dlg = wx.MessageDialog(None, STR_FILE_LOAD_ERROR % (filename, ), MSG_WARNING_TITLE, wx.OK | wx.ICON_WARNING)
                dlg.ShowModal()
                dlg.Destroy()
                return

            if t == IOError and rpdb2.ERROR_NO_BLENDER_SOURCE in v.args and not self.is_in_files(filename):
                dlg = wx.MessageDialog(None, STR_BLENDER_SOURCE_WARNING, MSG_WARNING_TITLE, wx.OK | wx.ICON_WARNING)
                dlg.ShowModal()
                dlg.Destroy()
            
            _filename = filename
            source = STR_FILE_LOAD_ERROR2 % (filename, )
            _time = time.time()
                    
        try:    
            self.m_lock.acquire()

            fNotify = not self.is_in_files(_filename)
            self.m_files[_filename] = (_time, source)

        finally:
            self.m_lock.release()

        _args = (_filename, ) + args + (fNotify, )

        callback(*_args)


        
class CCodeViewer(wx.Panel, CJobs, CCaptionManager):
    def __init__(self, *args, **kwargs):
        self.m_session_manager = kwargs.pop('session_manager')
        self.m_notify_filename = kwargs.pop('notify_filename', None)
        self.m_source_manager = kwargs.pop('source_manager')
        
        wx.Panel.__init__(self, *args, **kwargs)
        CJobs.__init__(self)
        
        self.init_jobs()

        self.m_async_sm = CAsyncSessionManager(self.m_session_manager, self)

        self.m_history = []
        self.m_history_index = 0

        self.m_fSwitch = False
        self.m_swiched_original = None
        
        self.m_files = {}

        self.m_cur_filename = None

        self.m_pos_filename = None
        self.m_pos_lineno = None
        self.m_pos_event = None

        self.m_breakpoint_lines = {}
        
        self.m_request_number = 0
        self.m_last_position_time = 0

        self.m_event2Marker = {'running': MARKER_RUNNING, 'call': MARKER_CALL, 'line': MARKER_LINE, 'return': MARKER_RETURN,  'exception': MARKER_EXCEPTION}
        
        _sizerv = wx.BoxSizer(wx.VERTICAL)
        sizerv = wx.BoxSizer(wx.VERTICAL)
        _sizerv.Add(sizerv, 1, wx.EXPAND | wx.ALL, 3)

        self.m_caption = CCaption(self, label = CAPTION_SOURCE)
        sizerv.Add(self.m_caption, 0, wx.EXPAND | wx.ALL, 0)

        self.m_viewer = CStyledViewer(self, style = wx.TAB_TRAVERSAL, margin_command = self.on_margin_clicked)
        self.bind_caption(self.m_viewer)
        sizerv.Add(self.m_viewer, 1, wx.EXPAND | wx.ALL, 0)

        self.SetSizer(_sizerv)
        _sizerv.Fit(self)

        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyPressed)
        self.Bind(wx.EVT_KEY_UP, self.OnKeyReleased)
        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroyWindow)


    def OnDestroyWindow(self, event):
        self.shutdown_jobs()

        
    def set_cursor(self, id):
        self.m_viewer.SetSTCCursor([stc.STC_CURSORNORMAL, stc.STC_CURSORWAIT][id == wx.CURSOR_WAIT])        


    def on_margin_clicked(self, event):
        lineno = self.m_viewer.LineFromPosition(event.GetPosition()) + 1
        self.__toggle_breakpoint(lineno)        
        event.Skip()


    def get_file_lineno(self):
        lineno = self.m_viewer.GetCurrentLine() + 1

        return (self.m_cur_filename, lineno)


    def toggle_breakpoint(self):
        lineno = self.m_viewer.GetCurrentLine() + 1 
        self.__toggle_breakpoint(lineno)        

        
    def __toggle_breakpoint(self, lineno):
        try:
            bpl = self.m_session_manager.get_breakpoints()
        except rpdb2.NotAttached:
            return
            
        id = self.m_breakpoint_lines.get(lineno, None)
        if id is not None:
            bp = bpl.get(id, None)
            
        if (id is None) or (bp is None):
            self.m_async_sm.set_breakpoint(self.m_cur_filename, '', lineno, True, '')            
            return

        self.m_async_sm.delete_breakpoint([id], False)


    def _disable(self):
        self.m_viewer.Disable()


    def _enable(self):
        self.m_viewer.Enable()


    def get_history(self, fBack):
        self.m_history_index = (self.m_history_index + [-1, 1][fBack]) % len(self.m_history)
        return self.m_history[self.m_history_index]

        
    def set_history(self, value):
        if value in self.m_history:
            self.m_history.remove(value)
            
        self.m_history.insert(0, value)
        self.m_history = self.m_history[:50]
        
        self.m_history_index = 0


    def OnKeyPressed(self, event):
        if len(self.m_history) < 2:
            return
            
        if self.m_fSwitch == False:
            self.m_fSwitch = True
            self.m_swiched_original = self.m_cur_filename
        
        value = self.get_history(event.ShiftDown())  

        self.set_file(value, fNoHistory = True)    

        
    def OnKeyReleased(self, event):
        if self.m_fSwitch == False:
            return

        if self.m_swiched_original == self.m_cur_filename:
            return
            
        self.set_history(self.m_cur_filename)

        
    def _clear(self):
        self.m_history = []
        self.m_history_index = 0

        self.m_fSwitch = False
        self.m_swiched_original = None

        self.m_files = {}

        self.m_cur_filename = None

        self.m_pos_filename = None
        self.m_pos_lineno = None
        self.m_pos_event = None

        self.m_viewer._clear()        


    def __notify_filename(self, filename, fNew):
        if self.m_notify_filename is None:
            return

        if fNew:    
            def command(event, filename = filename):
                self.set_file(filename)
        else:
            command = None

        self.m_notify_filename(filename, command)

        
    def set_file(self, filename, fNoHistory = False, request_number = 0, fNotify = False, fComplain = False):
        if fNotify:
            self.__notify_filename(filename, fNew = True)

        if request_number == 0:
            self.m_request_number += 1
            request_number = self.m_request_number
        elif request_number <  self.m_request_number:
            return

        if self.m_cur_filename == filename:
            return
            
        try:
            (_filename, source) = self.m_source_manager.get_source(filename)
        except KeyError:    
            self.m_source_manager.load_source(filename, self.set_file, (fNoHistory, request_number,), fComplain)
            return

        if self.m_cur_filename == _filename:
            return
            
        self.__notify_filename(filename, fNew = False)
        
        if self.m_cur_filename is not None:
            self.m_files[self.m_cur_filename] = self.m_viewer.GetCurrentLine() + 1  

        lineno = self.m_files.get(_filename, 1)
        
        self.m_viewer.load_source(source)
    
        self.m_viewer.EnsureVisibleEnforcePolicy(lineno - 1)
        self.m_viewer.GotoLine(lineno - 1)
        
        self.m_caption.m_static_text.SetLabel(CAPTION_SOURCE + ' ' + rpdb2.clip_filename(_filename))
        
        self.m_cur_filename = _filename

        self.set_markers()

        if fNoHistory == False:
            self.set_history(self.m_cur_filename)

        
    def set_position(self, filename, lineno, event, request_number = 0, fNotify = False):
        if fNotify:
            self.__notify_filename(filename, fNew = True)
        
        if request_number == 0:
            self.m_request_number += 1
            request_number = self.m_request_number
        elif request_number <  self.m_request_number:
            return

        if self.m_cur_filename != filename:
            try:
                (_filename, source) = self.m_source_manager.get_source(filename)
            except KeyError:    
                self.m_source_manager.load_source(filename, self.set_position, (lineno, event, request_number), fComplain = False)
                return

            self.__notify_filename(filename, fNew = False)
            
            if self.m_cur_filename is not None:
                self.m_files[self.m_cur_filename] = self.m_viewer.GetCurrentLine() + 1 

            self.m_viewer.load_source(source)

        self.m_viewer.EnsureVisibleEnforcePolicy(lineno - 1)
        self.m_viewer.GotoLine(lineno - 1)
        
        self.m_caption.m_static_text.SetLabel(CAPTION_SOURCE + ' ' + rpdb2.clip_filename(filename))
        
        self.m_cur_filename = filename

        self.m_pos_filename = filename
        self.m_pos_lineno = lineno
        self.m_pos_event = event

        self.set_markers()

        self.set_history(self.m_cur_filename)

        self.m_last_position_time = time.time()

        
    def update_bp(self, event):
        if self.m_pos_filename is None:
            return

        fposition_timeout = time.time() - self.m_last_position_time > POSITION_TIMEOUT

        if event.m_action == rpdb2.CEventBreakpoint.SET and fposition_timeout:
            if self.m_cur_filename == event.m_bp.m_filename:
                lineno = event.m_bp.m_lineno
                self.m_viewer.EnsureVisibleEnforcePolicy(lineno - 1)
                self.m_viewer.GotoLine(lineno - 1)            
            
        self.set_markers()

        
    def set_markers(self):
        for marker in MARKER_LIST:
            self.m_viewer.MarkerDeleteAll(marker)

        if self.m_pos_filename == self.m_cur_filename:    
            self.m_viewer.MarkerAdd(self.m_pos_lineno - 1, self.m_event2Marker[self.m_pos_event])

        f_current_line = False

        try:
            bpl = self.m_session_manager.get_breakpoints()
        except rpdb2.NotAttached:
            return

        self.m_breakpoint_lines = {}
        
        for bp in bpl.values():
            if bp.m_filename != self.m_cur_filename:
                continue

            self.m_breakpoint_lines[bp.m_lineno] = bp.m_id
            
            if (self.m_pos_filename == self.m_cur_filename) and (bp.m_lineno == self.m_pos_lineno) and bp.m_fEnabled:
                self.m_viewer.MarkerAdd(self.m_pos_lineno - 1, MARKER_CURRENT_LINE_HIT)
                f_current_line = True
            else:
                marker = [MARKER_BREAKPOINT_DISABLED, MARKER_BREAKPOINT_ENABLED][bp.m_fEnabled]
                self.m_viewer.MarkerAdd(bp.m_lineno - 1, marker)

        if (self.m_pos_filename == self.m_cur_filename) and not f_current_line:
            self.m_viewer.MarkerAdd(self.m_pos_lineno - 1, MARKER_CURRENT_LINE)
        
        

class CConsole(wx.Panel, CCaptionManager):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)

        self.m_history = ['']
        self.m_history_index = 0
        
        self.m_parent = None
        self.m_console = None

        self.m_queue = Queue.Queue()
        
        _sizerv = wx.BoxSizer(wx.VERTICAL)
        sizerv = wx.BoxSizer(wx.VERTICAL)
        _sizerv.Add(sizerv, 1, wx.EXPAND | wx.ALL, 3)

        self.m_caption = CCaption(self, label = CAPTION_CONSOLE)
        sizerv.Add(self.m_caption, 0, wx.EXPAND | wx.ALL, 0)

        self.m_console_out = wx.TextCtrl(self, style = wx.TAB_TRAVERSAL | wx.TE_MULTILINE | wx.HSCROLL | wx.VSCROLL)
        self.m_console_out.Bind(wx.EVT_KEY_DOWN, self.OnConsoleOutKeyPressed)
        self.bind_caption(self.m_console_out)
        self.set_font(self.m_console_out)
        sizerv.Add(self.m_console_out, 1, wx.EXPAND | wx.ALL, 0)

        sizerh = wx.BoxSizer(wx.HORIZONTAL)
        sizerv.Add(sizerh, 0, wx.EXPAND | wx.ALL, 0)
        
        label = wx.StaticText(self, -1, LABEL_CONSOLE, style = wx.TAB_TRAVERSAL)
        sizerh.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 0)

        self.m_console_in = wx.TextCtrl(self, style = wx.TE_PROCESS_ENTER)
        self.bind_caption(self.m_console_in)
        self.set_font(self.m_console_in)
        self.m_console_in.SetFocus()
        self.m_console_in.Bind(wx.EVT_CHAR, self.OnChar)
        self.m_console_in.Bind(wx.EVT_TEXT_ENTER, self.OnSendText)
        sizerh.Add(self.m_console_in, 1, wx.EXPAND | wx.ALL, 0)       

        self.SetSizer(_sizerv)
        _sizerv.Fit(self)


    def OnConsoleOutKeyPressed(self, event):
        key_code = event.GetKeyCode()

        if key_code != wx.WXK_TAB:
            return
            
        forward = not event.ShiftDown()            
        ne = wx.NavigationKeyEvent()
        ne.SetDirection(forward)
        ne.SetCurrentFocus(self.m_console_out)
        ne.SetEventObject(self.m_console_out)
        self.GetEventHandler().ProcessEvent(ne)
        event.Skip()
        return
            
        
    def set_focus(self):
        self.m_console_in.SetFocus()

        
    def set_filename(self, filename):
        self.m_console.set_filename(filename)


    def set_font(self, ctrl):
        font = ctrl.GetFont()

        if wx.Platform == '__WXMSW__':
            face = "Courier New"
            point_size = 9
        else:
            face = "Courier"
            point_size = font.GetPointSize()
            
        new_font = wx.Font(pointSize = point_size, family = font.GetFamily(), style = font.GetStyle(), weight = font.GetWeight(), face = face)
        ctrl.SetFont(new_font)

        
    def start(self, parent, session_manager, fchdir, command_line, fAttach):
        self.m_parent = parent
        self.m_console = rpdb2.CConsole(session_manager, stdin = self, stdout = self, fSplit = True)
        self.m_console.start()

        if fAttach:
            session_manager.attach_nothrow(command_line)
        elif command_line != '':
            session_manager.launch_nothrow(fchdir, command_line)

        
    def stop(self):
        self.m_queue.put('exit\n')
        self.m_console.join()


    def write(self, str):
        sl = str.split('\n')
        
        _str = ''
        
        for s in sl:
            while True:
                _str += '\n' + s[:81]
                s = s[81:] 
                if len(s) == 0:
                    break
            
        wx.CallAfter(self.m_console_out.write, _str[1:])    


    def flush(self):
        pass


    def readline(self):
        str = self.m_queue.get()
        return str


    def OnChar(self, event):
        key = event.GetKeyCode()
        
        if key in [wx.WXK_UP, wx.WXK_DOWN]:
            value = self.m_console_in.GetValue()
            _value = self.get_history(key == wx.WXK_UP, value)
            self.m_console_in.SetValue(_value)
            self.m_console_in.SetInsertionPointEnd()
            return
            
        event.Skip()    


    def OnSendText(self, event):
        value = self.m_console_in.GetValue()
        self.set_history(value)
        
        self.m_console_out.write(CONSOLE_PROMPT + value + '\n') 
        self.m_console_in.Clear()
        self.m_queue.put(value + '\n')

        if value in ['exit', 'EOF']:
            self.m_parent.do_exit()

            
    def get_history(self, fBack, value = None):
        if (value is not None) and (value != self.m_history[self.m_history_index]):
            self.m_history[0] = value
            self.m_history_index = 0
            
        self.m_history_index = (self.m_history_index + [-1, 1][fBack]) % len(self.m_history)
        return self.m_history[self.m_history_index]

        
    def set_history(self, value):
        self.m_history[0] = ''
        self.m_history.insert(1, value)
        self.m_history = self.m_history[:50]
        
        self.m_history_index = 0



class CThreadsViewer(wx.Panel, CCaptionManager):
    def __init__(self, *args, **kwargs):
        self.m_select_command = kwargs.pop('select_command', None)
        
        wx.Panel.__init__(self, *args, **kwargs)

        self.m_suppress_recursion = 0
        
        _sizerv = wx.BoxSizer(wx.VERTICAL)
        sizerv = wx.BoxSizer(wx.VERTICAL)
        _sizerv.Add(sizerv, 1, wx.EXPAND | wx.ALL, 3)

        self.m_caption = CCaption(self, label = CAPTION_THREADS)
        sizerv.Add(self.m_caption, 0, wx.EXPAND | wx.ALL, 0)

        self.m_threads = CListCtrl(parent = self, style = wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.bind_caption(self.m_threads)
        self.m_threads.InsertColumn(0, HLIST_HEADER_TID + '    ')
        self.m_threads.InsertColumn(1, HLIST_HEADER_NAME)
        self.m_threads.InsertColumn(2, HLIST_HEADER_STATE)
        sizerv.Add(self.m_threads, 1, wx.EXPAND | wx.ALL, 0)

        if self.m_select_command:
            self.m_threads.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnThreadSelected)
                    
        self.SetSizer(_sizerv)
        _sizerv.Fit(self)


    def set_cursor(self, id):
        cursor = wx.StockCursor(id)
        self.SetCursor(cursor)        
        self.m_threads.SetCursor(cursor)        


    def _clear(self):
        self.m_threads.DeleteAllItems()
        self.m_threads.Disable()


    def _disable(self):
        self.m_threads.Disable()


    def _enable(self):
        self.m_threads.Enable()


    def is_selected(self, index):
        return self.m_threads.IsSelected(index)


    def update_thread(self, thread_id, thread_name, fBroken):
        index = self.m_threads.FindItemData(-1, thread_id)
        if index < 0:
            return -1

        self.m_threads.SetStringItem(index, 1, thread_name)
        self.m_threads.SetStringItem(index, 2, [rpdb2.STATE_RUNNING, rpdb2.STR_STATE_BROKEN][fBroken])

        return index

        
    def update_threads_list(self, current_thread, threads_list):
        if self.m_suppress_recursion > 0:
            self.m_suppress_recursion -= 1
            return
            
        self.m_threads.DeleteAllItems()

        j = None
        for i, s in enumerate(threads_list):
            tid = s[rpdb2.DICT_KEY_TID]
            name = s[rpdb2.DICT_KEY_NAME]
            fBroken = s[rpdb2.DICT_KEY_BROKEN]
            index = self.m_threads.InsertStringItem(sys.maxint, repr(tid))
            self.m_threads.SetStringItem(index, 1, name)
            self.m_threads.SetStringItem(index, 2, [rpdb2.STATE_RUNNING, rpdb2.STR_STATE_BROKEN][fBroken])
            self.m_threads.SetItemData(index, tid)
            if tid == current_thread:
                j = i

        self.m_threads.set_columns_width()

        if j is not None:
            self.m_suppress_recursion += 1
            self.m_threads.Select(j)


    def OnThreadSelected(self, event):                
        if self.m_suppress_recursion == 0:
            self.m_suppress_recursion += 1
            index = event.m_itemIndex
            tid = self.m_threads.GetItemData(index)
            self.m_select_command(tid)
        else:
            self.m_suppress_recursion -= 1

        event.Skip()


        
class CNamespacePanel(wx.Panel, CJobs):
    def __init__(self, *args, **kwargs):
        self.m_session_manager = kwargs.pop('session_manager')

        wx.Panel.__init__(self, *args, **kwargs)
        CJobs.__init__(self)
        
        self.init_jobs()

        self.m_async_sm = CAsyncSessionManager(self.m_session_manager, self)

        self.m_lock = threading.RLock()
        self.m_jobs = []
        self.m_n_workers = 0
        
        self.m_fFilter = False
        self.m_key = None

        sizerv = wx.BoxSizer(wx.VERTICAL)
        
        self.m_tree = wx.gizmos.TreeListCtrl(self, -1, style = wx.TR_HIDE_ROOT | wx.TR_DEFAULT_STYLE | wx.TR_FULL_ROW_HIGHLIGHT | wx.NO_BORDER)

        self.m_tree.AddColumn(TLC_HEADER_NAME)
        self.m_tree.AddColumn(TLC_HEADER_TYPE)
        self.m_tree.AddColumn(TLC_HEADER_REPR)
        self.m_tree.SetColumnWidth(2, 800)
        self.m_tree.SetMainColumn(0) 
        self.m_tree.SetLineSpacing(0)
        
        self.m_tree.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.OnItemExpanding)
        self.m_tree.Bind(wx.EVT_TREE_ITEM_COLLAPSING, self.OnItemCollapsing)
        self.m_tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnItemActivated)

        try:
            self.m_tree.Bind(wx.EVT_TREE_ITEM_GETTOOLTIP, self.OnItemToolTip)
        except:
            pass

        self.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroyWindow)

        sizerv.Add(self.m_tree, flag = wx.GROW, proportion = 1)
        self.SetSizer(sizerv)
        sizerv.Fit(self)


    def OnDestroyWindow(self, event):
        self.shutdown_jobs()

        
    def _clear(self):
        self.m_tree.DeleteAllItems()


    def set_filter(self, fFilter):
        self.m_fFilter = fFilter

        
    def bind_caption(self, caption_manager):
        w = self.m_tree.GetMainWindow()
        caption_manager.bind_caption(w)

        
    def OnItemActivated(self, event):
        item = event.GetItem()
        expr = self.m_tree.GetPyData(item)
        if expr == STR_NAMESPACE_DEADLOCK:
            return

        expr_dialog = CExpressionDialog(self)
        pos = self.GetPositionTuple()
        expr_dialog.SetPosition((pos[0] + 50, pos[1] + 50))
        r = expr_dialog.ShowModal()
        if r != wx.ID_OK:
            expr_dialog.Destroy()
            return

        expr = expr_dialog.get_expression()
        expr_dialog.Destroy()

        _expr = self.m_tree.GetPyData(item)
        _suite = "%s = %s" % (_expr, expr)
        
        self.m_async_sm.with_callback(self.callback_execute).execute(_suite)


    def callback_execute(self, r, exc_info):
        (t, v, tb) = exc_info

        if t != None:
            rpdb2.print_exception(t, b, tb)
            return

        (warning, error) = r
        
        if error != '':
            dlg = wx.MessageDialog(self, error, MSG_ERROR_TITLE, wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()

        if not warning in g_ignored_warnings:
            dlg = wx.MessageDialog(self, MSG_WARNING_TEMPLATE % (warning, ), MSG_WARNING_TITLE, wx.OK | wx.CANCEL | wx.YES_DEFAULT | wx.ICON_WARNING)
            res = dlg.ShowModal()
            dlg.Destroy()

            if res == wx.ID_CANCEL:
                g_ignored_warnings[warning] = True
        
        
    def OnItemToolTip(self, event):
        item = event.GetItem()

        tt = self.m_tree.GetItemText(item, 2)[1:]
        event.SetToolTip(tt)

       
    def OnItemCollapsing(self, event):
        item = event.GetItem()

        event.Skip()


    def GetChildrenCount(self, item):
        n = self.m_tree.GetChildrenCount(item)
        if n != 1:
            return n 

        child = self.get_children(item)[0]
        expr = self.m_tree.GetPyData(child)

        if expr == STR_NAMESPACE_DEADLOCK:
            return 0

        return 1
        
        
    def expand_item(self, item, _map, froot = False, fskip_expansion_check = False):
        if not self.m_tree.ItemHasChildren(item):
            return
        
        if not froot and not fskip_expansion_check and self.m_tree.IsExpanded(item):
            return

        if self.GetChildrenCount(item) > 0:
            return
        
        expr = self.m_tree.GetPyData(item)

        l = [e for e in _map if e.get(rpdb2.DICT_KEY_EXPR, None) == expr]
        if l == []:
            return None

        _r = l[0] 
        if _r is None:
            return   

        if rpdb2.DICT_KEY_ERROR in _r:
            return
        
        if _r[rpdb2.DICT_KEY_N_SUBNODES] == 0:
            self.m_tree.SetItemHasChildren(item, False)
            return

        #
        # Create a list of the subitems.
        # The list is indexed by name or directory key.
        # In case of a list, no sorting is needed.
        #

        snl = _r[rpdb2.DICT_KEY_SUBNODES] 

        sorted_snl = [(r[rpdb2.DICT_KEY_NAME], r) for r in snl]
        if _r[rpdb2.DICT_KEY_TYPE] != 'list':
            sorted_snl.sort()
        
        for (key_name, r) in sorted_snl:
            child = self.m_tree.AppendItem(item, key_name)
            self.m_tree.SetItemText(child, ' ' + r[rpdb2.DICT_KEY_REPR], 2)
            self.m_tree.SetItemText(child, ' ' + r[rpdb2.DICT_KEY_TYPE], 1)
            self.m_tree.SetItemPyData(child, r[rpdb2.DICT_KEY_EXPR])
            self.m_tree.SetItemHasChildren(child, (r[rpdb2.DICT_KEY_N_SUBNODES] > 0))

        self.m_tree.Expand(item)

    
    def OnItemExpanding(self, event):
        item = event.GetItem()        

        if not self.m_tree.ItemHasChildren(item):
            event.Skip()
            return
        
        if self.GetChildrenCount(item) > 0:
            event.Skip()
            return
            
        self.m_tree.DeleteChildren(item)
        expr = self.m_tree.GetPyData(item)

        f = lambda r, exc_info: self.callback_ns(r, exc_info, expr)        
        self.m_async_sm.with_callback(f).get_namespace([(expr, True)], self.m_fFilter)
        
        event.Skip()


    def callback_ns(self, r, exc_info, expr):
        (t, v, tb) = exc_info

        item = self.find_item(expr)
        if item == None:
            return
            
        if t != None or r is None or len(r) == 0:
            child = self.m_tree.AppendItem(item, STR_NAMESPACE_DEADLOCK)
            self.m_tree.SetItemText(child, ' ' + STR_NAMESPACE_DEADLOCK, 2)
            self.m_tree.SetItemText(child, ' ' + STR_NAMESPACE_DEADLOCK, 1)
            self.m_tree.SetItemPyData(child, STR_NAMESPACE_DEADLOCK)
            self.m_tree.Expand(item)
            return
            
        self.expand_item(item, r, False, True)               
        

    def find_item(self, expr):
        item = self.m_tree.GetRootItem()
        while item:
            expr2 = self.m_tree.GetPyData(item)
            if expr2 == expr:
                return item               
                
            item = self.m_tree.GetNext(item)

        return None    
    

    def get_children(self, item):
        (child, cookie) = self.m_tree.GetFirstChild(item)
        cl = []
        
        while child and child.IsOk():
            cl.append(child)
            (child, cookie) = self.m_tree.GetNextChild(item, cookie)

        return cl    

                             
    def get_expression_list(self):
        if self.m_tree.GetCount() == 0:
            return None

        item = self.m_tree.GetRootItem()

        s = [item]
        el = []

        while len(s) > 0:
            item = s.pop(0)
            expr = self.m_tree.GetPyData(item)
            fExpand = self.m_tree.IsExpanded(item) and self.GetChildrenCount(item) > 0
            if not fExpand:
                continue

            el.append((expr, True))
            items = self.get_children(item)
            s = items + s

        return el    


    def update_namespace(self, key, el):
        old_key = self.m_key
        old_el = self.get_expression_list()

        if key == old_key:
            el = old_el

        self.m_key = key

        if el is None:
            el = [(self.get_root_expr(), True)]

        self.post(el, self.m_fFilter)

        return (old_key, old_el)


    def post(self, el, fFilter):
        self.m_jobs.insert(0, (el, fFilter))

        if self.m_n_workers == 0:
            self.job_post(self.job_update_namespace, ())

        
    def job_update_namespace(self):
        while len(self.m_jobs) > 0:
            self.m_lock.acquire()
            self.m_n_workers += 1
            self.m_lock.release()
            
            try:
                del self.m_jobs[1:]
                (el, fFilter) = self.m_jobs.pop()
                rl = self.m_session_manager.get_namespace(el, fFilter)
                wx.CallAfter(self.do_update_namespace, rl)

            except (rpdb2.ThreadDone, rpdb2.NoThreads):
                wx.CallAfter(self.m_tree.DeleteAllItems)
                
            except:
                rpdb2.print_debug()

            self.m_lock.acquire()
            self.m_n_workers -= 1
            self.m_lock.release()

        
    def do_update_namespace(self, rl):    
        self.m_tree.DeleteAllItems()

        root = self.m_tree.AddRoot('root')
        self.m_tree.SetItemPyData(root, self.get_root_expr())
        self.m_tree.SetItemHasChildren(root, True)

        s = [root]

        while len(s) > 0:
            item = s.pop(0)
            self.expand_item(item, rl, item is root)
            
            items = self.get_children(item)
            s = items + s


    def get_root_expr(self):
        """
        Over-ride in derived classes
        """
        pass



class CLocals(CNamespacePanel):
    def get_root_expr(self):
        return 'locals()'
        

    
class CGlobals(CNamespacePanel):
    def get_root_expr(self):
        return 'globals()'
        
        
        
class CException(CNamespacePanel):
    def get_root_expr(self):
        return rpdb2.RPDB_EXEC_INFO
        

    
class CNamespaceViewer(wx.Panel, CCaptionManager):
    def __init__(self, *args, **kwargs):
        self.m_session_manager = kwargs.pop('session_manager')

        self.m_key_map = {}
        
        wx.Panel.__init__(self, *args, **kwargs)

        _sizerv = wx.BoxSizer(wx.VERTICAL)
        sizerv = wx.BoxSizer(wx.VERTICAL)
        _sizerv.Add(sizerv, 1, wx.EXPAND | wx.ALL, 3)

        self.m_caption = CCaption(self, label = CAPTION_NAMESPACE)
        sizerv.Add(self.m_caption, 0, wx.EXPAND | wx.ALL, 0)

        self.m_notebook = wx.Notebook(self)

        self.m_locals = CLocals(self.m_notebook, session_manager = self.m_session_manager)
        self.m_notebook.AddPage(self.m_locals, "Locals")
        self.m_globals = CGlobals(self.m_notebook, session_manager = self.m_session_manager)
        self.m_notebook.AddPage(self.m_globals, "Globals")
        self.m_exception = CException(self.m_notebook, session_manager = self.m_session_manager)
        self.m_notebook.AddPage(self.m_exception, "Exception")

        self.bind_caption(self.m_notebook)
        self.m_locals.bind_caption(self)
        self.m_globals.bind_caption(self)
        self.m_exception.bind_caption(self)

        sizerv.Add(self.m_notebook, 1, wx.EXPAND | wx.ALL, 0)
        
        self.SetSizer(_sizerv)
        _sizerv.Fit(self)        


    def _clear(self):
        self.m_locals._clear()
        self.m_globals._clear()
        self.m_exception._clear()


    def _disable(self):
        self.m_notebook.Disable()
        self.m_locals.Disable()
        self.m_globals.Disable()
        self.m_exception.Disable()

        
    def _enable(self):
        self.m_notebook.Enable()
        self.m_locals.Enable()
        self.m_globals.Enable()
        self.m_exception.Enable()

        
    def set_filter(self, fFilter):
        self.m_locals.set_filter(fFilter)
        self.m_globals.set_filter(fFilter)
        self.m_exception.set_filter(fFilter)


    def get_local_key(self, _stack):
        frame_index = self.m_session_manager.get_frame_index()
        c = _stack.get(rpdb2.DICT_KEY_CODE_LIST, [])
        key = c[-(1 + frame_index)]
        return key        

            
    def get_global_key(self, _stack):
        frame_index = self.m_session_manager.get_frame_index()
        s = _stack.get(rpdb2.DICT_KEY_STACK, [])
        key = s[-(1 + frame_index)][0]
        return key

            
    def update_namespace(self, _stack):
        try:
            key = self.get_local_key(_stack)
            el = self.m_key_map.get(key, None)
            (key0, el0) = self.m_locals.update_namespace(key, el)
            self.m_key_map[key0] = el0
            
            key = self.get_global_key(_stack)
            el = self.m_key_map.get(key, None)
            (key1, el1) = self.m_globals.update_namespace(key, el)
            self.m_key_map[key1] = el1
            
            key = 'exception'
            el = self.m_key_map.get(key, None)
            (key1, el1) = self.m_exception.update_namespace(key, el)
            self.m_key_map[key] = el1

        except rpdb2.NotAttached:
            return

        

class CStackViewer(wx.Panel, CCaptionManager):
    def __init__(self, *args, **kwargs):
        self.m_select_command = kwargs.pop('select_command', None)
        
        wx.Panel.__init__(self, *args, **kwargs)

        self.m_suppress_recursion = 0
        
        _sizerv = wx.BoxSizer(wx.VERTICAL)
        sizerv = wx.BoxSizer(wx.VERTICAL)
        _sizerv.Add(sizerv, 1, wx.EXPAND | wx.ALL, 3)

        self.m_caption = CCaption(self, label = CAPTION_STACK)
        sizerv.Add(self.m_caption, 0, wx.EXPAND | wx.ALL, 0)

        self.m_stack = CListCtrl(parent = self, style = wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.bind_caption(self.m_stack)
        self.m_stack.InsertColumn(0, HLIST_HEADER_FRAME)
        self.m_stack.InsertColumn(1, HLIST_HEADER_FILENAME)
        self.m_stack.InsertColumn(2, HLIST_HEADER_LINENO)
        self.m_stack.InsertColumn(3, HLIST_HEADER_FUNCTION)
        self.m_stack.InsertColumn(4, HLIST_HEADER_PATH)

        sizerv.Add(self.m_stack, 1, wx.EXPAND | wx.ALL, 0)

        if self.m_select_command:
            self.m_stack.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnFrameSelected)
                    
        self.SetSizer(_sizerv)
        _sizerv.Fit(self)


    def set_cursor(self, id):
        cursor = wx.StockCursor(id)
        self.SetCursor(cursor)        
        self.m_stack.SetCursor(cursor)        


    def _clear(self):
        self.m_stack.DeleteAllItems()


    def _disable(self):
        self.m_stack.Disable()


    def _enable(self):
        self.m_stack.Enable()


    def is_selected(self, index):
        return self.m_stack.IsSelected(index)


    def update_stack_list(self, st):
        self.m_stack.DeleteAllItems()

        s = st.get(rpdb2.DICT_KEY_STACK, [])
        
        i = 0
        while i < len(s):
            e = s[-(1 + i)]

            index = self.m_stack.InsertStringItem(sys.maxint, repr(i))
            self.m_stack.SetStringItem(index, 1, os.path.basename(e[0]))
            self.m_stack.SetStringItem(index, 2, repr(e[1]))
            self.m_stack.SetStringItem(index, 3, e[2])
            self.m_stack.SetStringItem(index, 4, os.path.dirname(e[0]))
            self.m_stack.SetItemData(index, i)

            i += 1
            
        self.m_stack.set_columns_width()

        self.m_suppress_recursion += 1
        self.m_stack.Select(0)


    def select_frame(self, index):
        if self.m_suppress_recursion > 0:
            self.m_suppress_recursion -= 1
            return
            
        if (index < 0) or (index > self.m_stack.GetItemCount()):
            return

        if self.m_stack.IsSelected(index):
            return
            
        self.m_suppress_recursion += 1
        self.m_stack.Select(index)

    
    def OnFrameSelected(self, event):
        if self.m_suppress_recursion == 0:
            self.m_suppress_recursion += 1
            self.m_select_command(event)
        else:
            self.m_suppress_recursion -= 1

        event.Skip()    



class CHTMLDialog(wx.Dialog):
    def __init__(self, parent, title, text):
        wx.Dialog.__init__(self, parent, -1, title)

        sizerv = wx.BoxSizer(wx.VERTICAL)

        self.m_html = wx.html.HtmlWindow(self, -1, size = (600, -1))
        sizerv.Add(self.m_html, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        if "gtk2" in wx.PlatformInfo:
            self.m_html.SetStandardFonts()

        self.m_html.SetPage(self.get_html_text(text))
        
        ir = self.m_html.GetInternalRepresentation()
        self.m_html.SetSize((ir.GetWidth() + 25, min(500, ir.GetHeight() + 25)))

        btnsizer = wx.StdDialogButtonSizer()
        sizerv.Add(btnsizer, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        self.m_ok = wx.Button(self, wx.ID_OK)
        self.m_ok.SetDefault()
        btnsizer.AddButton(self.m_ok)
        btnsizer.Realize()

        self.SetSizer(sizerv)
        sizerv.Fit(self)
        self.CentreOnParent(wx.BOTH)


    def get_html_text(self, text):
        tl = text.split('\n')
        t = '<br>'.join(tl)
        
        return ABOUT_HTML_PREFIX + t + ABOUT_HTML_SUFFIX



class CListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, *args, **kwargs):
        wx.ListCtrl.__init__(self, *args, **kwargs)
        listmix.ListCtrlAutoWidthMixin.__init__(self)


    def set_columns_width(self):
        n = self.GetColumnCount()

        for i in range(0, n - 1):
            self.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)               

        if wx.Platform != '__WXMSW__':
            a = [self.GetColumnWidth(i) for i in range(0, n - 1)]
            
            for i in range(0, n - 1):
                self.SetColumnWidth(i, wx.LIST_AUTOSIZE)               

            b = [self.GetColumnWidth(i) for i in range(0, n - 1)]

            c = [max(i) for i in zip(a, b)]
            
            for i in range(0, n - 1):
                self.SetColumnWidth(i, c[i])
            
        self.resizeLastColumn(50)


    
class CAttachDialog(wx.Dialog, CJobs):
    def __init__(self, parent, session_manager):
        wx.Dialog.__init__(self, parent, -1, DLG_ATTACH_TITLE)
        CJobs.__init__(self)
        
        self.init_jobs()
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        self.m_session_manager = session_manager
        self.m_server_list = None
        self.m_errors = {}
        self.m_index = None
                        
        sizerv = wx.BoxSizer(wx.VERTICAL)
        sizerh = wx.BoxSizer(wx.HORIZONTAL)
        sizerv.Add(sizerh, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        label = wx.StaticText(self, -1, LABEL_ATTACH_HOST)
        sizerh.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        host = self.m_session_manager.get_host()
        self.m_entry_host = wx.TextCtrl(self, value = host, size = (200, -1))
        sizerh.Add(self.m_entry_host, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        btn = wx.Button(self, label = BUTTON_ATTACH_REFRESH)
        self.Bind(wx.EVT_BUTTON, self.do_refresh, btn)
        btn.SetDefault()
        sizerh.Add(btn, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        self.m_listbox_scripts = CListCtrl(parent = self, style = wx.LC_REPORT | wx.LC_SINGLE_SEL, size = (-1, 300))
        self.m_listbox_scripts.InsertColumn(0, HLIST_HEADER_PID + '    ')
        self.m_listbox_scripts.InsertColumn(1, HLIST_HEADER_FILENAME)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.m_listbox_scripts)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected, self.m_listbox_scripts)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated, self.m_listbox_scripts)
        sizerv.Add(self.m_listbox_scripts, 0, wx.EXPAND | wx.ALL, 5)

        btnsizer = wx.StdDialogButtonSizer()
        sizerv.Add(btnsizer, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.m_ok = wx.Button(self, wx.ID_OK)
        self.m_ok.Disable()
        btnsizer.AddButton(self.m_ok)

        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        self.SetSizer(sizerv)
        sizerv.Fit(self)

        wx.CallAfter(self.init2)


    def init2(self):
        pwd = self.m_session_manager.get_password()
        if pwd is not None:
            self.do_refresh()
            return

        pwd_dialog = CPwdDialog(self, pwd)
        pos = self.GetPositionTuple()
        pwd_dialog.SetPosition((pos[0] + 50, pos[1] + 50))
        r = pwd_dialog.ShowModal()
        if r != wx.ID_OK:
            pwd_dialog.Destroy()
            self.Close()
            return

        pwd = pwd_dialog.get_password()
        pwd_dialog.Destroy()

        try:
            self.m_session_manager.set_password(pwd)            

        except rpdb2.AlreadyAttached:    
            assert(0)

            self.Close()
            return
            
        self.do_refresh()

                
    def set_cursor(self, id):
        cursor = wx.StockCursor(id)
        self.SetCursor(cursor)        
        self.m_listbox_scripts.SetCursor(cursor)        


    def OnCloseWindow(self, event):
        self.shutdown_jobs()
        self.Destroy()


    def get_server(self):
        return self.m_server_list[self.m_index]

        
    def do_refresh(self, event = None):
        host = self.m_entry_host.GetValue()
        if host == '':
            host = 'localhost'
        self.job_post(self.job_calc_scripts, (host, ), self.update_body)

        
    def job_calc_scripts(self, host):
        try:
            self.m_session_manager.set_host(host)
            (self.m_server_list, self.m_errors) = self.m_session_manager.calc_server_list()
            return (True, host)
            
        except (rpdb2.UnsetPassword, rpdb2.AlreadyAttached):
            return
        except socket.gaierror, e:
            return (False, host)


    def update_body(self, result, host):
        if result == False:
            dlg = wx.MessageDialog(self, MSG_ERROR_HOST_TEXT % (host, ), MSG_ERROR_TITLE, wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()

        if len(self.m_errors) > 0:
            for k, el in self.m_errors.items():
                if k in [rpdb2.AuthenticationBadData, rpdb2.AuthenticationFailure]:
                    self.report_attach_warning(rpdb2.STR_ACCESS_DENIED)

                elif k == rpdb2.EncryptionNotSupported:
                    self.report_attach_warning(rpdb2.STR_DEBUGGEE_NO_ENCRYPTION)
                    
                elif k == rpdb2.EncryptionExpected:
                    self.report_attach_warning(rpdb2.STR_ENCRYPTION_EXPECTED)

                elif k == rpdb2.BadVersion:
                    for (t, v, tb) in el:
                        self.report_attach_warning(rpdb2.STR_BAD_VERSION % {'value': v})
            
        self.m_ok.Disable()

        host = self.m_session_manager.get_host()
        self.m_entry_host.SetValue(host)

        self.m_listbox_scripts.DeleteAllItems()

        for i, s in enumerate(self.m_server_list):
            index = self.m_listbox_scripts.InsertStringItem(sys.maxint, repr(s.m_pid))
            self.m_listbox_scripts.SetStringItem(index, 1, s.m_filename)
            self.m_listbox_scripts.SetItemData(index, i)

        self.m_listbox_scripts.set_columns_width()


    def report_attach_warning(self, warning):
        dlg = wx.MessageDialog(self, warning, MSG_WARNING_TITLE, wx.OK | wx.ICON_WARNING)
        dlg.ShowModal()
        dlg.Destroy()   
        

    def OnItemSelected(self, event):
        self.m_index = event.m_itemIndex
        self.m_ok.Enable()

        event.Skip()


    def OnItemDeselected(self, event):
        if self.m_listbox_scripts.GetSelectedItemCount() == 0:
            self.m_ok.Disable()

        event.Skip()    

        
    def OnItemActivated(self, event):
        self.m_index = event.m_itemIndex

        self.EndModal(wx.ID_OK)
        
        

class CExpressionDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, DLG_EXPR_TITLE)
        
        sizerv = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(self, -1, STATIC_EXPR)
        sizerv.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        sizerh = wx.BoxSizer(wx.HORIZONTAL)
        sizerv.Add(sizerh, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        label = wx.StaticText(self, -1, LABEL_EXPR)
        sizerh.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.m_entry_expr = wx.TextCtrl(self, size = (200, -1))
        self.Bind(wx.EVT_TEXT, self.OnText, self.m_entry_expr)
        sizerh.Add(self.m_entry_expr, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        btnsizer = wx.StdDialogButtonSizer()
        sizerv.Add(btnsizer, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        
        self.m_ok = wx.Button(self, wx.ID_OK)
        self.m_ok.SetDefault()
        self.m_ok.Disable()
        btnsizer.AddButton(self.m_ok)

        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        self.SetSizer(sizerv)
        sizerv.Fit(self)        

    def OnText(self, event):
        if event.GetString() == '':
            self.m_ok.Disable()
        else:
            self.m_ok.Enable()

        event.Skip()        
                   
    def get_expression(self):
        return self.m_entry_expr.GetValue()


    
class CPwdDialog(wx.Dialog):
    def __init__(self, parent, current_password):
        wx.Dialog.__init__(self, parent, -1, DLG_PWD_TITLE)
        
        sizerv = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(self, -1, STATIC_PWD)
        sizerv.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        sizerh = wx.BoxSizer(wx.HORIZONTAL)
        sizerv.Add(sizerh, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        label = wx.StaticText(self, -1, LABEL_PWD)
        sizerh.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        pwd = [current_password, ''][current_password is None]
        self.m_entry_pwd = wx.TextCtrl(self, value = pwd, size = (200, -1))
        self.Bind(wx.EVT_TEXT, self.OnText, self.m_entry_pwd)
        sizerh.Add(self.m_entry_pwd, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        btnsizer = wx.StdDialogButtonSizer()
        sizerv.Add(btnsizer, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        
        self.m_ok = wx.Button(self, wx.ID_OK)
        self.m_ok.SetDefault()
        if pwd == '':
            self.m_ok.Disable()
        btnsizer.AddButton(self.m_ok)

        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        self.SetSizer(sizerv)
        sizerv.Fit(self)        

    def OnText(self, event):
        if event.GetString() == '':
            self.m_ok.Disable()
        else:
            self.m_ok.Enable()

        event.Skip()        
                   
    def get_password(self):
        return self.m_entry_pwd.GetValue()


    
class COpenDialog(wx.Dialog):
    def __init__(self, parent, fLocal):
        wx.Dialog.__init__(self, parent, -1, DLG_OPEN_TITLE)
        
        sizerv = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(self, -1, STATIC_OPEN)
        sizerv.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        sizerh = wx.BoxSizer(wx.HORIZONTAL)
        sizerv.Add(sizerh, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        label = wx.StaticText(self, -1, LABEL_OPEN)
        sizerh.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        self.m_entry = wx.TextCtrl(self, size = (200, -1))
        self.m_entry.SetFocus()
        self.Bind(wx.EVT_TEXT, self.OnText, self.m_entry)
        sizerh.Add(self.m_entry, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        if fLocal:
            btn = wx.Button(self, label = BUTTON_LAUNCH_BROWSE)
            self.Bind(wx.EVT_BUTTON, self.do_browse, btn)
            sizerh.Add(btn, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        btnsizer = wx.StdDialogButtonSizer()
        sizerv.Add(btnsizer, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        
        self.m_ok = wx.Button(self, wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.do_ok, self.m_ok)
        self.m_ok.SetDefault()
        btnsizer.AddButton(self.m_ok)

        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        self.SetSizer(sizerv)
        sizerv.Fit(self)        

    def OnText(self, event):
        if event.GetString() == '':
            self.m_ok.Disable()
        else:
            self.m_ok.Enable()

        event.Skip()        
            
    def do_browse(self, event = None):
        command_line = self.m_entry.GetValue()
        (_path, filename, args) = rpdb2.split_command_line_path_filename_args(command_line)
        _abs_path = os.path.abspath(_path)

        dlg = wx.FileDialog(self, defaultDir = _abs_path, defaultFile = filename, wildcard = WINPDB_WILDCARD, style = wx.OPEN | wx.CHANGE_DIR)
        r = dlg.ShowModal()
        if r == wx.ID_OK:
            path = dlg.GetPaths()[0]
            abs_path = os.path.abspath(path)
            if (' ' in abs_path):
                abs_path = '"' + abs_path + '"'
        else:
            abs_path = command_line

        dlg.Destroy()
        
        self.m_entry.SetValue(abs_path)
        
    def do_validate(self):
        filename = self.m_entry.GetValue()
        if filename[:1] + filename[-1:] in ['""', "''"]:
            filename = filename[1:-1]

        if not rpdb2.IsPythonSourceFile(filename):
            dlg = wx.MessageDialog(self, MSG_ERROR_FILE_NOT_PYTHON, MSG_ERROR_TITLE, wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return False

        return True

    def do_ok(self, event):
        f = self.do_validate()
        if not f:
            return

        event.Skip()
        
    def get_file_name(self):
        return self.m_entry.GetValue()



class CLaunchDialog(wx.Dialog):
    def __init__(self, parent, fchdir = True, command_line = ''):
        wx.Dialog.__init__(self, parent, -1, DLG_LAUNCH_TITLE)
        sizerv = wx.BoxSizer(wx.VERTICAL)
        sizerh = wx.BoxSizer(wx.HORIZONTAL)
        sizerv.Add(sizerh, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        label = wx.StaticText(self, -1, LABEL_LAUNCH_COMMAND_LINE)
        sizerh.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        self.m_entry_commandline = wx.TextCtrl(self, value = command_line, size = (200, -1))
        self.m_entry_commandline.SetFocus()
        self.Bind(wx.EVT_TEXT, self.OnText, self.m_entry_commandline)
        sizerh.Add(self.m_entry_commandline, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        btn = wx.Button(self, label = BUTTON_LAUNCH_BROWSE)
        self.Bind(wx.EVT_BUTTON, self.do_browse, btn)
        sizerh.Add(btn, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        self.m_cb = wx.CheckBox(self, -1, CHECKBOX_LAUNCH)
        self.m_cb.SetValue(fchdir)
        sizerv.Add(self.m_cb, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        
        btnsizer = wx.StdDialogButtonSizer()
        sizerv.Add(btnsizer, 0, wx.ALIGN_RIGHT | wx.ALL, 5)

        self.m_ok = wx.Button(self, wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.do_ok, self.m_ok)
        self.m_ok.SetDefault()
        btnsizer.AddButton(self.m_ok)

        if command_line == '':
            self.m_ok.Disable()

        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        self.SetSizer(sizerv)
        sizerv.Fit(self)        

    def OnText(self, event):
        if event.GetString() == '':
            self.m_ok.Disable()
        else:
            self.m_ok.Enable()

        event.Skip()        
            
    def do_browse(self, event = None):
        command_line = self.m_entry_commandline.GetValue()
        (_path, filename, args) = rpdb2.split_command_line_path_filename_args(command_line)
        _abs_path = os.path.abspath(_path)

        dlg = wx.FileDialog(self, defaultDir = _abs_path, defaultFile = filename, wildcard = WINPDB_WILDCARD, style = wx.OPEN | wx.CHANGE_DIR)
        r = dlg.ShowModal()
        if r == wx.ID_OK:
            path = dlg.GetPaths()[0]
            abs_path = os.path.abspath(path)
            if (' ' in abs_path):
                abs_path = '"' + abs_path + '"'
        else:
            abs_path = command_line

        dlg.Destroy()
        
        self.m_entry_commandline.SetValue(abs_path)
        
    def do_validate(self):
        command_line = self.m_entry_commandline.GetValue()
        (_path, filename, args)  = rpdb2.split_command_line_path_filename_args(command_line)
        
        try:
            _filename = os.path.join(_path, filename)
            abs_path = rpdb2.FindFile(_filename)

        except IOError:                    
            dlg = wx.MessageDialog(self, MSG_ERROR_FILE_NOT_FOUND, MSG_ERROR_TITLE, wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return False
        
        if ' ' in abs_path:
            command_line = ('"' + abs_path + '" ' + args).strip()
        else:
            command_line = (abs_path + ' ' + args).strip()
            
        self.m_entry_commandline.SetValue(command_line)
        
        return True

    def do_ok(self, event):
        f = self.do_validate()
        if not f:
            return

        event.Skip()
        
    def get_command_line(self):
        return (self.m_entry_commandline.GetValue(), self.m_cb.GetValue())



def StartClient(command_line, fAttach, fchdir, pwd, fAllowUnencrypted, fRemote, host):
    sm = rpdb2.CSessionManager(pwd, fAllowUnencrypted, fRemote, host)
    app = CWinpdbApp(sm, fchdir, command_line, fAttach, fAllowUnencrypted)
    app.MainLoop()



def main():
    if rpdb2.get_version() != "RPDB_2_1_1":
        print STR_ERROR_INTERFACE_COMPATIBILITY % ("RPDB_2_1_1", rpdb2.get_version())
        return
        
    return rpdb2.main(StartClient)



def get_version():
    return WINPDB_VERSION



if __name__=='__main__':
    ret = main()
    sys.exit(ret)

    
    
