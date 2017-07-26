# Config - reads a configuration file.
#
# This module parses a configuration file using a restricted Python syntax.
# The Python tokenizer/parser is used to read the file, unwanted expressions
# are removed from the parser output before the result is compiled and
# executed. The initialised configuration settings are returned in a dict.

import parser
import compiler
import symbol
import token
 
def _get_forbidden_symbols():
    """
    Returns a list of symbol codes representing statements that are *not*
    wanted in configuration files.
    """
    try:
        # Python 2.5:
        symlst = [symbol.break_stmt, symbol.classdef, symbol.continue_stmt,
                  symbol.decorator, symbol.decorators, symbol.eval_input,
                  symbol.except_clause, symbol.exec_stmt, symbol.flow_stmt,
                  symbol.for_stmt, symbol.fpdef, symbol.fplist, symbol.funcdef,
                  symbol.global_stmt, symbol.import_as_name, symbol.import_as_names,
                  symbol.import_from, symbol.import_name, symbol.import_stmt,
                  symbol.lambdef, symbol.old_lambdef, symbol.print_stmt,
                  symbol.raise_stmt, symbol.try_stmt, symbol.while_stmt,
                  symbol.with_stmt, symbol.with_var, symbol.yield_stmt,
                  symbol.yield_expr]
        
    except AttributeError:
        # Python 2.4:        
        symlst = [symbol.break_stmt, symbol.classdef, symbol.continue_stmt,
                  symbol.decorator, symbol.decorators, symbol.eval_input,
                  symbol.except_clause, symbol.exec_stmt, symbol.flow_stmt,
                  symbol.for_stmt, symbol.fpdef, symbol.fplist, symbol.funcdef,
                  symbol.global_stmt, symbol.import_as_name, symbol.import_as_names,
                  symbol.import_from, symbol.import_name, symbol.import_stmt,
                  symbol.lambdef, symbol.print_stmt, symbol.raise_stmt,
                  symbol.try_stmt, symbol.while_stmt]
    
    return symlst

def _parseconf(confstr):
    """
    Parse the configuration *confstr* string and remove anything else
    than the supported constructs, which are:

    Assignments, bool, dict list, string, float, bool, and, or, xor,
    arithmetics, string expressions and if..then..else.

    The *entire* statement containing the unsupported statement is removed
    from the parser; the effect is that the whole expression is ignored
    from the 'root' down.  

    The modified AST object is returned to the Python parser for evaluation. 
    """
    # Initialise the parse tree, convert to list format and get a list of
    # the symbol ID's for the unwanted statements. Might raise SyntaxError.
    
    ast = parser.suite(confstr)
    #ast = parser.expr(confstr)
    stmts = parser.ast2list(ast)
    rmsym = _get_forbidden_symbols()

    result = list()
    
    # copy 256: 'single_input', 257: 'file_input' or 258: 'eval_input'. The
    # parse tree must begin with one of these to compile back to an AST obj.

    result.append(stmts[0])

    # NOTE: This might be improved with reduce(...) builtin!? How can we get
    #       line number for better warnings?

    for i in range(1, len(stmts)):
        # censor the parse tree produced from parsing the configuration.
        if _check_ast(stmts[i], rmsym):
            result.append(stmts[i])
        else:
            pass
        
    return parser.sequence2ast(result)

def _check_ast(astlist, forbidden):
    """
    Recursively check a branch of the AST tree (in list form) for "forbidden"
    symbols. A token terminates the search.

    Returns False if any "forbidden symbols" are present, True otherwise. 
    """
    # check for token - tokens are always allowed.
    if astlist[0] in token.tok_name.keys():
        return True
    
    elif astlist[0] in forbidden:
        raise UserWarning('Statement containing '+symbol.sym_name[astlist[0]]
            +' not allowed, ignored!')
        return False
    
    else:
        return _check_ast(astlist[1], forbidden)
                  
def parse_config(confstr):
    """
    Use *eval(...)* to execute a filtered AST tree formed by parsing a
    configuration file, removing unwanted expressions (if any) and then
    compiling the filtered output to Python byte code. This approach
    allows the use of Python expressions and comments in config files,
    avoids the use of modules which is not particularily pretty (IMO).

    The following expressions (and combinations of) are allowed:

    Assignments, Arithmetic, Strings, Lists, if...then...else and
    Comments.

    Returns a dict containing the configuration values, if successful. 
    """
    dummy  = dict()
    result = dict()

    # Parse the python source code into a filtered AST-tree.
    cast = _parseconf(confstr)

    # Compile AST to bytecode, this also detects syntax errors.
    cobj = parser.compileast(cast)

    # Run the bytecode. The dicts *dummy* and *results* are placeholders
    # for the *globals* *locals* environments used by *eval(...)*. The
    # variables declared and initialised in the config file will end up
    # in *locals* together with the *__globals__* environment while the
    # *locals* will contain only the values created by *eval(...)*. This
    # is good, because we can protect *__globals__* and return only the
    # configuration values by doing this:
    
    eval(cobj, dummy, result)

    return result

# EOF


# <--------- split here ----------->


