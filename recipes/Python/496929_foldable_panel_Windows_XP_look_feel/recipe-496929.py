#Simple foldable panels. Layout lifted off Windows. Use at your own risk!
#Code put in the public domain, for someone else could find a use for it.

import wx
#from images import Images

#---------------------------------------------------------------------------
#following code is normaly hidden in images.py
#---------------------------------------------------------------------------
import wx
from cStringIO import StringIO
from binascii import a2b_base64

class Images:
    def __init__(self):
        for name in _names:
            img = wx.ImageFromStream(StringIO(a2b_base64(eval("_"+name))))
            img.ConvertAlphaToMask(100)
            exec("self.bmp_"+name+"=img.ConvertToBitmap()")
        self._names=_names

_names=['bd', 'bdb', 'bu', 'bub', 'wd', 'wdb', 'wu', 'wub']

_bd="iVBORw0KGgoAAAANSUhEUgAAABEAAAAQCAYAAADwMZRfAAAABmJLR0QA/wD/AP+gvaeTAAAA\
CXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH1QgCEC0fpVpQHAAAAB10RVh0Q29tbWVudABDcmVhd\
GVkIHdpdGggVGhlIEdJTVDvZCVuAAAAJ0lEQVR42mNgGAXEgv9QTEiMJIPwGsBIhEHEqiXaoNEwoT\
BMRjIAACcEE/EBpo2WAAAAAElFTkSuQmCC"

_bdb="iVBORw0KGgoAAAANSUhEUgAAABEAAAAQCAYAAADwMZRfAAAABmJLR0QA/wD/AP+gvaeTAAA\
ACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH1QgCEC0JUY7lTQAAAB10RVh0Q29tbWVudABDcmVh\
dGVkIHdpdGggVGhlIEdJTVDvZCVuAAAATklEQVR42u2SQQrAMAgEs325vnx6ySGXVoMJuWRABMEBF\
wXQqlQlZsbTFrBVQq9o9ivRsDh2zZ6jjCCTiSJBNhPdTD5FZz52CgG4e0nyAuqUHhOGDvckAAAAAE\
lFTkSuQmCC"

_bu="iVBORw0KGgoAAAANSUhEUgAAABEAAAAQCAYAAADwMZRfAAAABmJLR0QA/wD/AP+gvaeTAAAA\
CXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH1QgCECoWk8d+fwAAAB10RVh0Q29tbWVudABDcmVhd\
GVkIHdpdGggVGhlIEdJTVDvZCVuAAAAK0lEQVR42mNgGHHgPyEFjCQYgFMtExEGMBLrImwG/CdCbD\
RMKAiTUUAGAAAJFA/7QbaUdQAAAABJRU5ErkJggg=="

_bub="iVBORw0KGgoAAAANSUhEUgAAABEAAAAQCAYAAADwMZRfAAAABmJLR0QA/wD/AP+gvaeTAAA\
ACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH1QgCECosVcunzQAAAB10RVh0Q29tbWVudABDcmVh\
dGVkIHdpdGggVGhlIEdJTVDvZCVuAAAATUlEQVR42uXSMQrAMAxD0cj04PbJf/dAE4FDl2jU8AYhA\
YxuukhmEuNAHIQuggOFAWgHhQksoecD0QRq6m7fZNXZZzvy2H8QAVRVC3kBY3EeFIhSPfsAAAAASU\
VORK5CYII="

_wd="iVBORw0KGgoAAAANSUhEUgAAABEAAAAQCAYAAADwMZRfAAAABmJLR0QA/wD/AP+gvaeTAAAA\
CXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH1QgCECwtdJYw3QAAAB10RVh0Q29tbWVudABDcmVhd\
GVkIHdpdGggVGhlIEdJTVDvZCVuAAAAKUlEQVR42mNgGAVEgf9QQEiMJIMIGcBIyCC4QkZGRoq8Nh\
omVAqTEQ4A+cRPu0JNXG8AAAAASUVORK5CYII="

