'''
@author: Yoav Glazner
'''


def block(code):
    code = 'def anon(*args, **kw):\n'+'\n'.join(
                    "\t\t%s" % line for line in code.split('\n') if line.strip())
    env = {}
    exec code in env
    return env['anon'] #@UndefinedVariable suppressed


if __name__ == '__main__':
    from threading import Thread
    
    t = Thread(target=block('''\
    print 'pop'
    print 'pop2'
    '''))
    p, c = 'pop', 'corn'
    t2 = Thread(target=block('''\
    a, b = args
    print a + b
    '''), args=(p, c))
    
    t.start()
    t2.start()
    t.join()
    t2.join()
