class Cache:
    def __init__(self):
        # cache of salf.fatorial()
        self.c_fatorial = {}
        
    def fatorial(self,  x):
        result = 0
        # first, verify in cache
        if x in self.c_fatorial.keys():
            return self.c_fatorial[x]
        # if not in cach, process
        if x <= 1:
            result = 1
        else:
            result = x * self.fatorial(x - 1)
        
        self.c_fatorial[x] = result # put the result in cache
        return result
