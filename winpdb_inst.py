"""
    winpdb_inst.py

    Post install script for winpdb

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



import distutils.sysconfig
import sys
import os



def InstallWinpdb():
    folders = ["CSIDL_COMMON_PROGRAMS", "CSIDL_PROGRAMS"]

    for folder in folders:
        f = get_special_folder_path(folder)
        dest_dir = os.path.join(f, 'Winpdb')
        if os.path.isdir(dest_dir):
            break

        try:
            os.mkdir(dest_dir)
            directory_created(dest_dir)

        except OSError:
            pass

    homepage_link = os.path.join(dest_dir, 'winpdb-homepage.lnk')
    create_shortcut('http://www.digitalpeers.com/pythondebugger/','Winpdb Homepage', homepage_link)
    file_created(homepage_link)

    winpdb_target = os.path.join(distutils.sysconfig.PREFIX, 'Scripts', 'winpdb_.pyw')
    winpdb_link = os.path.join(dest_dir, 'winpdb.pyw.lnk')
    create_shortcut(winpdb_target,'Winpdb', winpdb_link)
    file_created(winpdb_link)



if os.name == 'nt' and len(sys.argv) == 2 and sys.argv[1] == '-install':
    InstallWinpdb()



