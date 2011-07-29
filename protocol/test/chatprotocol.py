import sys
sys.path.append('/home/maxim/projects/python-chat/python_chat/')
import unittest

from protocol.chatprotocol import ChatProtocol
from protocol.chatprotocol import ChatClientFactory

from twisted.internet import defer, protocol
from twisted.trial import unittest

class TestDisconnect(unittest.TestCase):
    def setUp(self):
        self.serverDisconnected = defer.Deferred()
        self.serverPort = self._listenServer(self.serverDisconnected)
        connected = defer.Deferred()
        self.clientDisconnected = defer.Deferred()
        self.clientConnection = self._connectClient(connected,
                                                    self.clientDisconnected)
        return connected

    def _listenServer(self, d):
        from twisted.internet import reactor
        f = protocol.Factory()
        f.onConnectionLost = d
        f.protocol = ServerProtocol
        return reactor.listenTCP(0, f)

    def _connectClient(self, d1, d2):
        from twisted.internet import reactor
        factory = ChatClientFactory()
        factory.protocol = ChatProtocol
        factory.onConnectionMade = d1
        factory.onConnectionLost = d2
        return reactor.connectTCP('localhost',
                                  self.serverPort.getHost().port,
                                  factory)

    def tearDown(self):
        d = defer.maybeDeferred(self.serverPort.stopListening)
        self.clientConnection.disconnect()
        return defer.gatherResults([d,
                                    self.clientDisconnected,
                                    self.serverDisconnected])

    def test_disconnect(self):
        pass

