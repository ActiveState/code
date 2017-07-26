#!/usr/bin/env python

INPUT_FILE = 'input_file.txt'
OUTPUT_FILE = INPUT_FILE + '.out'

def condition():
    """Thid function provides condtion list, and values"""

    lst_condition = [('first marker line\n',
                      'first marker line\n'),
                     ('this line will be changed\n',
                      'this line is changed like this\n')]
    for testcond, value in lst_condition:
        yield testcond, value

def parse(cond):
    """parse file and return lines/values"""
    
    check = True
    testcond, value = cond.next()
    for line in file(INPUT_FILE):
        if check:
            if line == testcond:
                yield value
                try:
                    testcond, value = cond.next()
                except StopIteration:
                    check = False
            else:
                yield line
        else:
            yield line

if __name__ == '__main__':
    fd = open(OUTPUT_FILE, 'w')
    cond = condition()
    for line in parse(cond):
        fd.write(line)
        pass
    fd.close()
    pass
