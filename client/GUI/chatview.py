import time
import random

import wx
import wx.lib.newevent

from twisted.internet import reactor

from settingsdlg import SettingsDlg

ErrorEvent, EVT_ERROR_EVENT = wx.lib.newevent.NewEvent()
MsgEvent, EVT_NEW_MSG_EVENT = wx.lib.newevent.NewEvent()


class ChatView(wx.Frame):
  
    def __init__(self, parent, title):
        super(ChatView, self).__init__(parent, title=title, 
            size=(390, 350))
        
        self.InitUI()
        self.Centre()
        self.users = {}             
        
    def InitUI(self):
        toolbar = self.CreateToolBar()
        ID_SETTINGSTOOL = wx.NewId()
        toolbar.AddLabelTool(ID_SETTINGSTOOL, '',
                             wx.Bitmap('GUI/icons/settings_button.png'))
        toolbar.Realize()
                    
        splitter = wx.SplitterWindow(self, -1)
        left_panel = wx.Panel(splitter)

        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(9)
        
        chatbox = wx.BoxSizer(wx.VERTICAL)

        self.viewctrl = wx.TextCtrl(left_panel, style=wx.TE_MULTILINE|
                                    wx.TE_READONLY)
        chatbox.Add(self.viewctrl, proportion=1, flag=wx.EXPAND|wx.LEFT|
                    wx.BOTTOM, border=10)
                                
        chat_send_box = wx.BoxSizer(wx.HORIZONTAL)
        
        self.tc = wx.TextCtrl(left_panel)
        chat_send_box.Add(self.tc, proportion=1)
        
        sendbtn = wx.Button(left_panel, wx.NewId(), label='Send',
                            size=(70, 27))
        chat_send_box.Add(sendbtn, flag=wx.LEFT, border=5)
        
        chatbox.Add(chat_send_box, flag=wx.EXPAND|wx.BOTTOM|wx.LEFT,
                    border=10)
        left_panel.SetSizer(chatbox)
        
        right_panel = wx.Panel(splitter)
        
        listbox = wx.BoxSizer(wx.VERTICAL)
        self.listctr = wx.ListBox(right_panel, 26, (-1, -1), (80, 130),
                                  [], wx.LB_SINGLE) 
        listbox.Add(self.listctr, flag=wx.EXPAND|wx.RIGHT, border=10)
        right_panel.SetSizer(listbox)
        
        splitter.SetMinimumPaneSize(100)
        splitter.SplitVertically(left_panel, right_panel)  
        
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnListBoxClick,
                  id=self.listctr.GetId())
        self.Bind(wx.EVT_TOOL, self.OnSettings, id=ID_SETTINGSTOOL)
        self.Bind(wx.EVT_BUTTON, self.OnSend, id=sendbtn.GetId())
        self.Bind(wx.EVT_CLOSE, self.OnClose)  
        
        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL, 13, sendbtn.GetId())])
        self.SetAcceleratorTable(accel_tbl)            
        
    def OnSend(self, event):
        if(self.tc.IsEmpty()):
            return
        self.protocol.send_msg(self.tc.GetValue())
        self.tc.Clear()        
        
    def LoginDlg(self):
        cDlg = LoginDlgView(self, -1, 'Login')
        cDlg.ShowModal()
        cDlg.Destroy()
    
    def OnUpdateContactList(self, names):
        self.listctr.Clear()
        self.listctr.AppendItems(names)
        users = {}
        for name in set(names)&set(self.users):
            users[name] = self.users[name]
        for name in set(names) - set(self.users):
            r = random.randrange(0, 255)
            g = random.randrange(0, 255)
            b = random.randrange(0, 255)
            users[name] = (r, g, b)
        self.users = users
        
    def OnListBoxClick(self, event):
        index = event.GetSelection()
        nick = self.listctr.GetString(index)
        self.tc.AppendText('@%s' % nick)
        
    def OnUpdateChatView(self, sender, destination, text):
        msgtime = time.strftime('%H:%M:%S', time.localtime(time.time()))
        if destination == '*':
            destination = ''            
        msg = '(%s) %s: %s %s\n' % (msgtime, sender, destination, text)
        pos = self.viewctrl.GetLastPosition()
        self.viewctrl.AppendText(msg)
        
        colorLen = pos + 10
        rgb = self.users.get(sender, (0, 0, 0))
        color = wx.Color(rgb[0], rgb[1], rgb[2])
        self.viewctrl.SetStyle(pos, colorLen, wx.TextAttr(color))
        
        pos = colorLen + 1
        colorLen = pos + len(sender)
        self.viewctrl.SetStyle(pos, colorLen, wx.TextAttr(color))
        
        pos = colorLen + 2
        colorLen = pos + len(destination)
        rgb = self.users.get(destination, (0, 0, 0))
        color = wx.Color(rgb[0], rgb[1], rgb[2])
        self.viewctrl.SetStyle(pos, colorLen, wx.TextAttr(color))
        
    def OnServiceChatView(self, sender, text):
        msg = '%s %s\n' % (sender, text)
        pos = self.viewctrl.GetLastPosition()
        self.viewctrl.AppendText(msg)
        colorLen = pos + len(sender)
        rgb = self.users.get(sender, (0, 0, 0))
        color = wx.Color(rgb[0], rgb[1], rgb[2])
        self.viewctrl.SetStyle(pos, colorLen, wx.TextAttr(color))
             
    def OnSettings(self, event):
        Dlg = SettingsDlg(self, -1, 'Settings')
        Dlg.ShowModal()
        Dlg.Destroy()
        
    def OnClose(self, event):
        self.protocol.on_quit('')
        self.Destroy()
        
        