_wdb="iVBORw0KGgoAAAANSUhEUgAAABEAAAAQCAYAAADwMZRfAAAABmJLR0QA/wD/AP+gvaeTAAA\
ACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH1QgCECwQLP58zAAAAB10RVh0Q29tbWVudABDcmVh\
dGVkIHdpdGggVGhlIEdJTVDvZCVuAAAAVUlEQVR42uWSSwrAMAgF83pyPfl0UyGUNh9syKJvIwgOO\
iiAkk0WYmYc5YOsg3Cl12tCJKn2FTX6w+fcQW+ArpMYbAGGnNQb/dnJE2jPx85GAO6egpwFJkgTeB\
7jjAAAAABJRU5ErkJggg=="

_wu="iVBORw0KGgoAAAANSUhEUgAAABEAAAAQCAYAAADwMZRfAAAABmJLR0QA/wD/AP+gvaeTAAAA\
CXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH1QgCECsIcNNyXQAAAB10RVh0Q29tbWVudABDcmVhd\
GVkIHdpdGggVGhlIEdJTVDvZCVuAAAAM0lEQVR42mNgGFng/////wmpYSTWAEZGRpxqmQgZANNMjI\
swDEDXhE1sNEwoCJNRQB4AAEnQP9cbKVhHAAAAAElFTkSuQmCC"

_wub="iVBORw0KGgoAAAANSUhEUgAAABEAAAAQCAYAAADwMZRfAAAABmJLR0QA/wD/AP+gvaeTAAA\
ACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH1QgCECsgRWbapwAAAB10RVh0Q29tbWVudABDcmVh\
dGVkIHdpdGggVGhlIEdJTVDvZCVuAAAAT0lEQVR42u3SwQrAMAgD0Cbsw/XLs8t6K0RQdmqOAR8iQ\
pJWN10kIsQ1EE5sygrgIDoAABzECuCg51TuoT2IL/cmvis/28jH/oZAkjKzhbzRt0gLkdhH3gAAAA\
BJRU5ErkJggg=="
#---------------------------------------------------------------------------
#end of images.py
#---------------------------------------------------------------------------

