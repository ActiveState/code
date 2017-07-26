# -*- coding: iso-8859-1 -*-

import  wx
from twisted.internet import wxreactor
wxreactor.install()
from twisted.internet import reactor
from twisted.web import xmlrpc, server
    

#---------------------------------------------------------------------------

class MyFrame(wx.Frame):
    def __init__(
            self, parent, ID, title, pos=wx.DefaultPosition,
            size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE
            ):

        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
        
        panel = wx.Panel(self, -1)

        button = wx.Button(panel, 1003, "Close Me")
        button.SetPosition((15, 15))
        self.Bind(wx.EVT_BUTTON, self.OnCloseMe, button)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnCloseMe(self, event):
        self.Close(True)
        reactor.stop()

    def OnCloseWindow(self, event):
        self.Destroy()
        reactor.stop()

#---------------------------------------------------------------------------

class MyXMLRPCApp(wx.App, xmlrpc.XMLRPC):
    # Make a mixin of both
    
    # the wx related startup code, building the gui
    def OnInit(self):
        self.frame = MyFrame(None, -1, 'Hallo')
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True

    # some XML-RPC function calls for twisted server
    def xmlrpc_stop(self):
        """Closes the wx application."""
        self.frame.Close() # Sending closing event
        return 'Shutdown initiated'

    def xmlrpc_title(self, x):
        """Return all passed args."""
        self.frame.SetTitle(x)
        return x.upper()

    def xmlrpc_add(self, a, b):
        """Return sum of arguments."""
        return a + b
    


if __name__ == '__main__':

    # Initiliaze MyApp
    app = MyXMLRPCApp(False) # False -> printing stdout/stderr to shell, 
                             # not in an additional wx window
    
    # Make wx application twisted aware
    # Must have to start "wxreactor.install()" on top before
    reactor.registerWxApp(app)    

    # Make a XML-RPC Server listening to port 7080
    reactor.listenTCP(7080, server.Site(app))

    # Start both reactor parts (wx MainLoop and XML-RPC server)
    reactor.run()
    
    
