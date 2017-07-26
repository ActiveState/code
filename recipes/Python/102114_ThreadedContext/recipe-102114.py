ThreadedContext is like a dictionary, but stores its data in a private namespace for every thread.
A thread can't access to the data from other thread.
USAGE:
In Thread 1:
d = ThreadedContext()
d[1]=1

In Thread 2:
d[1] #raises KeyError exception
d[1]= 2

In Thread 1:
print d[1]	#prints 1

In Thread 2:
print d[1]	#prints 2
	
If a thread is deleted its keys in ThreadedContext are erased.
"""

from weakref import WeakKeyDictionary as _WeakKeyDictionary
from threading import currentThread as _currentThread

class ThreadedContext:
	def __init__(self):
		self.__thread_dict = _WeakKeyDictionary()
		
	def __getattr__(self,name):
		return getattr(self.__currentDict(),name)
		
	def __currentDict(self, _currentThread = _currentThread):
		try:
			return self.__thread_dict[_currentThread()]
		except KeyError:
			self.__thread_dict[_currentThread()] = result = {}
			return result
