def case(comparision):
    def __assign_case(f):
        f.__case = comparision
        return f
    return __assign_case

class switch:
    def __init__(self):
        self.__case_map = {}
        
        def set_case(key,f):
            self.__case_map[key] = f
        
        a = [getattr(self,e) for e in dir(self) if getattr(self,e) is not None and hasattr(getattr(self,e),'__case')]
        for f in a:
            cases = getattr(f,'__case')
            if isinstance(cases,tuple) or isinstance(cases,list):
                for c in cases: set_case(c,f)
            else:
                set_case(cases,f)
        
    def match(self,value):
        return self.__case_map[value]


class b(switch):
    @case((1,3))
    def event_one(self):
        print 'Event handler for 1,3 in b'
        
    @case(2)
    def event_two(self):
        print 'Event handler for 2 in b'



a = b()
a.match(1)()
a.match(2)()
