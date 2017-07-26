class Meta(type):
    @classmethod
    def __prepare__(meta, name, bases, **kwargs):
        return {"__name__": name}

class X(metaclass=Meta):
    print(locals())

#{'__name__': 'X', '__module__': 'X', '__locals__': {...}}
