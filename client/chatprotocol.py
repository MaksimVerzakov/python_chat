from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import ClientFactory
from twisted.internet import reactor
from twisted.internet import defer
from GUI.ChatView import ChatView
from GUI.LoginDlg import LoginDlgView
from GUI.ErrorDlg import OnError

class EchoClient(LineReceiver):
    
    ok_defer = defer.Deferred()
    
    def connectionMade(self):
        self.login_gui = LoginDlgView(None, -1, 'Login')
        self.login_gui.protocol = self
        self.login_gui.ShowModal()
               
    def lineReceived(self, line):
        print line
        self.parser(line)        
    
    def parser(self, line):
        textstart = line.find(" '")
        msg = []
        if textstart == -1:
            msg = line.split()
        else:
            msg = line[:textstart].split()
            msg.append(line[textstart + 1:])  
        print msg
        case = {'OK':self.Ok,
                'ERROR':self.Error,
                'MSG':self.MSG,
                'SERVICE':self.Service,
                'NAMES':self.Names
                }
        action = case.get(msg[0])
        if action:
            action(msg[1:])
            
    def Ok(self, arg):
        self.ok_defer.callback('OK')
        
    def Error(self, arg):
        self.ok_defer.errback(ValueError(arg[0]))
        
    def MSG(self, arg):
        self.gui.OnUpdateChatView(arg[0], arg[1], arg[2])
    
    def Names(self, names):
        self.gui.OnUpdateContactList(names)
    
    def Service(self, arg):
        print arg
        self.gui.OnServiceChatView(arg[0], arg[1])
        
    def sendMSG(self, line):
        self.sendLine(str("!%s MSG * '%s'" % (self.nick, line)))    
    
    def login(self, nick, password):
        self.sendLine(str('CONNECT %s %s' % (nick, password)))
        self.nick = nick
        self.ok_defer.addCallback(self.onLogin)
        self.ok_defer.addErrback(self.onError)
    
    def onLogin(self, msg):
        print 'onLogin'
        self.gui = ChatView(None, 'Chat')
        self.gui.protocol = self
        self.gui.Show(True) 
    
    def onError(self, err):
        OnError(err.getErrorMessage())        
    
    def signin(self, nick, password):
        self.sendLine(str('NEW %s %s' % (nick, password)))
        self.nick = nick
        self.ok_defer.addCallback(self.onLogin)
        self.ok_defer.addErrback(self.onError)
    
    def change_nick(self, new_nick):
        self.sendLine(new_nick)

class EchoClientFactory(ClientFactory):
    
    protocol = EchoClient
        
    def clientConnectionFailed(self, connector, reason):
        OnError('Connection Faild:\n%s' % reason.getErrorMessage())
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        OnError('Connection Lost:\n%s' % reason.getErrorMessage())
        reactor.stop()         


        


