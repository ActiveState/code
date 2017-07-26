def f(**kw):
    for k,v in kw.iteritems():
        locals()[k]=v
    exec('pass') # apply locals %)
    print x

f(x='test')
