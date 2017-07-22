| |Build Status Linux| |Build status Windows|

*Winpdb Reborn - A GPL Python Debugger, reborn from the unmaintained
Winpdb*

by Nir Aides (initial author) and Philippe Fremy (current maintainer)

Description
===========

Winpdb is a portable (Windows / Linux) graphical debugger for Python. It supports breakpoints, stepping, stack 
inspection, multithreaded debugging and more. It works on both Python 2 and 3.

The original Winpdb was no longer maintained since the release v1.4.8 in
2010. I (Philippe Fremy) am providing a maintained version and new
developments.

Requirements
============

Platform supported:

-  Linux
-  Windows XP and above
-  MacOs is probably working but not tested

To run Winpdb:

-  Any version of CPython above 2.5 included: 2.5, 2.6, 2.7, 3.0 - 3.6
-  WxPython 2.6 or above, and WxPython 4.0

Winpdb is NOT compatible with Jython or IronPython.

Release history
===============

Version 3.0
-----------

-  First official release by Philippe Fremy
-  Add support for python 3 GUI (using WxPython Phoenix)
-  Allow installation of all dependencies with pip
-  Add support for Python 2.7, 3.5 and 3.6
-  Add support for PyPy to Rpdb2
-  Can now specify a different Python interpreter for the program under
   debug, allowing PyPy support
-  Avoid crash on Windows when closing debugger
-  Support drag’n drop of files to display their source
-  Add unit-tests and a functional test suite
-  Add a Continuous Integration server with travis CI

Installation
============

The standard way to install winpdb is with pip, as administrator/root::

    # python -m pip install winpdb-reborn

This will install winpdb and the only dependency WxPython automatically. On Windows,
| shortcuts for the start menu are created. | *Winpdb Reborn* is not packaged yet by any linux distro. If you see a
  winpdb package,
| that’s the old unmaintained winpdb which does not work with python 2.7
  or python 3.

Additional installation methods
-------------------------------

To install from a checkout or from an archive::

    python setup.py install -f

No install mode
---------------

| If you don’t want to install winpdb, you can still try it by calling
  it explicitely with
| your program to debug::

    $ python /the/path/to/winpdb.py my_program.py 

Where do the files go?
----------------------

| The setup script copies rpdb2.py and winpdb.py modules to the Python
| site-packages folder. The scripts rpdb2, winpdb are copied to the
| Python binaries (scripts) folder:

On Linux this folder is usually /usr/bin and is in the path by default.

| On Windows this folder is %PYTHONHOME%\\Scripts and is not in the path
  by
| default.

Usage
=====

If you have installed Winpdb, the simplest way to launch winpdb is::

    $ python -m winpdb my_program.py

or even::

    $ winpdb my_program.py

Find out about the other command-line options with –help .

Documentation
=============

XXX

Use the -h command-line flag for command-line help.

| Use the RPDB2 console ‘help’ command for detailed description of
  debugger
| commands.

| Online documentation is available at:
| http://www.winpdb.org

Community
=========

You can ask questions about Winpdb on the dedicated google group:
https://groups.google.com/forum/#!forum/winpdb

Feel free to raise issues or propose improvements on the Github
repository.

XXX
===

PyPy and lower versions of Python
---------------------------------

| Because the Winpdb core and the console version Rpdb2 work with PyPy
  and Python 3, I have added
| the ability to specify the Python interpreter to use for the program
  being debugged (in the launch dialog of Winpdb, or on the command line
  with -i ). Just run Winpdb with Python 2 and specify the interpreter
  you want!

You can enjoy the beauty of a graphical debugger with the convenience of
latest Python advances.

|stats|


.. |Build Status Linux| image:: https://travis-ci.org/bluebird75/winpdb.svg?branch=winpdb
   :target: https://travis-ci.org/bluebird75/winpdb
.. |Build Status Windows| image:: https://ci.appveyor.com/api/projects/status/l3a98gaeamkgwrl7?svg=true&passingText=Windows%20Build%20passing&failingText=Windows%20Build%20failed
   :target: https://ci.appveyor.com/project/bluebird75/winpdb
.. |stats| image:: https://stats.sylphide-consulting.com/piwik/piwik.php?idsite=38&rec=1
