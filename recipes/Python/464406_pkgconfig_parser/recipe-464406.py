import os
from string import Template

class pkgconfig(dict):
  _paths = ['/usr/lib/pkgconfig', '/usr/local/lib/pkgconfig']

  def __init__(self, package):
    self._load(package)

  def _load(self, package):
    for path in self._paths:
      fn = os.path.join(path, '%s.pc' % package)
      if os.path.exists(fn):
        self._parse(fn)

  def _parse(self, filename):
    lines = open(filename).readlines()

    lokals = {}

    for line in lines:
      line = line.strip()

      if not line:
        continue
      elif ':' in line: # exported variable
        name, val = line.split(':')
        val = val.strip()
        if '$' in val:
          try:
            val = Template(val).substitute(lokals)
          except ValueError:
            raise ValueError("Error in variable substitution!")
        self[name] = val
      elif '=' in line: # local variable
        name, val = line.split('=')
        if '$' in val:
          try:
            val = Template(val).substitute(lokals)
          except ValueError:
            raise ValueError("Error in variable substitution!")
        lokals[name] = val
