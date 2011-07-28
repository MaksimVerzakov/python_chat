""" Module contains client part of classes required for connection 
between client and server.

Exported Classes:
    |ChatProtocol        provide receiving and sending messages between 
    client and server 
    |ChatClientFactory   derives twisted.internet.protocol.ClientFactory 

"""
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import ClientFactory
from twisted.internet import reactor
from twisted.internet import defer
from twisted.internet.error import ConnectionDone

from GUI.chatview import ChatView
from GUI.logindlg import LoginDlgView
from GUI.errordlg import error_dlg
from parser import parsingCommand

 
class ChatProtocol(LineReceiver):
    """Provide receiving and sending messages between client and server
    Class ChatProtocol derives twisted.protocol.basic.LineReceiver.    
    """
    def connectionMade(self):
        """
        Overrides twisted.protocol.basic.LineReceiver.connectionMade
        Initialize Login Dialog to set host and port for connection
        """
        self.ok_defer = defer.Deferred()
        self.login_gui = LoginDlgView(None, -1, 'Login')
        self.login_gui.protocol = self
        self.login_gui.ShowModal()
               
    def lineReceived(self, line):
        """
        Overrides twisted.protocol.basic.LineReceiver.lineReceived
        Send line to self.parser function.
        """
        self.parser(line)        
    
    def parser(self, line):
        """
        Parse line to tuple of prefix, command and message.
        Call a function due to command.
        """
        msg = parsingCommand(line)
        case = {'OK':self.recd_ok,
                'ERROR':self.recd_error,
                'MSG':self.recd_msg,
                'SERVICE':self.recd_service_msg,
                'NAMES':self.recd_names
                }
        action = case.get(msg[1])
        if action:
            action(msg[2])
            
    def recd_ok(self, arg):
        """
        Called when received OK command from server.
        
        Callback 'OK' to self.ok_defer
        """
        self.ok_defer.callback('OK')
        
    def recd_error(self, arg):
        """
        Called when received ERROR command from server.
        
        Callback error to self.ok_defer with an error description
        """
        self.ok_defer.errback(ValueError(arg[0]))
        
    def recd_msg(self, arg):
        """
        Called when received MSG command from server.
        
        Call OnUpdateChatView method of gui with arguments:
        sender, destination and text message
        """
        self.gui.OnUpdateChatView(arg[0], arg[1], arg[2][1:-1])
    
    def recd_names(self, names):
        """
        Called when received NAMES command from server.
        
        Call OnUpdateContactList method of gui with arguments:
        names - list of online users
        """
        self.names = names
        self.gui.OnUpdateContactList(names)
    
    def recd_service_msg(self, arg):
        """
        Called when received SERVICE command wrom server.
        
        Call OnServiceChatView method of gui with arguments:
        sender
        service text
        """
        self.gui.OnServiceChatView(arg[0], arg[1][1:-1])
        
    def send_msg(self, line):
        """
        Send broadcast message to server if destination unknown.
        Send direct message if line starts with @nickname and nickname
        contains in list of online users.
        
        *atributes:*
            line
        """
        destination = '*'
        msg = line.lstrip()
        if not msg: 
            return
        if line.split()[0].startswith('@') and line.split()[0][1:] in self.names:
            destination = line.split()[0][1:]
            msg = line[len(destination) + 2:]
        msg = "!%s MSG %s '%s'" % (self.nick, destination, msg)
        self.sendLine(msg.encode('utf8'))    
    
    def login(self, nick, password):
        """
        Send CONNECT message to server with nick and 
        password as arguments to register exicting user.
        Add callbacks self.on_login and errback self.on_login_error to
        self.ok_defer to catch Ok or Error message from server.
        
        *arguments:*
            nick
            password
        """
        self.sendLine(str('CONNECT %s %s' % (nick, password)))
        self.nick = nick
        self.ok_defer = defer.Deferred()
        self.ok_defer.addCallback(self.on_login)
        self.ok_defer.addErrback(self.on_login_error)
    
    def on_login(self, msg):
        """
        Called when recevied OK message when user login.
        Create ChatView frame from GUI.chatview.
        Set self as protocol to ChatView frame.
        """
        self.gui = ChatView(None, 'Chat')
        self.gui.protocol = self
        self.gui.Show(True) 
        
    def on_error(self, err):
        """
        Called when recevied error message from server.
        
        Create error_dlg from GUI.errordlg with error message.
        """
        error_dlg(err.getErrorMessage())               
    
    def on_login_error(self, err):
        """
        Called when recevied error message from server when user login.
        
        Create error_dlg from GUI.errordlg with error message.
        Show again login dialog.
        """
        error_dlg(err.getErrorMessage())
        self.login_gui.ShowModal()
    
    def signin(self, nick, password):
        """
        Send NEW message to server with nick and 
        password as arguments to register new user.
        Add callbacks self.on_login and errback self.on_login_error to
        self.ok_defer to catch Ok or Error message from server.
        """
        self.sendLine(str('NEW %s %s' % (nick, password)))
        self.nick = nick
        self.ok_defer = defer.Deferred()
        self.ok_defer.addCallback(self.on_login)
        self.ok_defer.addErrback(self.on_login_error)
    
    def change_nick(self, new_nick):
        """
        Send NICK message to server with new nick as arguments to
        change nickname.
        Add callbacks on_change_nick and errback self.on_error to
        self.ok_defer to catch Ok or Error message from server.
        """
        self.sendLine(str('!%s NICK %s' % (self.nick, new_nick)))
        
        def on_change_nick(msg):
            """Save new nick as self.nick if recivied OK message"""
            self.gui.users[new_nick] = self.gui.users[self.nick]
            self.nick = new_nick
            
        self.ok_defer = defer.Deferred()
        self.ok_defer.addCallback(on_change_nick)
        self.ok_defer.addErrback(self.on_error)
    
    def on_quit(self, bye):
        """
        Called when user try to close program.
        Send QUIT message to server with last message as argument.
        """
        self.sendLine(str("!%s QUIT '%s'" % (self.nick, bye)))
        reactor.stop()
    

class ChatClientFactory(ClientFactory):
    """Class ChatClientFactory derives twisted.internet.protocol.ClientFactory."""
    protocol = ChatProtocol
        
    def clientConnectionFailed(self, connector, reason):
        """
        Overrides twisted.internet.protocol.ClientFactory.clientConnectionFailed
        Create error_dlg from GUI.errordlg with the reason why connection
        was failed
        """
        error_dlg('Connection Faild:\n%s' % reason.getErrorMessage())        

    def clientConnectionLost(self, connector, reason):
        """
        Overrides twisted.internet.protocol.ClientFactory.clientConnectionFailed
        Create error_dlg from GUI.errordlg with the reason why connection
        was lost if it's not close clearly.
        """
        if not reason.check(ConnectionDone):
            error_dlg('Connection Lost:\n%s' % reason.getErrorMessage())  
 
