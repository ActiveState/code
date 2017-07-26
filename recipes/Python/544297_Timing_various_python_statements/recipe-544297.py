from timeit import Timer

class Timing:
    def __init__(self, name, num, init, statement):
        self.__timer = Timer(statement, init)
        self.__num   = num
        self.name    = name
        self.statement = statement
        self.__result  = None
        
    def timeit(self):
        self.__result = self.__timer.timeit(self.__num)
        
    def getResult(self):
        return self.__result
        
        
def times(num=1000000, reverse=False, init='', **statements):
    # time each statement
    timings = []
    for n, s in statements.iteritems():
        t = Timing(n, num, init, s)
        t.timeit()
        timings.append(t)
    
    # print results
    timings.sort(key=Timing.getResult, reverse=reverse)
    for t in timings:
        print "%s => %.3f s" % (t.name, t.getResult())
