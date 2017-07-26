class terminal(type):
    def __init__(self, cl_name, bases, namespace):
        for cls in bases:
            if isinstance(cls, terminal):
                raise TypeError("in "+cl_name+" definition : "+str(cls)+
                                " can't be used as a base class")
        super(terminal, self).__init__(cl_name, bases, namespace)


# first we create a normal class
class a(object):
    pass

#the terminal class: it can inherit from other classes but can't be
#used as base class
class b(a):
    __metaclass__= terminal

#this will fail at compile time, because inheriting from b is forbidden
class c(b):
    pass
