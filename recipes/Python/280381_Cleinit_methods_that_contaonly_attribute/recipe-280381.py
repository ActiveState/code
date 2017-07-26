def attributesFromDict(d, obj=None, objName="self"):
    if obj is None:
        obj = d.pop(objName)
    for n, v in d.iteritems():
        setattr(obj, n, v)

class Before:
    def __init__(self, foo, bar, baz, boom=1, bang=2):
        self.foo = foo
        self.bar = bar
        self.baz = baz
        self.boom = boom
        self.bang = bang

class After:
    def __init__(self, foo, bar, baz, boom=1, bang=2):
        attributesFromDict(locals())
