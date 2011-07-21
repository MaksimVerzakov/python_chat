
from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory 
from twisted.protocols.basic import LineOnlyReceiver 
from base_cmd import*

class ChatProtocol(LineOnlyReceiver): 

    nickname = None 

    def connectionMade(self): 
        self.factory.clientProtocols.append(self)

    def connectionLost(self, reason):
        CloseProtocol(self)

    def lineReceived(self, line):
        prefix, cmd, args = ParsingCommand(line)
        if not cmd:
            return
        commands[cmd](self, prefix, args)
            
class ChatProtocolFactory(ServerFactory): 

    protocol = ChatProtocol 
    
    filename = 'ChatUsers'

    def __init__(self): 
        self.clientProtocols = []
        self.activeUsers = []

print "Starting Server"
factory = ChatProtocolFactory()
reactor.listenTCP(1025, factory)
reactor.run() 
