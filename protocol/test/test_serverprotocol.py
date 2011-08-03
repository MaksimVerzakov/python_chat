from protocol.serverprotocol import ChatProtocol
from protocol.serverprotocol import ChatProtocolFactory

from twisted.trial.unittest import TestCase
from twisted.test.proto_helpers import StringTransportWithDisconnection

import os

class TestProtocol(TestCase):
    def setUp(self):
        self.protocol = ChatProtocol()
        self.transport = StringTransportWithDisconnection()
        self.protocol.factory = ChatProtocolFactory()
        
        fl = os.open(ChatProtocolFactory.filename, os.O_CREAT |
                                                   os.O_RDWR)
                                                    
        os.write(fl, 'hey ho\n')
        os.close(fl)

    def test_connect_disconnect(self):
        self.assertFalse(self.protocol in 
                                self.protocol.factory.clientProtocols)
        self.assertFalse(self.protocol in 
                                self.protocol.factory.activeUsers)
        
        self.protocol.makeConnection(self.transport)
        self.transport.protocol = self.protocol
        
        self.assertTrue(self.protocol in 
                                self.protocol.factory.clientProtocols)
        self.assertFalse(self.protocol in 
                                self.protocol.factory.activeUsers)
        
        self.protocol.lineReceived("CONNECT hey ho")
        self.assertTrue(self.protocol in 
                                self.protocol.factory.activeUsers)
        

        self.protocol.transport.loseConnection()
        self.assertFalse(self.protocol in 
                                self.protocol.factory.activeUsers)
        self.assertFalse(self.protocol in 
                                self.protocol.factory.clientProtocols)
        
