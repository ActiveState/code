import psyco
psyco.full()
#import win32traceutil
import sys
try:
	sys.setdefaultencoding('dbcs')
except:
	print 'encoding dbcs error!'
import os
if sys.platform == "win32":
	import msvcrt
	try:
		msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
	except:
		print 'Native std error!'
import gc
import threading
import wx
import gettext

class wxpbr(wx.App):
    def __init__(self,parent,*arg,**kwd):
        wx.App.__init__(self,redirect=0,*arg,**kwd)
        self.parent=parent
        self.title=self.parent.title
        self.text=self.parent.text
        self.max=self.parent.max
        self.style=self.parent.style
        self.count=self.parent.count
        self.status=self.parent.status
        self.dlg=0
    def OnInit(self):
        wx.InitAllImageHandlers()
        self.cscpbr=wx.Frame(None, -1, "")
        self.SetTopWindow(self.cscpbr)
        self.Bind(wx.EVT_TIMER, self.pbrm)
        self.t1 = wx.Timer(self.cscpbr)
        self.t1.Start(1)
        return 1
    def pbrm(self, evt):
        if self.dlg:
            if self.text<>self.parent.text or self.count<>self.parent.count:
                self.text=self.parent.text
                self.count=self.parent.count
                self.parent.status=self.status=self.dlg.Update(self.count,self.text)
        else:
            self.dlg = wx.ProgressDialog(self.title,self.text,self.max,self.cscpbr,self.style)
            self.dlg.Bind(wx.EVT_CLOSE, self.close)
        if self.count>=self.max:
            self.parent.status=self.status=True
            self.close(None)
        elif self.parent.stop or (not self.status):
            self.parent.status=self.status=False
            self.close(None)
    def close(self,evt):
        self.parent.stop=1
        self.dlg.Destroy()
        self.cscpbr.Close(True)
class pbr(threading.Thread,object):
    def __init__(self,title,text,max,style,*arg,**kwd):
        threading.Thread.__init__(self,*arg,**kwd)
        self.arg=arg
        self.kwd=kwd
        self.title=title
        self.text=text
        self.max=max
        self.style=style
        self.count=0
        self.status=True
        self.stop=0
        #self.pb=wxpbr(self.title,self.text,self.max,self.style,*self.arg,**self.kwd)
    def run(self):
        self.pb=wxpbr(self,*self.arg,**self.kwd)
        self.pb.MainLoop()
    def close(self):
        self.stop=1
def pbar(title="Progress dialog example",
        text="An informative message",
        max=100,
        style=wx.PD_CAN_ABORT|wx.PD_AUTO_HIDE|wx.PD_SMOOTH|wx.PD_ELAPSED_TIME|wx.PD_ESTIMATED_TIME|wx.PD_REMAINING_TIME,
        *arg,**kwd):
    sys.setcheckinterval(0)
    gettext.install("wxpbr")
    app = pbr(title,text,max,style,*arg,**kwd)
    app.start()
    return app
def pbardemo():
    app=pbar()
    for x in range(0,app.max+1):
        app.count=x
        wx.MilliSleep(100)
        app.text="%s%%"%(x)
        if app.stop:
            break
    print app.status
if __name__ == "__main__":
    pbardemo()
