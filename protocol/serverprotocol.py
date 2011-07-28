"""

"""
from twisted.internet.protocol import ServerFactory 
from twisted.protocols.basic import LineOnlyReceiver 
import base_cmd 
import accounts_class
import parser

class ExUnknownCommand:
    def __str__(self):
        return self.__class__

class ChatProtocol(LineOnlyReceiver): 

    nickname = None 

    def connectionMade(self): 
        self.factory.registerNewUser(self)

    def connectionLost(self, reason):
        base_cmd.closeProtocol(self)
        self.factory.destroyUser(self)

    def lineReceived(self, line):
        prefix, cmd, args = parser.parsingCommand(line)
        try:
            if cmd not in base_cmd.commands:
                raise ExUnknownCommand
            base_cmd.commands[cmd](self, prefix, args)
        except ExUnknownCommand, error:
            print error
        except base_cmd.ExClass, error:
            print error
            
class ChatProtocolFactory(ServerFactory): 

    protocol = ChatProtocol 
    
    filename = 'ChatUsers'

    def __init__(self): 
        self.clientProtocols = []
        self.activeUsers = []
        self.accountsData = accounts_class.AccountsClass(self.filename)

    def registerNewUser(self, protocol):
        self.clientProtocols.append(protocol)

    def destroyUser(self, protocol):
        self.clientProtocols.remove(protocol)

