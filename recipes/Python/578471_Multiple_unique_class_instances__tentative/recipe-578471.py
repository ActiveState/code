>>> import base
>>> class UniqueSub(base.UniqueBase):
    def __init__(self, unique_id, a=1, b=2, **kw_args):
        super(UniqueSub, self).__init__(unique_id, **kw_args)
        self.a = a
        self.b = b
>>> first = UniqueSub("item 1")
>>> second = UniqueSub("item 2", a=4, b=7) # keyword arguments are required
>>> third = UniqueSub("item 1", a=3, b=6) # new argument values are ignored
>>> third.a
1
>>> third.b
2
>>> first == third
True
>>> import pickle
>>> with open("/tmp/test.pkl", "wb") as handle:
    pickle.dump(first, handle, 0) # protocol level zero just to prove that it also works
>>> with open("/tmp/test.pkl", "rb") as handle:
    fourth = pickle.load(handle)
>>> fourth == first
True
