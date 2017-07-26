class Times:
    def __rmul__(self,n):
        for i in range(n):
            self.func()
    def __call__(self,func):
        self.func=func
        return self
times=Times()

class Each:
    def __rmul__(self,L):
        return map(self.func,L)
    def __call__(self,func):
        self.func=func
        return self
each=Each()

class Length:
    def __rmul__(self,L):
        return len(L)
length=Length()

def printf(x):
    print x

5 *times(lambda: printf("Hello"))
[1,2,3,4] *each(lambda x: printf("Count:"+str(x)))
print [1,2,3,4,5] *length
['a','b','c','d','e'] *each(lambda char: char+'!')
