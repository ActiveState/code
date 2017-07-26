"""
pkg-config support

The PkgConfig class is useful by itself.  It allows reading and writing
of pkg-config files.

This file, when executed, will read a .pc file and print the result of
processing.  The result will be functionally equivalent, but not identical.
Re-running on its own output *should* produce identical results.
"""
from string import Template
from StringIO import StringIO

class PkgConfig:
  """
  Contents of a .pc file for pkg-config.

  This can be initialized with or without a .pc file.
  Such a file consists of any combination of lines, where each is one of:
    - comment (starting with #)
    - variable definition (var = value)
    - field definition (field: value)
  (Allowable fields are listed in PgkConfig.fields.)
  All fields and variables become attributes of this object.
  Attributes can be altered, added, or removed at will.
  Attributes are interpolated when accessed as dictionary keys.

  When this is converted to a string, comments in the original file are
  re-printed in their original order (but all at the top), then any
  non-field attributes (as variables), then fields, and finally,
  unrecognized attributes from the original file, if any.

  @note Variables may not begin with '_'.
  """
  fields = ['Name', 'Description', 'Version', 'Requires', 'Conflicts', 'Libs', 'Cflags']
  own_comments = [
    "# Unrecognized fields",
    ]
  def __init__(self, FILE=None):
    self.__field_map = dict()
    self.__unrecognized_field_map = dict()
    self.__var_map = dict()
    self.__comments = []
    self.__parse(FILE)
  def __str__(self):
    OUT = StringIO()
    for comment in self.__comments:
      print>>OUT, comment
    print>>OUT
    for key in sorted(self.__var_map):
      print>>OUT, "%s=%s" %(key, self.__var_map[key])
    print>>OUT
    for key in PkgConfig.fields:
      if key not in self.__field_map: continue
      print>>OUT, "%s: %s" %(key, self.__field_map[key])
    if self.__unrecognized_field_map:
      print>>OUT
      print>>OUT, PkgConfig.own_comments[0]
      for key,val in self.__unrecognized_field_map.items():
        print>>OUT, "%s: %s" %(key, val)
    assert set(self.__field_map).issubset(PkgConfig.fields)
    return OUT.getvalue()
  def __interpolated(self, raw):
    prev = None; current = raw
    while prev != current:
      # Interpolated repeatedly, until nothing changes.
      #print "prev, current: %s, %s" %(prev, current)
      prev = current
      current = Template(prev).substitute(self.__var_map)
    return current
  def __getitem__(self, name):
    """
    Return interpolated keys or variables.
    >>> pc = PkgConfig()
    >>> pc.WHO = 'me'
    >>> pc.WHERE = 'ho${WHO}'
    >>> pc.Required = '${WHO} and you'
    >>> pc['WHO']
    'me'
    >>> pc['WHERE']
    'home'
    >>> pc['Required']
    'me and you'
    """
    if hasattr(self, name):
      return self.__interpolated(getattr(self, name))
    else:
      raise IndexError, name
  def __getattr__(self, name):
    if name in PkgConfig.fields:
      return self.__field_map.get(name, '')
    elif name in self.__var_map:
      return self.__var_map[name]
    else:
      raise AttributeError(name)
  def __setattr__(self, name, val):
    if name in PkgConfig.fields:
      self.__field_map[name] = val
    elif not name.startswith('_'):
      self.__var_map[name] = val
    else:
      self.__dict__[name] = val
  def __delattr__(self, name):
    if name in self.__field_map:
      del self.__field_map[name]
    if name in self.__unrecognized_field_map:
      del self.__unrecognized_field_map[name]
    if name in self.__var_map:
      del self.__var_map[name]
    if name in self.__dict__:
      del self.__dict__[name]
  def __parse(self, PC):
    if not PC: return
    for line in PC:
      line = line.strip()
      if line.startswith('#'):
        if line not in PkgConfig.own_comments:
          self.__comments.append(line)
      elif ':' in line: # exported variable
        name, val = line.split(':')
        val = val.strip()
        if name not in PkgConfig.fields:
          self.__unrecognized_field_map[name] = val
        else:
          self.__field_map[name] = val
      elif '=' in line: # local variable
        name, val = line.split('=')
        self.__var_map[name] = val
