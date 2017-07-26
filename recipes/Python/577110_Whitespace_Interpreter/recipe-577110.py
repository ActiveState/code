#! /usr/bin/env python
"""Interpreter.py

Runs programs in "Programs" and creates *.WSO files when needed.
Can be executed directly by double-click or on the command line.
If run on command line, add "ASM" flag to dump program assembly."""

################################################################################

__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__date__ = '14 March 2010'
__version__ = '$Revision: 4 $'

################################################################################

def test_file(path):
    disassemble(parse(trinary(load(path))), True)

################################################################################

load = lambda ws: ''.join(c for r in open(ws) for c in r if c in ' \t\n')

trinary = lambda ws: tuple(' \t\n'.index(c) for c in ws)

################################################################################

def enum(names):
    names = names.replace(',', ' ').split()
    space = dict((reversed(pair) for pair in enumerate(names)), __slots__=())
    return type('enum', (object,), space)()

INS = enum('''\
PUSH, COPY, SWAP, AWAY, \
ADD, SUB, MUL, DIV, MOD, \
SET, GET, \
PART, CALL, GOTO, ZERO, LESS, BACK, EXIT, \
OCHR, OINT, ICHR, IINT''')

################################################################################

def parse(code):
    ins = iter(code).__next__
    program = []
    while True:
        try:
            imp = ins()
        except StopIteration:
            return tuple(program)
        if imp == 0:
            # [Space]
            parse_stack(ins, program)
        elif imp == 1:
            # [Tab]
            imp = ins()
            if imp == 0:
                # [Tab][Space]
                parse_math(ins, program)
            elif imp == 1:
                # [Tab][Tab]
                parse_heap(ins, program)
            else:
                # [Tab][Line]
                parse_io(ins, program)
        else:
            # [Line]
            parse_flow(ins, program)
                    
def parse_number(ins):
    sign = ins()
    if sign == 2:
        raise StopIteration()
    buffer = ''
    code = ins()
    if code == 2:
        raise StopIteration()
    while code != 2:
        buffer += str(code)
        code = ins()
    if sign == 1:
        return int(buffer, 2) * -1
    return int(buffer, 2)

################################################################################

def parse_stack(ins, program):
    code = ins()
    if code == 0:
        # [Space]
        number = parse_number(ins)
        program.append((INS.PUSH, number))
    elif code == 1:
        # [Tab]
        code = ins()
        number = parse_number(ins)
        if code == 0:
            # [Tab][Space]
            program.append((INS.COPY, number))
        elif code == 1:
            # [Tab][Tab]
            raise StopIteration()
        else:
            # [Tab][Line]
            program.append((INS.AWAY, number))
    else:
        # [Line]
        code = ins()
        if code == 0:
            # [Line][Space]
            program.append(INS.COPY)
        elif code == 1:
            # [Line][Tab]
            program.append(INS.SWAP)
        else:
            # [Line][Line]
            program.append(INS.AWAY)

def parse_math(ins, program):
    code = ins()
    if code == 0:
        # [Space]
        code = ins()
        if code == 0:
            # [Space][Space]
            program.append(INS.ADD)
        elif code == 1:
            # [Space][Tab]
            program.append(INS.SUB)
        else:
            # [Space][Line]
            program.append(INS.MUL)
    elif code == 1:
        # [Tab]
        code = ins()
        if code == 0:
            # [Tab][Space]
            program.append(INS.DIV)
        elif code == 1:
            # [Tab][Tab]
            program.append(INS.MOD)
        else:
            # [Tab][Line]
            raise StopIteration()
    else:
        # [Line]
        raise StopIteration()

def parse_heap(ins, program):
    code = ins()
    if code == 0:
        # [Space]
        program.append(INS.SET)
    elif code == 1:
        # [Tab]
        program.append(INS.GET)
    else:
        # [Line]
        raise StopIteration()

def parse_io(ins, program):
    code = ins()
    if code == 0:
        # [Space]
        code = ins()
        if code == 0:
            # [Space][Space]
            program.append(INS.OCHR)
        elif code == 1:
            # [Space][Tab]
            program.append(INS.OINT)
        else:
            # [Space][Line]
            raise StopIteration()
    elif code == 1:
        # [Tab]
        code = ins()
        if code == 0:
            # [Tab][Space]
            program.append(INS.ICHR)
        elif code == 1:
            # [Tab][Tab]
            program.append(INS.IINT)
        else:
            # [Tab][Line]
            raise StopIteration()
    else:
        # [Line]
        raise StopIteration()

