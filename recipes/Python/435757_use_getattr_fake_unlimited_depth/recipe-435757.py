class MagicObject:

    def __call__(self,*args,**kwargs):
        return MagicObject.__dict__['_stop'](self,self.n,*args,**kwargs)

    def __getattr__(self,name):
        if name in ('__str__','__repr__'): return lambda:'instance of %s at %s' % (str(self.__class__),id(self))
        if not self.__dict__.has_key('n'):self.n=[]
        self.n.append(name)
        return self

    def _stop(self,n,*args,**kwargs):
        self.n=[]
        return self.default(n,*args,**kwargs)

    def default(self,n,*args,**kwargs):
        return 'stop',n,args,kwargs

#############################################################333

>>c=MagicObject()
>>x=c.beubeb.zzzzz(1,2,3,a='bbb')
>>print x
('stop', ['beubeb', 'zzzzz'], (1, 2, 3), {'a': 'bbb'})
