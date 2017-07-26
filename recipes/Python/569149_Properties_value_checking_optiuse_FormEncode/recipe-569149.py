import formencode.validators

class Property(object):
    def __init__(self,name,fget=getattr,fset=setattr,fdel=delattr,               
                doc=None,validator=None):

        self.name = name
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = doc or ""
        # the validator is an addition to the original recipe.
        self.validator = validator

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self

        if self.fget is None:
            raise AttributeError,"attribute is write-only"

        # from_python()
        return self.validator.from_python(self.fget(obj,self.name))

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError,"attribute is read-only"

        # to_python()
        self.fset(obj, self.name, self.validator.to_python(value))

    def __delete__(self,obj):
        if self.fdel is None:
            raise AttributeError,"attribute cannot be deleted"
        self.fdel(obj, self.name)


class IntValidator(object):
    """Validate a properties values.

    A validator must provide two methods:
    to_python -- used by __set__ to validate/convert the value. 
    from_python -- used by __get__ to validate/convert the value.

    This is modeled after the FormEncode package.
    """

    def __init__(self,min=None,max=None):
       self.min = min
       self.max = max

    def to_python(self,value):
       """Validate/convert value before setting the property.

       The value must be an integer and between self.min and
       self.max inclusive (if not None).
       """

       if (self.min is not None) and value < self.min:
           raise ValueError,"%s is less than %s" % (value,self.min)

       if (self.max is not None) and value > self.max:
           raise ValueError,"%s is greater than %s" % (value,self.max)

       return int(value)

    def from_python(self,value):
       """Validate/convert value when getting it.

       Usually we simply return the value as is.
       """
       return value


class MyClass(object):
    def __init__(self,x,r):
        self.x = x
        self.r = r

    # x must be an integer less than 10
    x = Property("_x",validator=IntValidator(max=9))

    # r must be an upper case character, we use the FormEncode
    # validator here.
    r = Property("_r",validator=formencode.validators.Regex(r"^[A-Z]+$"))


if __name__ == "__main__":
    c = MyClass(1,"A")  # this is fine.
    c.x = 9             # this is fine.
    c.r = "B"           # this is fine.
    c.x = 10            # this will raise a ValueError.
    c.r = "c"           # this will raise formencode.api.Invalid.
