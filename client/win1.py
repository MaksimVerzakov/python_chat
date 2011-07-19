# gotoclass.py
from twisted.spread import pb
import wx
import wx.lib.newevent
import time
from twisted.internet import wxreactor
wxreactor.install()
from chatprotocol import EchoClientFactory, EchoClient
# import t.i.reactor only after installing wxreactor:
from twisted.internet import reactor

ErrorEvent, EVT_ERROR_EVENT = wx.lib.newevent.NewEvent()
MsgEvent, EVT_NEW_MSG_EVENT = wx.lib.newevent.NewEvent()

def OnError (self, event):
    dial = wx.MessageDialog(None, event.text, 'Error', wx.OK|wx.ICON_ERROR)
    dial.ShowModal()

class SettingsDlg(wx.Dialog):
    
    def __init__(self, parent, id, title):
        
        wx.Dialog.__init__(self, parent, id, title, size=(250, 120))
        
        staticbox = wx.StaticBox(self, -1, 'Connection', (5, 5), size=(240, 110))
        hbox = wx.BoxSizer(wx.VERTICAL)
        fgs = wx.FlexGridSizer(2, 2, 9, 25)

        sthost = wx.StaticText(self, label="Host")
        stport = wx.StaticText(self, label="Port")
        
        self._host = wx.TextCtrl(self)
        self._port = wx.TextCtrl(self)
        
        fgs.AddMany([(sthost), (self._host, 1, wx.EXPAND), (stport), 
            (self._port, 1, wx.EXPAND)])

        fgs.AddGrowableCol(1, 1)
        hbox.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=30)
        self.SetSizer(hbox)
        

class ConnectionDlgView(wx.Dialog):
    
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(250, 140))
        panel = wx.Panel(self)

        hbox = wx.BoxSizer(wx.VERTICAL)

        fgs = wx.FlexGridSizer(2, 2, 9, 25)

        sthost = wx.StaticText(panel, label="Host")
        stport = wx.StaticText(panel, label="Port")
        
        self._host = wx.TextCtrl(panel)
        self._port = wx.TextCtrl(panel)
        
        fgs.AddMany([(sthost), (self._host, 1, wx.EXPAND), (stport), 
            (self._port, 1, wx.EXPAND)])

        fgs.AddGrowableCol(1, 1)
                
        connectbtn = wx.Button(panel, wx.ID_ANY, label='Connect', size=(70, 27))

        hbox.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
        hbox.Add(connectbtn, flag=wx.ALIGN_CENTER|wx.BOTTOM, border=15)
        
        panel.SetSizer(hbox)
        
        self.Bind(wx.EVT_BUTTON, self.OnConnect, id=connectbtn.GetId())
    
    def OnConnect(self, event):
        host = self._host.GetValue()
        port = int(self._port.GetValue())
        factory = EchoClientFactory()
        reactor.connectTCP(host, port, factory)
        d = factory.getRootObject()
        d.addCallback(clientConnect)
        self.Close()
        #Send an error event to parent window if connection failed
              
        
class LoginDlgView(wx.Dialog):
    
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 140))
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
        cDlg = CreateNewDlgView(self.GetParent(), -1, 'CreateNew')
        cDlg.ShowModal()
        cDlg.Destroy()
        self.Close()
        
    def OnLogin(self, event):
        nick = self._nick.GetValue()
        password = self._pass.GetValue()
        #Send an error event to parent window if login was failed
        evt = ErrorEvent(text="Wrong nickname or password")
        wx.PostEvent(self.GetParent(), evt)   
        
        
class CreateNewDlgView(wx.Dialog):
    
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 160))
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
        nick = self._nick.GetValue()
        password1 = self._pass1.GetValue()
        password2 = self._pass2.GetValue()
        if(password1 != password2):
            #Send an error event to parent window if login was failed
            evt = ErrorEvent(text="Passwords didn't match.")
            wx.PostEvent(self.GetParent(), evt)
            self._pass1.Clear()
            self._pass2.Clear()

