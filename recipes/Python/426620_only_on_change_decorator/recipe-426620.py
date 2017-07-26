def func_onchange(metric):
    def _inner_onchange(func):
        "A decorator that runs a function only when a generic metric changes."
        def decorated(*args, **kwargs):
            try:
                mresult = metric(*args, **kwargs)
                if decorated._last_metric != mresult:
                    decorated._last_metric = mresult
                    decorated._last_result = func(*args, **kwargs)
            except AttributeError:
                decorated._last_metric = mresult    
                decorated._last_result = func(*args, **kwargs)

            return decorated._last_result
        return decorated
    return _inner_onchange
    
def method_onchange(metric):
    def _inner_onchange(method):
        "A decorator that runs a method only when a generic metric changes."
        met_name = "_%s_last_metric" % id(method)
        res_name = "_%s_last_result" % id(method)
        def decorated(self, *args, **kwargs):
            try:
                mresult = metric(*args, **kwargs)
                if getattr(decorated, met_name)  != mresult:
                    setattr(decorated, met_name, mresult)
                    setattr(decorated, res_name, method(self, *args, **kwargs))
            except AttributeError:
                setattr(decorated, met_name, mresult)
                setattr(decorated, res_name, method(self, *args, **kwargs))

            return getattr(decorated, res_name)
        return decorated
    return _inner_onchange
    

# simple check to see if file changed
def cheezy_file_metric(filename):
    import os
    return os.stat(filename)

# Function example, will only read file contents when file stats change
@func_onchange(cheezy_file_metric)
def get_filecontents(filename):
    print 'reading "%s" contents' % filename
    return file(filename).read()

file('test.txt', 'w').write('original content')
print '-'*60
print get_filecontents('test.txt')
print '-'*60
print get_filecontents('test.txt')
file('test.txt', 'w').write('new and improved content!')
print '-'*60
print get_filecontents('test.txt')
print '-'*60
print get_filecontents('test.txt')


print '~'*60

# Method example, will only read file contents when file stats change
class FileReadThing:
    @method_onchange(cheezy_file_metric)
    def get_filecontents(self, filename):
        print 'reading "%s" contents' % filename
        return file(filename).read()

f = FileReadThing()
file('test.txt', 'w').write('original content')
print '-'*60
print f.get_filecontents('test.txt')
print '-'*60
print f.get_filecontents('test.txt')
file('test.txt', 'w').write('new and improved content!')
print '-'*60
print f.get_filecontents('test.txt')
print '-'*60
print f.get_filecontents('test.txt')