class FoldPanel(wx.Panel,Images):
    def __init__(self,parent,psizer,title,tooltip=None,rimcolour="light grey",
                                bgcolour="white",txtcolour="black",is_open=1):
        wx.Panel.__init__(self, parent, -1)
        Images.__init__(self)

        self.is_open=is_open
        #XXX It won't work properly without refreshing the parent sizer/panel.
        self.parentsizer=psizer
        self.parent=parent

        #now can add more than 1 page...
        self.pages=[]

        #the enter/leave counter
        self.counter_enterleave = 0

        self.rimcolour,self.bgcolour,self.txtcolour=rimcolour,bgcolour,txtcolour
        self.SetBackgroundColour(rimcolour)

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        box = wx.BoxSizer(wx.HORIZONTAL)

        #title panel
        self.tpanel = wx.Panel(self, -1)
        self.title=wx.StaticText( self.tpanel, -1, title)
        self.title.SetFont(wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.title.SetForegroundColour(txtcolour)
        
        if is_open==1:
            if txtcolour=="black": bmp = self.bmp_bu
            else: bmp = self.bmp_wu
        else:
            if txtcolour=="black": bmp = self.bmp_bd
            else: bmp = self.bmp_wd

        self.sb=wx.StaticBitmap(self.tpanel, -1, bmp,
                size=(bmp.GetWidth(), bmp.GetHeight()))

        box.Add(self.title,1, wx.EXPAND|wx.LEFT|wx.TOP,5)
        box.Add(self.sb,0,wx.ALL,4)

        if tooltip is not None:
            self.sb.SetToolTipString(tooltip)
            self.title.SetToolTipString(tooltip)
            self.tpanel.SetToolTipString(tooltip)

        cursor = wx.StockCursor(wx.CURSOR_HAND)
        self.tpanel.SetCursor(cursor)
        self.tpanel.SetSizer(box)

        self.vbox.Add(self.tpanel,0,wx.EXPAND)

        #page panel
        self.ppanel = wx.Panel(self, -1)
        self.ppanel.SetBackgroundColour(self.bgcolour)

        self.pbox = wx.BoxSizer(wx.VERTICAL)
        self.pbox.Layout()
        self.ppanel.SetSizer(self.pbox)

        self.vbox.Add(self.ppanel,1,wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT,1)

        if self.is_open==0:
            self.vbox.Hide(self.ppanel)

        self.vbox.Layout()
        self.SetSizer(self.vbox)

        self.sb.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
        self.sb.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        self.sb.Bind(wx.EVT_LEFT_UP, self.OnButton)

        self.title.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
        self.title.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        self.title.Bind(wx.EVT_LEFT_UP, self.OnButton)

        self.tpanel.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
        self.tpanel.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        self.tpanel.Bind(wx.EVT_LEFT_UP, self.OnButton)

    def OnEnter(self,event):
        self.counter_enterleave+=1
        if self.counter_enterleave > 0:
            if self.txtcolour=="black":
                if self.is_open == 1: bmp = self.bmp_bub
                else: bmp = self.bmp_bdb
            else:
                if self.is_open == 1: bmp = self.bmp_wub
                else: bmp = self.bmp_wdb

            self.sb.SetBitmap(bmp)

    def OnLeave(self,event):
        self.counter_enterleave-=1
        if self.counter_enterleave == 0:
            if self.txtcolour=="black":
                if self.is_open == 1: bmp = self.bmp_bu
                else: bmp = self.bmp_bd
            else:
                if self.is_open == 1: bmp = self.bmp_wu
                else: bmp = self.bmp_wd

            self.sb.SetBitmap(bmp)

    def OnButton(self,event):
        if self.is_open == 1:
            self.vbox.Hide(self.ppanel)
            if self.txtcolour=="black": bmp = self.bmp_bdb
            else: bmp = self.bmp_wdb
        else:
            self.vbox.Show(self.ppanel)
            if self.txtcolour=="black": bmp = self.bmp_bub
            else: bmp = self.bmp_wub

        #Ugly, all three statements are needed (only tested in windows, though)
        self.parentsizer.RecalcSizes()
        self.parentsizer.Layout()
        self.parent.Refresh()

        self.sb.SetBitmap(bmp)
        self.is_open=1-self.is_open
        event.Skip()

    def AddPage(self,page,setbg=0):
        page.Reparent(self.ppanel)
        self.pages.append(page)

        if setbg:
            page.SetBackgroundColour(self.bgcolour)

        if len(self.pages)==1:
            self.pbox.Add(page,1,wx.EXPAND|wx.ALL,5)
        else:
            self.pbox.Add(page,1,wx.EXPAND|wx.BOTTOM|wx.LEFT|wx.RIGHT,5)

        self.pbox.Layout()

    def GetPage(self,i_page=0):
        return self.pages[i_page]

if __name__ == "__main__":

    class ColorPanel(wx.Panel):
        def __init__(self, parent, color):
            wx.Panel.__init__(self, parent, -1,size=(-1,75))
            self.SetBackgroundColour(color)

    class MainPanel(wx.Panel):
        def __init__(self, parent):
            wx.Panel.__init__(self, parent, -1)
            self.SetBackgroundColour("white")

            self.vbox = wx.BoxSizer(wx.VERTICAL)

            tooltip="Click to unfold the green panel"
            p1=FoldPanel(self,self.vbox,"Green Panel",tooltip,
                                wx.Colour(10,10,96),"white","white",is_open=0)
            
            p1.AddPage(ColorPanel(p1,wx.Colour(128,255,128)),0)
            p1.AddPage(ColorPanel(p1,wx.Colour(128,128,255)),0)

            self.vbox.Add(p1,0,wx.EXPAND|wx.ALL,5)

            tooltip="The titlebar arrow icon is only available in two colours\n"\
                    "... but is transparent."
            p2=FoldPanel(self,self.vbox,"Red Panel",tooltip,"light grey","white")
            p2.AddPage(ColorPanel(p2,wx.Colour(255,128,128)),0)
            self.vbox.Add(p2,0,wx.EXPAND|wx.ALL,5)

            self.vbox.Layout()
            self.SetSizer(self.vbox)

    class MyFrame(wx.Frame):
        def __init__(self, pos=wx.DefaultPosition, size=(180,290)):
            wx.Frame.__init__(self, None, -1, "Foldable Panels", pos, size)
            self.CreateStatusBar()
            mp= MainPanel(self)

    app = wx.PySimpleApp()
    f = MyFrame(None)
    f.Show()
    app.MainLoop()
