class C:
    def met(self,foo):
        print 'from C: ', foo

class D:
    def met(self,foo):
        print 'from D: ', foo

def TClass(T):
    class TClass(T):
        def t_met(self, bar):
            print 'from TClass: ', bar
    return TClass

------

>>> MyC = TClass(C)
>>> myCObj = MyC()
>>> myCObj.met('hello, foo!')
from C: hello, foo!
>>> myCObj.t_met('hello, bar!')
from TClass: hello, bar!
>>>
>>> MyD = TClass(D)
>>> myDObj = MyD()
>>> myDObj.met('hello, foo!')
from D: hello, foo!
>>> myDObj.t_met('hello, bar!')
from TClass: hello, bar!
