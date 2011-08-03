import unittest
import wx
import wx.lib.newevent
from twisted.trial import unittest

from GUI.chatview import ChatView

class cap(object):
    def send_msg(self, msg):
        pass
    def on_quit(self, text):
        pass
    

class ChatViewTest(ChatView):
    
    def __init__(self, parent, id, title):
        super(ChatViewTest, self).__init__(parent, title)
        self.protocol = cap()
    
    def OnUpdateContactList(self, names):
        ChatView.OnUpdateContactList(self,names)
        return set(self.users.keys())
    
    def OnUpdateChatView(self, sender, destination, text):
        ChatView.OnUpdateChatView(self, sender, destination, text)
        num = self.viewctrl.GetNumberOfLines()
        return self.viewctrl.GetLineText(num-2)[11:]
    
    def OnServiceChatView(self, sender, text):
        ChatView.OnServiceChatView(self, sender, text)
        num = self.viewctrl.GetNumberOfLines()
        return self.viewctrl.GetLineText(num-2)
                        

class TestExample(unittest.TestCase):

    def setUp(self):
        self.app = wx.PySimpleApp()
        self.frame = ChatViewTest(None, -1, 'test2')

    def tearDown(self):
        self.frame.Destroy()

    def test_ContactList(self):
        names = ('one', 'two', 'three')
        test_res = self.frame.OnUpdateContactList(names)
        self.assertEqual(set(names), test_res)
        names = ('one', 'three')
        test_res = self.frame.OnUpdateContactList(names)
        self.assertEqual(set(names), test_res)
        names = ('one', 'three', 'four')
        test_res = self.frame.OnUpdateContactList(names)
        self.assertEqual(set(names), test_res)
        
    def test_ChatView(self):
        test_res = self.frame.OnUpdateChatView('joe', '*', 'test')
        self.assertEqual(u'joe:  test', test_res)
        test_res = self.frame.OnUpdateChatView('joe', 'fred', 'test')
        self.assertEqual(u'joe: fred test', test_res)        
        
    def test_ChatView2(self):
        test_res = self.frame.OnServiceChatView('joe', 'test')
        self.assertEqual(u'joe test', test_res)        

