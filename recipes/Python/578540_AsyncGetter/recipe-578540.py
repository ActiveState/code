import _thread as thread

class AsyncGetter:
    def __init__(self, method, args=()):
        self.method = method
        self.gotten = False
        self.args = args
        
        thread.start_new_thread(self.doGet, ())
        
    def doGet(self):
        self.result = self.method(*self.args)
        self.gotten = True
        
    def hasGotten(self):
        return self.gotten
    
    def getResult(self):
        return self.result
