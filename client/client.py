import wx

from twisted.internet import wxreactor
wxreactor.install()

from twisted.internet import reactor

from GUI.connectiondlg import ConnectionDlgView
from chatprotocol import ChatClientFactory

class MyApp(wx.App):

    def OnInit(self):
        frame = ConnectionDlgView(None, -1, 'Connect', ChatClientFactory())
        frame.Show(True)
        self.SetTopWindow(frame)                       
        return True
        
if __name__ == '__main__':
    myWxAppInstance = MyApp()
    reactor.registerWxApp(myWxAppInstance)
    reactor.run()
