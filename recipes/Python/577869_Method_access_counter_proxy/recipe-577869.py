def MakeProxy(obje):
	from collections import Counter
	class proxy(obje):
		def __init__(self,*args,**kwargs):
                        super(proxy,self).__init__(*args,**kwargs)
                        self.counter = Counter()
                def __getattribute__(self,attr):
                        counter = super(proxy,self).__getattribute__("counter")
                        if attr == "counter":
                            return counter
                        counter[attr] += 1
                        return super(proxy,self).__getattribute__(attr)
        return proxy
"""
>>> list_proxy = MakeProxy(list)
>>> a = list_proxy((1,2,3,4))
>>> a
[1, 2, 3, 4]
>>> a.extend([7,8,9])
>>> a
[1, 2, 3, 4, 7, 8, 9]
>>> a.counter["extend"]
1
>>> dict_proxy = MakeProxy(dict)
>>> b = dict_proxy({})
>>> b
{}
>>> b["osman"] = "arabaci"
>>> b
{'osman': 'arabaci'}
>>> b.keys()
['osman']
>>> b.counter["keys"]
1

"""
