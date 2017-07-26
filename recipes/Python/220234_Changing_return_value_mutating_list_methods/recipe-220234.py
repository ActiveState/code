def wrapedmeth(classname,meth):
    def _meth(self,*argl,**argd):
        getattr(super(globals()[classname],self),meth)(*argl,**argd)
        return self

    return _meth

class ReturnMeta(type):
    def __new__(cls,classname,bases,classdict):
        wrap = classdict.get('return_self_super_methods')
        if wrap is not None:
            for method in wrap:
                classdict[method] = wrapedmeth(classname,method)
        return super(ReturnMeta,cls).__new__(cls,classname,bases,classdict)

class mylist(list):
    __metaclass__ = ReturnMeta
    return_self_super_methods = ['append','extend','insert','remove','reverse','sort']


if __name__ == '__main__':
    print 'l = [1,2]'
    print 'mylist: print l.append(3)'
    l = mylist([1,2])
    print l.append(3)
    print 'list: print l.append(3)'
    l = [1,2]
    print l.append(3)
