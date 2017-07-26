####
# compile.py

#!/usr/bin/env python

import re
import os
import sys
import new
import imp
import time
import struct
import marshal
import compiler
from compiler.ast import Const, AssName, AssTuple

__author__ = 'Shimomura Ikkei'
__date__ = '2005-06-23'
__all__ = ['ConstantCompiler']


# Check the string is valid constant name,
isConstName = re.compile('^[A-Z][A-Z_]+$').match

def ispyfile(filename):
    "ispyfile(filename) ... The file is python source file."
    assert isinstance(filename, str) and filename
    return filename.endswith('.py') and os.path.isfile(filename)

def change_extension(name, ext='.pyc'):
    "change_extension(name, ext) ... Rename exstension."

    assert isinstance(name, str) and name
    assert isinstance(ext, str) and ext
    assert ext.startswith('.'), 'File extension must starts with dot.'

    return os.path.splitext(name)[0] + ext


class ConstantVisitor:
    def __init__(self, constants):
        self.constants = constants

    def __registerConstant(self, node, assign, const):
        assert isinstance(assign, AssName)
        if isConstName(assign.name):
            if self.constants.has_key(assign.name):
                print "Warning: %s at line %d: '%s' is already defined." % \
                  (node.filename, node.lineno, assign.name)
            else:
                if isinstance(const, Const):
                    self.constants[assign.name] = const.value
                else:
                    self.constants[assign.name] = None # dummy data

    def visitAssign(self, node):
        nodes = node.getChildren()

        if isinstance(nodes[0], AssName):
            name, const = nodes
            self.__registerConstant(node, name, const)

        elif isinstance(nodes[0], AssTuple):
            names, consts = nodes
            names = names.getChildren()
            consts = consts.getChildren()
            assert len(names) == len(consts)
            for name, const in zip(names, consts):
                self.__registerConstant(node, name, const)

    def visitName(self, node):
        assert isinstance(node, compiler.ast.Name)
        if isConstName(node.name) and self.constants.has_key(node.name):
            value = self.constants.get(node.name)
            # If the value can be constant(int, long, float, str, ...)
            if [True for type in (int, long, float, str) if isinstance(value, type)]:
                node.__class__ = Const
                node.value = value
                del node.name


class ConstantCompiler:

    def __init__(self, filename=None):
        self.constants = {}
        if os.path.isfile(filename) and filename.endswith('.py'):
            self.__load_constants(filename)

    def __load_constants(self, filename):
        assert isinstance(filename, str) and filename.endswith('.py')
        assert os.path.isfile(filename) and os.access(filename, os.R_OK)

        try:
            fh, filename, opts = imp.find_module(os.path.splitext(filename)[0])
            mod = imp.load_module("", fh, filename, opts)
            for k,v in ((x,getattr(mod,x)) for x in dir(mod) if isConstName(x)):
                self.constants[k] = v
        except ImportError:
            print "Failed to import module '%s'" % filename

    def __walk_ast(self, ast):
        compiler.walk(ast, ConstantVisitor(self.constants))

    def compile(self, filename):
        assert isinstance(filename, str) and filename
        assert os.path.isfile(filename) and filename.endswith('.py')

        # Parse python source -> AST(Abstract Syntax Tree)
        src = open(filename, 'r')
        ast = compiler.parse(src.read())
        src.close()

        # Syntax Macro (Expand constant values before compile)
        compiler.misc.set_filename(filename, ast)
        compiler.syntax.check(ast)
        self.__walk_ast(ast)

        # Compile AST -> code object.
        code = compiler.pycodegen.ModuleCodeGenerator(ast).getCode()

        return CodeWrapper(filename, code)


class CodeWrapper:
    """An utility class to save code object as .pyc file."""

    def __init__(self, src_filename, code):
        "CodeWrapper(code) This class only wrap an object for method chain."

        assert isinstance(src_filename, str) and src_filename
        assert os.path.isfile(src_filename) and src_filename.endswith('.py')
        assert isinstance(code, new.code)

        self.src_filename = src_filename
        self.__code = code

    def getCode(self):
        "getCode() ... Returns code object."
        assert isinstance(self.__code, new.code)
        return self.__code

    def __timestamp(self, pyc_filename):
        "__get_timestamp(pyc_filename) Gets timestamp stored in .pyc file."

        assert isinstance(pyc_filename, str) and pyc_filename
        assert pyc_filename.endswith('.pyc')
        assert os.path.isfile(pyc_filename)
        assert os.access(pyc_filename, os.R_OK)

        try:
            pyc = open(pyc_filename, 'rb')
            # The first 4 bytes is a magic number.for pyc file.
            # this checks the python's version.
            if pyc.read(4) == imp.get_magic():
                # The next 4 bytes is the timestamp stored as long,
                # we need this value.
                return struct.unpack("<l", pyc.read(4))[0]
            else:
                # Not .pyc file or wrong version of python.
                # It should be always updated.
                return -1
        finally:
            pyc.close()

    def __modified(self, src, pyc):
        "__modified(src_filename, pyc_filename) Returns True if src updated."

        assert isinstance(src, str) and src and src.endswith('.py')
        assert isinstance(pyc, str) and pyc and pyc.endswith('.pyc')
        assert os.path.isfile(src)

        # If not exists .pyc file then always True.
        if not os.path.isfile(pyc):
            return True

        # Is source's modified time newer than .pyc's timestamp ?
        return os.stat(src)[9] > self.__timestamp(pyc)

    def save_as(self, pyc_filename):
        "save_as(pyc_filename) ... Save current code object to .pyc file."

        assert isinstance(self.__code, new.code)
        assert isinstance(pyc_filename, str) and pyc_filename
        assert pyc_filename.endswith('.pyc')

        # Skip if the file was already updated.
        if self.__modified(self.src_filename, pyc_filename):

            # Output dump the code object to .pyc file.
            pyc = open(pyc_filename, 'wb')
            pyc.write(imp.get_magic())
            pyc.write(struct.pack('<l', time.time()))
            marshal.dump(self.__code, pyc)
            pyc.close()

        assert os.path.isfile(pyc_filename)
        assert os.path.getsize(pyc_filename) > 0


def main(const_file, *argv):
    pyc = ConstantCompiler(const_file)

    for filename in filter(os.path.exists, argv):
        pyc.compile(filename).save_as(change_extension(filename, ext='.pyc'))

if __name__ == '__main__':
    main(*sys.argv[1:])


####
# define_constants.py

import math
PI = math.atan(1) * 4.0

DEBUG = 1

####
# test_constants.py

print PI

def foo(num):
  if DEBUG:
    print "debug foo(%d)" num
  print num

for i in range(20): foo(i)
####
# how to run
# python compile.py define_constants.py test_constants.py
