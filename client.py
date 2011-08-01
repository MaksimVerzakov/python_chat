"""Main module to run client. 
Create wx application and run reactor.
"""
import wx

from twisted.internet import wxreactor
wxreactor.install()

from twisted.internet import reactor

from GUI.connectiondlg import ConnectionDlgView
from protocol.clientprotocol import ChatClientFactory

class MyApp(wx.App):
    """Class MyApp derived from wx.App."""
    def OnInit(self):
        """Override wx.App.OnInit.
        Create ConnectionDlgView frame from GUI.connectionglg
        """
        frame = ConnectionDlgView(None, -1, 'Connect', ChatClientFactory())
        frame.Show(True)
        self.SetTopWindow(frame)                       
        return True


def main():
    """
    Create MyApp instace, register it in reactor and run reactor.
    """
    myWxAppInstance = MyApp()
    reactor.registerWxApp(myWxAppInstance)
    reactor.run()

        
if __name__ == '__main__':
    main()
