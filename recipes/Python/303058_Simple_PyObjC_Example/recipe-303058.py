from math import sin, cos, pi
import objc
from Foundation import *
from AppKit import *

class DemoView(NSView):
  n = 10
  def X(self, t):
    return (sin(t) + 1) * self.width * 0.5
  def Y(self, t):
    return (cos(t) + 1) * self.height * 0.5
  def drawRect_(self, rect):
    self.width = self.bounds()[1][0]
    self.height = self.bounds()[1][1]
    NSColor.whiteColor().set()
    NSRectFill(self.bounds())
    NSColor.blackColor().set()
    step = 2 * pi/ self.n
    loop = [i * step  for i in range(self.n)]
    for f in loop:
      for g in loop:
        p1 = NSMakePoint(self.X(f), self.Y(f))
	p2 = NSMakePoint(self.X(g), self.Y(g))
	NSBezierPath.strokeLineFromPoint_toPoint_(p1, p2)

class AppDelegate(NSObject):
  def windowWillClose_(self, notification):
    app.terminate_(self)

def main():
  global app
  app = NSApplication.sharedApplication()
  graphicsRect = NSMakeRect(100.0, 350.0, 450.0, 400.0)
  myWindow = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
    graphicsRect, 
    NSTitledWindowMask 
    | NSClosableWindowMask 
    | NSResizableWindowMask
    | NSMiniaturizableWindowMask,
    NSBackingStoreBuffered,
    False)
  myWindow.setTitle_('Tiny Application Window')
  myView = DemoView.alloc().initWithFrame_(graphicsRect)
  myWindow.setContentView_(myView)
  myDelegate = AppDelegate.alloc().init()
  myWindow.setDelegate_(myDelegate)
  myWindow.display()
  myWindow.orderFrontRegardless()
  app.run()
  print 'Done'
  

if __name__ == '__main__':
  main()
    
