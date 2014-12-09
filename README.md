[![Build Status](https://travis-ci.org/bluebird75/winpdb.svg?branch=winpdb)](https://travis-ci.org/bluebird75/winpdb)
[![Build status](https://ci.appveyor.com/api/projects/status/l3a98gaeamkgwrl7?svg=true)](https://ci.appveyor.com/project/bluebird75/winpdb)


*A fork of Winpdb - A GPL Python Debugger*

* Modifications by Philippe Fremy (phil at freehackers dot org)
* Initial Author: Nir Aides, nir at winpdb dot org
* Website: http://www.winpdb.org/
* Based on version: 1.4.8


## Introduction

Winpdb is a portable (Windows / Linux) graphical debugger for Python. It supports breakpoints, stack inspection, multithreaded debugging and more.

This is a small fork of Winpdb. I started it when realising the the official Winpdb had a blocking bug
on the most recent Python 2.7 . I initially worked on fixing  Python 2.7 support, then fixed a few other minor
bugs and added some small useful features. I intend to contribute this back if Nir Aides allows it.
    
Changes from the official Windpb :
* Fix support for Python 2.7 for Winpdb
* Support for Python 2.7 - 3.4 for Rpdb2, the console version of Winpdb.
* Support for PyPy for Rpdb2
* Allow to specify a different Python interpreter for the debuggee
* Avoid crash on Windows when closing debugger
* support drag'n drop of files to display their source
* Add unit-tests and a functional test suite 
* Add a Continuous Integration server with travis CI
  
The changes allow Winpdb to be usable with the most recent Python versions.

## PyPy, Python 3, Winpdb and WxPython

Winpdb uses WxPython for its graphical interface. However, WxPython is not yet available for Python 3: it is impossible to run the graphical interface of Winpdb on Python 3. The same restrictions apply to PyPy which does
not support WxPython.

The Python 3 problem will be fixed when WxPython finally supports Python 3 (see Phoenix project: http://wiki.wxpython.org/ProjectPhoenix ) but you can already debug your Python 3 and PyPy programs.

Because the Winpdb core and the console version Rpdb2 work with PyPy and Python 3, I have added
the ability to specify the Python interpreter to use for the program being debugged (in the launch dialog of Winpdb, or on the command line with -i ). Just run Winpdb with Python 2 and specify the interpreter you want!

You can enjoy the beauty of a graphical debugger with the convenience of latest Python advances.


## Requirements

Platform supported:
* Linux
* Windows XP and above
* MacOs is probably working but not tested

To run the graphical interface Winpdb:
* CPython 2.5 - 2.7
* WxPython 2.6 and above

To debug a program:
* CPython 2.5 - 2.7 or CPython 3.0 - 3.4 or PyPy

Winpdb is NOT compatible with Jython or IronPython.

## Installation

Most Linux distributions include wxPython as a package called python-wxgtk. 
Use your distribution’s package manager (e.g. synaptic, aptitude or yum) 
to find and install it.

On Windows you need to install the wxPython runtime from 
http://www.wxpython.org/ (The unicode version is preferred).

You can run Winpdb without installing it by just downloading it :

    python /path/to/winpdb/directory/winpdb.py program_to_debug.py

#### Installation by hand

In a console with admin privileges type:

    python setup.py install -f

On Ubuntu you can type in a normal console:
    
    sudo python setup.py install -f

**Where do the files go?**

The setup script copies rpdb2.py and winpdb.py modules to the Python 
site-packages folder. The scripts rpdb2, winpdb are copied to the 
Python binaries (scripts) folder:

On Linux this folder is usually /usr/bin and is in the path by default. 

On Windows this folder is %PYTHONHOME%\Scripts and is not in the path by
default.

**Insufficient permissions?**

In the event of insufficient permissions, installation can be avoided 
completely. To use Winpdb simply launch it from the folder in which it is 
placed.

## Launch Time

The simplest way to launch winpdb is:

    python -m winpdb
    
To launch the console debugger:

    python -m rpdb2


## Documentation

Use the -h command-line flag for command-line help.

Use the RPDB2 console 'help' command for detailed description of debugger 
commands.

Online documentation is available at:
http://www.winpdb.org


## Community

You can ask questions about Winpdb on the dedicated google group: https://groups.google.com/forum/#!forum/winpdb

## Further Development

Winpdb is open source. If you would like it to develop further you are
welcome to contribute to development, send feedback or make a donation.

The official repository of Winpdb (un-)maintained by Nir Aides is : https://code.google.com/p/winpdb/

Else, you can just open bugs and contribute on Github.

	



[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/bluebird75/winpdb/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

