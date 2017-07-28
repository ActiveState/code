class Abbr(object):
  def __init__(self, **kwargs):
    self.abbrs = kwargs
    self.store = {}

  def __enter__(self):
    for key, value in self.abbrs.iteritems():
      try:
        self.store[key] = globals()[key]
      except KeyError:
        pass
      globals()[key] = value

  def __exit__(self, *args, **kwargs):
    for key in self.abbrs:
      try:
        globals()[key] = self.store[key]
      except KeyError:
        del globals()[key]
