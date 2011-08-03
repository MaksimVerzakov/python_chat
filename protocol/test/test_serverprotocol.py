import sys
sys.path.append('/home/volodya/projects/python_chat/python_chat/')

from protocol.serverprotocol import ChatProtocol
from protocol.serverprotocol import ChatProtocolFactory
from protocol.serverprotocol import ExUnknownCommand

from twisted.trial.unittest import TestCase
from twisted.test.proto_helpers import StringTransportWithDisconnection

class TestProtocol(TestCase):
    def setUp(self):
        self.protocol = ChatProtocol()
        self.transport = StringTransportWithDisconnection()
        self.protocol.factory = ChatProtocolFactory()

    def test_connect_disconnect(self):
        self.assertFalse(self.protocol in self.protocol.factory.clientProtocols)
        self.assertFalse(self.protocol in self.protocol.factory.activeUsers)
        
        self.protocol.makeConnection(self.transport)
        self.transport.protocol = self.protocol
        
        self.assertTrue(self.protocol in self.protocol.factory.clientProtocols)
        self.assertFalse(self.protocol in self.protocol.factory.activeUsers)
        
        self.protocol.lineReceived("CONNECT hey ho")
        self.assertTrue(self.protocol in self.protocol.factory.activeUsers)
        
        self.protocol.lineReceived("!hey QUIT 'bye bye'")
        self.assertFalse(self.protocol in self.protocol.factory.activeUsers)
        
        #self.assertRaises(ExUnknownCommand, self.protocol.lineReceived, "CMD arg")
        
        self.protocol.transport.loseConnection()
        self.assertFalse(self.protocol in self.protocol.factory.clientProtocols)
        
