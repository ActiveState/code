"""This module enables wxPython and twisted to peacefully co-exist.

It does this by running wxPython in the main thread and starting a secondary thread for the twisted library.

It also provides a set of tools to enable communication between the two librarys

WARNING: DON'T use setTimeout on deferreds made/used in wx thread!
"""

import wx
from threading import Thread
from twisted.internet import reactor
from twisted.python import threadable
from twisted.internet.defer import maybeDeferred, Deferred
from time import sleep

# Make our own wxEvent for responding to messages
wxEVT_RESPONSE = wx.NewEventType()

class ResponseEvent(wx.PyCommandEvent):
    """This is our event used to pass net info
    (success, failure, progress, and status)
    to the gui"""

    def __init__(self, func, onSuccess, onFailure, *params, **kwparams):
        wx.PyCommandEvent.__init__(self, wxEVT_RESPONSE, 1)
        self.func = func
        self.onSuccess = onSuccess
        self.onFailure = onFailure
        self.params = params
        self.kwparams = kwparams


class TwistedThread(Thread):
    """Starts twisted in a secondary thread.
    It uses "commands" which are calls to the net thread from the gui thread
    and "responses" which are calls to the gui thread from the net thread
    but as both "commands" and "responses" have "onSuccess" and "onFailure"
    callbacks which must again cross the thread boundary, these are reversed
    so: A call from gui to net is a command, and its onSuccess call is a response
    but a call from net to gui is a "response" and its onSuccess call is a "command"
    so try not to get confused...
    """

    def __init__(self, app, twistedLogFileName=None):
        """'app' is a wx.App instance"""
        Thread.__init__(self)
        self.app = None
        self.twistedLogFileName = twistedLogFileName
        self.setApp(app)
        ThreadCommand.twistedThread = self
        if app:
            self.running = True
            self.start()

    def run(self):
        threadable.init(1)
        if self.twistedLogFileName:
            from twisted.python import log
            self.log = log
            self.log.startLogging(open(self.twistedLogFileName, 'w'), 0)
            self.log.msg('Started')
        reactor.run(installSignalHandlers=0)
        
    # Methods called from gui thread

    def stop(self):
        """Call to cleanup the reactor"""
        ThreadCommand((self._doStop, (), {}), self._onStopped, self._onStopFailed)
    
    def _onStopped(self, res):
        """Called once the reactor has stopped"""
        self.running = False
        
    def _onStopFailed(self, reason):
        self.running = False
        raise Exception('Could not stop reactor: %s' % reason)

    def setApp(self, app):
        """Call this first of all and every time you change
        your application object (like in some testing programs)
        It makes the app subscribe to our special events so that it can
        call your callback functions.
        """
        if app is not self.app:
            if self.app:
                self.app.Disconnect(1, 1, wxEVT_RESPONSE, self._runResponse)
            self.app = app
            self.app.Connect(1, 1, wxEVT_RESPONSE, self._runResponse)

    def runCommand(self, tc):
        """Called from the gui thread, pass a ThreadCommand instance to the
        network"""
        reactor.callFromThread(self._doRunCommand, tc)

    def _runResponse(self, evt):
        """Passes on a response from the net thread.
        Called from wx main loop on reception of an wxEVT_RESPONSE"""
        d = maybeDeferred(evt.func, *evt.params, **evt.kwparams)
        if evt.onSuccess:
            def onDone(r):
                simpleCommand((evt.onSuccess, (r,), {}))
            d.addCallback(onDone)
        if evt.onFailure:
            def onFail(r):
                simpleCommand((evt.onFailure, (r,), {}))
            d.addErrback(onFail)

    # Methods called from net thread
    
    def _doStop(self, tc):
        reactor.stop()

    def _doRunCommand(self, tc):
        """Called in the net thread to execute a gui command"""
        # Run the command and get a deferred
        if tc.passTC: d = maybeDeferred(tc.command[0], tc, *tc.command[1], **tc.command[2])
        else: d = maybeDeferred(tc.command[0], *tc.command[1], **tc.command[2])
        if tc.onSuccess: d.addCallback(self._success, tc)
        if tc.onFailure: d.addErrback(self._failure, tc)
        
    def _success(self, result, tc):
        """Called from the net thread. Appends a ThreadCommand
        success callback to the gui thread's queue"""
        if tc.param:
            evt = ResponseEvent(tc.onSuccess, None, None, tc.param, result)
        else:
            evt = ResponseEvent(tc.onSuccess, None, None, result)
        self.app.AddPendingEvent(evt)

    def _failure(self, reason, tc):
        """Called from the net thread. Appends a ThreadCommand
        failure callback to the gui thread's queue"""
        if tc.param:
            evt = ResponseEvent(tc.onFailure, None, None, tc.param, reason)
        else:
            evt = ResponseEvent(tc.onFailure, None, None, reason)
        self.app.AddPendingEvent(evt)


