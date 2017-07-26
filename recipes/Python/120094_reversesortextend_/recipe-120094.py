#features:
#oneliner to reverse,sort,extend a string /tuple/list
#can also pass user defined func in sort
#string or tuple or list can be extended to list,tuple
#for None returns 0

op=lambda o,f,p='',t=type:t(o) in [t(()),t(''),t([])] and eval("lambda o,l,t,p:[l.extend(o),l.%s(%s),%s(l)][2]"%(f,['p',''][f=='reverse' or not p],[["''.join","tuple"][t(o)==t(())],''][t(o)==t([])]))(o,[],t,p)

#if u want that faster versions
#then use this as it creates three lambdas and returns them
#so that they may be used later
reverse,extend,sort = map(lambda a:eval("lambda o,%sl=[[]],t=type:t(o) in [t(()),t(''),t([])] \
                           and [l.pop(0),l.append(list(o)),l[0].%s, t(o)==t('') and ''.join(l[0])\
                           or t(o)==t(()) and tuple(l[0]) or l[0]][3]"%(a[0],a[1])),
            [['','reverse()'],['o1=[],','extend(o1)'],['f=cmp,','sort(f)']])


#if you are wondering whats happening above....
#the basic approach is to convert tuple/string to list
#do operation and reconvert it to tuple/string
#may be recipe
#http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/119029
#will help u to understand that

#test code
obj=(2,1,3)
print 'sort',obj,op(obj,'sort')
print 'extend',obj,op(obj,'extend',obj)
print 'reverse',obj,op(obj,'reverse')
obj='anurag'
print 'sort',obj,op(obj,'sort',lambda a,b:cmp(b,a))
print 'extend',obj,op(obj,'extend',' uniyal')
print 'reverse',obj,op(obj,'reverse')
obj=[6,2,5]
print 'sort',obj,op(obj,'sort')
print 'extend',obj,op(obj,'extend','abc')
print 'reverse',obj,op(obj,'reverse')
