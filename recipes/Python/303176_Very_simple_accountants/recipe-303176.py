"""A *very* simple command-line accountant's calculator.

Uses the decimal package (introduced in Python 2.4) for calculation accuracy.
Input should be a number (decimal point is optional), an optional space, and an
operator (one of /, *, -, or +).  A blank line will output the total.
Inputting just 'q' will output the total and quit the program.

"""
import decimal
import re

parse_input = re.compile(r'(?P<num_text>\d*(\.\d*)?)\s*(?P<op>[/*\-+])')

total = decimal.Decimal('0')

total_line = lambda val: ''.join(('=' * 5, '\n', str(val)))

while True:
    tape_line = raw_input()
    if not tape_line:
        print total_line(total)
        continue
    elif tape_line is 'q':
        print total_line(total)
        break
    try:
        num_text, space, op = parse_input.match(tape_line).groups()
    except AttributeError:
        raise ValueError("invalid input")
    num = decimal.Decimal(num_text)
    if op is '/':
        total /= num
    elif op is '*':
        total *= num
    elif op is '-':
        total -= num
    elif op is '+':
        total += num
    else:
        raise ValueError("unsupported operator: %s" % op)
