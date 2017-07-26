""" EXAMPLE USAGE:

  opts = Opts(environ,
      opt('q', default=''),
      opt('pages', default=2),
      opt('split', default=0),
      opt('simple', default=0),
      opt('max_topics', default=40),
      opt('ncol', default=3),
      opt('save', default=False),
      opt('load', default=False),
      opt('smoothing', default='lidstone'),
      opt('single_query', default=0),
      opt('format', default='dev'),
      )

... then opts is a hash.
"""

#### first, from anyall.org/util.py

def safehtml(x):
  return cgi.escape(str(x),quote=True)

def unicodify(s, encoding='utf8', *args):
  """ because {str,unicode}.{encode,decode} is anti-polymorphic, but sometimes
  you can't control which you have. """
  if isinstance(s,unicode): return s
  if isinstance(s,str): return s.decode(encoding, *args)
  return unicode(s)

class Struct(dict):
  def __getattr__(self, a):
    if a.startswith('__'):
      raise AttributeError
    return self[a]
  def __setattr__(self, a, v):
    self[a] = v

#### main code

type_builtin = type
def opt(name, type=None, default=None):
  o = Struct(name=name, type=type, default=default)
  if type is None:
    if default is not None:
      o.type = type_builtin(default)
    else:
      o.type = str #raise Exception("need type for %s" % name)
  #if o.type==bool: o.type=int
  return o

def type_clean(val,type):
  if type==bool:
    if val in (False,0,'0','f','false','False','no','n'): return False
    if val in (True,1,'1','t','true','True','yes','y'): return True
    raise Exception("bad bool value %s" % repr(val))
  if type==str or type==unicode:
    # nope no strings, you're gonna get unicode instead!
    return unicodify(val)
  return type(val)

class Opts(Struct):
  " modelled on trollop.rubyforge.org and gist.github.com/5682 "
  def __init__(self, environ, *optlist):
    vars = cgi.parse_qs(environ['QUERY_STRING'])
    for opt in optlist:
      val = vars.get(opt.name)
      val = val[0] if val else None
      if val is None and opt.default is not None:
        val = copy(opt.default)
      elif val is None:
        raise Exception("option not given: %s" % opt.name)
      val = type_clean(val, opt.type)
      self[opt.name] = val
  def input(self, name, **kwargs):
    val = self[name]
    h = '''<input id=%s name=%s value="%s"''' % (name, name, safehtml(val))
    more = {}
    if type(val)==int:
      more['size'] = 2
    elif type(val)==float:
      more['size'] = 4
    more.update(kwargs)
    for k,v in more.iteritems():
      h += ''' %s="%s"''' % (k,v)
    h += ">"
    return h
