class channel(object):
  def __init__(self, gen):
    self.gen = gen
    self.args = ()
    self.kwargs = {}
  def __iter__(self):
    return self
  def next(self):
    self.args = ()
    self.kwargs = {}
    return self.gen.next()
  def send(self, *args, **kwargs):
    self.args = args
    self.kwargs = kwargs
    return self.gen.next()

class channelgen(object):
  def __init__(self, genfunc):
    self.genfunc = genfunc
  def __call__(self, *args, **kwargs):
    c = channel(None)
    c.gen = self.genfunc(c, *args, **kwargs)
    return c

# A simple example

@channelgen
def skipper(chan, seq, skip = 0):
  for i in seq:
    if skip:
      skip -= 1
    else:
      yield i
      if chan.args:
        skip = chan.args[0]

skip = skipper(xrange(100))
skip.next()
skip.next()
skip.send(10) # Skips ten items in the sequence before yeilding one
