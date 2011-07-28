from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import ClientFactory
from twisted.internet import reactor
from twisted.internet import defer

from GUI.chatview import ChatView
from GUI.logindlg import LoginDlgView
from GUI.errordlg import error_dlg
from parser import parsingCommand

 
class ChatProtocol(LineReceiver):
    
    def connectionMade(self):
        self.ok_defer = defer.Deferred()
        self.login_gui = LoginDlgView(None, -1, 'Login')
        self.login_gui.protocol = self
        self.login_gui.ShowModal()
               
    def lineReceived(self, line):
        self.parser(line)        
    
    def parser(self, line):
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
        self.ok_defer.callback('OK')
        
    def recd_error(self, arg):
        self.ok_defer.errback(ValueError(arg[0]))
        
    def recd_msg(self, arg):
        self.gui.OnUpdateChatView(arg[0], arg[1], arg[2][1:-1])
    
    def recd_names(self, names):
        self.names = names
        self.gui.OnUpdateContactList(names)
    
    def recd_service_msg(self, arg):
        self.gui.OnServiceChatView(arg[0], arg[1][1:-1])
        
    def send_msg(self, line):
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
        self.sendLine(str('CONNECT %s %s' % (nick, password)))
        self.nick = nick
        self.ok_defer = defer.Deferred()
        self.ok_defer.addCallback(self.on_login)
        self.ok_defer.addErrback(self.on_login_error)
    
    def on_login(self, msg):
        self.gui = ChatView(None, 'Chat')
        self.gui.protocol = self
        self.gui.Show(True) 
        
    def on_error(self, err):
        error_dlg(err.getErrorMessage())               
    
    def on_login_error(self, err):
        error_dlg(err.getErrorMessage())
        self.login_gui.ShowModal()
    
    def signin(self, nick, password):
        self.sendLine(str('NEW %s %s' % (nick, password)))
        self.nick = nick
        self.ok_defer = defer.Deferred()
        self.ok_defer.addCallback(self.on_login)
        self.ok_defer.addErrback(self.on_login_error)
    
    def change_nick(self, new_nick):
        self.sendLine(str('!%s NICK %s' % (self.nick, new_nick)))
        def on_change_nick(msg):
            self.nick = new_nick
        self.ok_defer = defer.Deferred()
        self.ok_defer.addCallback(on_change_nick)
        self.ok_defer.addErrback(self.on_error)
    
    def on_quit(self, bye):
        print 'quit'
        self.sendLine(str("!%s QUIT '%s'" % (self.nick, bye)))
        reactor.callLater(0.1, reactor.stop)
    

class ChatClientFactory(ClientFactory):
    
    protocol = ChatProtocol
        
    def clientConnectionFailed(self, connector, reason):
        error_dlg('Connection Faild:\n%s' % reason.getErrorMessage())        

    def clientConnectionLost(self, connector, reason):
        error_dlg('Connection Lost:\n%s' % reason.getErrorMessage())