# Constants for ThreadCommand states
QUEUED, RUNNING, SUCCEEDED, FAILED, CANCELLED = 'queued', 'running', 'succeeded', 'failed', 'cancelled'

class ThreadCommand(object):
    """This object represents a command from the gui
    to the network library"""
    
    twistedThread = None # Filled when a TwistedThread instance is created

    def __init__(self, command, onSuccess, onFailure, param=None, onStatusReport=None, onProgressReport=None, onCustomReport=None, passTC=True):
        """'command' is a tuple containing a function reference, a sequence of parameters and a dictionary of parameters.
        The func will be called but the first arg will be 'self' (this ThreadCommand instance)
        'onSuccess' will be called passing 'param' and the result on success 
        'onFailure' will be called passing 'param' and an error message object on failure
        'param' is passed to all callback funcs, unless it is 'None'
        'onStatusReport' will be called passing a string for showing to the user along with param
        'onProgressReport' will be called passing a float between 0 and 100 along with param
        'onCustomReport' will be called with whatever params and kwparams the caller and server decide on,
        but the first param will be 'param'
        """
        self.command = command
        self.onStatusReport = onStatusReport
        self.onProgressReport = onProgressReport
        self.onSuccess = onSuccess
        self.onFailure = onFailure
        self.onCustomReport = onCustomReport
        self.param = param
        self.state = QUEUED
        self.passTC = passTC
        # Queue ourselves or...
        if self.twistedThread: self.twistedThread.runCommand(self)
        else:
            # Just run in current thread
            import pdb
            pdb.set_trace()
            try:
                if passTC: res = command[0](self, *command[1], **command[2])
                else: res = command[0](*command[1], **command[2])
            except Exception, e:
                if onFailure:
                    if param: onFailure(e, param)
                    else: onFailure(e)
                else:
                    if param: onFailure(e, param)
                    else: onFailure(e)
            if onSuccess:
                if isinstance(res, Deferred):
                    if param: res.addCallback(onSuccess, param)
                    else: res.addCallback(onSuccess)
                else:
                    if param: onSuccess(res, param)
                    else: onSuccess(res)

    
    # Methods called from the net thread
    
    def progressReport(self, done, outOf=100):
        """Passes on a progress report to the gui thread"""
        if self.param:
            if outOf == 100: evt = ResponseEvent(self.onProgressReport, None, None, float(done), self.param)
            else: evt = ResponseEvent(self.onProgressReport, None, None, (done/float(outOf))*100, self.param)
        else:
            if outOf == 100: evt = ResponseEvent(self.onProgressReport, None, None, float(done))
            else: evt = ResponseEvent(self.onProgressReport, None, None, (done/float(outOf))*100)
        self.twistedThread.app.AddPendingEvent(evt)
    
    def statusReport(self, msg):
        """Passes on a status message to the gui"""
        if self.param:
            evt = ResponseEvent(self.onStatusReport, None, None, msg, self.param)
        else:
            evt = ResponseEvent(self.onStatusReport, None, None, msg)
        self.twistedThread.app.AddPendingEvent(evt)
        
    def customReport(self, *params, **kwparams):
        """Passes on a custom event to the gui thread"""
        if self.param:
            evt = ResponseEvent(self.onCustomReport, None, None, self.param, *params, **kwparams)
        else:
            evt = ResponseEvent(self.onCustomReport, None, None, *params, **kwparams)            
        self.twistedThread.app.AddPendingEvent(evt)

