from wxPython.wx import *
from twisted.internet import reactor

class MyApp(wxApp):
    def OnInit(self):
        # Twisted Reactor Code
        reactor.startRunning()
        EVT_TIMER(self,999999,self.OnTimer)
        self.timer=wxTimer(self,999999)
        self.timer.Start(250,False)
        # End Twisted Code
	# Do whatever you need to do here
        return True

    def OnTimer(self,event):
        reactor.runUntilCurrent()
        reactor.doIteration(0)
