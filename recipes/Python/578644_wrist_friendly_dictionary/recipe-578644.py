class easyaccessdict(dict):
    def __getattr__(self,name):
        if name in self:
            return self[name]
        n=easyaccessdict()
        super().__setitem__(name, n)
        return n
    def __getitem__(self,name):
        if name not in self:
            super().__setitem__(name,nicedict())
        return super().__getitem__(name)
    def __setattr__(self,name,value):
        super().__setitem__(name,value)
