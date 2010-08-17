"""
    setup.py

    Setup script for winpdb

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



LONG_DESC = """Winpdb is a platform independent GPL Python debugger 
with support for multiple threads, namespace modification, 
embedded debugging, encrypted communication 
and is up to 20 times faster than pdb."""



if os.name == 'nt':
    write_file('rpdb2.bat', ['@python -c "import rpdb2;rpdb2.main()" %*'])
    write_file('winpdb.bat', ['@python -c "import winpdb;winpdb.main()" %*'])
    copy_file('winpdb', 'winpdb_.pyw')
    
    _scripts = ['winpdb_inst.py', 'winpdb_.pyw', 'winpdb.bat', 'rpdb2.bat']

else:
    _scripts = ['winpdb', 'rpdb2']



setup(
    name = 'winpdb',
    version = '1.4.8',
    description = 'A platform independent GPL Python debugger.',
    long_description = LONG_DESC,
    author = 'Nir Aides',
    author_email = 'nir@winpdb.org',
    url = 'http://www.winpdb.org/',
    license = 'GNU GPL',
    platforms = ["any"],
    py_modules = ['winpdb', 'rpdb2'],
    scripts = _scripts
    )



