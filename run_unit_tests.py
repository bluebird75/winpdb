
import sys
from unittest import main, TestCase

import rpdb2
import run_func_tests

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

class TestCEventDispatcherRecord( TestCase ):

    def testNoMatchForEmptyCallback( self ):
        er = rpdb2.CEventDispatcherRecord( None, {}, False)
        self.assertEquals( False, er.is_match( rpdb2.CEventNull() ) )

    def testMatchNormal( self ):
        er = rpdb2.CEventDispatcherRecord( None, { rpdb2.CEventExit: {} }, False)
        self.assertEquals( False, er.is_match( rpdb2.CEventNull() ) )
        self.assertEquals( True, er.is_match( rpdb2.CEventExit() ) )

    def testMatchNormalWithArgs( self ):
        er = rpdb2.CEventDispatcherRecord( None, { rpdb2.CEventState: {} }, False)
        self.assertEquals( True, er.is_match( rpdb2.CEventState( rpdb2.STATE_BROKEN ) ) )

    def testMatchExclude( self ):
        er = rpdb2.CEventDispatcherRecord( None, { rpdb2.CEventState: { rpdb2.EVENT_EXCLUDE: [rpdb2.STATE_BROKEN, rpdb2.STATE_ANALYZE] } }, False)
        self.assertEquals( False, er.is_match( rpdb2.CEventState( rpdb2.STATE_BROKEN ) ) )
        self.assertEquals( False, er.is_match( rpdb2.CEventState( rpdb2.STATE_ANALYZE ) ) )
        self.assertEquals( True, er.is_match( rpdb2.CEventState( rpdb2.STATE_RUNNING ) ) )

    def testMatchInclude( self ):
        er = rpdb2.CEventDispatcherRecord( None, {rpdb2.CEventState: { 
            rpdb2.EVENT_INCLUDE: [rpdb2.STATE_BROKEN, rpdb2.STATE_ANALYZE],
            } } , False)
        self.assertEquals( True, er.is_match( rpdb2.CEventState( rpdb2.STATE_BROKEN ) ) )
        self.assertEquals( True, er.is_match( rpdb2.CEventState( rpdb2.STATE_ANALYZE ) ) )
        self.assertEquals( False, er.is_match( rpdb2.CEventState( rpdb2.STATE_RUNNING ) ) )

    def testMatchIncludeExclude( self ):
        er = rpdb2.CEventDispatcherRecord( None, {rpdb2.CEventState: { 
            rpdb2.EVENT_INCLUDE: [rpdb2.STATE_BROKEN, rpdb2.STATE_ANALYZE],
            rpdb2.EVENT_EXCLUDE: [rpdb2.STATE_BROKEN],
            } } , False)
        self.assertEquals( True, er.is_match( rpdb2.CEventState( rpdb2.STATE_ANALYZE ) ) )
        self.assertEquals( False, er.is_match( rpdb2.CEventState( rpdb2.STATE_BROKEN ) ) )


