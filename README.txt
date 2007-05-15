


Winpdb - A GPL Python Debugger

Contact: Nir Aides
Email:   nir@digitalpeers.com
Website: http://sourceforge.net/projects/winpdb/
Version: 1.1.3		 



Requirements

    CPython - Winpdb is compatible with CPython 2.3 or later. Winpdb is NOT 
    compatible with Jython or IronPython. (http://www.python.org/download/)

    wxPython - To use the Winpdb GUI you need wxPython 2.6.x or later 
    installed. You can still use rpdb2 which is the console version of the 
    debugger without wxPython. (http://www.wxpython.org/)


	
Installation

    From a console type:

        python setup.py install -f


    Where do the files go? 

    The setup script copies rpdb2.py and winpdb.py modules to the Python 
    site-packages folder. The scripts rpdb2, winpdb are copied to the 
    Python binaries (scripts) folder:

    On Linux this folder is usually /usr/bin and is in the path by default. 

    On OS X this folder might be
    /System/Library/Frameworks/Python.framework/Versions/2.4/bin  and is not 
    in the path by default.

    On Windows this folder is %PYTHONHOME%\Scripts and is not in the path by
    default.


    Insufficient permissions?

    In the event of insufficient permissions, installation can be avoided 
    completely. To use Winpdb simply launch it from the folder in which it is 
    placed.



Launch Time

    On Linux systems start the debugger from a console with:

        winpdb

    On Windows systems start the debugger with:

        %PYTHONHOME%\Scripts\winpdb



Documentation

    Use the -h command-line flag for command-line help.

    Use the RPDB2 console 'help' command for detailed description of debugger 
    commands.

    Online documentation is available at:
    http://www.digitalpeers.com/pythondebugger/docs.htm



Further Development

    Winpdb is open source. If you would like it to develop further you are
    welcome to contribute to development, send feedback or make a donation.

	

