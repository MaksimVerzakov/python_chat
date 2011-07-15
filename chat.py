#чат с массовой рассылкой и сменой ника
#запускаешь чат F5, потом в другом терминале пишешь telnet localhost 1025 -> получаешь клиента
#потом еще и еще через телнет можно коннектиться

from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory 
from twisted.protocols.basic import LineOnlyReceiver 

class ChatProtocol(LineOnlyReceiver): 

    name = "" 

    def getName(self): 
        if self.name!="": 
            return self.name 
        return self.transport.getPeer().host 

    def connectionMade(self): 
        print "New connection from "+self.getName() 
        self.sendLine("Welcome to my my chat server.") 
        self.sendLine("Send '/NAME [new name]' to change your name.") 
        self.sendLine("Send '/EXIT' to quit.") 
        self.factory.sendMessageToAllClients(self.getName()+" has joined the party.") 
        self.factory.clientProtocols.append(self)

    def connectionLost(self, reason): 
        print "Lost connection from "+self.getName() 
        self.factory.clientProtocols.remove(self) 
        self.factory.sendMessageToAllClients(self.getName()+" has disconnected.") 

    def lineReceived(self, line): 
        print self.getName()+" : "+line 
        if line[:5]=="/NAME": 
            oldName = self.getName() 
            self.name = line[5:].strip() 
            self.factory.sendMessageToAllClients(oldName+" changed name to "+self.getName()) 
        elif line=="/EXIT": 
            self.transport.loseConnection() 
        else: 
            self.factory.sendMessageToAllClients(self.getName()+" : "+line) 

    def sendLine(self, line): 
        self.transport.write(line+"\r\n") 

class ChatProtocolFactory(ServerFactory): 

    protocol = ChatProtocol 

    def __init__(self): 
        self.clientProtocols = [] 

    def sendMessageToAllClients(self, mesg): 
        for client in self.clientProtocols:
            client.sendLine(mesg) 

print "Starting Server"
factory = ChatProtocolFactory()
reactor.listenTCP(1025, factory)
reactor.run() 
