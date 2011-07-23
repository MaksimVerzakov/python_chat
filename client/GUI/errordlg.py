import wx

def error_dlg(text):
    print text
    dial = wx.MessageDialog(None, text, 'Error', wx.OK|wx.ICON_ERROR)
    dial.ShowModal()


