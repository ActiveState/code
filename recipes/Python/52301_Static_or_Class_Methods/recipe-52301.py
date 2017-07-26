>>> class Class:
... 	class StaticFudge:
... 		def __call__(self): print "I do not require an instance."
... 	classmethod = StaticFudge()
... 
>>> Class.classmethod()
I do not require an instance.