def simpleCommand(command, onSuccess=None, onFailure=None, param=None, onStatusReport=None, onProgressReport=None, onCustomReport=None):
    """A convinience function to allow you to call net commands without having to pass a tc"""
    ThreadCommand(command, onSuccess, onFailure, param, onStatusReport, onProgressReport, onCustomReport, False)

def netCall(func, *params, **kwparams):
    """A nice wrapper function, returns a deferred.
    Lets you safely call a function in the net thread
    from the gui thread"""
    d = Deferred()
    simpleCommand((func, params, kwparams), d.callback, d.errback)
    return d
    
def makeNetSafe(func):
    """Makes NET function safe for calling from the GUI thread.
    Takes a func and returns a thread safe version of it
    for calling a net func from the gui func"""
    def result(*params, **kwparams):
        return netCall(func, *params, **kwparams)
    return result

def guiCall(func, *params, **kwparams):
    """Calls a gui func safely from the net thread"""
    d = Deferred()
    evt = ResponseEvent(func, d.callback, d.errback, *params, **kwparams)
    ThreadCommand.twistedThread.app.AddPendingEvent(evt)
    return d

def makeGuiSafe(func):
    """Makes a GUI function safe for calling from the NET thread.
    Returns a wrapper func that allows you to
    safely call the gui func 'func' from the net thread"""
    def result(*params, **kwparams):
        return guiCall(func, *params, **kwparams)
    return result


---------------- 8< -----------------------------
Chat example files
---------------- 8< -----------------------------
chatDemo.wxg - A wxGlade file, used to generate chatExampleGui.py
---------------- 8< -----------------------------

<?xml version="1.0"?>
<!-- generated by wxGlade 0.3.2 on Mon Jul 05 14:12:09 2004 -->

