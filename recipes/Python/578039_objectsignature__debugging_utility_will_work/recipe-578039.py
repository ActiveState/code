#  Copyright (C)  Boris Kats 2011 - 2012.
#  Inspired and based on  Yaniv Aknin "objwalk" http://code.activestate.com/recipes/577982/
#  The small debug utility will help to detect unwonted changes to content of user's class
#  or containers during the program execution. Just call it before and after some part 
#  of program and compare the results. Also, one can dump the contents of the class into
#  files and investigate details. If argument "withValues" of functon "objview" is set to False,
#  just types of members will be printed, instead of values.
#  Any additional type of collection  can be embodied with small helper functions.

import collections
from collections import Mapping, Set, Sequence, namedtuple, deque 
from datetime import datetime
from datetime import date as date
import array

__string_types__ = (str, unicode) if str is bytes else (str, bytes)
__primitiveTypes__ =['int', 'float','bool','date'] + [str(m)[8:-2] for m in __string_types__]

def Round(input,digits):
    if digits and isinstance(input,float):
       return round(input,digits)
    else:
       return input

def class__view(obj):
   ''' helper function for classes'''
   internaldict = dict()
   if hasattr(obj,'_asdict'):
      internaldict = obj._asdict()
   else:
      internaldict  = { member:getattr(obj, member) for member in dir(obj) \
                        if not member.startswith('__') and not callable(getattr(obj, member)) }
   keylist = list(internaldict.keys())
   keylist.sort(key=str.upper)
   res = collections.OrderedDict([(key,internaldict[key]) for key in keylist])
   return res.items()                          

iteritems = lambda mapping: getattr(mapping, 'iteritems', mapping.items)()

def objview(obj,withValues,path = str()):
    ''' That function will iterate recursivlly accross members of class
        or collections, until all primitives are found '''
    if not len(path): path = type(obj).__name__ 
    iterator = None
    if isinstance(obj, Mapping):
         iterator = iteritems
    else: 
         if isinstance(obj, (Sequence,Set,array.array,deque)) \
            and not isinstance(obj,__string_types__)  and not hasattr(obj,'_asdict'):
            iterator = enumerate
         else: 
            if not type(obj).__name__ in __primitiveTypes__:
               iterator = class__view

    if iterator:
            for path_component, value in iterator(obj):
                valuetype = type(value).__name__ 
                nextpath = path + ('[%s]' % str(path_component)) 
                if (not withValues): yield nextpath, valuetype
                for result in objview(value,withValues,nextpath):               
                    if (withValues or (valuetype not in __primitiveTypes__)):  yield result
    else:
        yield path, obj 

def objsignature(obj, *,file = None, precision = 10):
   res = objview(obj,True)
   r_str = '%s %s%s'
   for x in res :
     r_str = r_str %(x[0],str(Round(x[1],precision)), '\n%s %s%s')
   r_str = r_str[:-7]
   if (file):
      debugFile = open(file,'w')
      debugFile.write(r_str)
      debugFile.close()
   return hash(r_str)

   
if __name__ =='__main__':
   myList = [1,2,3,[4,5,6]]
   res = objview(myList,True)
   for x in res :
     print(x[0],' => ',Round(x[1],4))

   class MyRandomClass(object):
       def __init__(self,limit):
        super()
        import random
        self.numbers = [random.random() for i in range(limit)]

   class MyClass(object):
     def __init__(self,name,rd):
        super() 
        self.name = '"MyClass"'
        self.desription = (name,datetime.strptime('01/12/2012','%m/%d/%Y').date(),25)
        self.myList = [1.0,2.0,3.0,[5.0,6.0,7.0]]
        self.myDict = dict(a=1, b=2, c=3, d=set(['one','two','three']))
        Temp = collections.namedtuple('namedtuple','first second third')
        self.myNamedTuple = Temp('red','blue','green')
        self.myTuple = (('white','black'),'yellow')
        self.myFrosenSet = frozenset(['four','five','six'])
        self.myDeque = deque(iter([8.0,9.0,10.0]))
        self.Randoms = rd
        self.MyArray = array.array('f', [3,5,7])

   myrd = MyRandomClass(3)
   mycl = MyClass('The one',myrd) 
   print('Members of %s are:' % type(mycl).__name__)
   res = objview(mycl,True)
   for x in res :
     print(x[0],' => ',Round(x[1],4))

   sig1 = objsignature(mycl,file='before.txt',precision=4)
   print('class signature before',sig1)

   z = myrd.numbers[0]
   myrd.numbers[0] = 1.0
   sig2 = objsignature(mycl,file='after.txt',precision=4)
   print('class signature after',sig2)
   if sig1 != sig2:
      print('The content of class has been changed\n', \
            'compare two files before.txt and after.txt')   

   myrd.numbers[0] = z
   sig3 = objsignature(mycl,precision=4)
   assert(sig1 == sig3)
