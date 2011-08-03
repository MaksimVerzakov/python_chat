import unittest
import wx
import wx.lib.newevent
from twisted.trial import unittest
from GUI.createnewdlg import CreateNewDlgView, PasswordError

class cap(object):
    def signin(self, nick, password1):
        pass

class CreateNewDlgTest(CreateNewDlgView):
    
    def __init__(self, parent, id, title):
        super(CreateNewDlgTest, self).__init__(parent, id, title)
        self.protocol = cap()
    
    def OnCreate(self, event):
        CreateNewDlgView.OnCreate(self, event)
        nick = self._nick.GetValue()
        password1 = self._pass1.GetValue()
        return (nick, password1)                  

class TestExample(unittest.TestCase):

    def setUp(self):
        self.app = wx.PySimpleApp()
        self.frame = CreateNewDlgTest(None, -1, 'test2')

    def tearDown(self):
        self.frame.Destroy()

    def test_ok(self):
        self.frame._nick.AppendText('nick')
        self.frame._pass1.AppendText('password')
        self.frame._pass2.AppendText('password')
        test_res = self.frame.OnCreate(None)
        self.assertEqual('nick', test_res[0],
                msg="First is wrong")
        self.assertEqual('password', test_res[1])
