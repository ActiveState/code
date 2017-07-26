import matplotlib
matplotlib.interactive( True )
matplotlib.use( 'WXAgg' )

import wx
import pylab

H = pylab.imshow(pylab.random((10,10)))

def callback(*args):
   H.set_array(pylab.random((10,10)))
   pylab.draw()
   wx.WakeUpIdle() # ensure that the idle event keeps firing

app = wx.PySimpleApp( 0 )
wx.EVT_IDLE(app, callback)
app.MainLoop()
