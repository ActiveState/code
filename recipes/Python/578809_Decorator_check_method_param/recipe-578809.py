def accepts(exception,**types):
    def check_accepts(f):
        assert len(types) == f.func_code.co_argcount, \
        'accept number of arguments not equal with function number of arguments in "%s"' % f.func_name
        def new_f(*args, **kwds):
            for i,v in enumerate(args):
                if types.has_key(f.func_code.co_varnames[i]) and \
                    not isinstance(v, types[f.func_code.co_varnames[i]]):
                    raise exception("arg '%s'=%r does not match %s" % \
                        (f.func_code.co_varnames[i],v,types[f.func_code.co_varnames[i]]))
                    del types[f.func_code.co_varnames[i]]

            for k,v in kwds.iteritems():
                if types.has_key(k) and not isinstance(v, types[k]):
                    raise exception("arg '%s'=%r does not match %s" % \
                        (k,v,types[k]))

            return f(*args, **kwds)
        new_f.func_name = f.func_name
        return new_f
    return check_accepts


def exmaple():

    @accepts(Exception,a=int,b=list,c=(str,unicode))
    def test(a,b=None,c=None)
        print 'ok'

    test(13,c=[],b='df') 
