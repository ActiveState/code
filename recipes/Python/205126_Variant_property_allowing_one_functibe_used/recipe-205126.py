class CommonProperty(object):
    """A more flexible version of property()

    Saves the name of the managed attribute and uses the saved name
    in calls to the getter, setter, or destructor.  This allows the
    same function to be used for more than one managed variable.

    As a convenience, the default functions are gettattr, setattr,
    and delattr.  This allows complete access to the managed
    variable.  All or some of those can be overridden to provide
    custom access behavior.

    """

    def __init__(self, realname, fget=getattr, fset=setattr, fdel=delattr, doc=None):
        self.realname = realname
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = doc or ""

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError, "unreadable attribute"
        return self.fget(obj, self.realname)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError, "can't set attribute"
        self.fset(obj, self.realname, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError, "can't delete attribute"
        self.fdel(obj, self.realname, value)




## Example of requiring password access to view selected attributes

class SecurityError(Exception): pass

def securitycheck(*args):
    "Stub function.  A real check should be a bit more thorough ;)"
    return True


class Employee(object):
    __authenticate = False

    def __init__(self, name, dept, salary, age):
        self.name=name
        self.dept=dept
        self._salary = salary
        self._age = age

    def authorize(self, userid, password):
        if securitycheck(userid, password):
            self.__authenticate = True

    def passwordget(self, name):
        if not self.__authenticate:
            raise SecurityError, "Viewing secure data requires valid password"
        return getattr(self, name)
    
    salary = CommonProperty('_salary', passwordget, None, None, doc="Annual Salary")
    age = CommonProperty('_age', passwordget, None, None, doc="Age as of 1 Jan 2003")            

manager = Employee('Raymond', 'PySystemsGroup', 'ProBono', 38)
manager.authorize('Guido', 'omega5')
print manager.name
print manager.salary
