class OnlyOne(object):
    """
    Signleton class , only one obejct of this type can be created
    any class derived from it will be Singleton
    """
    __instance = None
    def __new__(typ, *args, **kwargs):
        if OnlyOne.__instance == None:
            obj = object.__new__(typ, *args, **kwargs)
            OnlyOne.__instance = obj
            
        return OnlyOne.__instance

print OnlyOne() == OnlyOne()

# testing derived class

class My1(OnlyOne): pass 

print My1() == My1()
