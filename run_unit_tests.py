
import sys
from unittest import main, TestCase

import rpdb2

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


if __name__ == '__main__':
	main()