
import sys
from unittest import main, TestCase

import rpdb2
import test_rpdb2

class TestGetPythonExecutable( TestCase ):
    def setUp(self):
        self.__sys_executable = sys.executable
        sys.executable = 'fake_executable'

    def tearDown(self):
        sys.executable = self.__sys_executable

    def testGetPythonExecutable(self):
        self.assertEqual( 'titi', rpdb2.get_python_executable( interpreter='titi' ) )
        self.assertEqual( 'fake_executable', rpdb2.get_python_executable( interpreter='' ) )
        self.assertEqual( 'fake_executable', rpdb2.get_python_executable( interpreter=rpdb2.as_unicode('') ) )
        self.assertEqual( 'fake_executable', rpdb2.get_python_executable( interpreter=None ) )
        self.assertEqual( 'fake_executable', rpdb2.get_python_executable() )

    def testGetPythonExecutableWithPythonW(self):
        sys.executable = 'python30w.exe'
        self.assertEqual( 'python30.exe', rpdb2.get_python_executable( ) )

class TestFindBpHint( TestCase ):
    def testReBpHint(self):
        self.assertEqual( test_rpdb2.reBpHint.search( 'asldfkj # BP1\n').group(1), 'BP1' )

class TestRpdb2( TestCase ):

    def testParseConsoleLaunchBackwardCompatibility( self ):
        # Positive tests
        self.assertEqual( (False, None, 'titi' ), rpdb2.parse_console_launch( '-k titi' ) )

        self.assertEqual( (True, None, 'titi -k' ), rpdb2.parse_console_launch( 'titi -k' ) )

        # Negative tests
        self.assertEqual( '', rpdb2.parse_console_launch( '' )[2] )


    def testParseConsoleLaunchWithInterpreter( self ):
        self.assertEqual( (False, 'toto', 'titi' ), rpdb2.parse_console_launch( '-k -i toto titi' ) )
        self.assertEqual( (False, 'toto', 'titi' ), rpdb2.parse_console_launch( '-i toto -k titi' ) )
        self.assertEqual( (True, '"toto tutu"', 'titi' ), rpdb2.parse_console_launch( '-i "toto tutu" titi' ) )
        self.assertEqual( (True, '"toto tutu"', 'titi' ), rpdb2.parse_console_launch( "-i 'toto tutu' titi" ) )
        self.assertEqual( (True, 'toto', 'tutu titi' ), rpdb2.parse_console_launch( '-i toto tutu titi' ) )


        self.assertEqual( (True, None, 'titi -k -i toto' ), rpdb2.parse_console_launch( 'titi -k -i toto' ) )
        self.assertEqual( (True, None, 'titi -i toto' ), rpdb2.parse_console_launch( 'titi -i toto' ) )


if __name__ == '__main__':
    main()