#!/usr/bin/env python
"""
Unit test for configuration handling. This is intended to be
run through the *tests* package, but should work stand-alone.
"""

import unittest
import sys, os
import tempfile
import string

# Adjust the import path to get the module we want to test.
# We are sitting in '<module>\\test' so one directory up
# will do the trick.

mod_path = os.path.normpath(os.getcwd()+'/..')
sys.path.append(mod_path)

import config

# import modules used internally by config.py.
import parser
import compiler
import symbol
import token
 

# Test: Assignments, bool, dict list, string, float, bool, and,
# or, xor,arithmetics, string expressions and if..then..else.
#
# The test code is mostly ripped from 'test_grammar.py', available
# from the Python source tree. 

test_backslash_1 = r"""
x = 1 \
+ 1
"""
test_backslash_2 = r"""
# Backslash does not means continuation in comments :\
x = 0
"""

test_integers_1 = r"""
a = 0xff
b = 0377
c = 2147483647
"""

test_long_ints_1 = r"""
x = 0L
x = 0l
x = 0xffffffffffffffffL
x = 0xffffffffffffffffl
x = 077777777777777777L
x = 077777777777777777l
x = 123456789012345678901234567890L
x = 123456789012345678901234567890l
"""

test_string_literals_1 = r"""
x = ''; y = ""
"""
test_string_literals_2 = r"""
x = '\''; y = "'"
"""
test_string_literals_3 = r"""
x = '"'; y = "\""
"""
test_string_literals_4 = r"""
x = "doesn't \"shrink\" does it"
y = 'doesn\'t "shrink" does it'
"""
test_string_literals_5 = r"""
x = "does \"shrink\" doesn't it"
y = 'does "shrink" doesn\'t it'
"""
test_string_literals_6 = r'''
x = r"""
The "quick"
brown fox
jumps over
the 'lazy' dog.
"""
y = '\nThe "quick"\nbrown fox\njumps over\nthe \'lazy\' dog.\n'
'''
test_string_literals_7 = r"""
y = '''
The "quick"
brown fox
jumps over
the 'lazy' dog.
'''
"""
test_string_literals_8 = r'''
y = "\n\
The \"quick\"\n\
brown fox\n\
jumps over\n\
the 'lazy' dog.\n\
"
'''
test_string_literals_9 = r"""
y = '\n\
The \"quick\"\n\
brown fox\n\
jumps over\n\
the \'lazy\' dog.\n\
'
"""

test_if_stmt_1 = r"""
if 1: pass
if 1: pass
else: pass
if 0: pass
elif 0: pass
if 0: pass
elif 0: pass
elif 0: pass
elif 0: pass
else: pass
"""

test_and_or_not_1 = r"""
if not 1: pass
if 1 and 1: pass
if 1 or 1: pass
if not not not 1: pass
if not 1 and 1 and 1: pass
if 1 and 1 or 1 and 1 and 1 or not 1 and 1: pass
"""

test_comparison_1 = r"""
if 1: pass
x = (1 == 1)
if 1 == 1: pass
if 1 != 1: pass
if 1 <> 1: pass
if 1 < 1: pass
if 1 > 1: pass
if 1 <= 1: pass
if 1 >= 1: pass
if 1 is 1: pass
if 1 is not 1: pass
if 1 in (): pass
if 1 not in (): pass
if 1 < 1 > 1 == 1 >= 1 <= 1 <> 1 != 1 in 1 not in 1 is 1 is not 1: pass
"""

test_binary_ops_1 = r"""
x = 1 & 1
x = 1 ^ 1
x = 1 | 1
"""

test_shift_ops_1 = r"""
x = 1 << 1
x = 1 >> 1
x = 1 << 1 >> 1
"""

test_additive_ops_1 = r"""
x = 1
x = 1 + 1
x = 1 - 1 - 1
x = 1 - 1 + 1 - 1 + 1
"""

test_multiplicative_ops_1 = r"""
x = 1 * 1
x = 1 / 1
x = 1 % 1
x = 1 / 1 * 1 % 1
"""

test_unary_ops_1 = r"""
x = +1
x = -1
x = ~1
x = ~1 ^ 1 & 1 | 1 & 1 ^ -1
x = -1*1/1 + 1*1 - ---1*1
"""

test_stmt_suite_1 = r"""
if 1: pass
if 1:
    pass
if 1:
#
#
#
    pass
pass
#
pass
#
"""

test_atoms_1 = r"""
x = (1)
x = (1 or 2 or 3)
x = (1 or 2 or 3, 2, 3)

x = []
x = [1]
x = [1 or 2 or 3]
x = [1 or 2 or 3, 2, 3]
x = []

x = {}
x = {'one': 1}
x = {'one': 1,}
x = {'one' or 'two': 1 or 2}
x = {'one': 1, 'two': 2}
x = {'one': 1, 'two': 2,}
x = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6}

x = `x`
x = `1 or 2 or 3`
x = x
x = 'x'
x = 123
"""

