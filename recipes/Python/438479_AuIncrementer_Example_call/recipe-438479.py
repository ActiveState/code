class Inc:
    def __init__(self):
        self.x=0
        self.inc=self.giveone()
    def giveone(self):
        while True:
            yield self.x
            self.x+=1
    def __call__(self):
        return self.inc.next()  
inc=Inc()

for x in range(10):
    inc()
    
assert (inc()==10)==True
assert (inc()==12)==False
