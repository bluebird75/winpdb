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
from unittest import main, TestCase

import rpdb2
import rpdb.exceptions
import rpdb.utils
import rpdb.events

from tests.utils_func_tests import reBpHint, _findBpHintWithContent, Rpdb2Stdout
from tests.test_events import *

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


class TestRpdb2( TestCase ):

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

class TestFindBpHint( TestCase ):
    def testReBpHint(self):
        self.assertEqual( reBpHint.search( 'asldfkj # BP1\n').group(1), 'BP1' )

    def testFindBpHint( self ):
        self.assertEqual( _findBpHintWithContent( ['coucou\n', 'asd # BPXXX\n'] ), { 'BPXXX': 2 } )


class TestRpdb2Stdout( TestCase ):

    def testAttaching( self ):
        rso = Rpdb2Stdout( dispStdout=False )
        self.assertEqual( False, rso.attached )
        rso.write(r'*** Successfully attached to.*\n')
        self.assertEqual( True, rso.attached )
        rso.write(r'*** Detached from script.*\n' )
        self.assertEqual( False, rso.attached )

    def testReAttached( self ):
        self.assertNotEqual( Rpdb2Stdout.reAttached.match( '*** Successfully attached to\n' ), None )

    def testreWaitingOnBp( self ):
        self.assertTrue( Rpdb2Stdout.reWaitingOnBp.match('*** Debuggee is waiting at break point for further commands.') != None )
        self.assertTrue( Rpdb2Stdout.reNotWaitingOnBp.match('*** Debuggee is waiting at break point for further commands.') == None )

        self.assertTrue( Rpdb2Stdout.reWaitingOnBp.match('*** Totoro .') == None )
        self.assertTrue( Rpdb2Stdout.reNotWaitingOnBp.match('*** Totoro .') != None )

if __name__ == '__main__':
    main()