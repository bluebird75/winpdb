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
import run_func_tests

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

class TestCEventDispatcherRecord( TestCase ):

    def testNoMatchForEmptyCallback( self ):
        er = rpdb.events.CEventDispatcherRecord( None, {}, False)
        self.assertEqual( False, er.is_match( rpdb.events.CEventNull() ) )

    def testMatchNormal( self ):
        er = rpdb.events.CEventDispatcherRecord( None, { rpdb.events.CEventExit: {} }, False)
        self.assertEqual( False, er.is_match( rpdb.events.CEventNull() ) )
        self.assertEqual( True, er.is_match( rpdb.events.CEventExit() ) )

    def testMatchNormalWithArgs( self ):
        er = rpdb.events.CEventDispatcherRecord( None, { rpdb.events.CEventState: {} }, False)
        self.assertEqual( True, er.is_match( rpdb.events.CEventState( rpdb.const.STATE_BROKEN ) ) )

    def testMatchExclude( self ):
        er = rpdb.events.CEventDispatcherRecord( None, { 
            rpdb.events.CEventState: { rpdb.events.EVENT_EXCLUDE: [rpdb.const.STATE_BROKEN, rpdb.const.STATE_ANALYZE] } 
                                                        }, False)
        self.assertEqual( False, er.is_match( rpdb.events.CEventState( rpdb.const.STATE_BROKEN ) ) )
        self.assertEqual( False, er.is_match( rpdb.events.CEventState( rpdb.const.STATE_ANALYZE ) ) )
        self.assertEqual( True, er.is_match( rpdb.events.CEventState( rpdb.const.STATE_RUNNING ) ) )

    def testMatchInclude( self ):
        er = rpdb.events.CEventDispatcherRecord( None, {rpdb.events.CEventState: { 
            rpdb.events.EVENT_INCLUDE: [rpdb.const.STATE_BROKEN, rpdb.const.STATE_ANALYZE],
            } } , False)
        self.assertEqual( True, er.is_match( rpdb.events.CEventState( rpdb.const.STATE_BROKEN ) ) )
        self.assertEqual( True, er.is_match( rpdb.events.CEventState( rpdb.const.STATE_ANALYZE ) ) )
        self.assertEqual( False, er.is_match( rpdb.events.CEventState( rpdb.const.STATE_RUNNING ) ) )

    def testMatchIncludeExclude( self ):
        er = rpdb.events.CEventDispatcherRecord( None, {rpdb.events.CEventState: { 
            rpdb.events.EVENT_INCLUDE: [rpdb.const.STATE_BROKEN, rpdb.const.STATE_ANALYZE],
            rpdb.events.EVENT_EXCLUDE: [rpdb.const.STATE_BROKEN],
            } } , False)
        self.assertEqual( True, er.is_match( rpdb.events.CEventState( rpdb.const.STATE_ANALYZE ) ) )
        self.assertEqual( False, er.is_match( rpdb.events.CEventState( rpdb.const.STATE_BROKEN ) ) )


