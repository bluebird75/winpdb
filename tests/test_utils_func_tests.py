from unittest.case import TestCase

from tests.utils_func_tests import reBpHint, _findBpHintWithContent, Rpdb2Stdout


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