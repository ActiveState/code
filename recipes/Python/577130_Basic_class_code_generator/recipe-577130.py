import os
import sys
import re
import yaml
from new import classobj

"""
Yaml file looks like this -

Class:
    Name: GeneratedClassCode
    Super: Whatever
    DocString: You better comment this Class
    Args: firstArg, secondArg 
    Kwds: this=that, andThat=thisThing
    Methods:
        sync_method:
            Sig:
                Sync: True
                Args: date
                Kwds: keywords
                DocString: This is my doc string
        unsynced_method:
            Sig:
                Sync: False
                Args:
                Kwds:
                DocString: This is my other doc string

And gererates this -

import sys
import os
import yaml
import re
from new import classobj
import inspect
import threading
import unittest
#
#
#
class GeneratedClassCode(Whatever):
  '''
    You better comment this Class
  '''
    def __init__(self, firstArg, secondArg, this=that, andThat=thisThing):
      '''
        Comment this Method
      '''
      Whatever.__init__(self)
      try:
        self.generatedClassCodeLock = threading.RLock()
        self.firstArg = firstArg
        self.secondArg = secondArg
        self.this = that
        self.andThat = thisThing

      except Exception, e:
        raise Exception(
          'Raising Exception "%s" from %s.%s()'%(e, self.__class__.__name__, str(inspect.stack()[0][3]))
        )
    @synchronous(generatedClassCodeLock)
    def sync_method(self, date, keywords):
      '''
        This is my doc string
      '''
      try:
        pass
      except Exception, e:
        raise Exception(
          'Raising Exception "%s" from %s.%s()'%(e, self.__class__.__name__, str(inspect.stack()[0][3]))
        )
    def unsynced_method(self, *args, **kwds):
      '''
        This is my other doc string
      '''
      try:
        pass
      except Exception, e:
        raise Exception(
          'Raising Exception "%s" from %s.%s()'%(e, self.__class__.__name__, str(inspect.stack()[0][3]))
        )

#
#
#
class TestGeneratedClassCode(unittest.TestCase):
    def setUp(self, *args, **kwds):
      '''
        Comment this Method
      '''
      try:
        pass
      except Exception, e:
        raise Exception(
          'Raising Exception "%s" from %s.%s()'%(e, self.__class__.__name__, str(inspect.stack()[0][3]))
        )
    def tearDown(self, *args, **kwds):
      '''
        Comment this Method
      '''
      try:
        pass
      except Exception, e:
        raise Exception(
          'Raising Exception "%s" from %s.%s()'%(e, self.__class__.__name__, str(inspect.stack()[0][3]))
        )
    def test_sync_method(self, *args, **kwds):
      '''
        Comment this Method
      '''
      try:
        pass
      except Exception, e:
        raise Exception(
          'Raising Exception "%s" from %s.%s()'%(e, self.__class__.__name__, str(inspect.stack()[0][3]))
        )
    def test_unsynced_method(self, *args, **kwds):
      '''
        Comment this Method
      '''
      try:
        pass
      except Exception, e:
        raise Exception(
          'Raising Exception "%s" from %s.%s()'%(e, self.__class__.__name__, str(inspect.stack()[0][3]))
        )


"""

#
#
#
class ConfigOptions(object):
  def __init__(self, **kwds):
    self.set_inners(**kwds)
  def set_inners(self, **kwds):
    for k,v in kwds.items():
      if type(v) == dict:
        setattr(self, k, ConfigOptions(**v))
      else:
        setattr(self, k,v)    
#   
def get_options_dict(configFile):
  f = open(configFile)
  d = yaml.load(f)
  f.close()
  objs = {}
  for k,v in d.items():
    oClz = classobj('%sOptions'%k.capitalize(),(ConfigOptions,), {})
    obj = oClz(**d[k])
    objs[oClz.__name__]=obj
  return ConfigOptions(**objs)
#
def code_line(line, tabIn=1):
  tSeq = list(('\t' for t in xrange(0,tabIn)))
  cSeq = ['%s\n'%line]
  lineSeq = tSeq + cSeq
  return ''.join(lineSeq)