def parse_flow(ins, program):
    code = ins()
    if code == 0:
        # [Space]
        code = ins()
        label = parse_number(ins)
        if code == 0:
            # [Space][Space]
            program.append((INS.PART, label))
        elif code == 1:
            # [Space][Tab]
            program.append((INS.CALL, label))
        else:
            # [Space][Line]
            program.append((INS.GOTO, label))
    elif code == 1:
        # [Tab]
        code = ins()
        if code == 0:
            # [Tab][Space]
            label = parse_number(ins)
            program.append((INS.ZERO, label))
        elif code == 1:
            # [Tab][Tab]
            label = parse_number(ins)
            program.append((INS.LESS, label))
        else:
            # [Tab][Line]
            program.append(INS.BACK)
    else:
        # [Line]
        code = ins()
        if code == 2:
            # [Line][Line]
            program.append(INS.EXIT)
        else:
            # [Line][Space] or [Line][Tab]
            raise StopIteration()

################################################################################

MNEMONIC = '\
push copy swap away add sub mul div mod set get part \
call goto zero less back exit ochr oint ichr iint'.split()

HAS_ARG = [getattr(INS, name) for name in
           'PUSH COPY AWAY PART CALL GOTO ZERO LESS'.split()]

HAS_LABEL = [getattr(INS, name) for name in
             'PART CALL GOTO ZERO LESS'.split()]

def disassemble(program, names=False):
    if names:
        names = create_names(program)
    for ins in program:
        if isinstance(ins, tuple):
            ins, arg = ins
            assert ins in HAS_ARG
            has_arg = True
        else:
            assert INS.PUSH <= ins <= INS.IINT
            has_arg = False
        if ins == INS.PART:
            if names:
                print(MNEMONIC[ins], '"' + names[arg] + '"')
            else:
                print(MNEMONIC[ins], arg)
        elif has_arg and ins in HAS_ARG:
            if ins in HAS_LABEL and names:
                assert arg in names
                print('     ' + MNEMONIC[ins], '"' + names[arg] + '"')
            else:
                print('     ' + MNEMONIC[ins], arg)
        else:
            print('     ' + MNEMONIC[ins])

################################################################################

def create_names(program):
    names = {}
    number = 1
    for ins in program:
        if isinstance(ins, tuple) and ins[0] == INS.PART:
            label = ins[1]
            assert label not in names
            names[label] = number_to_name(number)
            number += 1
    return names

def number_to_name(number):
    name = ''
    for offset in reversed(list(partition_number(number, 27))):
        if offset:
            name += chr(ord('A') + offset - 1)
        else:
            name += '_'
    return name

def partition_number(number, base):
    div, mod = divmod(number, base)
    yield mod
    while div:
        div, mod = divmod(div, base)
        yield mod

################################################################################

CODE = ('   \t\n',
        ' \n ',
        ' \t  \t\n',
        ' \n\t',
        ' \n\n',
        ' \t\n \t\n',
        '\t   ',
        '\t  \t',
        '\t  \n',
        '\t \t ',
        '\t \t\t',
        '\t\t ',
        '\t\t\t',
        '\n   \t\n',
        '\n \t \t\n',
        '\n \n \t\n',
        '\n\t  \t\n',
        '\n\t\t \t\n',
        '\n\t\n',
        '\n\n\n',
        '\t\n  ',
        '\t\n \t',
        '\t\n\t ',
        '\t\n\t\t')

EXAMPLE = ''.join(CODE)

################################################################################

NOTES = '''\
STACK
=====
  push number
  copy
  copy number
  swap
  away
  away number

MATH
====
  add
  sub
  mul
  div
  mod

HEAP
====
  set
  get

FLOW
====
  part label
  call label
  goto label
  zero label
  less label
  back
  exit

I/O
===
  ochr
  oint
  ichr
  iint'''

################################################################################
################################################################################