<application path="C:\work\play\chatExample\chatExampleGui.py" name="" class="" option="0" language="python" top_window="" encoding="ANSI_X3.4-1968" use_gettext="0" overwrite="0" use_new_namespace="1">
    <object class="ChatFrameGui" name="frmMain" base="EditFrame">
        <style>wxDEFAULT_FRAME_STYLE</style>
        <title>Chat</title>
        <statusbar>1</statusbar>
        <object class="wxStatusBar" name="frmMain_statusbar" base="EditStatusBar">
            <fields>
                <field width="-1">frmMain_statusbar</field>
            </fields>
        </object>
        <object class="wxBoxSizer" name="sizer_1" base="EditBoxSizer">
            <orient>wxVERTICAL</orient>
            <object class="sizeritem">
                <flag>wxEXPAND</flag>
                <border>0</border>
                <option>1</option>
                <object class="wxPanel" name="panel_1" base="EditPanel">
                    <style>wxRAISED_BORDER|wxTAB_TRAVERSAL</style>
                    <object class="wxBoxSizer" name="sizer_3" base="EditBoxSizer">
                        <orient>wxVERTICAL</orient>
                        <object class="sizeritem">
                            <flag>wxEXPAND</flag>
                            <border>0</border>
                            <option>0</option>
                            <object class="wxPanel" name="panel_4" base="EditPanel">
                                <style>wxTAB_TRAVERSAL</style>
                                <object class="wxBoxSizer" name="sizer_4" base="EditBoxSizer">
                                    <orient>wxHORIZONTAL</orient>
                                    <object class="sizeritem">
                                        <flag>wxALL|wxALIGN_RIGHT|wxALIGN_CENTER_VERTICAL</flag>
                                        <border>3</border>
                                        <option>0</option>
                                        <object class="wxStaticText" name="lblIpAddress" base="EditStaticText">
                                            <attribute>1</attribute>
                                            <label>IP &amp;Address</label>
                                            <size>51, 13</size>
                                        </object>
                                    </object>
                                    <object class="sizeritem">
                                        <flag>wxALL|wxEXPAND</flag>
                                        <border>3</border>
                                        <option>1</option>
                                        <object class="wxTextCtrl" name="edtIPAddress" base="EditTextCtrl">
                                            <tooltip>The ip address or host name of a remote machine running chat</tooltip>
                                            <value>127.0.0.1</value>
                                        </object>
                                    </object>
                                    <object class="sizeritem">
                                        <flag>wxALL|wxEXPAND</flag>
                                        <border>3</border>
                                        <option>0</option>
                                        <object class="wxSpinCtrl" name="spnConnectPort" base="EditSpinCtrl">
                                            <style>wxSP_ARROW_KEYS|wxSP_WRAP</style>
                                            <tooltip>The port on which the remote chat program is listening</tooltip>
                                            <range>1, 65535</range>
                                            <value>8080</value>
                                        </object>
                                    </object>
                                    <object class="sizeritem">
                                        <flag>wxALL</flag>
                                        <border>3</border>
                                        <option>0</option>
                                        <object class="wxToggleButton" name="btnConnect" base="EditToggleButton">
                                            <label>&amp;Connect</label>
                                        </object>
                                    </object>
                                </object>
                            </object>
                        </object>
                        <object class="sizeritem">
                            <flag>wxEXPAND</flag>
                            <border>0</border>
                            <option>0</option>
                            <object class="wxPanel" name="panel_3" base="EditPanel">
                                <style>wxTAB_TRAVERSAL</style>
                                <object class="wxBoxSizer" name="sizer_6" base="EditBoxSizer">
                                    <orient>wxHORIZONTAL</orient>
                                    <object class="sizeritem">
                                        <flag>wxALL|wxALIGN_RIGHT|wxALIGN_CENTER_VERTICAL</flag>
                                        <border>3</border>
                                        <option>0</option>
                                        <object class="wxStaticText" name="lblListenPort" base="EditStaticText">
                                            <attribute>1</attribute>
                                            <label>Listen &amp;on port</label>
                                            <size>64, 13</size>
                                        </object>
                                    </object>
                                    <object class="sizeritem">
                                        <flag>wxALL|wxEXPAND</flag>
                                        <border>3</border>
                                        <option>1</option>
                                        <object class="wxSpinCtrl" name="spnListenPort" base="EditSpinCtrl">
                                            <style>wxSP_ARROW_KEYS|wxSP_WRAP</style>
                                            <tooltip>The port on which to listen for incoming connections</tooltip>
                                            <range>1, 65535</range>
                                            <value>8080</value>
                                        </object>
                                    </object>
                                    <object class="sizeritem">
                                        <flag>wxALL</flag>
                                        <border>3</border>
                                        <option>0</option>
                                        <object class="wxToggleButton" name="btnListen" base="EditToggleButton">
                                            <tooltip>Listen for incoming connections</tooltip>
                                            <label>Lis&amp;ten</label>
                                        </object>
                                    </object>
                                </object>
                            </object>
                        </object>
                        <object class="sizeritem">
                            <border>0</border>
                            <option>0</option>
                            <object class="wxStaticText" name="lblReceived" base="EditStaticText">
                                <attribute>1</attribute>
                                <label>Received</label>
                            </object>
                        </object>
                        <object class="sizeritem">
                            <flag>wxEXPAND</flag>
                            <border>0</border>
                            <option>1</option>
                            <object class="wxTextCtrl" name="edtReceived" base="EditTextCtrl">
                                <foreground>#000000</foreground>
                                <style>wxTE_MULTILINE|wxTE_READONLY|wxTE_RICH2|wxTE_AUTO_URL</style>
                                <background>#c0c0c0</background>
                            </object>
                        </object>
                        <object class="sizeritem">
                            <border>0</border>
                            <option>0</option>
                            <object class="wxStaticText" name="lblSent" base="EditStaticText">
                                <attribute>1</attribute>
                                <label>Sent:</label>
                            </object>
                        </object>
                        <object class="sizeritem">
                            <flag>wxEXPAND</flag>
                            <border>0</border>
                            <option>1</option>
                            <object class="wxTextCtrl" name="edtSent" base="EditTextCtrl">
                                <style>wxTE_MULTILINE|wxTE_READONLY|wxTE_RICH2|wxTE_AUTO_URL</style>
                                <background>#c0c0c0</background>
                            </object>
                        </object>
                    </object>
                </object>
            </object>
            <object class="sizeritem">
                <flag>wxEXPAND</flag>
                <border>0</border>
                <option>0</option>
                <object class="wxPanel" name="panel_2" base="EditPanel">
                    <style>wxRAISED_BORDER|wxTAB_TRAVERSAL</style>
                    <object class="wxBoxSizer" name="sizer_2" base="EditBoxSizer">
                        <orient>wxHORIZONTAL</orient>
                        <object class="sizeritem">
                            <flag>wxALL|wxEXPAND</flag>
                            <border>5</border>
                            <option>1</option>
                            <object class="wxTextCtrl" name="edtToSend" base="EditTextCtrl">
                            </object>
                        </object>
                        <object class="sizeritem">
                            <flag>wxALL</flag>
                            <border>4</border>
                            <option>0</option>
                            <object class="wxButton" name="btnSend" base="EditButton">
                                <default>1</default>
                                <label>&amp;Send</label>
                            </object>
                        </object>
                        <object class="sizeritem">
                            <flag>wxALL</flag>
                            <border>4</border>
                            <option>0</option>
                            <object class="wxButton" name="btnClose" base="EditButton">
                                <label>&amp;Close</label>
                            </object>
                        </object>
                    </object>
                </object>
            </object>
        </object>
    </object>
