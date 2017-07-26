from StringIO import StringIO

def execute(code, _globals={}, _locals={}):
    import sys
    fake_stdout = StringIO()
    __stdout = sys.stdout
    sys.stdout = fake_stdout
    try:
        #try if this is expressions
        ret = eval(code, _globals, _locals)
        result = fake_stdout.getvalue()
        sys.stdout = __stdout
        if ret:
            result += str(ret)
        return result
    except:
        try:
            exec(code, _globals, _locals)
        except:
            sys.stdout = __stdout
            import traceback
            buf = StringIO()
            traceback.print_exc(file=buf)
            return buf.getvalue()
        else:
            sys.stdout = __stdout
            return fake_stdout.getvalue()
