#
# replcode.py
# By Joel Gould
#   joelg@alum.mit.edu
#   http://www.gouldhome.com/
#
# This subroutine takes a string, which may have embedded Python code, and
# executes that embedded code, returning the resulting string.  It is useful
# for things like dynamically producing webpages.
#
# We first execute any code in [!! ... !!].  Then we evaluate any code in
# [?? ... ??].  We do allow nested block of executed code.  To use a nested
# block, include an integer in the block delimiters, ex: [1!! ... !!1]
#
# You can pass an errorLogger function to runPythonCode.  This function
# will be called to print additional error messages.  Default is 
# sys.stdout.write().
#
# Use the special function "OUTPUT" inside the embeded Python code to add text
# to the output.
#
# Here is a sample of using replcode:
#
# >>> import replcode
# >>> input_text = """
# ...     Normal line.
# ...     Expression [?? 1+2 ??].
# ...     Global variable [?? variable ??].
# ...     [!!
# ...         def foo(x):
# ...         	return x+x !!].
# ...     Function [?? foo('abc') ??].
# ...     [!!
# ...         OUTPUT('Nested call [?? variable ??]') !!].
# ...     [!!
# ...         OUTPUT('''Double nested [1!!
# ...                       myVariable = '456' !!1][?? myVariable ??]''') !!].
# ... """
# >>> global_dict = { 'variable': '123' }
# >>> output_text = replcode.runPythonCode(input_text,global_dict)
# >>> print output_text
#
#     Normal line.
#     Expression 3.
#     Global variable 123.
#     .
#     Function abcabc.
#     Nested call 123.
#     Double nested 456.
#

import re
import sys
import string

#---------------------------------------------------------------------------

def runPythonCode(data, global_dict={}, local_dict=None, errorLogger=None):
    eval_state = EvalState(global_dict, local_dict, errorLogger)

    data = re.sub(r'(?s)\[(?P<num>\d?)!!(?P<code>.+?)!!(?P=num)\]', eval_state.exec_python, data)
    data = re.sub(r'(?s)\[\?\?(?P<code>.+?)\?\?\]', eval_state.eval_python, data)
    return data

#---------------------------------------------------------------------------
# This class is used to encapuslate the global and local dictionaries with
# the exec_python and eval_python functions.
    
class EvalState:

    def __init__(self, global_dict, local_dict, errorLogger):
        self.global_dict = global_dict
        self.local_dict = local_dict
        if errorLogger:
            self.errorLogger = errorLogger
        else:
            self.errorLogger = sys.stdout.write
        # copy these things into the global dictionary
        self.global_dict['OUTPUT'] = OUTPUT
        self.global_dict['sys'] = sys
        self.global_dict['string'] = string
        self.global_dict['__builtins__'] = __builtins__
        
    # Subroutine called from re module for every block of code to be
    # executed. Executed code can not return anything but it is allowed to
    # call the OUTPUT subroutine.  Any string produced from OUTPUT will
    # added to the OUTPUT_TEXT global variable and returned.

    def exec_python(self, result):
        # Condition the code.  Replace all tabs with four spaces.  Then make
        # sure that we unindent every line by the indentation level of the
        # first line.
        code = result.group('code')
        code = string.replace(code, '\t', '    ')
        result2 = re.search(r'(?P<prefix>\n[ ]*)[#a-zA-Z0-9''"]', code)
        if not result2:
            raise ParsingError,'Invalid template code expression: ' + code
        code = string.replace(code, result2.group('prefix'), '\n')
        code = code + '\n'

        try:
            self.global_dict['OUTPUT_TEXT'] = ''
            if self.local_dict:
                exec code in self.global_dict, self.local_dict 
            else:
                exec code in self.global_dict
            return self.global_dict['OUTPUT_TEXT']
        except:
            self.errorLogger('\n---- Error parsing: ----\n')
            self.errorLogger(code)
            self.errorLogger('\n------------------------\n')
            raise

    # Subroutine called from re module for every block of code to be
    # evaluated. Returned the result of the evaluation (should be a string).

    def eval_python(self, result):
        code = result.group('code')
        code = string.replace(code, '\t', '    ')
        try:
            if self.local_dict:
                result = eval(code, self.global_dict, self.local_dict)
            else:
                result = eval(code, self.global_dict)
            return str(result)
        except:
            self.errorLogger('\n---- Error parsing: ----\n')
            self.errorLogger(code)
            self.errorLogger('\n------------------------\n')
            raise

#---------------------------------------------------------------------------
# This routine is only called when OUTPUT() is included in executed Python
# code from the templates.  It evaluates its parameter as if it was a
# template and appends the result to the OUTPUT_TEXT variable in the global
# dictionary.    

def OUTPUT(data):
    # This magic python code extracts the local and global dictionaries in
    # the stack frame which was in effect when OUTPUT was called.
    try:
        raise ZeroDivisionError
    except ZeroDivisionError:
        local_dict = sys.exc_info()[2].tb_frame.f_back.f_locals
        global_dict  = sys.exc_info()[2].tb_frame.f_back.f_globals

    global_dict['OUTPUT_TEXT'] = global_dict['OUTPUT_TEXT'] +         runPythonCode(data, global_dict, local_dict)
