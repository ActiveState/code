#! /usr/bin/env python
"""Assembler.py

Compiles a program from "Assembly" folder into "Program" folder.
Can be executed directly by double-click or on the command line.
Give name of *.WSA file without extension (example: stack_calc)."""

################################################################################

__author__ = 'Stephen "Zero" Chappell <Noctis.Skytower@gmail.com>'
__date__ = '14 March 2010'
__version__ = '$Revision: 3 $'

################################################################################

import string
from Interpreter import INS, MNEMONIC

################################################################################

def parse(code):
    program = []
    process_virtual(program, code)
    process_control(program)
    return tuple(program)

def process_virtual(program, code):
    for line, text in enumerate(code.split('\n')):
        if not text or text[0] == '#':
            continue
        if text.startswith('part '):
            parse_part(program, line, text[5:])
        elif text.startswith('     '):
            parse_code(program, line, text[5:])
        else:
            syntax_error(line)

def syntax_error(line):
    raise SyntaxError('Line ' + str(line + 1))

################################################################################

def process_control(program):
    parts = get_parts(program)
    names = dict(pair for pair in zip(parts, generate_index()))
    correct_control(program, names)

def get_parts(program):
    parts = []
    for ins in program:
        if isinstance(ins, tuple):
            ins, arg = ins
            if ins == INS.PART:
                if arg in parts:
                    raise NameError('Part definition was found twice: ' + arg)
                parts.append(arg)
    return parts

def generate_index():
    index = 1
    while True:
        yield index
        index *= -1
        if index > 0:
            index += 1

def correct_control(program, names):
    for index, ins in enumerate(program):
        if isinstance(ins, tuple):
            ins, arg = ins
            if ins in HAS_LABEL:
                if arg not in names:
                    raise NameError('Part definition was never found: ' + arg)
                program[index] = (ins, names[arg])

################################################################################

def parse_part(program, line, text):
    if not valid_label(text):
        syntax_error(line)
    program.append((INS.PART, text))

def valid_label(text):
    if not between_quotes(text):
        return False
    label = text[1:-1]
    if not valid_name(label):
        return False
    return True

def between_quotes(text):
    if len(text) < 3:
        return False
    if text.count('"') != 2:
        return False
    if text[0] != '"' or text[-1] != '"':
        return False
    return True

def valid_name(label):
    valid_characters = string.ascii_letters + string.digits + '_'
    valid_set = frozenset(valid_characters)
    label_set = frozenset(label)
    if len(label_set - valid_set) != 0:
        return False
    return True

################################################################################

from Interpreter import HAS_LABEL, Program

NO_ARGS = Program.NO_ARGS
HAS_ARG = Program.HAS_ARG
TWO_WAY = tuple(set(NO_ARGS) & set(HAS_ARG))

################################################################################

def parse_code(program, line, text):
    for ins, word in enumerate(MNEMONIC):
        if text.startswith(word):
            check_code(program, line, text[len(word):], ins)
            break
    else:
        syntax_error(line)

def check_code(program, line, text, ins):
    if ins in TWO_WAY:
        if text:
            number = parse_number(line, text)
            program.append((ins, number))
        else:
            program.append(ins)
    elif ins in HAS_LABEL:
        text = parse_label(line, text)
        program.append((ins, text))
    elif ins in HAS_ARG:
        number = parse_number(line, text)
        program.append((ins, number))
    elif ins in NO_ARGS:
        if text:
            syntax_error(line)
        program.append(ins)
    else:
        syntax_error(line)

def parse_label(line, text):
    if not text or text[0] != ' ':
        syntax_error(line)
    text = text[1:]
    if not valid_label(text):
        syntax_error(line)
    return text

################################################################################

def parse_number(line, text):
    if not valid_number(text):
        syntax_error(line)
    return int(text)

