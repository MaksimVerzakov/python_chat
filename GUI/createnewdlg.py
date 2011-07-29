import wx
import wx.lib.newevent

from errordlg import error_dlg


class CreateNewDlgView(wx.Dialog):
    """Create dialog frame to get information for new user."""    
    def __init__(self, parent, id, title):
        """Override __init__ of wx.Dialod.
        Create all controls and binds to catch events.
        """
        super(CreateNewDlgView, self).__init__(self, parent, id,
              title, size=(300, 160))
        panel = wx.Panel(self)
        
        hbox = wx.BoxSizer(wx.VERTICAL)
        fgs = wx.FlexGridSizer(3, 2, 3, 25)
        tnick = wx.StaticText(panel, label="Nickname")
        tpass1 = wx.StaticText(panel, label="Password")
        tpass2 = wx.StaticText(panel, label="Password Again")
                
        self._nick = wx.TextCtrl(panel)
        self._pass1 = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        self._pass2 = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
                
        fgs.AddMany([(tnick), (self._nick, 1, wx.EXPAND), (tpass1), 
            (self._pass1, 1, wx.EXPAND),(tpass2), (self._pass2, 1, wx.EXPAND)])
        
        fgs.AddGrowableCol(1, 1)
        
        hbox.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
            
        bttnbox = wx.BoxSizer(wx.HORIZONTAL)
        create_btn = wx.Button(panel, label='Create', size=(100, 27))
        bttnbox.Add(create_btn)
        
        hbox.Add(bttnbox, flag=wx.BOTTOM|wx.ALIGN_CENTER, border=15)
        
        panel.SetSizer(hbox)
        
        self.Bind(wx.EVT_BUTTON, self.OnCreate, id=create_btn.GetId())          
    
    def OnCreate(self, event):
        """Called when user pushes Create bitton.
           
        If passwords didn't match create error_dlg from errdlg.
        Call signin method of protocol.            
        """
        nick = self._nick.GetValue()
        password1 = self._pass1.GetValue()
        password2 = self._pass2.GetValue()
        if(password1 != password2):
            error_dlg("Passwords didn't match")            
            self._pass1.Clear()
            self._pass2.Clear()
        else:
            print nick, password1
            self.protocol.signin(nick, password1)
        self.Close()
