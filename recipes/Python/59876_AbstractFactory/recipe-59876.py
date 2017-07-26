class Klass1:
    """ a very simple obj """
    def __init__(self):
        pass
    def hi(self):
        print 'hi'
    
class Factory:
    """ base factory that can construct objects in a variety of ways:
            * modules ['package1.subpackage',] to be searched for klass
            * search global namespace
            * create takes a arguement of what type of class to return
            * return a default implementation - subclass must define createDefault()
    """
    def __init__(self, modules=[]):
        self.modules=modules
        
    def createDefault(self):
        print dir()
        raise NotImplementedError
    
    def create(self, klass=None):
        import string
        if klass in globals().keys():
            if type(globals()[klass]).__name__=='class':
                return globals()[klass]()
        for module in self.modules:
            try:
                fromlist = []
                if string.find(module, '.'): fromlist = string.split(module, '.')[:-1]
                module = __import__(module, globals(), locals(), fromlist)
                if hasattr(module, klass): return getattr(module, klass)()
            except AttributeError: pass 
        return self.createDefault()

class MyFactory(Factory):
    """ concrete factory that specifies:
        * what modules to search for
        * implements a createDefault() - which is used if class isnt found
    """
    def __init__(self, modules=[]):
        Factory.__init__(self,modules)
    def createDefault(self):
        return Klass1()


#--------much simpler one by mark lutz, http://shell.rmi.net/~lutz/talk.html
def factory(aClass, *args):        # varargs tuple
    return apply(aClass, args)     # call aClass

class Spam:
    def doit(self, message):
        print message

class Person:
    def __init__(self, name, job):
        self.name = name
        self.job  = job

object1 = factory(Spam)
object2 = factory(Person, "Guido", "guru")
