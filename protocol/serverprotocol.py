"""
A chat server protocol and factory classes

Exported classes :

chatProtocolFactory -- this class is inheritor of 
                       twisted.internet.protocol.ServerFactory class
                    
"""
from twisted.internet.protocol import ServerFactory 
from twisted.protocols.basic import LineOnlyReceiver 
import base_cmd 
import accounts_class
import parser

class ExUnknownCommand(BaseException):
    """Class for exception which raises when server got incorrect command"""
    
    def __str__(self):
        """"Prints exception name in server terminal"""
        return self.__class__.__name__

class ChatProtocol(LineOnlyReceiver):
    """
    This class realize server-client relations (for each one client)
    Inherits from twisted.protocols.basic.LineOnlyReceiver class
    
    Class data attributes :
    
    nickname -- string-type user nick that used for identitification client in chat
    
    Override methods : 
    
    connectionMade -- callback, calls when user connected to server
    conectionLost -- callback, calls when user disconnected from server
    lineReceived -- callback, calls when server received some data from user
    
    """

    nickname = None 

    def connectionMade(self):
        """Callback, calls each time when client connected to server"""
        self.factory.registerNewUser(self)

    def connectionLost(self, reason):
        """Callback, calls each time when client disconnected from server"""
        base_cmd.closeProtocol(self)
        self.factory.destroyUser(self)

    def lineReceived(self, line):
        """
        Callback, calls each time when client recieved data from client
        Data must be the correct command
        Function calls parser for this command and 
        than calls command handler fucntion
        If command is not correct, function raises exception
        
        """
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
    """
    This class stores a server configurations
    Inherits from twisted.internet.protocol.ServerFactory class
    
    Class data attributes :
    
    protocol -- name of the protocol class for server
    filename -- string-type name of file where saves informations about chat users
    
    Override methods : 
    
    __init__ -- constuctor, calls one time when class is created
    
    Public methods :
    
    registerNewUser --  calls when client is connected to server
    destroyUser -- calls when client is disconnected from server
    
    Example attributes :
    
    clientProtocols -- list of connected in this time clients.
                       Contents their protocols
    activeUsers -- list of active in this time chat users.
                   There are protocols of authorized clients.
    accountsData -- example of class which realize control of users information
    
    """

    protocol = ChatProtocol 
    
    filename = 'ChatUsers'

    def __init__(self): 
        """Set up default server configuration"""
        self.clientProtocols = []
        self.activeUsers = []
        self.accountsData = accounts_class.AccountsClass(self.filename)

    def registerNewUser(self, protocol):
        """Method adds protocol to other connected client's protocols"""
        self.clientProtocols.append(protocol)

    def destroyUser(self, protocol):
        """Method deletes protocol from connected client's protocols"""
        self.clientProtocols.remove(protocol)

