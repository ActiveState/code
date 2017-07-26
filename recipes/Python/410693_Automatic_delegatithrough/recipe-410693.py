# helper descriptor
class _descr(object):
    objrefs = {}
    clsrefs = {}
    def __init__(self,name):
        self.name = name
    def __get__(self,instance,owner):
        if instance is None:
            return getattr(_descr.clsrefs[id(owner)],self.name)
        else:
            return getattr(_descr.objrefs[id(instance)],self.name)
    def __set__(self,instance,value):
        setattr(_descr.objrefs[id(instance)],self.name,value)

# main function
def immerse(source_obj,dest_obj):
    dest_cls = dest_obj.__class__
    _descr.objrefs[id(dest_obj)]=source_obj
    _descr.clsrefs[id(dest_cls)]=source_obj.__class__
    for name in dir(source_obj):
        if not hasattr(dest_obj,name):
            setattr(dest_cls,name,_descr(name))

### TEST ###

# class whose instance will be immersed in B instances
class A:
    x1 = "A.x1"
    y1 = "A.y1"
    def __init__(self):
        self.x2 = "x2 of %s"%self
        self.y2 = "y2 of %s"%self

    def foo1(self,z):
        print "A.foo1(%s,%s)"%(self,z)

    def foo2(self,z):
        print "A.foo2(%s,%s)"%(self,z)

    def __getitem__(self,value):
        print "A.__getitem__(%s,%s)"%(self,value)
        return value

# main class
class B(object):
    x1 = "B.x1"
    def __init__(self):
        self.y2 = "y2 of %s"%self

        self.a = A() # instance to be immersed
        immerse(self.a,self) # immersion

    def foo1(self,z):
        print "B.foo1(%s,%s)"%(self,z)

b=B()

print "b.x1="+b.x1
print "b.x2="+b.x2
print "b.y1="+b.y1
print "b.y2="+b.y2

print "executing b.foo1(10)..."
b.foo1(10)
print "executing b.foo2(20)..."
b.foo2(20)
print "executing b['hi all']..."
b["hi all"]

# output:
# b.x1=B.x1
# b.x2=x2 of <__main__.A instance at 0x00B85828>
# b.y1=A.y1
# b.y2=y2 of <__main__.B object at 0x00B83A50>
# executing b.foo1(10)...
# B.foo1(<__main__.B object at 0x00B83A50>,10)
# executing b.foo2(20)...
# A.foo2(<__main__.A instance at 0x00B85828>,20)
# executing b['hi all']...
# A.__getitem__(<__main__.A instance at 0x00B85828>,hi all)
