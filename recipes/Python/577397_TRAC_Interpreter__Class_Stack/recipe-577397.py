import sys
import unittest
import time

EOF = ""
SEGMENT_GAP = "\xff"
INCOMPLETE, COMPLETE = range(0,2)

class TracError(Exception): 
    pass

class Io(object):
    def __init__(self, s=""):
        self.buffer = []
        self.buffer += s
        
    def pop(self, default=EOF):
        try:
            return self.buffer.pop(0)
        except:
            return default

    def push(self, s):
        self.buffer[0:0] += s

    def delete(self, i, j):
        del self.buffer[i:j]

    def peek(self, count=1):
        try:
            chars = self.buffer[0:0 + count]
        except:
            chars = [EOF]
        return "".join(chars)
    
    def get_trac_protected_string(self):
        chars = []
        paren_count = 0
        matched = False
        c = self.pop()
        while c != EOF and not matched:
            if c == '(':
                paren_count += 1
            elif c == ')':
                paren_count -= 1
            chars.append(c)
            if paren_count != 0:
                c = self.pop()
            else:
                matched = True                 
        if not matched:
            raise TracError, "%s: can't find matching end parenthesis" %("get_trac_protected_string") 
        s = "".join(chars[1:-1])
        return s

def list_get(list_, index, default=""):
    try:
        return list_[index]
    except:
        return default
    
class Expr(object):
    def __init__(self):
        self.chars = []
        
    def value(self):
        return "".join(self.chars)
    
    def append(self, c):
        self.chars.append(c)
        
    def process_char(self, c):
        self.append(c)
        return INCOMPLETE

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.chars)
    
class Root(Expr):
    def __init__(self):
        Expr.__init__(self)

class Protected(Expr):
    def __init__(self):
        Expr.__init__(self)


class Function(Expr):
    def __init__(self):
        Expr.__init__(self)
        self.args = []

    def process_char(self, c):
        if c == ',' or c == ')':
            arg = self.value()
            self.args.append(arg)
            del self.chars[:]
            if c == ')':
                return COMPLETE
        else:
            self.append(c)
        return INCOMPLETE
    
    def __repr__(self):
        return '%s(%s %s)' % (self.__class__.__name__, self.chars, self.args)
    
class Active(Function):
    def __init__(self):
        Function.__init__(self)

class Neutral(Function):
    def __init__(self):
        Function.__init__(self)

class Processor(object):
    def __init__(self, program=""):
        self.io = Io(program)           
        self.forms = {}          # key-value storage for program variables
        self.output = ""         # last string printed to output by ps for unit testing
        self.trace = True        # flag for printing trace results of function evaluation

    def tn(self, args):
        self.trace = True
        return ""

    def tf(self, args):
        self.trace = False
        return ""

    def ds(self, args):
        key = list_get(args, 0)
        value = list_get(args, 1)
        self.forms[key] = value
        return ""

    def ps(self, args):
        try:
            s = list_get(args, 0)
            print s
            self.output = s
        except:
            pass
        return ""
    
    def ad(self, args):
        try:
            num1 = int(list_get(args, 0))
            num2 = int(list_get(args, 1))
            return str(num1 + num2)
        except:
            return ""
    
    def su(self, args):
        try:
            num1 = int(list_get(args, 0))
            num2 = int(list_get(args, 1))
            return str(num1 - num2)
        except:
            return ""
    
    def ml(self, args):
        try:
            num1 = int(list_get(args, 0))
            num2 = int(list_get(args, 1))
            return str(num1 * num2)
        except:
            return ""
    
    def dv(self, args):
        try:
            num1 = int(list_get(args, 0))
            num2 = int(list_get(args, 1))
            return str(num1 / num2)
        except:
            return ""

    def eq(self, args):
        try:
            s1 = list_get(args, 0)
            s2 = list_get(args, 1)
            eq_result = list_get(args, 2)
            neq_result = list_get(args, 3)
            if s1 == s2:
                return eq_result
            else:
                return neq_result
        except:
            return ""
    
    def ss(self, args):
        try:
            form_key = args.pop(0)
            form = self.forms[form_key]
            form_marked = form
            for i in range(len(args)):
                arg = args[i]
                marker = "%s%s" % (SEGMENT_GAP, chr(i))
                form_marked = form_marked.replace(arg, marker)
            self.forms[form_key] = form_marked
            form_list = []
            form_list += form_marked
            #print "ss: %s" % (form_list)
            return ""
        except:
            return ""
            
    def cl(self, args):
        try:
            form_key = args.pop(0)
            form = self.forms[form_key]
            form_processed = form
            for i in range(len(args)):
                arg = args[i]
                marker = "%s%s" % (SEGMENT_GAP, chr(i))
                form_processed = form_processed.replace(marker, arg)
            return form_processed
        except:
            return ""

    def initialize(self, program=""):
        self.forms = {}
        self.io = Io(program)           
        self.primitives = {"ds":self.ds, \
                           "ps":self.ps, \
                           "ss":self.ss, \
                           "cl":self.cl, \
                           "ad":self.ad, \
                           "su":self.su, \
                           "ml":self.ml, \
                           "dv":self.dv, \
                           "tn":self.tn, \
                           "tf":self.tf, \
                           "eq":self.eq \
                            }
        self.output = []
        self.stack = []
        self.cur_expr = Root()
        self.stack.append(self.cur_expr)
        return self

    def push(self, expr):
        self.stack.append(expr)
        self.cur_expr = expr

    def pop(self):
        if self.stack:
            expr = self.stack.pop()
            self.cur_expr = self.stack[-1]
            return expr
        return None
        
    def eval(self, func_expr):
        result = ""
        try:
            func_name = func_expr.args[0]
            args = func_expr.args[1:]
            primitive = self.primitives.get(func_name, None)
            if primitive:
                result = primitive(args)
                if self.trace:
                    print "eval: %s %s -> [%s]" % (func_name, args, result)
        except Exception, e:
            raise TracError, "%s: failed - %s" %("eval", e) 
        return result

    def run(self):
        while self.io.buffer:
