import wx

def error_dlg(text):
    """
       Create and show message dialog with text.
       
       *atributes:*
           text - Error message       
    """
    dial = wx.MessageDialog(None, text, 'Error', wx.OK|wx.ICON_ERROR)
    dial.ShowModal()


