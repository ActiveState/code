class mylist(list):
    def __getitem__(self, item):
        r = []
        if type(item) == tuple:
                for i in item:
                    if type(i) == slice:
                        r.extend(super(self.__class__, self).__getitem__(i))
                    else:
                        r.append(super(self.__class__, self).__getitem__(i))
                return r
        else:
                return super(mylist, self).__getitem__(item)

    def __setitem__(self, item, value):
        if type(item) == tuple:
                for i, val in zip(item, value):
                    super(self.__class__, self).__setitem__(i, val)
        else:
                super(self.__class__, self).__setitem__(item, value)
        


class mytuple(tuple):
    def __getitem__(self, item):
        r = []
        if type(item) == tuple:
                for i in item:
                    if type(i) == slice:
                        r.extend(super(self.__class__, self).__getitem__(i))
                    else:
                        r.append(super(self.__class__, self).__getitem__(i))
                return r
        else:
                return super(mylist, self).__getitem__(item)



# Not a good idea, is tuple a key or a set of keys?
class mydict(dict):
    def __getitem__(self, item):
        r = []
        if type(item) == tuple:
                for i in item:
                        r.append((super(self.__class__, self).__getitem__(i)))
                return r
        else:
                return super(mylist, self).__getitem__(item)

# Examples
l = mylist(range(0,10))
t = mytuple(range(0,10))
d = mydict({'1':'one', '2':'two', '3':'three', '4':'four', '5':'five'})

print l[0,-1]        # Get only the first and last item
                     # [ l[0], l[-1] ]
print l[1,3:]        # Get item 1 and items 3 till the end
                     # [ l[1] ] + l[3:]
print l[1,5,7,2,3]   # Get items 1, 5, 7, 2 and 3
                     # [ l[1], l[5], l[7], l[2], l[3] ]
l[0,1:] = None, [] # Setting the first element of the list to None and removeing the rest
print l              # l[0], l[1:] = None, []
            

print t[:,0,:]  # Get the tuple twice qith the first element in between
                # t + (t[0],) + t
print t[:,::-1] # Get the tuple twice, once foreward and once reversed
                # t + t[::-1]
