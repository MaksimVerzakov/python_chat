import wx

class SettingsDlg(wx.Dialog):
    """
       Dialog for getting new nickname.
    """ 
    def __init__(self, parent, id, title):
        """
           Create dialog frame and all controls and buttons.
           Add binds to catch events.
        """
        wx.Dialog.__init__(self, parent, id, title, size=(250, 100))
        self.protocol = parent.protocol
        panel = wx.Panel(self)

        hbox = wx.BoxSizer(wx.VERTICAL)

        sizer = wx.FlexGridSizer(2, 2, 9, 25)

        stnick = wx.StaticText(panel, label="New Nick")
               
        self._nick = wx.TextCtrl(panel)
                
        sizer.AddMany([(stnick), (self._nick, 1, wx.EXPAND)])

        sizer.AddGrowableCol(1, 1)
                
        connectbtn = wx.Button(panel, wx.ID_ANY, label='Change', size=(70, 27))

        hbox.Add(sizer, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
        hbox.Add(connectbtn, flag=wx.ALIGN_CENTER|wx.BOTTOM, border=15)
        
        panel.SetSizer(hbox)
        
        self.Bind(wx.EVT_BUTTON, self.OnChange, id=connectbtn.GetId())        
    
    def OnChange(self, event):
        """
           Called when user pushes Change button.
           
           Call chang_nick method of protocol.
        """
        nick = self._nick.GetValue()
        self.protocol.change_nick(nick)
        self.Show(False)
        self.Close()
