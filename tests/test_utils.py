import sys
from unittest.case import TestCase

import rpdb.utils
import rpdb2

class TestGetPythonExecutable( TestCase ):
    def setUp(self):
        self.__sys_executable = sys.executable
        sys.executable = 'fake_executable'

    def tearDown(self):
        sys.executable = self.__sys_executable

    def testGetPythonExecutable(self):
        self.assertEqual( 'titi', rpdb.utils.get_python_executable( interpreter='titi' ) )
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