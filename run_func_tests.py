#! /usr/bin/env python

"""
    Functional tests for rpdb2

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


# Python
import unittest
import os, sys

# RPDB2

from tests.utils_func_tests import BaseTestRpdb2, Rpdb2Stdout


class TestRpdb2Stdout( unittest.TestCase ):
    def testReAttached( self ):
        self.assertNotEqual( Rpdb2Stdout.reAttached.match( '*** Successfully attached to\n' ), None )

    def testReDetached( self ):
        self.assertEqual( Rpdb2Stdout.reDetached.match( '*** Successfully attached to\n' ), None )
        self.assertNotEqual( Rpdb2Stdout.reDetached.match( '*** Detached from script.\n' ), None )

    def testreWaitingOnBp( self ):
        self.assertTrue( Rpdb2Stdout.reWaitingOnBp.match('*** Debuggee is waiting at break point for further commands.') != None )
        self.assertTrue( Rpdb2Stdout.reNotWaitingOnBp.match('*** Debuggee is waiting at break point for further commands.') == None )

        self.assertTrue( Rpdb2Stdout.reWaitingOnBp.match('*** Totoro .') == None )
        self.assertTrue( Rpdb2Stdout.reNotWaitingOnBp.match('*** Totoro .') != None )


class TestRpb2( BaseTestRpdb2 ):

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

if __name__ == '__main__':
    unittest.main( argv=[sys.argv[0] + '-v'] + sys.argv[1:] )
