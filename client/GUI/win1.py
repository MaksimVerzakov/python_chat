import wx
import wx.lib.newevent
import time

ErrorEvent, EVT_ERROR_EVENT = wx.lib.newevent.NewEvent()
MsgEvent, EVT_NEW_MSG_EVENT = wx.lib.newevent.NewEvent()


def OnError(text):
    dial = wx.MessageDialog(None, text, 'Error', wx.OK|wx.ICON_ERROR)
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

class ChatView(wx.Frame):
  
    def __init__(self, parent, title):
        super(ChatView, self).__init__(parent, title=title, 
            size=(390, 350))
        
        self.InitUI()
        self.Centre()                   
        
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
        self.protocol.sendMSG(str(self.tc.GetValue()))
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
        
    def OnUpdateChatView(self, text):
        msgtime = time.strftime('%H:%M:%S', time.localtime(time.time()))                 
        msg = '[%s]: %s\n' % (msgtime, text)
        pos = self.viewctrl.GetLastPosition()
        self.viewctrl.AppendText(msg)
        self.viewctrl.SetStyle(pos, pos + 10,  wx.TextAttr("blue"))
     
    def OnSettings(self, event):
        print 'fuuu'
        Dlg = SettingsDlg(None, -1, 'Settings')
        Dlg.ShowModal()
        Dlg.Destroy()
        
    