class test_config_internals(unittest.TestCase):
    """
    Verify the internal functions in the config module. 
    """
    def test_get_forbidden_symbols(self):
        # verify that we can get the symbol ID's.
        res = config._get_forbidden_symbols()
        self.failUnless(len(res) > 0)
        
        # verify that the forbidden symbols are valid.
        for i in range(0, len(res)):
            self.failUnless(res[i] in symbol.sym_name.keys())

### BUG? Unittest flags expected exception as Error!
###        
##    def test_warning_on_banned_statement(self):
##        d = config._get_forbidden_symbols()
##        self.failUnlessRaises(UserWarning,
##            config._check_ast([d[0],[d[1]]], d))

    def test_parseconf(self):
        pass

    def test_check_ast(self):
        pass

class test_config(unittest.TestCase):
    """
    Verify the functionality of the configuration parser for
    a range of different data types and statements.
    """

    # Only use setUp() and tearDown() if necessary

    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
##    def _remove_rc_files(self, root):
##        # wipe out the temp files we created for the file load 
##        # tests.
##        #
##        for root, dirs, files in os.walk(root, topdown=False):
##            for name in files:
##                os.remove(os.path.join(root, name))
##            for name in dirs:
##                os.rmdir(os.path.join(root, name))
##
##    def _create_rc_files(self):
##        # create a set of rc-files containing test data
##        # and return the path to them.
##
##        rc_data_path = [
##            os.path.join(self.tmpdir, 'rc_data_0.conf'),
##            os.path.join(self.tmpdir, 'rc_data_1.conf'),
##            os.path.join(self.tmpdir, 'rc_data_2.conf')]
##        
##        rc_data = {
##            rc_data_path[0]: defaults.get_config_file_str(alpha),
##            rc_data_path[1]: defaults.get_config_file_str(beta),
##            rc_data_path[2]: defaults.get_config_file_str(gamma)}
##
##        for path in rc_data_path:
##            try:
##                fp = open(path, 'w')
##                fp.write(rc_data[path])
##            finally:
##                fp.close()
##
##        return rc_data_path

    def test_backslash(self):
        # Backslash means line continuation:
        res = config.parse_config(test_backslash_1)
        self.failUnless(res['x'] == 2)

        res = config.parse_config(test_backslash_2)
        self.failUnless(res['x'] == 0)

    def test_integers(self):
        # hex, octal and large positive ints.
        res = config.parse_config(string.lstrip(test_integers_1))
        self.failUnless(res['a'] == 255 and res['b'] == 255
                   and res['c'] == 017777777777)

    def test_long_ints(self):
        # test that the longint formats parses.
        res = config.parse_config(test_long_ints_1)
 
    def test_string_literals(self):
        # test some string definitions.
        res = config.parse_config(test_string_literals_1)
        self.failUnless(len(res['x']) == 0 and res['x'] == res['y'])

###BUG? Single quote ' seems to translate into "!!
###       
        res = config.parse_config(test_string_literals_2)
        self.failUnless(len(res['x']) == 1
                        and res['x'] == res['y'] and ord(res['x']) == 39)

        res = config.parse_config(test_string_literals_3)
        self.failUnless(len(res['x']) == 1
                        and res['x'] == res['y'] and ord(res['x']) == 34)
        
        res = config.parse_config(test_string_literals_4)
        self.failUnless(len(res['x']) == 24 and res['x'] == res['y'])

        res = config.parse_config(test_string_literals_5)
        self.failUnless(len(res['x']) == 24 and res['x'] == res['y'])

        res = config.parse_config(test_string_literals_6)
        self.failUnless(res['x'] == res['y'])

        res = config.parse_config(test_string_literals_6
                                  + test_string_literals_7)
        self.failUnless(res['x'] == res['y'])

        res = config.parse_config(test_string_literals_6
                                  + test_string_literals_8)
        self.failUnless(res['x'] == res['y'])

        res = config.parse_config(test_string_literals_6
                                  + test_string_literals_9)
        self.failUnless(res['x'] == res['y'])
        
### BUG? Unittest flags expected exception as Error!
###        
##    def test_syntax_error(self):
##        self.failUnlessRaises(SyntaxError,
##                              config.parse_config("a + 1 = b + 2"))
##        self.failUnlessRaises(SyntaxError,
##                              config.parse_config("x + 1 = 1"))
 
    def test_if_stmt(self):
        res = config.parse_config(test_if_stmt_1)

    def test_and_or_not(self):
        res = config.parse_config(test_and_or_not_1)

    def test_comparison(self):
        res = config.parse_config(test_comparison_1)

    def test_binary_ops(self):
        res = config.parse_config(test_binary_ops_1)

    def test_shift_ops(self):
        res = config.parse_config(test_shift_ops_1)

    def test_additive_ops(self):
        res = config.parse_config(test_additive_ops_1)

    def test_multiplicative_ops(self):
        res = config.parse_config(test_multiplicative_ops_1)

    def test_unary_ops(self):
        res = config.parse_config(test_unary_ops_1)

    def test_stmt_suite(self):
        res = config.parse_config(test_stmt_suite_1)

    def test_atoms(self):
        res = config.parse_config(test_atoms_1)

 
# run tests as default.
#
if __name__ == '__main__':
    unittest.main()

# EOF.
