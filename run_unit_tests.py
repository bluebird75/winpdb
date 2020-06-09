"""
    Unit tests for rpdb2

    Copyright (C) 2013-2017 Philippe Fremy

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
    51 Franklin Street, Fifth Floor, Boston, MA 02111-1307 USA
"""

import sys
from unittest import main

import rpdb.exceptions
import rpdb.utils
import rpdb.events

from tests.test_events import *
from tests.test_utils_func_tests import *

class TestGetPythonExecutable( TestCase ):
    def setUp(self):
        self.__sys_executable = sys.executable
        sys.executable = 'fake_executable'

    def tearDown(self):
        sys.executable = self.__sys_executable

    def testGetPythonExecutable(self):
        self.assertEqual( 'titi', rpdb2.get_python_executable( interpreter='titi' ) )
        self.assertEqual( 'fake_executable', rpdb.utils.get_python_executable( interpreter='' ) )
        self.assertEqual( 'fake_executable', rpdb.utils.get_python_executable( interpreter=rpdb.utils.as_unicode('') ) )
        self.assertEqual( 'fake_executable', rpdb.utils.get_python_executable( interpreter=None ) )
        self.assertEqual( 'fake_executable', rpdb.utils.get_python_executable() )

    def testGetPythonExecutableWithPythonW(self):
        sys.executable = 'python30w.exe'
        self.assertEqual( 'python30.exe', rpdb.utils.get_python_executable( ) )


class TestParseConsoleLaunch( TestCase ):

    def testParseConsoleLaunchBackwardCompatibility( self ):
        # Positive tests
        fchdir, interpreter, arg = rpdb2.parse_console_launch( '-k titi' )
        self.assertEqual( (False, 'titi' ), (fchdir, arg) )
        self.assertTrue( interpreter != None )

        fchdir, interpreter, arg = rpdb2.parse_console_launch( 'titi -k' )
        self.assertEqual( (True, 'titi -k' ), (fchdir, arg) )

        # Negative tests
        self.assertEqual( '', rpdb2.parse_console_launch( '' )[2] )


    def testParseConsoleLaunchWithInterpreter( self ):
        self.assertEqual( (False, 'toto', 'titi' ), rpdb2.parse_console_launch( '-k -i toto titi' ) )
        self.assertEqual( (False, 'toto', 'titi' ), rpdb2.parse_console_launch( '-i toto -k titi' ) )
        self.assertEqual( (True, '"toto tutu"', 'titi' ), rpdb2.parse_console_launch( '-i "toto tutu" titi' ) )
        self.assertEqual( (True, '"toto tutu"', 'titi' ), rpdb2.parse_console_launch( "-i 'toto tutu' titi" ) )
        self.assertEqual( (True, 'toto', 'tutu titi' ), rpdb2.parse_console_launch( '-i toto tutu titi' ) )


        fchdir, interpreter, arg = rpdb2.parse_console_launch( 'titi -k -i toto' )
        self.assertEqual( (True, 'titi -k -i toto' ), (fchdir, arg) )
        fchdir, interpreter, arg = rpdb2.parse_console_launch( 'titi -i toto' )
        self.assertEqual( (True, 'titi -i toto' ), (fchdir, arg) )

#
# Tests related to Rpdb2 functional tests
#


if __name__ == '__main__':
    main()