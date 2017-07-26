class SuperClass:
    def supermethod(self):
        return 'Output of "SuperClass.supermethod(self)".'

class SubClass(SuperClass):
    def __getattr__(self, name):
        if name == 'special':
            return 'Value of attribute "special".'
        else:  raise AttributeError, name  # <<< DON'T FORGET THIS LINE !!
