import sys
import unittest

BEGIN_ACTIVE_FUNC = "\x80"
BEGIN_NEUTRAL_FUNC = "\x81"
END_FUNC = "\x8f"
END_ARG = "\x8e"
SEGMENT_GAP = "\xff"

class TracError(Exception): 
    pass

def list_get(list_, index, default=""):
    try:
        return list_[index]
    except:
        return default
    
def scan_char(list_, pos):
    return list_get(list_, pos)

def scan_chars(list_, pos, n):
    chars = []
    for i in range(n):
        c = scan_char(list_, pos + i)
        if c:
            chars.append(c)
    return "".join(chars)

class Processor(object):
    def __init__(self, program=""):
        self.work = []           # workspace containing current TRAC program
        self.sp = 0              # position of scanning pointer in workspace
        self.forms = {}          # key-value storage for program variables
        self.output = ""         # last string printed to output by ps for unit testing
        self.trace = True        # flag for printing trace results of function evaluation
        self.primitives = {}     # dictionary containing bound methods for TRAC primitives
        self.initialize(program)
        
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
        self.work = []
        self.reset()
        self.work += program
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
        
    def run(self):
        args = []
        handler = self.scan_next_char
        while handler:
            try:
                next_handler, args = handler(args)
            except TracError, e:
                sys.stderr.write("TracError: %s\n" % e )
                next_handler, args = self.reset, []
            handler = next_handler      
                    

    def scan_next_char(self, args):  # Rule 1
        args = []
        #self.db("scan_next_char")
        c = scan_char(self.work, self.sp)
        if c:
            if c == '(':
                handler = self.handle_begin_paren
            elif c in "\n\r\t":
                handler = self.handle_tab_return
            elif c == ',':
                handler = self.handle_comma
            elif c == '#' and scan_chars(self.work, self.sp, 2) == '#(':
                handler = self.handle_begin_active_func
            elif c == '#' and scan_chars(self.work, self.sp, 3) == '##(':
                handler = self.handle_begin_neutral_func
            elif c == '#':
                handler = self.handle_sharp_sign
            elif c == ')':
                handler = self.handle_end_paren
            else:
                args.append(c)
                handler = self.handle_char
        else:
            self.db("exit")
            print "Forms: %s" % (self.forms)
            print "Output: [%s]" % (self.output)
            handler = None
        return handler, args
     
    def handle_begin_paren(self, args): # Rule 2 
        args = []
        nested_count = 1
        chars = []
        matched = False
        del self.work[self.sp]
        c = scan_char(self.work, self.sp)
        while c and not matched:
            if c == ')':
                nested_count -= 1
                if nested_count == 0:
                    matched = True         
                    break         
            if not matched:                
                if c == '(':
                    nested_count += 1
                chars.append(c)
            self.sp += 1
            c = scan_char(self.work, self.sp)
        if matched:
            del self.work[self.sp]
        else:
            raise TracError, "%s: can't find matching end parenthesis" %("handle_begin_paren") 
        return self.scan_next_char, []
    
    def handle_tab_return(self, args):  # Rule 3
        args = []
        del self.work[self.sp]
        self.sp -= 1
        return self.inc_scan_pointer_continue, args
    
    def handle_comma(self, args):  # Rule 4
        args = []
        self.work[self.sp] = END_ARG
        return self.inc_scan_pointer_continue, args

    def handle_begin_active_func(self, args):  # Rule 5 
        args = []
        del self.work[self.sp:self.sp + 2]
        self.work.insert(self.sp, BEGIN_ACTIVE_FUNC)
        self.sp += 1
        return self.scan_next_char, args
    
    def handle_begin_neutral_func(self, args):  # Rule 6
        args = []
        del self.work[self.sp:self.sp + 3]
        self.work.insert(self.sp, BEGIN_NEUTRAL_FUNC)
        self.sp += 1
        return self.scan_next_char, args
    
    def handle_sharp_sign(self, args):  # Rule 7
        args = []
        return self.inc_scan_pointer_continue, args
        
    def handle_end_paren(self, args): # Rule 8
        #self.db("end_paren_0")
        args = []
        self.work[self.sp] = END_FUNC 
        func_begin = self.get_func_begin()
        func_result = self.eval_func(func_begin)
        func_marker = self.work[func_begin]
        args.append(func_begin)
        if func_result == "":
            handler = self.handle_null_func_result  # Rule 10
        elif func_marker == BEGIN_ACTIVE_FUNC:
            args.append(func_result)
            handler = self.handle_active_func_result  # Rule 11
        elif func_marker == BEGIN_NEUTRAL_FUNC:
            args.append(func_result)
            handler = self.handle_neutral_func_result  # Rule 12
        else:
            raise TracError, "%s: invalid func_marker" %("handle_end_paren") 
        #self.db("end_paren_1")
        return handler, args
        
    def get_func_begin(self):
        pos = self.sp - 1
        c = self.work[pos]
        while c:
            if c == BEGIN_ACTIVE_FUNC or c == BEGIN_NEUTRAL_FUNC:
                break
            pos -= 1
            if pos >= 0:
                c = self.work[pos]
            else:
                raise TracError, "%s: can't find begin function marker" %("get_func_begin") 
        return pos

    def get_func_end(self, func_begin):
        pos = func_begin
        c = self.work[pos]
        while c:
            if c == END_FUNC:
                break
            pos += 1
            c = self.work[pos]
        return pos
    
    def get_func_args(self, func_begin):
        args = []
        cur_arg = []
        pos = func_begin
        c = self.work[pos]
        db = []
        while c:
            db.append(c)
            if c == BEGIN_ACTIVE_FUNC or c == BEGIN_NEUTRAL_FUNC:
                pass
            elif c == END_ARG or c == END_FUNC:
                arg = "".join(cur_arg)
                args.append(arg)
                cur_arg = []
            else:
                cur_arg.append(c)    
            if c != END_FUNC:
                pos += 1
                c = self.work[pos]   
                db = []
            else:
                break
        return args
    
    def eval_func(self, func_begin):
        result = ""
        try:
            args = self.get_func_args(func_begin)
            func_name = args[0]
            primitive = self.primitives.get(func_name, None)
            if primitive:
                result = primitive(args[1:])
                if self.trace:
                    print "eval_func: %s %s -> [%s]" % (func_name, args[1:], result)
        except Exception, e:
            raise TracError, "%s: failed - %s" %("eval_func", e) 
        return result
    
    def handle_char(self, args):  # Rule 9
        c = args[0]
        args = []
        return self.inc_scan_pointer_continue, args
    
    def handle_null_func_result(self, args):  # Rule 10
        return self.handle_func_cleanup, args
    
    def handle_active_func_result(self, args):  # Rule 11 
        func_begin = args[0]
        func_result = args[1]
        args = []
        self.work[self.sp+1:self.sp+1] += func_result
        args.append(func_begin)
        #self.db("handle_active_func_result")
        return self.handle_func_cleanup, args
         
    def handle_neutral_func_result(self, args):  # Rule 12
        func_begin = args[0]
        func_result = args[1]
        args = []
        self.work[self.sp+1:self.sp+1] += func_result
        func_end = self.sp
        del self.work[func_begin:func_end + 1]
        self.sp = func_begin + len(func_result) - 1
        #self.db("handle_neutral_func_result")
        return self.inc_scan_pointer_continue, args
    
    def handle_func_cleanup(self, args):  # Rule 13
        if args:
            func_begin = args[0]
            func_end = self.get_func_end(func_begin)
            args = []
            del self.work[func_begin:func_end + 1]
            self.sp = func_begin - 1
        #self.db("handle_func_cleanup")
        return self.inc_scan_pointer_continue, args
    
    def reset(self, args=[]):  # Rule 14
        args = []
        self.work = []
        self.sp = 0
        return self.scan_next_char, args
    
    def inc_scan_pointer_continue(self, args):  # Rule 15
        args = []
        self.sp += 1
        return self.scan_next_char, args
    
    def db(self, msg="db"):
        print "%s: %s SP:%d %s" % (msg, self.work[0:self.sp], self.sp, self.work[self.sp:])       


class TestTrac(unittest.TestCase):
        
    def setUp(self):
        pass
        
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
