
from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory 
from twisted.protocols.basic import LineOnlyReceiver 
import base_cmd 
import parser

class ChatProtocol(LineOnlyReceiver): 

    nickname = None 

    def connectionMade(self): 
        self.factory.registerNewUser(self)

    def connectionLost(self, reason):
        base_cmd.closeProtocol(self)
        self.factory.destroyUser(self)

    def lineReceived(self, line):
        prefix, cmd, args = parser.parsingCommand(line)
        if not cmd:
            return
        base_cmd.commands[cmd](self, prefix, args)
            
class ChatProtocolFactory(ServerFactory): 

    protocol = ChatProtocol 
    
    filename = 'ChatUsers'

    def __init__(self): 
        self.clientProtocols = []
        self.activeUsers = []

    def registerNewUser(self, protocol):
        self.clientProtocols.append(protocol)

    def destroyUser(self, protocol):
        self.clientProtocols.remove(protocol)
        

print "Starting Server"
factory = ChatProtocolFactory()
reactor.listenTCP(1025, factory)
reactor.run() 