class TestCEventDispatcher( TestCase ):

    def setUp( self ):
        self.m_callbackTrace = []

    def callback( self, event ):
        self.m_callbackTrace.append( event )

    def testEventCallsCallback( self ):
        evd = rpdb2.CEventDispatcher()
        evd.register_callback( self.callback, { rpdb2.CEventNull: {} }, False )
        ev1 = rpdb2.CEventNull() 
        evd.fire_event( ev1 )
        self.assertEquals( self.m_callbackTrace, [ ev1 ] )

        ev2 = rpdb2.CEventExit()
        evd.fire_event( ev2 )
        self.assertEquals( self.m_callbackTrace, [ ev1 ] )

    def testCallbackRemoval( self ):
        evd = rpdb2.CEventDispatcher()
        evd.register_callback( self.callback, { rpdb2.CEventNull: {} }, False )
        ev1 = rpdb2.CEventNull() 
        evd.fire_event( ev1 )
        self.assertEquals( self.m_callbackTrace, [ ev1 ] )

        evd.remove_callback( self.callback )
        ev2 = rpdb2.CEventNull() 
        evd.fire_event( ev2 )
        self.assertEquals( self.m_callbackTrace, [ ev1 ] )

    def testCallbackDoubleRemoval( self ):
        evd = rpdb2.CEventDispatcher()
        # no exception raised evcen if not registed
        evd.remove_callback( self.callback )

        evd.register_callback( self.callback, { rpdb2.CEventNull: {} }, False )
        evd.remove_callback( self.callback )

        # no exception raised evcen if not registed
        evd.remove_callback( self.callback )

    def testEventCallsCallbackMultipleUse( self ):
        evd = rpdb2.CEventDispatcher()
        evd.register_callback( self.callback, { rpdb2.CEventNull: {} }, False )

        ev1 = rpdb2.CEventNull() 
        evd.fire_event( ev1 )
        self.assertEquals( self.m_callbackTrace, [ ev1 ] )

        ev2 = rpdb2.CEventNull()
        evd.fire_event( ev2 )
        self.assertEquals( self.m_callbackTrace, [ ev1, ev2 ] )

    def testEventCallsCallbackSingleUse( self ):
        evd = rpdb2.CEventDispatcher()
        evd.register_callback( self.callback, { rpdb2.CEventNull: {} }, True )

        ev1 = rpdb2.CEventNull() 
        evd.fire_event( ev1 )
        self.assertEquals( self.m_callbackTrace, [ ev1 ] )
        
        ev2 = rpdb2.CEventNull()
        evd.fire_event( ev2 )
        self.assertEquals( self.m_callbackTrace, [ ev1 ] )

    def testChainedDispatcher( self ):
        evd_first = rpdb2.CEventDispatcher()
        evd_second = rpdb2.CEventDispatcher( evd_first )

        secondCallbackTrace = []
        def secondCallback( ev ):
            secondCallbackTrace.append( ev )

        self.assertEquals( secondCallbackTrace, [] )
        self.assertEquals( self.m_callbackTrace, [] )

        evd_first.register_callback( self.callback, { rpdb2.CEventNull: {} }, False)
        evd_second.register_callback( secondCallback, { rpdb2.CEventNull: {} }, False)

        # Event on first dispatcher
        ev1 = rpdb2.CEventNull() 
        evd_first.fire_event( ev1 )
        self.assertEquals( self.m_callbackTrace, [ ev1 ] )
        self.assertEquals( secondCallbackTrace, [ ev1 ] )

        # Event on second dispatcher 
        ev2 = rpdb2.CEventNull() 
        evd_second.fire_event( ev2 )
        self.assertEquals( self.m_callbackTrace, [ ev1 ] )
        self.assertEquals( secondCallbackTrace, [ ev1, ev2 ] )

    def testChainedDispatcherChainOverride( self ):
        evd_first = rpdb2.CEventDispatcher()
        evd_second = rpdb2.CEventDispatcher( evd_first )

        secondCallbackTrace = []
        def secondCallback( ev ):
            secondCallbackTrace.append( ev )

        self.assertEquals( secondCallbackTrace, [] )
        self.assertEquals( self.m_callbackTrace, [] )

        evd_second.register_chain_override( { rpdb2.CEventNull: {} } )
        evd_first.register_callback( self.callback, { rpdb2.CEventNull: {} }, False)
        evd_second.register_callback( secondCallback, { rpdb2.CEventNull: {} }, False)

        # Event on first dispatcher
        ev1 = rpdb2.CEventNull() 
        evd_first.fire_event( ev1 )
        self.assertEquals( self.m_callbackTrace, [ ev1 ] )
        self.assertEquals( secondCallbackTrace, [] )

        # Event on second dispatcher 
        ev2 = rpdb2.CEventNull() 
        evd_second.fire_event( ev2 )
        self.assertEquals( self.m_callbackTrace, [ ev1 ] )
        self.assertEquals( secondCallbackTrace, [ ev2 ] )


