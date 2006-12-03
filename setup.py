"""
    setup.py

    Setup script for winpdb

    Copyright (C) 2005 Nir Aides

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



from distutils.core import setup



LONG_DESC = """Winpdb is an advanced Python debugger with smart breakpoints, 
thread support, modifiable namespace, and secure connections."""



setup(
    name = 'winpdb',
    version = '1.0.6',
    description = 'An advanced Python debugger.',
    long_description = LONG_DESC,
    author = 'Nir Aides',
    author_email = 'nir@digitalpeers.com',
    url = 'http://www.digitalpeers.com/pythondebugger/',
    py_modules = ['winpdb', 'rpdb2'],
    scripts = ['_winpdb.py', '_rpdb2.py']
    )



