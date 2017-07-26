# Enum type with default positional values
# Enum('STATE', 'A','B','C') => returns object
# e so that e.A=>0, e.B=>1, e.C=>2 etc.

def Enum(name, *args):
    args_m = [arg for arg in args if type(arg)==str]
    return type(name, (object,), dict(((v,k) for k, v in enumerate(args_m)), __slots__=args_m))() 

# Enum type with keyword values
# Enum('STATE',A=1, B=3,C=2) => returns object 
# e so that e.A=1, e.B=>3, e.C=>2 etc.

Enum_kw = lambda name, **kwargs: type(name, (object,), [item for item in (kwargs.update({'__slots__': [k for k in kwargs]}), kwargs)][1])()

e=Enum('STATE','A','B','C','D')
print e.A, e.B, e.C
#e.A=1    # Can't do this
#e.X=100   # Can't do this 

e=Enum_kw('STATE',A=1,B=2,C=3)
print e.A, e.B, e.C
# Can't change existing attribute
# e.A=10
# Can't assign new attributes
# e.X=100
