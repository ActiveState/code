import sys
import os
import unittest

EOF = ""
SEGMENT_GAP = "\xff"

class TracException(Exception):
    pass

def list_get(list_, index, default=EOF):
    try:
        return list_[index]
    except:
        return default

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
    
    def get_trac_string(self):
        chars = []
        c = self.pop()
        while True:
            if c == '#':
                if self.peek(1) == '(' or self.peek(2) == '#(':
                    break
            elif c in "(),":
                break
            else:
                chars.append(c)
                c = self.pop()
        if c != EOF: 
            self.push(c)
        s = "".join(chars)
        return s

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
            raise TracException, "%s: can't find matching end parenthesis" %("get_trac_protected_string") 
        s = "".join(chars[1:-1])
        return s

class Tag(object):
    CLOSE_PAREN = ')'
    COMMA = ','    
    NONE = -1
    STRING = 300
    OPEN_ACTIVE_FUNC = 400
    OPEN_NEUTRAL_FUNC = 500
    DONE = 600    
    
class Token(object):
    def __init__(self, t, value=''):
        self.tag = t
        self.value = value
        
    def __str__(self):
        return "Token([%s] [%s])" % (str(self.tag), str(self.value))
    
class String(Token):
    def __init__(self, v):
        Token.__init__(self, Tag.STRING, v)
      
class Lexer(object):
    def __init__(self):
        self.lookahead = None
        self.output = ""         # last string printed to output by ps for unit testing
        self.trace = True        # flag for printing trace results of function evaluation     
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

    def initialize(self, program=""):
        self.forms = {}
        self.io = Io(program)

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

    def lexan(self):
        token = None
        while not token:
            c = self.io.pop()
            if c == '\t' or  c == '\n':
                pass # strip out white space
            elif c == '(':
                self.io.push(c)
                s = self.io.get_trac_protected_string()
                token = String(s)       
            elif c == ')':
                token = Token(Tag.CLOSE_PAREN)
            elif c == '#' and self.io.peek(1) == '(':
                self.io.delete(0,1)
                token = Token(Tag.OPEN_ACTIVE_FUNC)
            elif c == '#' and self.io.peek(2) == '#(':
                self.io.delete(0,2)
                token = Token(Tag.OPEN_NEUTRAL_FUNC)
            elif c == ',':
                token = Token(Tag.COMMA)
            elif c == EOF:
                token = Token(Tag.DONE)
            else:
                self.io.push(c)
                s = self.io.get_trac_string()
                token = String(s)       
        
        return token
            
    def func(self, tag=""):
        result = ""
        args = []
        token = self.lookahead
        if token.tag == Tag.STRING:
            args.append(token.value)        
        self.factor()
        while True:
            token = self.lookahead
            if token.tag in (Tag.STRING, Tag.OPEN_ACTIVE_FUNC, 
                             Tag.OPEN_NEUTRAL_FUNC, Tag.COMMA):
                if token.tag == Tag.STRING:
                    args.append(token.value)
                result = self.factor()
                if token.tag == Tag.OPEN_NEUTRAL_FUNC:
                    args.append(result)
            else:
                if tag:
                    result = self.eval_func(args)
                break
        return result
            
    def factor(self):
        result = None
        token = self.lookahead
        if token.tag == Tag.OPEN_ACTIVE_FUNC:
            self.match(Tag.OPEN_ACTIVE_FUNC)
            result = self.func(token.tag)
            self.match(Tag.CLOSE_PAREN, result)
        elif token.tag == Tag.OPEN_NEUTRAL_FUNC:
            self.match(Tag.OPEN_NEUTRAL_FUNC)
            result = self.func(token.tag)
            self.match(Tag.CLOSE_PAREN)
        elif token.tag == Tag.COMMA:
            self.match(Tag.COMMA)
        elif token.tag == Tag.STRING:
            self.match(Tag.STRING)
        elif self.lookahead.tag == Tag.DONE:
            self.match(Tag.DONE)
        else:
            raise TracException("factor: bad token tag - %s" % token)     
        return result
   
    def match(self, tag, result=None):
        if self.lookahead.tag == tag:
            if result != None:
                self.io.push(result)
            self.lookahead = self.lexan()
        else:
            raise TracException("match: tag %s doesn't match %s" % (tag, self.lookahead))

    def eval_func(self, args):
        result = ""
        try:
            func_name = args[0]
            args = args[1:]
            primitive = self.primitives.get(func_name, None)
            if primitive:
                result = primitive(args)
                if self.trace:
                    print "eval: %s %s -> [%s]" % (func_name, args, result)
        except Exception, e:
            raise TracException, "%s: failed - %s" %("eval", e) 
        return result
        
    def parse(self):
        self.lookahead = self.lexan()
        while self.lookahead.tag != Tag.DONE:
            self.func()
            self.match(Tag.DONE)
        print "Forms: %s" % self.forms
        print "Output: %s" % self.output
        return self
            
class TestTrac(unittest.TestCase):
        
    def setUp(self):
        pass
        
    def __test(self, program, output):
        self.lexer = Lexer()
        self.lexer.initialize(program)
        self.lexer.parse()
        self.assertEqual(self.lexer.output, output)

    def test_1_ps(self):
        self.__test("#(ps,Hello world)", "Hello world")
    
    def test_2_equal(self):
        self.__test("#(ps,#(eq,A,A,=,!=))", "=")

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
