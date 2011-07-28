import wx

from twisted.internet import reactor

class ConnectionDlgView(wx.Dialog):
    """
       Dialog for getting host and port for connection with server. 
    """
    def __init__(self, parent, id, title, client_factory):
        """
           Create dialog frame with all controls and buttons.
           Add bind to catch events.
        """
        wx.Dialog.__init__(self, parent, id, title, size=(250, 140))
        self.client_factory = client_factory
        panel = wx.Panel(self)

        hbox = wx.BoxSizer(wx.VERTICAL)

        sizer = wx.FlexGridSizer(2, 2, 9, 25)

        sthost = wx.StaticText(panel, label="Host")
        stport = wx.StaticText(panel, label="Port")
        
        self._host = wx.TextCtrl(panel)
        self._port = wx.TextCtrl(panel)
        
        sizer.AddMany([(sthost), (self._host, 1, wx.EXPAND), (stport), 
            (self._port, 1, wx.EXPAND)])

        sizer.AddGrowableCol(1, 1)
                
        connectbtn = wx.Button(panel, wx.ID_ANY, label='Connect', size=(70, 27))

        hbox.Add(sizer, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
        hbox.Add(connectbtn, flag=wx.ALIGN_CENTER|wx.BOTTOM, border=15)
        
        panel.SetSizer(hbox)
        
        self.Bind(wx.EVT_BUTTON, self.OnConnect, id=connectbtn.GetId())
        self.Bind(wx.EVT_CLOSE, self.OnClose)           
    
    def OnConnect(self, event):
        """
           Called when user pushes Connect button.
           
           Call reactor.ConnectTCP to connect with host and port
           inputed in text controls
        """
        host = self._host.GetValue()
        port = int(self._port.GetValue())  
        reactor.connectTCP(host, port, self.client_factory)
        self.Show(False)
                
    def OnClose(self, event):
        """
           Calls when user tyr close the frame.
           Quit program. 
        """
        #self.Destroy()
        reactor.stop()
        
