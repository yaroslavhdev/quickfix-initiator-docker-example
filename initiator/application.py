#!/usr/bin/python
# -*- coding: utf8 -*-
"""FIX Application"""
import threading
import quickfix as fix
import quickfix42 as fix42
import quickfix44 as fix44
import logging
from model.logger import setup_logger

# configured
__SOH__ = chr(1)

# Logger
setup_logger('FIX')
logfix = logging.getLogger('FIX')


class Application(fix.Application):
    """FIX Application"""
    def __init__(self):
        fix.Application.__init__(self)
        self.response_event = threading.Event()

    def onCreate(self, sessionID):
        self.sessionID = sessionID
        return
    def onLogon(self, sessionID):
        self.sessionID = sessionID
        return
    def onLogout(self, sessionID):
        return

    def toAdmin(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        #logfix.info("S >> (%s)" % msg)
        return
    def fromAdmin(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        #logfix.info("R >> (%s)" % msg)
        return
    def toApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("S >> (%s)" % msg)
        return
    def fromApp(self, message, sessionID):
        msg = message.toString().replace(__SOH__, "|")
        logfix.info("R >> (%s)" % msg)
        self.onMessage(message, sessionID)
        return


    def onMessage(self, message, sessionID):
        print("Received message from", sessionID, message)

        # Set the event to notify the caller that a response is received
        self.response_event.set()

    def queryNewOrderSingle42(self):
        message = fix42.NewOrderSingle()
        message.setField(fix.ClOrdID())
        message.setField(fix.HandlInst('1'))
        message.setField(fix.Symbol( "AAPL" ))
        message.setField(fix.Side( fix.Side_BUY ))
        message.setField(fix.TransactTime())
        message.setField(fix.OrdType( fix.OrdType_MARKET ))
        message.setField(fix.OrderQty( int(1) ))
        message.setField(fix.TimeInForce( fix.TimeInForce_DAY ))
        header = message.getHeader()
        self.queryHeader(header)

        return message

    def executeOrder(self, order: fix.Message):
        fix.Session.sendToTarget(order)

    def queryHeader(self, header):
        header.setField( self.querySenderCompID() )
        header.setField( self.queryTargetCompID() )

    def querySenderCompID(self):
        return self.sessionID.getSenderCompID()

    def queryTargetCompID(self):
        return self.sessionID.getTargetCompID()
