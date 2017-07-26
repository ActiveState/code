import sys, inspect
from types import FunctionType

def magic():
    """
    Returns a string which represents Python code that copies instance 
    variables to their local counterparts. I.e:
        var = self.var
        var2 = self.var2
    """
    s = ""
    for var, value in inspect.getmembers(sys._getframe(1).f_locals["self"]):
        if not (var.startswith("__") and var.endswith("__")):
            s += var + " = self." + var + "\n"
    return s
    
def outdent_lines(lines):
    """
    Removes the outer indentation on the method's source code. The extra
    indentation comes from the fact that the method is defined within a
    class and therefore has an extra level of indentation around itself.
    """
    outer_ws_count = 0
    for ch in lines[0]:
        if not ch.isspace():
            break
        outer_ws_count += 1
    return [line[outer_ws_count:] for line in lines]
        
def insert_self_in_header(header):
    return header[0:header.find("(") + 1] + "self, " + \
        header[header.find("(") + 1:]
            
def get_indent_string(srcline):
    """
    Determines and returns how the line passed in is indented. That 
    information is used by rework() so that it can determine how much
    indentation to use to insert lines into the source. 
    """
    indent = ""
    for ch in srcline:
        if not ch.isspace():
            break
        indent += ch
    return indent
        
def rework(func):
    """
    rework() modifies the functions source code by first adding self 
    as the first argument in the parameter list and then adding
    'exec(magic())' as the first line of the function body. It does this
    by reading the functions source code and then creating a new modified
    function definition with exec() and then returns the new function.
    """
    srclines, line_num = inspect.getsourcelines(func)
    srclines = outdent_lines(srclines)
    dst = insert_self_in_header(srclines[0])
    if len(srclines) > 1:
        dst += get_indent_string(srclines[1]) + "exec(magic())\n"
        for line in srclines[1:]:
            dst += line
    dst += "new_func = eval(func.__name__)\n"
    exec(dst)
    return new_func
    
class LocalVarsMC(type):
    """
    A metaclass that transform all instance methods by applying rework()
    on them all. Some of the implementation is borrowed from
    http://www.xs4all.nl/~thomas/python/conveniencytypes.py.
    """
    def __init__(self, name, bases, attrs):
        super(LocalVarsMC, self).__init__(name, bases, attrs)
        ## Creates an unbound super object
        supername = "_%s__super" % name
        if hasattr(self, supername):
            raise TypeError, "Conflicting classname " + supername
        setattr(self, supername, super(self))
        try:
            for attr, value in attrs.items():
                if isinstance(value, FunctionType):
                    setattr(self, attr, rework(value))
        except IOError:
            print "Couldn't read source code - it wont work."
            sys.exit()
            
class LocalsFromInstanceVars(object):
    """
    Inherit from this class to make it work.
    """
    __metaclass__ = LocalVarsMC
    
import math

## ------- testcode ---------
    
class Vector3d(LocalsFromInstanceVars):
    def __init__(x, y, z):
        self.x, self.y, self.z = x, y, z
        
    def length():
        return math.sqrt(x*x + y*y + z*z)
        
    def dummy(): 
        pass
        
        
if __name__ == "__main__":    
    print "-"*20
    v = Vector3d(5, 4, 3)
    print v.length()
    v.x = 10
    print v.length()
    print v.dummy()
