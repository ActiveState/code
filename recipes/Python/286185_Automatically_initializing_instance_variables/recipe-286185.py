# This code was taken and modified from Alex Martelli's
# "determine the name of the calling function" recipe (Thanks, Alex!)
#
# This code also benefits from a useful enhancement from Gary Robinson, allowing 
# only the arguments to __init__ to be copied, if that is desired.
#
# use sys._getframe() -- it returns a frame object, whose attribute
# f_locals is the list of local variables.  Before any processing goes on,
# will be the list of parameters passed in.
import sys

# By calling sys._getframe(1), you can get this information
# for the *caller* of the current function.  So you can package
# this functionality up into your own handy functions:
def initFromArgs(beingInitted, bJustArgs=False):
    import sys
    codeObject = beingInitted.__class__.__init__.im_func.func_code
    for k,v in sys._getframe(1).f_locals.items():
        if k!='self' and ((not bJustArgs) or k in codeObject.co_varnames[1:codeObject.co_argcount]):
            setattr(beingInitted,k,v)

class Animal:
    def __init__(self,name='Dog',numberOfLegs=4,habitat='Temperate'):
        # any local variables added here will be assigned to the object
        # as if they were parameters
        if name in ('Dog','Cat'):
            pet=True
        initFromArgs(self)
        # modify things here

if __name__ == '__main__':
    dog=Animal()
    octopus = Animal('Octopus',8,'Aquatic')
    print [i.__dict__.items() for i in (dog,octopus)] 
        
