import inspect

test_template = '''Hello, %(first_name)s %(last_name)s'''

def call_template(template,context=None,**kw):
    """ Calls a template and returns the generated content.
        this is pretty much braindead, it's just meant to give you
        the general idea.
    """

    # efficiency is not the problem here
    if context is not None:
        d = dict(context)
        d.update(kw)
    else:
        d = kw
    
    return template%d

def call_contextual_template(template):
    # this is the magic line    
    frame = inspect.currentframe().f_back
    
    # again, we don't care about efficiency, it's not the point here
    d = dict(frame.f_globals)
    d.update(frame.f_locals)
    
    return call_template(template,d)

def test_1():
    first_name = "Foo" # imagine it is fetched from database
    last_name = "Bar"
    print call_template(test_template,{
        "first_name":first_name,
        "last_name":last_name,
    }) # this is ugly !

def test_2():
    first_name = "Foo" # imagine it is fetched from database
    last_name = "Bar"
    print call_template(test_template,
        first_name=first_name,
        last_name=last_name,
    ) # this is ugly !
    
def test_3():
    first_name = "Foo" # imagine it is fetched from database
    last_name = "Bar"
    print call_contextual_template(test_template) # this is much better
    
if __name__=='__main__':
    test_1()
    test_2()
    test_3()
