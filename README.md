[![Build Status](https://travis-ci.org/bluebird75/winpdb.svg?branch=winpdb)](https://travis-ci.org/bluebird75/winpdb)


A fork of Winpdb - A GPL Python Debugger

Modifications by Philippe Fremy (phil at freehackers dot org)
Initial Author: Nir Aides, nir@winpdb.org
Website: http://www.winpdb.org/
Version: 1.4.8


Introduction

    This is a small fork of Winpdb. The official Winpdb development is stale and the fact that Winpdb
    did not work on Python 2.7 prompted me to work on this. I worked on a very minimal changes (see below) 
    that I intend to contribute back if Nir Aides allows it.
    
    Changes from the official Windpb :
    * Fix an a bug that prevented Winpdb to work on Python 2.7
    * Adapt Rpdb2 (the console version of Winpdb) to Python 2.7 - 3.4
    * Add unit-tests and a functional test suite and 
    * Add a Continuous Integration server with travis CI
    * Allow to specify the Python interpreter being used on the command-line and in the launcher dialog of Winpdb
    * Change the default behavior of break-on-exit to fix a recurring crash on Windows when closing abruptly
      the debuggee
    * support drag'n drop of files to display their source

    The rest of this page is from the original Winpdb README

Requirements

    CPython
    Winpdb graphical interface is compatible with CPython 2.3 - 2.7 . 
    Winpdb console and core (rpdb2) is compatible with CPython 2.3 - 3.4 and PyPy. 
    
    Winpdb is NOT compatible with Jython or IronPython. (http://www.python.org/download/)

    wxPython
    To use the Winpdb GUI you need wxPython 2.6.x or later 
    installed. WxPython is not available for Python 3.x , which is why
    you can only use the console Winpdb (rpdb2) with Python 3. When WxPython
    gets ported to Python 3, this fork will support it. See the Project Phoenix
    on WxPython wiki: http://wiki.wxpython.org/ProjectPhoenix .
    
    Most Linux distributions include wxPython as a package called python-wxgtk. 
    Use your distribution’s package manager (e.g. synaptic, aptitude or yum) 
    to find and install it.

    On Windows you need to install the wxPython runtime from 
    http://www.wxpython.org/ (The unicode version is preferred).

	
Installation

    In a console with admin privileges type:

        python setup.py install -f

    On Ubuntu you can type in a normal console:
        
        sudo python setup.py install -f

    Where do the files go? 

    The setup script copies rpdb2.py and winpdb.py modules to the Python 
    site-packages folder. The scripts rpdb2, winpdb are copied to the 
    Python binaries (scripts) folder:

    On Linux this folder is usually /usr/bin and is in the path by default. 

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

    Note that the Python interpreter must be in the PATH for this to work.



Documentation

    Use the -h command-line flag for command-line help.

    Use the RPDB2 console 'help' command for detailed description of debugger 
    commands.

    Online documentation is available at:
    http://www.winpdb.org



Further Development

    Winpdb is open source. If you would like it to develop further you are
    welcome to contribute to development, send feedback or make a donation.

	

