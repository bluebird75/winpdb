from unittest.case import TestCase

import rpdb.events
import rpdb2

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