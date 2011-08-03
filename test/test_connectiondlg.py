import unittest
import wx
from twisted.trial import unittest
from GUI.connectiondlg import ConnectionDlgView

class ConnectionDlgTest(ConnectionDlgView):
    
    def OnConnect(self, event):
        host = self._host.GetValue()
        port = int(self._port.GetValue())
        return (host, port)
        
    def OnClose(self, event):
        self.Destroy()
        

class TestExample(unittest.TestCase):

    def setUp(self):
        self.app = wx.PySimpleApp()
        self.frame = ConnectionDlgTest(None, -1, 'test', 1)

    def tearDown(self):
        self.frame.Destroy()

    def test_Button(self):
        self.frame._host.AppendText('host')
        self.frame._port.AppendText('1234')
        test_res = self.frame.OnConnect(None)
        self.assertEqual('host', test_res[0],
                msg="First is wrong")
        self.assertEqual(1234, test_res[1])