#            print "Stack: %s" % self.stack
            c = self.io.pop()
            if c == '(':
                self.io.push(c)
                s = self.io.get_trac_protected_string()
                self.cur_expr.chars += s
            elif c == '#' and self.io.peek(1) == '(':
                self.io.delete(0,1)
                self.push(Active())
            elif c == '#' and self.io.peek(2) == '#(':
                self.io.delete(0,2)
                self.push(Neutral())
            elif c == ',':
                self.cur_expr.process_char(c)
            elif c in "\n\r\t":
                pass
            elif c == ')':
                complete = self.cur_expr.process_char(c)
                if complete == COMPLETE:
                    func_expr = self.pop()
                    func_result = self.eval(func_expr)
                    if isinstance(func_expr, Active):
                        self.io.push(func_result)
                    else:
                        self.cur_expr.chars += func_result
            else:
                self.cur_expr.process_char(c)
        if self.trace:
            print "Stack: %s" % self.stack
            print "Forms: %s" % self.forms
            print "Output: %s" % self.output

class TestTrac(unittest.TestCase):
    def setUp(self):
        pass

    def __setup(self, program, correct=""):
        self.processor = Processor()
        self.processor.initialize(program)
        self.processor.run()
        print str(self.processor.stack)

    def __test(self, program, output):
        self.processor = Processor()
        self.processor.initialize(program)
        self.processor.run()
        self.assertEqual(self.processor.output, output)

    def test_1_ps(self):
        self.__test("#(ps,Hello world)", "Hello world")

    def test_2_equal(self):
        self.__test("#(ps,#(eq,Cat,Cat,equal,not equal))", "equal")

    def test_3_not_equal(self):
        self.__test("#(ps,#(eq,Cat,Dog,equal,not equal))", "not equal")

    def test_4_ds(self):
        self.__test("#(ds,AA,Cat)#(ps,#(cl,AA))", "Cat")

    def test_5_protect_parens(self):
        self.__test("#(ds,AA,Cat)#(ds,BB,(#(cl,AA)))#(ps,(#(cl,BB)))", "#(cl,BB)")

    def test_6_neutral_func(self):
        self.__test("#(ds,AA,Cat)#(ds,BB,(#(cl,AA)))#(ps,##(cl,BB))", "#(cl,AA)")

    def test_7_indirection(self):
        self.__test("#(ds,AA,Cat)#(ds,BB,(#(cl,AA)))#(ps,#(cl,BB))", "Cat")

    def test_8_ss(self):
        self.__test("#(ds,AA,Hello X)#(ss,AA,X)#(ps,#(cl,AA,world))", "Hello world")

    def test_9_factorial(self):
        self.__test("""
#(ds,Factorial,(#(eq,X,1,1,(#(ml,X,#(cl,Factorial,#(su,X,1)))))))
#(ss,Factorial,X)
#(ps,#(cl,Factorial,5))
""", "120")

if __name__ == "__main__":
    print __file__
    unittest.main()

    
