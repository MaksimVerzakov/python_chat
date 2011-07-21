import wx
from twisted.internet import wxreactor
wxreactor.install()
from twisted.internet import reactor
from GUI.ConnectionDlg import ConnectionDlgView
from chatprotocol import EchoClientFactory

class MyApp(wx.App):

    def twoSecondsPassed(self):
        print "two seconds passed"

    def OnInit(self):
        frame = ConnectionDlgView(None, -1, 'Connect', EchoClientFactory())
        frame.Show(True)
        self.SetTopWindow(frame)        
        # look, we can use twisted calls!        
        return True
        
if __name__ == '__main__':
    myWxAppInstance = MyApp()
    reactor.registerWxApp(myWxAppInstance)
    reactor.run()
