from protocol.serverprotocol import ChatProtocol
from protocol.serverprotocol import ChatProtocolFactory

from protocol.basecmd import serv_text
from protocol.basecmd import err_text

from protocol.myparser import parsingCommand

from twisted.trial.unittest import TestCase
from twisted.test.proto_helpers import StringTransportWithDisconnection


class TestProtocol(TestCase):
    def setUp(self):
        self.protocol = ChatProtocol()
        self.transport = StringTransportWithDisconnection()
        self.protocol.factory = ChatProtocolFactory()
        self.protocol.makeConnection(self.transport)
        self.transport.protocol = self.protocol
    
    def split_commands(self):
        return self.transport.value().splitlines()
        
    def assertCommands(self, args):
        commands = self.split_commands()
        cmd_list = [parsingCommand(cmd) for cmd in commands]
        arg_list = [parsingCommand(arg) for arg in args]
        for (cmd, arg) in zip(cmd_list, arg_list):
            self.assertEquals(arg[1], cmd[1])
            if arg[2]:
                self.assertEquals(arg[2], cmd[2])
        
    def test_connect_command(self):
        self.protocol.lineReceived("CONNECT hey ho")
        self.assertCommands(['OK', 'SERVICE', 'NAMES'])
       
    def test_new_command_error_incorrect_data(self):
        self.protocol.lineReceived("NEW gahhahjjkjsfkkfkk ho")
        self.assertCommands(["ERROR '%s'" % 
                             err_text['err_incorrect_data']])
       
    
    def test_new_command_error_usr_exist(self):
        self.protocol.lineReceived("NEW hey ho")
        self.assertCommands(["ERROR '%s'" % 
                              err_text['err_user_exist']])
    
    def test_msg_command(self):
        self.protocol.lineReceived("CONNECT hey ho")
        self.protocol.lineReceived("!hey MSG * 'message'")
        
        self.assertCommands(['OK', 'SERVICE', 'NAMES', 'MSG'])
        
    def test_nick_command(self):
        self.protocol.lineReceived("CONNECT hey ho")
        self.protocol.lineReceived("!hey NICK newnick")

        self.assertCommands(['OK', 'SERVICE', 'NAMES']*2)
        
    def test_quit_command(self):
        self.protocol.lineReceived("CONNECT hey ho")
        self.protocol.lineReceived("!hey QUIT 'message'")

        self.assertFalse(self.protocol in 
                         self.protocol.factory.activeUsers)
    
    def tearDown(self):
        self.protocol.transport.loseConnection()
