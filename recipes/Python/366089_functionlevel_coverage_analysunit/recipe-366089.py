from inspect import isroutine,isclass,getmodule
covers=[]
ignore=[]

def watch(scope):
    for attr in scope.__dict__.keys():
        obj=getattr(scope,attr)
        if isroutine(obj) and getmodule(obj)==getmodule(scope):
            setattr(scope,attr,cover(obj))
        elif isclass(obj):
            watch(obj)

def cover(func):
    co=[0,func]
    covers.append(co)
    def cover_proxy(*args,**kw):
        co[0]+=1
        return func(*args,**kw)
    return cover_proxy

def uncovered():
    return [c[1] for c in covers if not c[0] and not ignored(c[1])]

def ignored(func):
    try:
        return func in ignore or func.im_class in ignore
    except:
        return False
