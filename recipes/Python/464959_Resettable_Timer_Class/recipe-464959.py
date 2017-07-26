import sys
import threading
import time
from Tkinter import *     # for rtTester class

class ResettableTimer(threading.Thread):
  """
  The ResettableTimer class is a timer whose counting loop can be reset
  arbitrarily. Its duration is configurable. Commands can be specified
  for both expiration and update. Its update resolution can also be
  specified. Resettable timer keeps counting until the "run" method
  is explicitly killed with the "kill" method.
  """
  def __init__(self, maxtime, expire, inc=None, update=None):
    """
    @param maxtime: time in seconds before expiration after resetting
                    in seconds
    @param expire: function called when timer expires
    @param inc: amount by which timer increments before
                updating in seconds, default is maxtime/2
    @param update: function called when timer updates
    """
    self.maxtime = maxtime
    self.expire = expire
    if inc:
      self.inc = inc
    else:
      self.inc = maxtime/2
    if update:
      self.update = update
    else:
      self.update = lambda c : None
    self.counter = 0
    self.active = True
    self.stop = False
    threading.Thread.__init__(self)
    self.setDaemon(True)
  def set_counter(self, t):
    """
    Set self.counter to t.

    @param t: new counter value
    """
    self.counter = t
  def deactivate(self):
    """
    Set self.active to False.
    """
    self.active = False
  def kill(self):
    """
    Will stop the counting loop before next update.
    """
    self.stop = True
  def reset(self):
    """
    Fully rewinds the timer and makes the timer active, such that
    the expire and update commands will be called when appropriate.
    """
    self.counter = 0
    self.active = True

  def run(self):
    """
    Run the timer loop.
    """
    while True:
      self.counter = 0
      while self.counter < self.maxtime:
        self.counter += self.inc
        time.sleep(self.inc)
        if self.stop:
          return
        if self.active:
          self.update(self.counter)
      if self.active:
        self.expire()
        self.active = False

class rtTester(Frame):
  def __init__(self, parent=None):
    self.timer = ResettableTimer(5, self.command, inc=1,
                                 update=self.update)
    Frame.__init__(self, parent)
    self.pack()
    self.make_widgets()
    self.timer.start()
  def destroy(self, *args, **kwargs):
    self.timer.kill()
    Frame.destroy(self, *args, **kwargs)
  def command(self, e=None):
    self.rwbut.config(state = DISABLED)
    self.deactbut.config(state=DISABLED)
    self.reactbut.config(state = NORMAL)
    self.label.config(text='expired', fg='red')
  def update(self, c):
    self.label.config(text=str(c))
  def rewind(self, e=None):
    self.timer.reset()
    self.label.config(text='0')
  def deactivate(self, e=None):
    self.rwbut.config(state=DISABLED)
    self.reactbut.config(state=NORMAL)
    self.deactbut.config(state=DISABLED)
    self.label.config(text='deactivated', fg='red')
    self.timer.deactivate()
  def reactivate(self, e=None):
    self.deactbut.config(state=NORMAL)
    self.rwbut.config(state=NORMAL)
    self.reactbut.config(state=DISABLED)
    self.label.config(text='started', fg='black')
    self.timer.reset()
  def make_widgets(self):
    self.rwbut = Button(self, text='rewind', command=self.rewind)
    self.rwbut.pack(fill=X)
    self.label = Label(self, text='started', fg='black')
    self.label.pack(fill=X)
    self.deactbut = Button(self, text='deactivate',
                           command=self.deactivate)
    self.deactbut.pack(fill=X)
    self.reactbut = Button(self, text='reactivate',
                           command=self.reactivate,
                           state=DISABLED)
    self.reactbut.pack(fill=X)

def test():
  tk = Tk()
  rtTester(tk)
  tk.mainloop()

if __name__ == "__main__":
  test()
