"""classes for timing during development

by wolfgang resch, 070722
"""

from time import clock, time

#--- timer decorator -----------------------------------
class Timer(object):
    def __init__(self, f):
        self.__f=f
        self.__name__=f.__name__
        self.__doc__=f.__doc__
        self.times=[]
    def __call__(self, *args, **kwargs):
        start=time()
        result=self.__f(*args, **kwargs)
        stop=time()
        self.times.append(stop-start)
    def report(self):
        results = {'min':min(self.times)*1000, 'max':max(self.times)*1000, 'mean':sum(self.times)/len(self.times)*1000}
        return self.__doc__.ljust(70) + "\t%(mean)6.5fms [%(min)6.5f - %(max)6.5f]" % results
    def reset(self):
        self.times=[]

#--- scenarios -------------------------------------------
class Scenario(object):
    def __init__(self, **kw):
        """
        pass each scenario as a kw={'desc':"", data:(), functions:()}
        
        for each scenario each function is applied to the data and results are printed
        """
        self.scenarios=kw
    def run(self, nr_iter):
        for title, scenario in self.scenarios.items():
            print 50*'-' + "\n" + title.upper()
            print scenario['desc']
            for f in scenario['functions']:
                for x in xrange(nr_iter):
                    f(*scenario['data'])
                print "\t" + f.report()
                f.reset()


#--- example: validators------------------------------------------
# validator takes a iterable object and checks if each element
# in the object is part of a defined alphabet
@Timer
def validate1(s, a):
    """validate1(s, a): list comprehension with a.index"""
    try:
        [a.index(x) for x in s]
        return True
    except:
        return False

@Timer
def validate2(s,a):
    """validate2(s, a): for loop with a.index"""
    for l in s:
        try:
            a.index(l)
        except:
            return False
    return True

@Timer
def validate3(s,a):
    """validate3(s, a): list comprehension with (l in a)"""
    return min([(l in a) for l in s])

@Timer
def validate4(s,a):
    """validate4(s, a): for loop with generator and (l in a)"""
    for x in ((l in a) for l in s):
        if not x:
            return False
    return True    

@Timer
def validate5(s,a):
    """validate5(s,a): convert s to set and compare to set alphabet"""
    return set(s).issubset(a)

#--- main-------------------------------------------------

if __name__=='__main__':
    replications=1000
    s_false="GATCTTGACGATGCGATGCGATG"*40 + "==" + "GATCTTGACGATGCGATGCGATG"*40
    s_true=80*"GATCTTGACGATGCGATGCGATG" + "GA"
    a=['G','A','T','C','R','W','B','C','M','T','Q','X','.','-','~','U']
   
    testValidator = Scenario(scene_1={'desc':"Validator evaluates to true; alphabet is a list",
                                      'data':(s_true, a),
                                      'functions':(validate1, validate2, validate3, validate4, validate5)},
                             scene_2= {'desc':"Validator evaluates to false; alphabet is a list",
                                      'data':(s_false, a),
                                      'functions':(validate1, validate2, validate3, validate4, validate5)},
                             scene_3={'desc':"Validator evaluates to true; alphabet is a tuple",
                                      'data':(s_true, tuple(a)),
                                      'functions':( validate3, validate4, validate5)})
    testValidator.run(1000)                         
-----------------------------
