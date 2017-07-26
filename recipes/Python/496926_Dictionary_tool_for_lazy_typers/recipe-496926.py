# new dictionary. Instead of {"a":3}, do this: nd(a=3)

def nd(**kargs): 
    d={}
    d.update(kargs)
    return d

# update dict. Instead of d.update({"a":3,"b":4}),
# do this: ud(d,a=3,b=4) 

def ud(obj, **kargs): 
    obj.update(kargs)
