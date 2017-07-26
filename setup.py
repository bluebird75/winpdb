"""
    setup.py

    Setup script for winpdb

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
    59 Temple Place, Suite 330, Boston, MA 02111-1307 USA    
"""



from distutils.file_util import write_file
from distutils.file_util import copy_file
from distutils.core import setup

import os



LONG_DESC = '''*Winpdb Reborn* is a platform independent lightweight 
standalone graphical debugger for Python 2 and 3. It supports
conditional breakpoints, multi-threaded debugging, smart 
handling of forks, remote debugging and more.
'''


if os.name == 'nt':
    write_file('rpdb2.bat', ['@python -c "import rpdb2;rpdb2.main()" %*'])
    write_file('winpdb.bat', ['@python -c "import winpdb;winpdb.main()" %*'])
    copy_file('winpdb', 'winpdb_.pyw')
    
    _scripts = ['winpdb_inst.py', 'winpdb_.pyw', 'winpdb.bat', 'rpdb2.bat']

else:
    _scripts = ['winpdb', 'rpdb2']



setup(
    name = 'winpdb-reborn',
    version = '1.5.0',
    description = 'A platform independent GPL Python debugger.',
    long_description = LONG_DESC,
    author = 'Philippe Fremy, Nir Aides',
    author_email = 'phil.fremy@free.fr',
    url = 'https://github.com/bluebird75/winpdb',
    license = 'GNU GPL',
    platforms = ["any"],
    py_modules = ['winpdb', 'rpdb2'],
    scripts = _scripts
    )



