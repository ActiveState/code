def get_names_dict(*args):
    id2name = dict((id(val), key) for key, val in inspect.stack()[1][0].f_locals.items())
    return dict((id2name[id(a)], a) for a in args)

# >>> a = 1
# >>> b = 'b'
# >>> print get_names_dict(a, b)
# {'a': 1, 'b': 'b'}

def foo(a, b, c, d, e):
    #something interesting here



def main(argv):
    a, b, c, d, e = get_some_interesting_values()
    print 'calling foo with ', get_names_dict(a, b, c, d, e)
    foo(a, b, c, d, e)