#
def docstring(docstring, tabIn=1):
  tSeq = list(('\t' for t in xrange(0,tabIn)))
  sSeq = ["'''\n"]
  docSeq = tSeq + sSeq + tSeq + ['\t%s\n'%docstring] + tSeq + sSeq
  return ''.join(docSeq)
#
def parse_args(args):
  return (args if args != None else '*args')
#
def parse_kwds(keywords):
  return (keywords if keywords != None else '**kwds')
#
def make_lock(line):
  return 'self.%s%sLock = threading.RLock()\n'%(
    line[0].lower(), line[1:len(options.ClassOptions.Name)])
#
def define_method(methodName, arguments, keywords, 
      synchronised=False, docStr='Comment this Method', tryExcept=True):
  mSeq = []
  if synchronised: mSeq.append(
      code_line('@synchronous("%s%sLock")'%(
        options.ClassOptions.Name[0].lower(),
        options.ClassOptions.Name[1:len(options.ClassOptions.Name)]),
        tabIn=2))
  mSeq.append(code_line('def %s(self, %s, %s):'%( 
        methodName,
        (arguments if arguments != None else '*args'),
        (keywords if keywords != None else '**kwds')),
        tabIn=2))
  mSeq.append(docstring(docStr, tabIn=3))
  if tryExcept:
    mSeq.append(try_except())
  return ''.join(mSeq)
#
def try_except(line='pass'):
  return '''\t\t\ttry:\n\t\t\t\t'''+line+'''\n\t\t\texcept Exception, e:\n\t\t\t\traise Exception(\n\t\t\t\t\t'Raising Exception "%s" from %s.%s()'%(e, self.__class__.__name__, str(inspect.stack()[0][3]))\n\t\t\t\t)\n'''
#
def get_kwds(line):
  if line:
    line = line.replace(' ', '')
    g = (k.split('=') for k in line.split(','))
    return dict(g)
  return {}
#
def get_args(line):
  if line:
    return line.replace(' ', '').split(',')
#
def define_members(args, kwds):
  memSeq = []
  if args:
    memSeq = list(('\t\t\t\tself.%s = %s\n'%(a, a) for a in args))
  if kwds:
    for k,v in kwds.items():
      memSeq.append('\t\t\t\tself.%s = %s\n'%(k,v))
  return ''.join(memSeq)
#
def define_class(options):
  classSeq = []
  classSeq.append(code_line('#\n#\n#\nclass %s(%s):'%(
      options.ClassOptions.Name,
      ('object' if options.ClassOptions.Super==None else options.ClassOptions.Super)),
      tabIn=0))
  classSeq.append(docstring(options.ClassOptions.DocString))
  # add __init__
  classSeq.append(define_method(  '__init__',
                  parse_args(options.ClassOptions.Args),
                  parse_kwds(options.ClassOptions.Kwds),
                  tryExcept=False)
                )
  if options.ClassOptions.Super != None:
    classSeq.append(code_line('%s.__init__(self)'%options.ClassOptions.Super, tabIn=3))
  memberLines = define_members(
        get_args(options.ClassOptions.Args), 
        get_kwds(options.ClassOptions.Kwds))
  classSeq.append(
    try_except(line=make_lock(options.ClassOptions.Name)+memberLines)
  )
  # add methods
  for mName, mOptions in options.ClassOptions.Methods.__dict__.items():
    classSeq.append(
      define_method(
        mName, 
        mOptions.Sig.Args, 
        mOptions.Sig.Kwds, 
        mOptions.Sig.Sync, 
        mOptions.Sig.DocString)
    )
  
  return ''.join(classSeq)
#
def define_tests(options):
  testSeq = []
  testSeq.append(code_line('#\n#\n#\nclass Test%s(%s):'%(
          options.ClassOptions.Name,'unittest.TestCase'), tabIn=0))
  testSeq.append(define_method('setUp',None, None))
  testSeq.append(define_method('tearDown',None, None))
  for mName, mOptions in options.ClassOptions.Methods.__dict__.items():
    testSeq.append(define_method('test_%s'%mName, None, None))
  
  return ''.join(testSeq)
#
if __name__ == '__main__':
  options = get_options_dict(sys.argv[1])
  print 'import sys\nimport os\nimport yaml\nimport re\nfrom new import classobj\nimport inspect\nimport threading\nimport unittest'
  print define_class(options)
  print define_tests(options)