class TestCEventDispatcher( TestCase ):

    def setUp( self ):
        self.m_callbackTrace = []

    def callback( self, event ):
        self.m_callbackTrace.append( event )

    def testEventCallsCallback( self ):
        evd = rpdb.events.CEventDispatcher()
        evd.register_callback( self.callback, { rpdb.events.CEventNull: {} }, False )
        ev1 = rpdb.events.CEventNull() 
        evd.fire_event( ev1 )
        self.assertEqual( self.m_callbackTrace, [ ev1 ] )

        ev2 = rpdb.events.CEventExit()
        evd.fire_event( ev2 )
        self.assertEqual( self.m_callbackTrace, [ ev1 ] )

    def testCallbackRemoval( self ):
        evd = rpdb.events.CEventDispatcher()
        evd.register_callback( self.callback, { rpdb.events.CEventNull: {} }, False )
        ev1 = rpdb.events.CEventNull() 
        evd.fire_event( ev1 )
        self.assertEqual( self.m_callbackTrace, [ ev1 ] )

        evd.remove_callback( self.callback )
        ev2 = rpdb.events.CEventNull() 
        evd.fire_event( ev2 )
        self.assertEqual( self.m_callbackTrace, [ ev1 ] )

    def testCallbackDoubleRemoval( self ):
        evd = rpdb.events.CEventDispatcher()
        # no exception raised evcen if not registed
        evd.remove_callback( self.callback )

        evd.register_callback( self.callback, { rpdb.events.CEventNull: {} }, False )
        evd.remove_callback( self.callback )

        # no exception raised evcen if not registed
        evd.remove_callback( self.callback )

    def testEventCallsCallbackMultipleUse( self ):
        evd = rpdb.events.CEventDispatcher()
        evd.register_callback( self.callback, { rpdb.events.CEventNull: {} }, False )

        ev1 = rpdb.events.CEventNull() 
        evd.fire_event( ev1 )
        self.assertEqual( self.m_callbackTrace, [ ev1 ] )

        ev2 = rpdb.events.CEventNull()
        evd.fire_event( ev2 )
        self.assertEqual( self.m_callbackTrace, [ ev1, ev2 ] )

    def testEventCallsCallbackSingleUse( self ):
        evd = rpdb.events.CEventDispatcher()
        evd.register_callback( self.callback, { rpdb.events.CEventNull: {} }, True )

        ev1 = rpdb.events.CEventNull() 
        evd.fire_event( ev1 )
        self.assertEqual( self.m_callbackTrace, [ ev1 ] )
        
        ev2 = rpdb.events.CEventNull()
        evd.fire_event( ev2 )
        self.assertEqual( self.m_callbackTrace, [ ev1 ] )

    def testChainedDispatcher( self ):
        evd_first = rpdb.events.CEventDispatcher()
        evd_second = rpdb.events.CEventDispatcher( evd_first )

        secondCallbackTrace = []
        def secondCallback( ev ):
            secondCallbackTrace.append( ev )

        self.assertEqual( secondCallbackTrace, [] )
        self.assertEqual( self.m_callbackTrace, [] )

        evd_first.register_callback( self.callback, { rpdb.events.CEventNull: {} }, False)
        evd_second.register_callback( secondCallback, { rpdb.events.CEventNull: {} }, False)

        # Event on first dispatcher
        ev1 = rpdb.events.CEventNull() 
        evd_first.fire_event( ev1 )
        self.assertEqual( self.m_callbackTrace, [ ev1 ] )
        self.assertEqual( secondCallbackTrace, [ ev1 ] )

        # Event on second dispatcher 
        ev2 = rpdb.events.CEventNull() 
        evd_second.fire_event( ev2 )
        self.assertEqual( self.m_callbackTrace, [ ev1 ] )
        self.assertEqual( secondCallbackTrace, [ ev1, ev2 ] )

    def testChainedDispatcherChainOverride( self ):
        evd_first = rpdb.events.CEventDispatcher()
        evd_second = rpdb.events.CEventDispatcher( evd_first )

        secondCallbackTrace = []
        def secondCallback( ev ):
            secondCallbackTrace.append( ev )

        self.assertEqual( secondCallbackTrace, [] )
        self.assertEqual( self.m_callbackTrace, [] )

        evd_second.register_chain_override( { rpdb.events.CEventNull: {} } )
        evd_first.register_callback( self.callback, { rpdb.events.CEventNull: {} }, False)
        evd_second.register_callback( secondCallback, { rpdb.events.CEventNull: {} }, False)

        # Event on first dispatcher
        ev1 = rpdb.events.CEventNull() 
        evd_first.fire_event( ev1 )
        self.assertEqual( self.m_callbackTrace, [ ev1 ] )
        self.assertEqual( secondCallbackTrace, [] )

        # Event on second dispatcher 
        ev2 = rpdb.events.CEventNull() 
        evd_second.fire_event( ev2 )
        self.assertEqual( self.m_callbackTrace, [ ev1 ] )
        self.assertEqual( secondCallbackTrace, [ ev2 ] )


