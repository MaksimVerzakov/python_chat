""" Module contains client part of classes required for connection 
between client and server.

Exported Classes:
    ChatProtocol -- provide receiving and sending messages between 
    client and server
 
    ChatClientFactory -- derives twisted.internet.protocol.ClientFactory 

"""
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import ClientFactory
from twisted.internet import reactor
from twisted.internet import defer
from twisted.internet.error import ConnectionDone

from GUI.chatview import ChatView
from GUI.logindlg import LoginDlgView
from GUI.errordlg import error_dlg
import myparser

 
class ChatProtocol(LineReceiver):
    """Provide receiving and sending messages between client and server.
    Class ChatProtocol derives twisted.protocol.basic.LineReceiver.    
    """
    def __init__(self):
        self.login_gui = LoginDlgView(None, -1, 'Login')
        self.login_gui.protocol = self
        self.gui = ChatView(None, 'Chat')
        self.gui.protocol = self

    def connectionMade(self):
        """Overrides twisted.protocol.basic.LineReceiver.connectionMade.
        Initialize Login Dialog to set host and port for connection.
        """
        self.ok_defer = defer.Deferred()
        self.login_gui.Show(True)
               
    def lineReceived(self, line):
        """Overrides twisted.protocol.basic.LineReceiver.lineReceived.
        Send line to self.parser function.
        """
        self._parser(line)        
    
    def _parser(self, line):
        """Parse line to tuple of prefix, command and message.
        Call a function due to command.

        :param line: string message received from server
        """
        msg = myparser.parsingCommand(line)
        case = {'OK':self._recd_ok,
                'ERROR':self._recd_error,
                'MSG':self._recd_msg,
                'SERVICE':self._recd_service_msg,
                'NAMES':self._recd_names
                }
        action = case.get(msg[1])
        if action:
            action(msg[2])
            
    def _recd_ok(self, arg):
        """Called when received OK command from server.
        Callback 'OK' to self.ok_defer
        """
        self.ok_defer.callback('OK')          
        
    def _recd_error(self, error_msg):
        """Called when received ERROR command from server.
        Callback error to self.ok_defer with an error description

        :param error_msg: description of error
        """
        self.ok_defer.errback(ValueError(error_msg[0]))
        
    def _recd_msg(self, args):
        """Called when received MSG command from server.
        Call OnUpdateChatView method of gui with arguments:
        sender, destination and text message.

        :param args: list of sender, destination and text message.
        """
        self.gui.OnUpdateChatView(args[0], args[1], args[2][1:-1])
    
    def _recd_names(self, names):
        """Called when received NAMES command from server.
        Call OnUpdateContactList method of gui with names as argument

        :param names: list of online users
        """
        self.names = names
        self.gui.OnUpdateContactList(names)
    
    def _recd_service_msg(self, args):
        """Called when received SERVICE command wrom server.
        Call OnServiceChatView method of gui with sender and
        service text as arguments.

        :param args: list of user's nick and service text
        """
        self.gui.OnServiceChatView(args[0], args[1][1:-1])
        
    def send_msg(self, line):
        """Send broadcast message to server if destination unknown.
        Send direct message if line starts with @nickname and nickname
        contains in list of online users.
        
        :param line: text string sended by user
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
        return msg    
    
    def login(self, nick, password):
        """Send CONNECT message to server with nick and 
        password as arguments to register exicting user.
        Add callbacks self.on_login and errback self.on_login_error to
        self.ok_defer to catch Ok or Error message from server.
        
        :param nick: user's nickname

        :param password: user's password

        """
        self.sendLine(str('CONNECT %s %s' % (nick, password)))
        self.nick = nick
        self.ok_defer = defer.Deferred()
        self.ok_defer.addCallback(self._on_login)
        self.ok_defer.addErrback(self._on_login_error)
    
    def _on_login(self, msg):
        """Called when recevied OK message when user login.
        Create ChatView frame from GUI.chatview.
        Set self as protocol to ChatView frame.
        """
        self.gui.Show(True) 
        
    def _on_error(self, err):
        """Called when recevied error message from server.
        Create error_dlg from GUI.errordlg with error message.

        :param err: error
        """
        error_dlg(err.getErrorMessage()[1:-1])               
    
    def _on_login_error(self, err):
        """Called when recevied error message from server when user login.
        Create error_dlg from GUI.errordlg with error message.
        Show again login dialog.

        :param err: error
        """
        error_dlg(err.getErrorMessage())
        self.login_gui.Show(True)
    
    def signin(self, nick, password):
        """Send NEW message to server with nick and 
        password as arguments to register new user.
        Add callbacks self.on_login and errback self.on_login_error to
        self.ok_defer to catch Ok or Error message from server.

        :param nick: nickname of new user

        :param password: password of new user 
        """
        self.sendLine(str('NEW %s %s' % (nick, password)))
        self.nick = nick
        self.ok_defer = defer.Deferred()
        self.ok_defer.addCallback(self._on_login)
        self.ok_defer.addErrback(self._on_login_error)
    
    def change_nick(self, new_nick):
        """Send NICK message to server with new nick as arguments to
        change nickname.
        Add callbacks on_change_nick and errback self.on_error to
        self.ok_defer to catch Ok or Error message from server.

        :param new_nick: new user's nickname
        """
        self.sendLine(str('!%s NICK %s' % (self.nick, new_nick)))
        
        def on_change_nick(msg):
            """Save new nick as self.nick if recivied OK message"""
            self.gui.NewNick(new_nick, self.nick)
            self.nick = new_nick
            self.d.callback(self.nick)
            
        self.ok_defer = defer.Deferred()
        self.ok_defer.addCallback(on_change_nick)
        self.ok_defer.addErrback(self._on_error)                     
        self.d = defer.Deferred()
        return self.d
    

class ChatClientFactory(ClientFactory):
    """Class ChatClientFactory derives twisted.internet.protocol.ClientFactory."""
    def __init__(self):
        self.protocol = ChatProtocol
        
    def clientConnectionFailed(self, connector, reason):
        """Overrides twisted.internet.protocol.ClientFactory.clientConnectionFailed.
        Create error_dlg from GUI.errordlg with the reason why connection
        was failed
        """
        error_dlg('Connection Faild:\n%s' % reason.getErrorMessage())        

    def clientConnectionLost(self, connector, reason):
        """Overrides twisted.internet.protocol.ClientFactory.clientConnectionFailed.
        Create error_dlg from GUI.errordlg with the reason why connection
        was lost if it's not close clearly.
        """
        if not reason.check(ConnectionDone):
            error_dlg('Connection Lost:\n%s' % reason.getErrorMessage())
        else:
            reactor.stop()
