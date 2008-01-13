"""
    winpdb_inst.py

    Post install script for winpdb

    Copyright (C) 2005-2008 Nir Aides

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



def PrepareFolder():
    #
    # First remove previous directory if found under user\start\program_files.
    #

    path_user = get_special_folder_path('CSIDL_PROGRAMS')
    dest_dir = os.path.join(path_user, 'Winpdb')

    if os.path.isdir(dest_dir):
        for f in os.listdir(dest_dir):
            p = os.path.join(dest_dir, f)
            os.remove(p)

        os.rmdir(dest_dir)

    #
    # Then, try to install under all_users\start\program_files.
    #

    path_all = get_special_folder_path('CSIDL_COMMON_PROGRAMS')
    dest_dir = os.path.join(path_all, 'Winpdb')

    if os.path.isdir(dest_dir):
        return dest_dir

    try:
        os.mkdir(dest_dir)
        directory_created(dest_dir)

        return dest_dir

    except:
        pass

    #
    # And fall-back to install under user\start\program_files.
    #

    dest_dir = os.path.join(path_user, 'Winpdb')
    os.mkdir(dest_dir)
    directory_created(dest_dir)

    return dest_dir



def InstallWinpdb():
    dest_dir = PrepareFolder()

    homepage_link = os.path.join(dest_dir, 'winpdb-homepage.lnk')
    create_shortcut('http://www.winpdb.org/','Winpdb Homepage', homepage_link)
    file_created(homepage_link)

    winpdb_target = os.path.join(distutils.sysconfig.PREFIX, 'Scripts', 'winpdb_.pyw')
    winpdb_link = os.path.join(dest_dir, 'winpdb.pyw.lnk')
    create_shortcut(winpdb_target,'Winpdb', winpdb_link)
    file_created(winpdb_link)



if os.name == 'nt' and len(sys.argv) == 2 and sys.argv[1] == '-install':
    InstallWinpdb()



