from types import *

def check_type(obj,atts=[],callables=[]):
    got_atts=True
    for att in atts:
	if not hasattr(obj,att):
           got_atts=False;break
    got_callables=True
    for call in callables:
	if not hasattr(obj,call):
	    got_callables=False;break
        the_attr=getattr(obj,call)
        if not callable(the_attr):
	    got_callables=False;break
    if got_atts and got_callables: return -1
    return 0

def is_iter(obj):
   if isinstance(obj,ListType): return 1
   if isinstance(obj,TupleType): return 1
   if isinstance(obj,DictType): return 1
   if isinstance(obj,FileType): return 1
   try: 
     iter(obj)
     return -1
   except TypeError:
   return 0

def is_gen(obj):
	   if isinstance(obj,GeneratorType): return 1
	   return 0
def is_seq(obj):
   if isinstance(obj,ListType): return 1
   if isinstance(obj,TupleType): return 1
   if is_iter(obj):
      try: 
         obj[0:0]
         return -1
      except TypeError:
         pass
   return 0  
   
def is_mapping(obj):
   if isinstance(obj,DictType): return 1
   if is_iter(obj):
      return check_type(obj,callables=['iteritems','has_key'])
   return 0

def is_list(obj):
   if isinstance(obj,ListType): return 1
   if is_seq(obj):
       if check_type(obj,callables=['append','extend','pop']): return -1
   return 0

def is_str(obj):
     if isinstance(obj, basestring): return 1
     if is_iter(obj):
        if check_type(obj,callables=['index','count','replace']): return -1
     return 0
	
def is_file(obj):
    if isinstance(obj,FileType): return 1
    if check_type(obj,callables=['read','close']): return -1
    return 0

def check_all(obj):
	result=[ str(i) for i in (is_iter(obj),is_gen(obj),is_seq(obj),is_list(obj),is_str(obj),is_mapping(obj),is_file(obj))]
	return '\t'.join(result)
#####################examples
print '\t'+'\t'.join(['iter','gen','seq','list','str','dict','file'])
print 'str\t',check_all('str')
print '(1,)\t',check_all((1,))
print '[]\t',check_all([])
print '{}\t',check_all({})

f=open('tmp.txt','w')
print 'file\t',check_all(f)

import cStringIO
cstr=cStringIO.StringIO()
print 'cstrio\t',check_all(cstr)

gen=(i for  i in (1,2,3))
print 'gen\t',check_all(gen)
def test(): yield 1
print 'test()\t',check_all(test())

class fdict:
	def iteritems(self): pass
	def has_key(self): pass

print 'fdict\t',check_all(fdict)