def valid_number(text):
    if len(text) < 2:
        return False
    if text[0] != ' ':
        return False
    text = text[1:]
    if '+' in text and '-' in text:
        return False
    if '+' in text:
        if text.count('+') != 1:
            return False
        if text[0] != '+':
            return False
        text = text[1:]
        if not text:
            return False
    if '-' in text:
        if text.count('-') != 1:
            return False
        if text[0] != '-':
            return False
        text = text[1:]
        if not text:
            return False
    valid_set = frozenset(string.digits)
    value_set = frozenset(text)
    if len(value_set - valid_set) != 0:
        return False
    return True

################################################################################
################################################################################

from Interpreter import partition_number

VMC_2_TRI = {
    (INS.PUSH, True):  (0, 0),
    (INS.COPY, False): (0, 2, 0),
    (INS.COPY, True):  (0, 1, 0),
    (INS.SWAP, False): (0, 2, 1),
    (INS.AWAY, False): (0, 2, 2),
    (INS.AWAY, True):  (0, 1, 2),
    (INS.ADD, False):  (1, 0, 0, 0),
    (INS.SUB, False):  (1, 0, 0, 1),
    (INS.MUL, False):  (1, 0, 0, 2),
    (INS.DIV, False):  (1, 0, 1, 0),
    (INS.MOD, False):  (1, 0, 1, 1),
    (INS.SET, False):  (1, 1, 0),
    (INS.GET, False):  (1, 1, 1),
    (INS.PART, True):  (2, 0, 0),
    (INS.CALL, True):  (2, 0, 1),
    (INS.GOTO, True):  (2, 0, 2),
    (INS.ZERO, True):  (2, 1, 0),
    (INS.LESS, True):  (2, 1, 1),
    (INS.BACK, False): (2, 1, 2),
    (INS.EXIT, False): (2, 2, 2),
    (INS.OCHR, False): (1, 2, 0, 0),
    (INS.OINT, False): (1, 2, 0, 1),
    (INS.ICHR, False): (1, 2, 1, 0),
    (INS.IINT, False): (1, 2, 1, 1)
    }

################################################################################

def to_trinary(program):
    trinary_code = []
    for ins in program:
        if isinstance(ins, tuple):
            ins, arg = ins
            trinary_code.extend(VMC_2_TRI[(ins, True)])
            trinary_code.extend(from_number(arg))
        else:
            trinary_code.extend(VMC_2_TRI[(ins, False)])
    return tuple(trinary_code)

def from_number(arg):
    code = [int(arg < 0)]
    if arg:
        for bit in reversed(list(partition_number(abs(arg), 2))):
            code.append(bit)
        return code + [2]
    return code + [0, 2]

to_ws = lambda trinary: ''.join(' \t\n'[index] for index in trinary)

def compile_wsa(source):
    program = parse(source)
    trinary = to_trinary(program)
    ws_code = to_ws(trinary)
    return ws_code

################################################################################
################################################################################

import os
import sys
import time
import traceback

def main():
    name, source, command_line, error = get_source()
    if not error:
        start = time.clock()
        try:
            ws_code = compile_wsa(source)
        except:
            print('ERROR: File could not be compiled.\n')
            traceback.print_exc()
            error = True
        else:
            path = os.path.join('Programs', name + '.ws')
            try:
                open(path, 'w').write(ws_code)
            except IOError as err:
                print(err)
                error = True
            else:
                div, mod = divmod((time.clock() - start) * 1000, 1)
                args = int(div), '{:.3}'.format(mod)[1:]
                print('DONE: Compiled in {}{} ms'.format(*args))
    handle_close(error, command_line)

def get_source():
    if len(sys.argv) > 1:
        command_line = True
        name = sys.argv[1]
    else:
        command_line = False
        try:
            name = input('Source File: ')
        except:
            return None, None, False, True
    print()
    path = os.path.join('Assembly', name + '.wsa')
    try:
        return name, open(path).read(), command_line, False
    except IOError as err:
        print(err)
        return None, None, command_line, True

def handle_close(error, command_line):
    if error:
        usage = 'Usage: {} <assembly>'.format(os.path.basename(sys.argv[0]))
        print('\n{}\n{}'.format('-' * len(usage), usage))
    if not command_line:
        time.sleep(10)

################################################################################

if __name__ == '__main__':
    main()
