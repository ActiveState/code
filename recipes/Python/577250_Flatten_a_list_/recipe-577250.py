    def flattenlist(L):
        import types
        WhiteTypes = ('StringType', 'UnicodeType', 'StringTypes', 'ListType',
                  'ObjectType', 'TupleType')
        BlackTypes= tuple( [getattr(types, x) for x in dir(types)
                      if not x.startswith('_')
                      and x not in whites] )

        tmp = []
        def core(L):
            if  not hasattr(L,'__iter__'):
                return [L]
            else :
                for i in L:
                    if isinstance(i,BlackTypes):
                        tmp.append(i)
                        continue
                    if type(i) == type(str()):
                        tmp.append(i)
                    else:
                        core(i)
            return tmp
        return core(L)




#Examples x=[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[['x']]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
>>> flattenlist(x)
['x']
>>> x=(((((1)))))
>>> flattenlist(x)
[1]
>>> x=[(),(),[]]
>>> flattenlist(x)
[]
>>> x=[(1),('1'),[1.0]]
>>> flattenlist(x)
[1, '1', 1.0]
>>> x=[[[[[[(((([1,1]))))]]]]]]
>>> flattenlist(x)
[1, 1]
>>> x=1
>>> flattenlist(x)
[1]
>>> x=flattenlist
>>> flattenlist(x)
[<function flattenlist at 0x16a8320>]
>>> 
