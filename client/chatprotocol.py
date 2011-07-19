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
        self.sendLine(self.end)

    def lineReceived(self, line):
        print "receive:", line
        if line==self.end:
            self.transport.loseConnection()
    
    def sendMSG(self, msg):
        self.sendLine(msg)

class EchoClientFactory(pb.PBClientFactory):
    
    protocol = EchoClient

    def clientConnectionFailed(self, connector, reason):
        print 'connection failed:', reason.getErrorMessage()
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print 'connection lost:', reason.getErrorMessage()
        reactor.stop()


        


