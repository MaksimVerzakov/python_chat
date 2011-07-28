import wx
import wx.lib.newevent

from twisted.internet import reactor

from createnewdlg import CreateNewDlgView

class LoginDlgView(wx.Dialog):
    """
    Dialog for getting nickname and password for authorization on server.
    """
    def __init__(self, parent, id, title):
        """
        Create dialog frame and all controls and buttons.
        Add binds to catch events.
        """
        super(LoginDlgView, self).__init__(parent, id, title, size=(300, 140))
        panel = wx.Panel(self)

        hbox = wx.BoxSizer(wx.VERTICAL)

        fgs = wx.FlexGridSizer(2, 2, 3, 25)

        tnick = wx.StaticText(panel, label="Nickname")
        tpass = wx.StaticText(panel, label="Password")
                
        self._nick = wx.TextCtrl(panel)
        self._pass = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
                
        fgs.AddMany([(tnick), (self._nick, 1, wx.EXPAND), (tpass), 
            (self._pass, 1, wx.EXPAND)])
        
        fgs.AddGrowableCol(1, 1)
        
        hbox.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
            
        bttnbox = wx.BoxSizer(wx.HORIZONTAL)
        
        login_btn = wx.Button(panel, wx.NewId(), label='Login', size=(70, 27))
        create_new_btn = wx.Button(panel, wx.NewId(), label='Create New', size=(100, 27))
        
        bttnbox.Add(login_btn, flag=wx.RIGHT, border=15)
        bttnbox.Add(create_new_btn)

        
        hbox.Add(bttnbox, flag=wx.BOTTOM|wx.ALIGN_CENTER, border=15)
        
        panel.SetSizer(hbox)
        
        self.Bind(wx.EVT_BUTTON, self.OnNewUser, id=create_new_btn.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnLogin, id=login_btn.GetId())  
                
    def OnNewUser(self, event):
        """
        Called when user pushes Create new button.
        Create CreateNewDlgView from createnewdlgview.
        """
        cDlg = CreateNewDlgView(self.GetParent(), -1, 'CreateNew')
        cDlg.protocol = self.protocol
        self.Close()
        cDlg.ShowModal()
        cDlg.Destroy()        
        
    def OnLogin(self, event):
        """
        Called when user pushes Login button.
        Call login method of protocol.
        """
        nick = self._nick.GetValue()
        password = self._pass.GetValue()
        self.protocol.login(nick, password)
        self.Close()