</application>
---------------- 8< -----------------------------
chatExampleGui.py - The wx bits
---------------- 8< -----------------------------
#!/usr/bin/env python
# generated by wxGlade 0.3.2 on Sun Jul  4 09:38:17 2004

import wx

class ChatFrameGui(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: ChatFrameGui.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.panel_2 = wx.Panel(self, -1, style=wx.RAISED_BORDER|wx.TAB_TRAVERSAL)
        self.panel_1 = wx.Panel(self, -1, style=wx.RAISED_BORDER|wx.TAB_TRAVERSAL)
        self.panel_3 = wx.Panel(self.panel_1, -1)
        self.panel_4 = wx.Panel(self.panel_1, -1)
        self.frmMain_statusbar = self.CreateStatusBar(1)
        self.lblIpAddress = wx.StaticText(self.panel_4, -1, "IP &Address")
        self.edtIPAddress = wx.TextCtrl(self.panel_4, -1, "127.0.0.1")
        self.spnConnectPort = wx.SpinCtrl(self.panel_4, -1, "8080", min=1, max=65535, style=wx.SP_ARROW_KEYS|wx.SP_WRAP)
        self.btnConnect = wx.ToggleButton(self.panel_4, -1, "&Connect")
        self.lblListenPort = wx.StaticText(self.panel_3, -1, "Listen &on port")
        self.spnListenPort = wx.SpinCtrl(self.panel_3, -1, "8080", min=1, max=65535, style=wx.SP_ARROW_KEYS|wx.SP_WRAP)
        self.btnListen = wx.ToggleButton(self.panel_3, -1, "Lis&ten")
        self.lblReceived = wx.StaticText(self.panel_1, -1, "Received")
        self.edtReceived = wx.TextCtrl(self.panel_1, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH2|wx.TE_AUTO_URL)
        self.lblSent = wx.StaticText(self.panel_1, -1, "Sent:")
        self.edtSent = wx.TextCtrl(self.panel_1, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH2|wx.TE_AUTO_URL)
        self.edtToSend = wx.TextCtrl(self.panel_2, -1, "")
        self.btnSend = wx.Button(self.panel_2, -1, "&Send")
        self.btnClose = wx.Button(self.panel_2, -1, "&Close")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: ChatFrameGui.__set_properties
        self.SetTitle("Chat")
        self.frmMain_statusbar.SetStatusWidths([-1])
        # statusbar fields
        frmMain_statusbar_fields = ["frmMain_statusbar"]
        for i in range(len(frmMain_statusbar_fields)):
            self.frmMain_statusbar.SetStatusText(frmMain_statusbar_fields[i], i)
        self.lblIpAddress.SetSize((51, 13))
        self.edtIPAddress.SetToolTipString("The ip address or host name of a remote machine running chat")
        self.spnConnectPort.SetToolTipString("The port on which the remote chat program is listening")
        self.lblListenPort.SetSize((64, 13))
        self.spnListenPort.SetToolTipString("The port on which to listen for incoming connections")
        self.btnListen.SetToolTipString("Listen for incoming connections")
        self.edtReceived.SetBackgroundColour(wx.Colour(192, 192, 192))
        self.edtReceived.SetForegroundColour(wx.Colour(0, 0, 0))
        self.edtSent.SetBackgroundColour(wx.Colour(192, 192, 192))
        self.btnSend.SetDefault()
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: ChatFrameGui.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4.Add(self.lblIpAddress, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 3)
        sizer_4.Add(self.edtIPAddress, 1, wx.ALL|wx.EXPAND, 3)
        sizer_4.Add(self.spnConnectPort, 0, wx.ALL|wx.EXPAND, 3)
        sizer_4.Add(self.btnConnect, 0, wx.ALL, 3)
        self.panel_4.SetAutoLayout(1)
        self.panel_4.SetSizer(sizer_4)
        sizer_4.Fit(self.panel_4)
        sizer_4.SetSizeHints(self.panel_4)
        sizer_3.Add(self.panel_4, 0, wx.EXPAND, 0)
        sizer_6.Add(self.lblListenPort, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 3)
        sizer_6.Add(self.spnListenPort, 1, wx.ALL|wx.EXPAND, 3)
        sizer_6.Add(self.btnListen, 0, wx.ALL, 3)
        self.panel_3.SetAutoLayout(1)
        self.panel_3.SetSizer(sizer_6)
        sizer_6.Fit(self.panel_3)
        sizer_6.SetSizeHints(self.panel_3)
        sizer_3.Add(self.panel_3, 0, wx.EXPAND, 0)
        sizer_3.Add(self.lblReceived, 0, 0, 0)
        sizer_3.Add(self.edtReceived, 1, wx.EXPAND, 0)
        sizer_3.Add(self.lblSent, 0, 0, 0)
        sizer_3.Add(self.edtSent, 1, wx.EXPAND, 0)
        self.panel_1.SetAutoLayout(1)
        self.panel_1.SetSizer(sizer_3)
        sizer_3.Fit(self.panel_1)
        sizer_3.SetSizeHints(self.panel_1)
        sizer_1.Add(self.panel_1, 1, wx.EXPAND, 0)
        sizer_2.Add(self.edtToSend, 1, wx.ALL|wx.EXPAND, 5)
        sizer_2.Add(self.btnSend, 0, wx.ALL, 4)
        sizer_2.Add(self.btnClose, 0, wx.ALL, 4)
        self.panel_2.SetAutoLayout(1)
        self.panel_2.SetSizer(sizer_2)
        sizer_2.Fit(self.panel_2)
        sizer_2.SetSizeHints(self.panel_2)
        sizer_1.Add(self.panel_2, 0, wx.EXPAND, 0)
        self.SetAutoLayout(1)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        sizer_1.SetSizeHints(self)
        self.Layout()
        # end wxGlade

# end of class ChatFrameGui
---------------- 8< -----------------------------
chatExample.py - Notice the various different uses of the library.
Refer to comment above for easiest use (makeNetSafe, netCall, makeGuiSafe, guiCall). guiCall is not tested, haven't needed to use it yet.
---------------- 8< -----------------------------
import wx
from chatExampleGui import ChatFrameGui
from guinet import TwistedThread, ThreadCommand, netCall, makeNetSafe, guiCall, makeGuiSafe
from wxPython.lib.evtmgr import eventManager
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory, ClientFactory
from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.python.failure import Failure

###############################################################################
## Classes that run in the net thread #########################################
###############################################################################

class ChatProtocol(LineReceiver):

    def __init__(self):
        self.setLineMode()


    def dataReceived(self, data):
        LineReceiver.dataReceived(self, data)

    def lineReceived(self, line):
        self.factory.onLine(line)

class ChatFactory(Factory):
    
    protocol = ChatProtocol
    
    def __init__(self, tc, onConnectionMade, onLine):
        self.tc = tc
        self.onConnectionMade = onConnectionMade
        self.onLine = onLine
        
    def buildProtocol(self, addr):
        p = ChatProtocol()
        p.factory = self
        self.onConnectionMade(p, addr)
        return p
    
class ChatClientFactory(ClientFactory):
    
    def __init__(self, deferred, tc, onConnectionMade):
        self.tc = tc
        self.deferred = deferred
        self.onConnectionMade = onConnectionMade
    
    def startedConnecting(self, connector):
        self.tc.customReport('Started to connect.')
    
    def buildProtocol(self, addr):
        p = ChatProtocol()
        p.factory = self
        self.deferred.callback('Connected')
        self.onConnectionMade(p)
        return p
    
    def clientConnectionLost(self, connector, reason):
        self.tc.customReport('Lost connection.  Reason: %s' % reason)
    
    def clientConnectionFailed(self, connector, reason):
        self.deferred.errback(Failure('Connection failed. Reason: %s' % reason))
        
    def onLine(self, line):
        self.tc.statusReport(line)


###############################################################################
## Classes that run in the gui thread #########################################
###############################################################################

class ChatServer(object):
    """This object is created in the gui thread
    and allows for communication between the threads"""
    
    def __init__(self, app, onStarted, onFailed, onLine, onMsg):
        self.app = app
        self.onStarted = onStarted
        self.onFailed = onFailed
        self.onLine = onLine
        self.onMsg = onMsg
        self.started = False

    def start(self, port):
        ThreadCommand((self._doStart, [port], {}),
                      self.onStarted, self.onFailed, onStatusReport=self.onLine,
                      onCustomReport=self.onMsg)
        self.started = True

    def stop(self, onStopped, onFail):
        ThreadCommand((self._doStop, (), {}), onStopped, onFail)
        self.started = False

    def send(self, line):
        """Sends a line to the other end"""
        return self.connection.transport.write(str(line) + '\r\n')
    # This is soooo coool. Just call self.send from the gui
    # and your data is sent. (it returns a deferred by the way)
    send = makeNetSafe(send)

    # Methods called from net thread
    
    def _doStart(self, tc, port):
        """Starts the factory"""
        self.factory = ChatFactory(tc, self._doOnConnectionMade, self._doOnLine)
        self.port = reactor.listenTCP(int(port), self.factory)
        
    def _doStop(self, tc):
        """Stops listening"""
        self.port.stopListening()
        
    def _doOnConnectionMade(self, connection, addr):
        """Receives an instance of 'ChatProtocol' for each incoming connection"""
        self.connection = connection  # We only really handle one connection at a time
        guiCall(self.onMsg, 'Connection from %s' % addr)
        
    def _doOnLine(self, line):
        """Passes the on line received event to the gui"""
        self.factory.tc.statusReport(line)


class ChatClient(object):
    """A nice interface to be used from the gui"""

    # Methods called in the gui thread
    
    def connect(self, server, port, onSuccess, onFailure, onLine, onMsg):
        ThreadCommand((self._doConnect, (server, port), {}), onSuccess, onFailure, onStatusReport=onLine, onCustomReport=onMsg)
        
    def disconnect(self, onDone, onErr):
        ThreadCommand((self._doDisconnect, (), {}), onDone, onErr)

    def send(self, line):
        """Sends the line"""
        return netCall(self._doSend, line)

    # Methods called in the net thread
    
    def _doConnect(self, tp, server, port):
        d = Deferred()
        self.factory = ChatClientFactory(d, tp, self.onConnectionMade)
        self.connector = reactor.connectTCP(server, int(port), self.factory)
        return d
        
    def _doDisconnect(self, tp):
        return self.connector.disconnect()

    def _doSend(self, line):
        self.connection.transport.write(str(line) + '\r\n')

    def onConnectionMade(self, connection):
        """Called once we have connected."""
        self.connection = connection

class ChatFrame(ChatFrameGui):
    
    def __init__(self):
        ChatFrameGui.__init__(self, None, -1, 'Chat')
        self._assignEvents()
        self.server = ChatServer(wx.GetApp(), self.onServerStarted, self.onServerFailed, self.onLine, self.onMsg)
        self.client = ChatClient()
        
    def _assignEvents(self):
        eventManager.Register(self.onListen, wx.EVT_TOGGLEBUTTON, self.btnListen)
        eventManager.Register(self.onConnect, wx.EVT_TOGGLEBUTTON, self.btnConnect)
        eventManager.Register(lambda e: self.Close(), wx.EVT_BUTTON, self.btnClose)
        eventManager.Register(self.onSend, wx.EVT_BUTTON, self.btnSend)
        
    # Event handlers for gui framework
        
    def onListen(self, evt):
        """Starts or stops listening"""
        if evt.Checked():
            self.server.start(self.spnListenPort.GetValue())
        else:
            self.server.stop(self.onServerStopped, self.onServerFailed)
    
    def onConnect(self, evt):
        """Called from connect button. Connects to a server"""
        if evt.Checked():
            self.client.connect(self.edtIPAddress.GetValue(), self.spnConnectPort.GetValue(),
                                self.onClientConnected, self.onClientFailed, self.onLine,
                                self.onClientMsg)
        else:
            self.client.disconnect(lambda tc: self.onClientMsg('Client disconnected'), self.onClientFailed)
    
    def onSend(self, evt):
        """Sends the stuff in edtToSend"""
        line = self.edtToSend.GetValue()
        if not line: return
        if self.server.started:
            d = self.server.send(line)
        else:
            d = self.client.send(line)
        d.addCallback(self.onSent, line)
        d.addErrback(self.onSendFailed, line)
        self.edtToSend.SetValue('')
        self.edtToSend.SetFocus()

    def onSent(self, result, line):
        """Called once some text has been succesfully sent"""
        self.edtSent.AppendText(line + '\n')

    def onSendFailed(self, reason, line):
        """Called if a send failed"""
        wx.MessageBox(str(reason), 'Could not send %s' % line, wx.OK|wx.ICON_ERROR, self)

    # Event handlers for net framework
        
    def onServerStarted(self, server):
        """Called once the server has started listening"""
        self.GetStatusBar().SetStatusText('Server started')
        
    def onServerStopped(self, server):
        """The server has been stopped by the user"""
        self.GetStatusBar().SetStatusText('Server stopped')
        
    def onServerFailed(self, reason):
        """Called if the server can't listen"""
        self.btnListen.SetValue(False)
        wx.MessageBox(reason, 'Server Failed', wx.OK|wx.ICON_ERROR, self)
        self.GetStatusBar().SetStatusText('Server failed: %s' % reason)
        
    def onClientConnected(self, c):
        self.GetStatusBar().SetStatusText('Client Connected')
        
    def onClientFailed(self, reason):
        self.btnConnect.SetValue(False)
        wx.MessageBox(str(reason), 'Client Connection Failed', wx.OK|wx.ICON_ERROR, self)
        self.GetStatusBar().SetStatusText('Client Connection Failed: %s' % reason)
        
    def onClientMsg(self, msg, extra=None):
        if isinstance(msg, Failure):
            msg = msg.getErrorMessage()
        self.GetStatusBar().SetStatusText(msg)
        
    def onLine(self, line):
        """Called when a line is received from the other end"""
        self.edtReceived.AppendText(line + '\n')
    
    def onMsg(self, msg):
        """Called when the server has a message for us"""
        self.GetStatusBar().SetStatusText(msg)


class App(wx.App):
    
    def OnInit(self):
        self.twistedThread = TwistedThread(self, 'twistd.log')
        #self.twistedThread = TwistedThread(self)
        from twisted.internet.defer import Deferred
        Deferred.debug = 1
        self.main = ChatFrame()
        eventManager.Register(self.onClose, wx.EVT_CLOSE, self.main)
        self.main.Show()
        return True
    
    def onClose(self, evt):
        """Stops the twisted threads"""
        self.twistedThread.stop()
        evt.Skip()


if __name__ == '__main__':
    a = App(0)
    a.MainLoop()
