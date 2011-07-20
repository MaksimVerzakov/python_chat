from twisted.spread import pb
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from twisted.internet import defer
import sys


from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import sys

class EchoClient(LineReceiver):
    end="Bye-bye!"
    
    def connectionMade(self):
        self.sendLine("Hello, world!")
        self.sendLine("What a fine day it is.")        

    def lineReceived(self, line):
        print "receive:", line
        reactor.callLater(2, self.factory.msgtochat().callback, line)
            

class EchoClientFactory(ClientFactory):
    
    protocol = EchoClient
    
    def clientConnectionFailed(self, connector, reason):
        print 'connection failed:', reason.getErrorMessage()
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print 'connection lost:', reason.getErrorMessage()
        reactor.stop()
    
    def msgtochat(self):
        self.d = defer.Deferred()
        return self.d

def dosmth(msg):
    print msg

if __name__ == '__main__':
    f = EchoClientFactory()
    reactor.connectTCP('localhost', 1025, f)
    d = f.msgtochat()
    d.addCallback(dosmth)
    reactor.run()
        