class TestCEventQueue( TestCase ):
    def testGetEventIndex( self ):
        evd = rpdb.events.CEventDispatcher()
        evq = rpdb2.CEventQueue( evd, 5 )
        evq.register_event_types( { rpdb.events.CEventNull : {} } )

        ev1 = rpdb.events.CEventNull() 
        evd.fire_event( ev1 )
        self.assertEqual( 1, evq.get_event_index() )
        ev2 = rpdb.events.CEventNull() 
        evd.fire_event( ev2 )
        self.assertEqual( 2, evq.get_event_index() )

    def testWaitForEvent( self ):
        evd = rpdb.events.CEventDispatcher()
        evq = rpdb2.CEventQueue( evd, 5 )
        evq.register_event_types( { rpdb.events.CEventNull : {} } )

        ev1 = rpdb.events.CEventNull() 
        evd.fire_event( ev1 )
        ev2 = rpdb.events.CEventNull() 
        evd.fire_event( ev2 )

        new_index, sub_events = evq.wait_for_event( 0.1, 0 )
        self.assertEqual( 2, new_index )
        self.assertEqual( [ev1, ev2], sub_events )

        new_index, sub_events = evq.wait_for_event( 0.1, 1 )
        self.assertEqual( 2, new_index )
        self.assertEqual( [ ev2 ], sub_events )

        new_index, sub_events = evq.wait_for_event( 0.1, 2 )
        self.assertEqual( 2, new_index )
        self.assertEqual( [], sub_events )

        new_index, sub_events = evq.wait_for_event( 0.1, 3 )
        self.assertEqual( 2, new_index )
        self.assertEqual( [], sub_events )

    def testEventQueueOverflow(self):
        evd = rpdb.events.CEventDispatcher()
        evq = rpdb2.CEventQueue( evd, 3 )
        evq.register_event_types( { rpdb.events.CEventNull : {} } )

        ev1 = rpdb.events.CEventNull() 
        ev2 = rpdb.events.CEventNull() 
        ev3 = rpdb.events.CEventNull() 
        ev4 = rpdb.events.CEventNull() 
        evd.fire_event( ev1 )
        evd.fire_event( ev2 )

        new_index, sub_events = evq.wait_for_event( 0.1, 0 )
        self.assertEqual( 2, new_index )
        self.assertEqual( [ev1, ev2], sub_events )

        evd.fire_event( ev3 )
        new_index, sub_events = evq.wait_for_event( 0.1, 2 )
        self.assertEqual( 3, new_index )
        self.assertEqual( [ev3], sub_events )

        new_index, sub_events = evq.wait_for_event( 0.1, 0 )
        self.assertEqual( 3, new_index )
        self.assertEqual( [ev1, ev2, ev3], sub_events )

        evd.fire_event( ev4 )
        new_index, sub_events = evq.wait_for_event( 0.1, 3 )
        self.assertEqual( 4, new_index )
        self.assertEqual( [ev4], sub_events )

        new_index, sub_events = evq.wait_for_event( 0.1, 0 )
        self.assertEqual( 4, new_index )
        self.assertEqual( [ev2, ev3, ev4], sub_events )


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
        self.assertEqual( run_func_tests.reBpHint.search( 'asldfkj # BP1\n').group(1), 'BP1' )

    def testFindBpHint( self ):
        self.assertEqual( run_func_tests._findBpHintWithContent( ['coucou\n', 'asd # BPXXX\n'] ), { 'BPXXX': 2 } )


class TestRpdb2Stdout( TestCase ):

    def testAttaching( self ):
        rso = run_func_tests.Rpdb2Stdout( dispStdout=False )
        self.assertEqual( False, rso.attached )
        rso.write(r'*** Successfully attached to.*\n')
        self.assertEqual( True, rso.attached )
        rso.write(r'*** Detached from script.*\n' )

    def testReAttached( self ):
        self.assertNotEqual( run_func_tests.Rpdb2Stdout.reAttached.match( '*** Successfully attached to\n' ), None )

    def testreWaitingOnBp( self ):
        self.assertTrue( run_func_tests.Rpdb2Stdout.reWaitingOnBp.match('*** Debuggee is waiting at break point for further commands.') != None )
        self.assertTrue( run_func_tests.Rpdb2Stdout.reNotWaitingOnBp.match('*** Debuggee is waiting at break point for further commands.') == None )

        self.assertTrue( run_func_tests.Rpdb2Stdout.reWaitingOnBp.match('*** Totoro .') == None )
        self.assertTrue( run_func_tests.Rpdb2Stdout.reNotWaitingOnBp.match('*** Totoro .') != None )

if __name__ == '__main__':
    main()