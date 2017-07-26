class InwardMeta(type):
    @classmethod
    def __prepare__(meta, name, bases, **kwargs):
        cls = super().__new__(meta, name, bases, {})
        return {"__newclass__": cls}
    def __new__(meta, name, bases, namespace):
        cls = namespace["__newclass__"]
        del namespace["__newclass__"]
        for name in namespace:
            setattr(cls, name, namespace[name])
        return cls
