"""XRC dialog runner.

This module facilitates creating and running simple dialogs that are defined
in XRC files. The XRC file must define OK and Cancel buttons with XRC IDs of
'ID_OK' and 'ID_CANCEL'. The feature to run a dialog will only set and return
values for controls that support GetValue() and SetValue().

Customizing this to support other types of controls is doable.

The basic principle of operation can be summarized with this sample code:

import wx
from wx import xrc
app = wx.PySimpleApp() # assuming you don't already have an app running
# Load the dialog from the resource file.
res = xrc.XmlResource('dialog.xrc')
dlg = res.LoadDialog(None, 'dlgLogin')
dlg.Fit()
# Configure OK & Cancel buttons for default behavior.
dlg.FindWindowByName('ID_OK'    ).SetId(wx.ID_OK)
dlg.FindWindowByName('ID_CANCEL').SetId(wx.ID_CANCEL)
# Run the dialog.
if dlg.ShowModal() == wx.ID_OK:
    print 'OK'
else:
    print 'Cancel'
# Extract results.
print '%r' % dlg.FindWindowByName('fldUser'    ).GetValue()
print '%r' % dlg.FindWindowByName('fldPassword').GetValue()

Once the dialog or frame is created, you are free to use Bind() calls to add
handlers to various controls:

def myHandler(evt):
    print 'click!'
dlg.FindWindowByName('myButton').Bind(wx.EVT_BUTTON, myHandler)
"""

import os
import wx
from wx import xrc


resourceCache = dict()


def insureWxApp():
    """Create an instance of PySimpleApp if there is no app already.
    This is required by wxPython before creating any GUI objects.
    """
    global _wxApp
    _wxApp = wx.GetApp()
    if not _wxApp:
        _wxApp = wx.PySimpleApp()
    return _wxApp


def loadXrc(filePath, reload=False):
    """Return an xrc.XmlResource instance."""
    filePath = os.path.abspath(filePath)
    if reload or (filePath not in resourceCache):
        result = xrc.XmlResource(filePath)
        resourceCache[filePath] = result
    else:
        result = resourceCache[filePath]
    return result


def escapeSuppressor(evt):
    """wx.EVT_CHAR_HOOK handler that suppresses processing ESC.
    By default, if you don't have a Cancel button, wx will trigger the
    OK button when you press ESC. Binding this to a dialog will deactivate
    the ESC key. We need this when there is no Cancel button.
    """
    evt.Skip(evt.GetKeyCode() != wx.WXK_ESCAPE)


def buildDialog(filePath, resourceName, mayCancel, **defaults):
    """Return a configured wx.Dialog.
    Assumes that the OK and Cancel buttons are named ID_OK & ID_CANCEL.
    """
    res = loadXrc(filePath)
    insureWxApp()
    dlg = res.LoadDialog(None, resourceName)
    assert isinstance(dlg, wx.Dialog)
    dlg.Fit()
    fetchWidget = dlg.FindWindowByName
    bOk     = dlg.FindWindowByName('ID_OK')
    bCancel = dlg.FindWindowByName('ID_CANCEL')
    bOk.SetId(wx.ID_OK)
    bCancel.SetId(wx.ID_CANCEL)
    if not mayCancel:
        bCancel.Disable()
        bCancel.Hide()
    for name, value in defaults.items():
        dlg.FindWindowByName(name).SetValue(value)
    if not mayCancel:
        dlg.Bind(wx.EVT_CHAR_HOOK, escapeSuppressor)
    return dlg


def runDialog(dlg, mayCancel, *itemNames):
    """Run the specified dialog and return the values of the named items.
    Return None if the user cancels.
    """
    while True:
        if dlg.ShowModal() == wx.ID_OK:
            result = tuple((dlg.FindWindowByName(name).GetValue()
                            for name in itemNames))
            break
        elif mayCancel:
            result = None
            break
        else:
            wx.Bell()
    return result


def useTemporaryDialog(filePath, resourceName, mayCancel,
                       *itemNames, **defaults):
    """Create a dialog, run it, capture the results, destroy the dialog,
    and return the results.
    Return None if the user cancels.
    """
    dlg = buildDialog(filePath, resourceName, mayCancel, **defaults)
    try:
        result = runDialog(dlg, mayCancel, *itemNames)
    finally:
        dlg.Destroy()
    return result


# --- Sample Dialog ---
def askLogin(defaultUser='', defaultPassword='', mayCancel=True):
    """Return None if user cancels; otherwise (user, password) as unicode."""
    result = useTemporaryDialog('dialog.xrc', 'dlgLogin', mayCancel,
                                'fldUser', 'fldPassword',
                                fldUser=defaultUser,
                                fldPassword=defaultPassword)
    return result


# --- Sample Usage ---
import sys
print askLogin('john_doe', '123', mayCancel=False)
print askLogin()


# --- Sample XRC File named dialog.xrc ---
# Open in XRCed (part of "wxPython Docs Demos & Tools") or wxGlade to edit.
"""
<?xml version="1.0" encoding="utf-8"?>
<resource>
  <object class="wxDialog" name="dlgLogin">
    <title>Login</title>
    <object class="wxBoxSizer">
      <orient>wxVERTICAL</orient>
      <object class="sizeritem">
        <object class="wxFlexGridSizer">
          <cols>2</cols>
          <rows>2</rows>
          <object class="sizeritem">
            <object class="wxStaticText">
              <label>User:</label>
            </object>
            <flag>wxALL|wxALIGN_LEFT|wxALIGN_CENTRE_VERTICAL</flag>
            <border>8</border>
          </object>
          <object class="sizeritem">
            <object class="wxTextCtrl" name="fldUser"/>
            <flag>wxALL|wxEXPAND</flag>
            <border>8</border>
            <minsize>200,20</minsize>
          </object>
          <object class="sizeritem">
            <object class="wxStaticText">
              <label>Password:</label>
            </object>
            <flag>wxALL|wxALIGN_LEFT|wxALIGN_CENTRE_VERTICAL</flag>
            <border>8</border>
          </object>
          <object class="sizeritem">
            <object class="wxTextCtrl" name="fldPassword">
              <style>wxTE_PASSWORD</style>
            </object>
            <flag>wxALL|wxEXPAND</flag>
            <border>8</border>
          </object>
          <growablecols>1</growablecols>
        </object>
        <flag>wxALL|wxEXPAND</flag>
        <border>8</border>
      </object>
      <object class="sizeritem">
        <object class="wxBoxSizer">
          <orient>wxHORIZONTAL</orient>
          <object class="sizeritem">
            <object class="wxButton" name="ID_CANCEL">
              <label>Cancel</label>
            </object>
            <flag>wxALL|wxALIGN_BOTTOM</flag>
            <border>8</border>
          </object>
          <object class="sizeritem">
            <object class="wxButton" name="ID_OK">
              <label>OK</label>
              <default>1</default>
            </object>
            <flag>wxALL|wxALIGN_BOTTOM</flag>
            <border>8</border>
          </object>
        </object>
        <option>1</option>
        <flag>wxBOTTOM|wxLEFT|wxRIGHT|wxALIGN_RIGHT</flag>
        <border>8</border>
      </object>
    </object>
    <centered>1</centered>
    <style>wxDEFAULT_DIALOG_STYLE|wxSTAY_ON_TOP|wxRESIZE_BORDER|wxDIALOG_MODAL|wxTAB_TRAVERSAL</style>
  </object>
</resource>"""