class Stack:

    def __init__(self):
        self.__data = []

    # Stack Operators

    def push(self, number):
        self.__data.append(number)

    def copy(self, number=None):
        if number is None:
            self.__data.append(self.__data[-1])
        else:
            size = len(self.__data)
            index = size - number - 1
            assert 0 <= index < size
            self.__data.append(self.__data[index])

    def swap(self):
        self.__data[-2], self.__data[-1] = self.__data[-1], self.__data[-2]

    def away(self, number=None):
        if number is None:
            self.__data.pop()
        else:
            size = len(self.__data)
            index = size - number - 1
            assert 0 <= index < size
            del self.__data[index:-1]

    # Math Operators

    def add(self):
        suffix = self.__data.pop()
        prefix = self.__data.pop()
        self.__data.append(prefix + suffix)

    def sub(self):
        suffix = self.__data.pop()
        prefix = self.__data.pop()
        self.__data.append(prefix - suffix)
    
    def mul(self):
        suffix = self.__data.pop()
        prefix = self.__data.pop()
        self.__data.append(prefix * suffix)

    def div(self):
        suffix = self.__data.pop()
        prefix = self.__data.pop()
        self.__data.append(prefix // suffix)

    def mod(self):
        suffix = self.__data.pop()
        prefix = self.__data.pop()
        self.__data.append(prefix % suffix)

    # Program Operator

    def pop(self):
        return self.__data.pop()

################################################################################

class Heap:

    def __init__(self):
        self.__data = {}

    def set_(self, addr, item):
        if item:
            self.__data[addr] = item
        elif addr in self.__data:
            del self.__data[addr]

    def get_(self, addr):
        return self.__data.get(addr, 0)

################################################################################

import os
import zlib
import msvcrt
import pickle
import string

class CleanExit(Exception): pass

NOP = lambda arg: None

DEBUG_WHITESPACE = False

################################################################################

class Program:

    # Version System
    _MAGIC_ = 'WS'
    VERSION = 0, 2, 9, 0

    # Argument Tables
    NO_ARGS = INS.COPY, INS.SWAP, INS.AWAY, INS.ADD, \
              INS.SUB, INS.MUL, INS.DIV, INS.MOD, \
              INS.SET, INS.GET, INS.BACK, INS.EXIT, \
              INS.OCHR, INS.OINT, INS.ICHR, INS.IINT
    HAS_ARG = INS.PUSH, INS.COPY, INS.AWAY, INS.PART, \
              INS.CALL, INS.GOTO, INS.ZERO, INS.LESS

    def __init__(self, code):
        self.__data = code
        self.__validate()
        self.__build_jump()
        self.__check_jump()
        self.__setup_exec()

    def __setup_exec(self):
        self.__iptr = 0
        self.__stck = stack = Stack()
        self.__heap = Heap()
        self.__cast = []
        self.__meth = (stack.push, stack.copy, stack.swap, stack.away,
                       stack.add, stack.sub, stack.mul, stack.div, stack.mod,
                       self.__set, self.__get,
                       NOP, self.__call, self.__goto, self.__zero,
                            self.__less, self.__back, self.__exit,
                       self.__ochr, self.__oint, self.__ichr, self.__iint)

    def step(self):
        ins = self.__data[self.__iptr]
        self.__iptr += 1
        if isinstance(ins, tuple):
            self.__meth[ins[0]](ins[1])
        else:
            self.__meth[ins]()

    def run(self):
        while True:
            ins = self.__data[self.__iptr]
            self.__iptr += 1
            if isinstance(ins, tuple):
                self.__meth[ins[0]](ins[1])
            else:
                self.__meth[ins]()

    def __oint(self):
        for digit in str(self.__stck.pop()):
            msvcrt.putwch(digit)

    def __ichr(self):
        addr = self.__stck.pop()
        # Input Routine
        while msvcrt.kbhit():
            msvcrt.getwch()
        while True:
            char = msvcrt.getwch()
            if char in '\x00\xE0':
                msvcrt.getwch()
            elif char in string.printable:
                char = char.replace('\r', '\n')
                msvcrt.putwch(char)
                break
        item = ord(char)
        # Storing Number
        self.__heap.set_(addr, item)

    def __iint(self):
        addr = self.__stck.pop()
        # Input Routine
        while msvcrt.kbhit():
            msvcrt.getwch()
        buff = ''
        char = msvcrt.getwch()
        while char != '\r' or not buff or len(buff) == 1 and buff in '+-':
            if char in '\x00\xE0':
                msvcrt.getwch()
            elif char in '+-' and not buff:
                msvcrt.putwch(char)
                buff += char
            elif '0' <= char <= '9':
                msvcrt.putwch(char)
                buff += char
            elif char == '\b':
                if buff:
                    buff = buff[:-1]
                    msvcrt.putwch(char)
                    msvcrt.putwch(' ')
                    msvcrt.putwch(char)
            char = msvcrt.getwch()
        msvcrt.putwch(char)
        msvcrt.putwch('\n')
        item = int(buff)
        # Storing Number
        self.__heap.set_(addr, item)

    def __goto(self, label):
        self.__iptr = self.__jump[label]

    def __zero(self, label):
        if self.__stck.pop() == 0:
            self.__iptr = self.__jump[label]

    def __less(self, label):
        if self.__stck.pop() < 0:
            self.__iptr = self.__jump[label]

    def __exit(self):
        self.__setup_exec()
        raise CleanExit()

    def __set(self):
        item = self.__stck.pop()
        addr = self.__stck.pop()
        self.__heap.set_(addr, item)

    def __get(self):
        addr = self.__stck.pop()
        item = self.__heap.get_(addr)
        self.__stck.push(item)

    def __validate(self):
        assert isinstance(self.__data, tuple)
        for code in self.__data:
            if isinstance(code, int):
                assert code in self.NO_ARGS
            elif isinstance(code, tuple):
                code, arg = code
                assert code in self.HAS_ARG
                assert isinstance(arg, int)
            else:
                raise TypeError()

    def __build_jump(self):
        self.__jump = {}
        for pointer, ins in enumerate(self.__data):
            if isinstance(ins, tuple):
                ins, arg = ins
                if ins == INS.PART:
                    assert arg not in self.__jump
                    addr = pointer + 1
                    assert addr != len(self.__data)
                    self.__jump[arg] = addr

    def __check_jump(self):
        for ins in self.__data:
            if isinstance(ins, tuple):
                ins, arg = ins
                if ins in (INS.CALL, INS.GOTO, INS.ZERO, INS.LESS):
                    assert arg in self.__jump

    @classmethod
    def load(cls, path):
        # Loads programs and handles optimized files.
        ws = path + '.ws'
        cp = path + '.wso'
        compiled = False
        if os.path.isfile(cp):
            compiled = True
            if os.path.isfile(ws):
                if os.path.getmtime(ws) > os.path.getmtime(cp):
                    compiled = False
        final = cls._final()
        cls._check(final)
        if compiled:
            try:
                with open(cp, 'rb') as file:
                    code = file.read(len(final))
                    cls._check(code)
                    data = file.read()
                return cls(pickle.loads(zlib.decompress(data)))
            except:
                pass
        data = load(ws)
        code = trinary(data)
        program = parse(code)
        serialized = pickle.dumps(program, pickle.HIGHEST_PROTOCOL)
        optimized = zlib.compress(serialized, 9)
        with open(cp, 'wb') as file:
            file.write(final + optimized)
        return cls(program)

    @classmethod
    def _final(cls):
        # Builds a unique identifier for this verion.
        return b'\0' + cls._MAGIC_.encode() + bytes(cls.VERSION) + b'\0'

    @classmethod
    def _check(cls, code):
        # Check version code, including _final() code.
        if len(code) != 8:
            raise ValueError('Code is not of right length!')
        if code[0] != 0 or code[7] != 0:
            raise ValueError('Code markers are not present!')
        if len(cls._MAGIC_) != 2 or code[1:3] != cls._MAGIC_.encode():
            raise ValueError('Magic value is not correct!')
        if len(cls.VERSION) != 4 or code[3:7] != bytes(cls.VERSION):
            raise ValueError('Version numbers are not equal!')

    def assembly(self, names=False):
        disassemble(self.__data, names)

    if DEBUG_WHITESPACE:

        def __ochr(self):
            for c in repr(chr(self.__stck.pop())):
                msvcrt.putwch(c)

        def __call(self, label):
            self.__cast.append(self.__iptr)
            self.__iptr = self.__jump[label]
            print('\nCALL\n', self.__stck._Stack__data)

        def __back(self):
            self.__iptr = self.__cast.pop()
            print('\nBACK\n', self.__stck._Stack__data)

    else:

        def __ochr(self):
            msvcrt.putwch(chr(self.__stck.pop()))

        def __call(self, label):
            self.__cast.append(self.__iptr)
            self.__iptr = self.__jump[label]

        def __back(self):
            self.__iptr = self.__cast.pop()

################################################################################
################################################################################

import sys
import time
import traceback

################################################################################

def main():
    path, command_line, error = get_program()
    try:
        assert not error
        program = Program.load(path)
    except:
        error = show_error('The program could not be loaded.')
    else:
        try:
            if len(sys.argv) > 2 and sys.argv[2].upper() == 'ASM':
                program.assembly(True)
            else:
                program.run()
        except CleanExit:
            pass
        except:
            error = show_error('A runtime error has been raised.')
    handle_close(error, command_line)

def get_program():
    if len(sys.argv) > 1:
        command_line = True
        name = sys.argv[1]
    else:
        command_line = False
        try:
            name = input('Program Name: ')
        except:
            return None, False, True
    sys.stdout.write('\n')
    return os.path.join('Programs', name), command_line, False

def show_error(message):
    sys.stdout.write('\nERROR: ' + message + '\n\n')
    traceback.print_exc()
    return True

def handle_close(error, command_line):
    if error:
        usage = 'Usage: {} {}'.format(os.path.basename(sys.argv[0]),
                                      '<program> [ASM]')
        sys.stdout.write('\n{}\n{}\n'.format('-' * len(usage), usage))
    if not command_line:
        time.sleep(10)

################################################################################

if __name__ == '__main__':
    main()