class TestCEventQueue( TestCase ):
    def testGetEventIndex( self ):
        evd = rpdb2.CEventDispatcher()
        evq = rpdb2.CEventQueue( evd, 5 )
        evq.register_event_types( { rpdb2.CEventNull : {} } )

        ev1 = rpdb2.CEventNull() 
        evd.fire_event( ev1 )
        self.assertEquals( 1, evq.get_event_index() )
        ev2 = rpdb2.CEventNull() 
        evd.fire_event( ev2 )
        self.assertEquals( 2, evq.get_event_index() )

    def testWaitForEvent( self ):
        evd = rpdb2.CEventDispatcher()
        evq = rpdb2.CEventQueue( evd, 5 )
        evq.register_event_types( { rpdb2.CEventNull : {} } )

        ev1 = rpdb2.CEventNull() 
        evd.fire_event( ev1 )
        ev2 = rpdb2.CEventNull() 
        evd.fire_event( ev2 )

        new_index, sub_events = evq.wait_for_event( 0.1, 0 )
        self.assertEquals( 2, new_index )
        self.assertEquals( [ev1, ev2], sub_events )

        new_index, sub_events = evq.wait_for_event( 0.1, 1 )
        self.assertEquals( 2, new_index )
        self.assertEquals( [ ev2 ], sub_events )

        new_index, sub_events = evq.wait_for_event( 0.1, 2 )
        self.assertEquals( 2, new_index )
        self.assertEquals( [], sub_events )

        new_index, sub_events = evq.wait_for_event( 0.1, 3 )
        self.assertEquals( 2, new_index )
        self.assertEquals( [], sub_events )

    def testEventQueueOverflow(self):
        evd = rpdb2.CEventDispatcher()
        evq = rpdb2.CEventQueue( evd, 3 )
        evq.register_event_types( { rpdb2.CEventNull : {} } )

        ev1 = rpdb2.CEventNull() 
        ev2 = rpdb2.CEventNull() 
        ev3 = rpdb2.CEventNull() 
        ev4 = rpdb2.CEventNull() 
        evd.fire_event( ev1 )
        evd.fire_event( ev2 )

        new_index, sub_events = evq.wait_for_event( 0.1, 0 )
        self.assertEquals( 2, new_index )
        self.assertEquals( [ev1, ev2], sub_events )

        evd.fire_event( ev3 )
        new_index, sub_events = evq.wait_for_event( 0.1, 2 )
        self.assertEquals( 3, new_index )
        self.assertEquals( [ev3], sub_events )

        new_index, sub_events = evq.wait_for_event( 0.1, 0 )
        self.assertEquals( 3, new_index )
        self.assertEquals( [ev1, ev2, ev3], sub_events )

        evd.fire_event( ev4 )
        new_index, sub_events = evq.wait_for_event( 0.1, 3 )
        self.assertEquals( 4, new_index )
        self.assertEquals( [ev4], sub_events )

        new_index, sub_events = evq.wait_for_event( 0.1, 0 )
        self.assertEquals( 4, new_index )
        self.assertEquals( [ev2, ev3, ev4], sub_events )


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

#
# Tests related to Rpdb2 functional tests
#

class TestFindBpHint( TestCase ):
    def testReBpHint(self):
        self.assertEqual( run_func_tests.reBpHint.search( 'asldfkj # BP1\n').group(1), 'BP1' )


class TestRpdb2Stdout( TestCase ):

    def testAttaching( self ):
        rso = run_func_tests.Rpdb2Stdout( dispStdout=False )
        self.assertEquals( False, rso.attached )
        rso.write(r'*** Successfully attached to.*\n')
        self.assertEquals( True, rso.attached )
        rso.write(r'*** Detached from script.*\n' )

if __name__ == '__main__':
    main()