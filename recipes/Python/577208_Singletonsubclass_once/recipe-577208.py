class Singleton(object):
        
    def __new__(cls,*dt,**mp):
        if not hasattr(cls,'_inst'):
            cls._inst = super(Singleton, cls).__new__(cls,dt,mp)
        else:
            def init_pass(self,*dt,**mp):pass
            cls.__init__ = init_pass
            
        return cls._inst
    
if __name__ == '__main__':
    
    
    class A(Singleton):
    
        def __init__(self):
            """Super constructor
                There is we can open file or create connection to the database
            """
            print "A init"
        
        
    a1 = A()
    a2 = A()
