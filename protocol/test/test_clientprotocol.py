import unittest
import wx

from protocol.clientprotocol import ChatProtocol
from protocol.clientprotocol import ChatClientFactory

from twisted.internet import defer, protocol
from twisted.internet import reactor
from twisted.trial import unittest
from twisted.test.proto_helpers import StringTransportWithDisconnection

class GuiSub(object):
    def __init__(self):
        self.is_shown = defer.Deferred()
        self.users = {}
    def OnUpdateChatView(self, nick, dest, text):
        self.msg = (nick, dest, text)
    def OnServiceChatView(self, nick, text):
        self.smsg = (nick, text)
    def OnUpdateContactList(self, names):
        self.names = names
    def ShowModal(self):
        self.is_shown.callback(True)
    def OnError(self, err_msg):
        self.err = err_msg
    def NewNick(self, one, two):
        pass

class ChatProtocolTest(ChatProtocol):
    
    def __init__(self):
       self.gui = GuiSub()
       self.login_gui = GuiSub()
       self.gui.protocol = self
       self.login_gui.protocol = self
    
    def _on_error(self, err):
        self.gui.OnError(err.getErrorMessage()[1:-1])
    
    def _on_login_error(self, err):
        self.gui.OnError(err.getErrorMessage()[1:-1])
        
    def on_quit(self, bye):
        self.sendLine(str("!%s QUIT '%s'" % (self.nick, bye)))        

class ChatClientFactoryTest(ChatClientFactory):
    def __init__(self):
        self.protocol = ChatProtocolTest

class TestProtocol(unittest.TestCase):
    def setUp(self):
        self.protocol = ChatProtocolTest()
        self.transport = StringTransportWithDisconnection()
        self.protocol.makeConnection(self.transport)
        self.transport.protocol = self.protocol
        self.protocol.factory = ChatClientFactoryTest() 
        self.protocol.nick = 'fred'     

    def test_names(self):
        self.protocol.lineReceived('NAMES john derrek')
        self.assertEquals(self.protocol.gui.names, ['john', 'derrek'])
    
    def test_login(self):
        self.protocol.login(1,1)
        self.protocol.lineReceived('OK')
        self.assertTrue(self.protocol.gui.is_shown)
    
    def test_login(self):
        self.protocol.login('one', 'two')
        self.protocol.lineReceived('OK')
        self.assertTrue(self.protocol.gui.is_shown)
        self.protocol.login('zeds', 'dead')
        self.protocol.lineReceived("ERROR 'user already exist'")
        self.assertEquals(self.protocol.gui.err, 'user already exist')
    
    def test_newuser(self):
        self.protocol.signin('new', 'pass')
        self.protocol.lineReceived('OK')
        self.assertTrue(self.protocol.gui.is_shown)
        self.protocol.signin('new2', 'pass2')
        self.protocol.lineReceived("ERROR 'user already exist'")
        self.assertEquals(self.protocol.gui.err, 'user already exist')
    
    def test_msg(self):
        self.protocol.lineReceived("MSG John * 'hello'")
        self.assertEquals(self.protocol.gui.msg, ('John', '*', 'hello'))
   
    def test_smsg(self):
        self.protocol.lineReceived("SERVICE John 'test'")
        self.assertEquals(self.protocol.gui.smsg, ('John', 'test'))
    
    def test_send(self):
        msg = self.protocol.send_msg('hello')
        self.assertEquals(msg, "!%s MSG * 'hello'" % self.protocol.nick)
   
    def test_changenick(self):
        d = self.protocol.change_nick('god')
        d.addCallback(self.comparenick)
        self.protocol.lineReceived('OK')
        return d
    
    def comparenick(self, nick):
        self.assertEquals(nick, 'god')        
