"""
Exports class Chatview
"""
import time
import random

import wx
import wx.lib.newevent

from twisted.internet import reactor

from settingsdlg import SettingsDlg

ErrorEvent, EVT_ERROR_EVENT = wx.lib.newevent.NewEvent()
MsgEvent, EVT_NEW_MSG_EVENT = wx.lib.newevent.NewEvent()


class ChatView(wx.Frame):
    """
    Main Frame that contains text controls for display chat and for 
    add message to chat. Also it contains listbox where are all
    online users.  
    """  
    def __init__(self, parent, title):
        """
        Override __init__ of wx.Frame.           
        """
        super(ChatView, self).__init__(parent, title=title, 
            size=(390, 350))
        
        self.InitUI()
        self.Centre()
        self.users = {}             
        
    def InitUI(self):
        """
        Create all controls to a frame.
        Add binds to catch events
        """
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
        """
        Called when user pushes Send button.
        If message isn't empty call send_msg method of protocol
        and clear text control.
        """
        if(self.tc.IsEmpty()):
            return
        self.protocol.send_msg(self.tc.GetValue())
        self.tc.Clear()        
        
    def OnUpdateContactList(self, names):
        """
        Called when server reports about changings in list of online users
        Update dictionary of online users and set random colors to new users.
         
        *atributes:*
            names -- list of online users

        """
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
        """
        Called when user clicks on nickname in listbox.
         
        Add nickname to textbox to send direct message.
        """
        index = event.GetSelection()
        nick = self.listctr.GetString(index)
        self.tc.AppendText('@%s' % nick)
        
    def OnUpdateChatView(self, sender, destination, text):
        """Called when server reports about adding new message to chat.

        Add time, sender name, destination name (if necessary) to view text control.
        
        *atributes*:
            sender -- nickname of person who send message

            destination -- nickname of person which should received message or '*' if it's broadcast message

            text -- message itself

        """
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
        """
        Called when server reports about service message.
           
        Add sender name and service message to view text control.

        *atributes:*
            sender -- nickname of person who made action

            text -- message itself
        """
        msg = '%s %s\n' % (sender, text)
        pos = self.viewctrl.GetLastPosition()
        self.viewctrl.AppendText(msg)
        colorLen = pos + len(sender)
        rgb = self.users.get(sender, (0, 0, 0))
        color = wx.Color(rgb[0], rgb[1], rgb[2])
        self.viewctrl.SetStyle(pos, colorLen, wx.TextAttr(color))
             
    def OnSettings(self, event):
        """
        Called when user pushes Settings button.
         
        Create SettingsDlg from settingsdlg.
        """
        Dlg = SettingsDlg(self, -1, 'Settings')
        Dlg.ShowModal()
        Dlg.Destroy()
        
    def OnClose(self, event):
        """
        Called when user close the frame.
           
        Send quit message to server and destoy self.
        """
        self.protocol.on_quit('goodbye fellas')
        #reactor.stop()