class ChatView(wx.Frame):
  
    def __init__(self, parent, title):
        super(ChatView, self).__init__(parent, title=title, 
            size=(390, 350))
        
        self.Bind(EVT_ERROR_EVENT, OnError)
        self.Bind(EVT_NEW_MSG_EVENT, self.OnUpdateChatView)
        self.LoginDlg() 
        self.InitUI()
        self.Centre()
        self.Show()     
        
    def InitUI(self):
    
    
        toolbar = self.CreateToolBar()
        ID_SETTINGSTOOL = wx.NewId()
        toolbar.AddLabelTool(ID_SETTINGSTOOL, '', wx.Bitmap('icons/settings_button.png'))
        toolbar.Realize()
        
        self.Bind(wx.EVT_TOOL, self.OnSettings, id=ID_SETTINGSTOOL)
            
        splitter = wx.SplitterWindow(self, -1)
            
        panel1 = wx.Panel(splitter)

        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)
        
        chatbox = wx.BoxSizer(wx.VERTICAL)

        self.viewctrl = wx.TextCtrl(panel1, style=wx.TE_MULTILINE)
        chatbox.Add(self.viewctrl, proportion=1, flag=wx.EXPAND|wx.LEFT|
                    wx.BOTTOM, border=10)
                                
        chat_send_box = wx.BoxSizer(wx.HORIZONTAL)
        
        self.tc = wx.TextCtrl(panel1)
        chat_send_box.Add(self.tc, proportion=1)
        
        sendbtn = wx.Button(panel1, wx.NewId(), label='Send', size=(70, 27))
        self.Bind(wx.EVT_BUTTON, self.OnSend, id=sendbtn.GetId())
        chat_send_box.Add(sendbtn, flag=wx.LEFT, border=5)
        
        chatbox.Add(chat_send_box, flag=wx.EXPAND|wx.BOTTOM|wx.LEFT,
                    border=10)
        panel1.SetSizer(chatbox)
        
        panel2 = wx.Panel(splitter)
        
        listbox = wx.BoxSizer(wx.VERTICAL)
        self.listctr = wx.ListBox(panel2, 26, (-1, -1), (80, 130), 
		['xam_vz', 'g00se'], wx.LB_SINGLE) 
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnListBoxClick, id=self.listctr.GetId())
        listbox.Add(self.listctr, flag=wx.EXPAND|wx.RIGHT, border=10)
        panel2.SetSizer(listbox)
        
        splitter.SetMinimumPaneSize(100)
        splitter.SplitVertically(panel1, panel2)               
        
    def OnSend(self, event):
        if(self.tc.IsEmpty()):
            return
        msgtime = time.strftime('%H:%M:%S', time.localtime(time.time()))                 
        evt = MsgEvent(text='[%s]: %s\n' % (msgtime, self.tc.GetValue()))
        reactor.callLater(2, f.protocol.msg(self.tc.GetValue()))
        wx.PostEvent(self, evt) 
        self.tc.Clear()        
        
    def LoginDlg(self):
        cDlg = LoginDlgView(self, -1, 'Login')
        cDlg.ShowModal()
        cDlg.Destroy()
        
   
    
    def OnUpdateContactList(self, event):
        pass
        
    def OnListBoxClick(self, event):
        index = event.GetSelection()
        nick = self.listctr.GetString(index)
        self.tc.AppendText(nick)
        
    def OnUpdateChatView(self, event):
        pos = self.viewctrl.GetLastPosition()
        self.viewctrl.AppendText(event.text)
        self.viewctrl.SetStyle(pos, pos + 10,  wx.TextAttr("blue"))
        
    
    def OnSettings(self, event):
        print 'fuuu'
        Dlg = SettingsDlg(None, -1, 'Settings')
        Dlg.ShowModal()
        Dlg.Destroy()
        
def clientConnect():
    print 'sss'
    
def error(err):
    state.outstanding-=1
    print "%s" % (err.getErrorMessage())
    
if __name__ == '__main__':
  
    app = wx.App()
    
    cDlg = ConnectionDlgView(None, -1, 'Connect')
    cDlg.ShowModal()    
    reactor.registerWxApp(app)
    reactor.run()
    
