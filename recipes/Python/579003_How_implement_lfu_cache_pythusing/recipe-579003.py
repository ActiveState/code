import random

class Process:
    def __init__(self,name,times):
        self.name = name
        self.times = times
    def run(self):
        print("Process %d run for the %d times" %(self.name, self.times))
    def __str__(self):
        return "Process %d run for the %d times" %(self.name, self.times)

def generate(n):
        lst=[]
        for i in range(n):
                     x = random.randint(1,50)
                     p = Process(i+1,x)
                     lst.append(p)
        return lst
