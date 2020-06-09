

# Python
import unittest
import os

# RPDB2
from tests.utils_func_tests import BaseTestRpdb2, Rpdb2Stdout, dbg


class TestRpdb2( BaseTestRpdb2 ):

    def testGo( self ):
        self.startPdb2()
        self.attach()
        self.goAndExit()

        assert os.path.exists( 'tests/f1' )
        assert os.path.exists( 'tests/done' )
        assert os.path.exists( 'tests/atexit' )

    def testBp( self ):
        self.startPdb2()
        self.attach()
        self.breakp( 'f1' )
        self.breakp( self.bp1Line )
        self.goAndWaitOnBp() # break during definition of f1
        self.goAndWaitOnBp() # break during call of f1
        assert os.path.exists( 'tests/start' )
        assert not os.path.exists( 'tests/f1' )
        self.goAndWaitOnBp() # break after call of f2
        assert os.path.exists( 'tests/f1' )
        assert os.path.exists( 'tests/f2' )
        self.goAndExit() # run until the end
        assert os.path.exists('tests/done')
        assert os.path.exists('tests/atexit')

    def testStack( self ):
        self.startPdb2()
        self.attach()
        self.breakp( 'f4' )
        self.goAndWaitOnBp() # break during definition of f4
        self.goAndWaitOnBp() # break during call of f4

        stack_list = self.stack()
        self.assertIn( 'debugme.py', stack_list)
        self.assertIn( ' f4', stack_list)
        self.assertIn( ' f1', stack_list)
        self.assertIn( ' >     0', stack_list)

        self.command('down')
        stack_list = self.stack()
        self.assertIn( ' >     1', stack_list)

        self.command('up')
        stack_list = self.stack()
        self.assertIn( ' >     0', stack_list)




# Disable this long and tedious test
class XXXTestBreakOnExit(BaseTestRpdb2):

    def testChangingBreakonexit( self ):
        self.startPdb2()
        self.attach()
        self.getBreakonexit()
        self.assertEqual( self.rpdb2Stdout.breakonexit, False )
        self.setBreakonexit( True )
        self.assertEqual( self.rpdb2Stdout.breakonexit, True )
        self.setBreakonexit( False )
        self.assertEqual( self.rpdb2Stdout.breakonexit, False )

    # disable for now, this test is not working anymore
    def XXXtestRunWithBreakonexit( self ):
        self.startPdb2()
        self.assertEqual( self.rpdb2Stdout.waitingOnBp, False )
        self.attach()
        self.setBreakonexit( True )
        self.goAndWaitOnBp()
        self.assertEqual( self.rpdb2Stdout.attached, True )
        self.assertEqual( self.rpdb2Stdout.waitingOnBp, True )
        self.goAndExit()

    def testRunWithoutBreakonexit( self ):
        self.startPdb2()
        self.attach()
        self.setBreakonexit( False )
        self.goAndExit()
        self.assertEqual( self.rpdb2Stdout.attached, False )
