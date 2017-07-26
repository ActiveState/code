#!/usr/bin/env python

"""Format Number separating groups of 3 digits

This implements a simple state machine that implements the following
regular expression (which achieve the same goal):

(\d)(?=(\d{3})+$)
"""


def get_groups(s):
    test = lambda x: len(x) == 3 and "".join(x).isdigit()
    groups = [s[i:][:3] for i in range(0, len(s), 3)]
    if all(map(test, groups)):
        return groups


def generate_format(s):
    i = 0
    N = len(s)

    while i < N:
        if s[i].isdigit():
            groups = get_groups(s[(i + 1):])
            if groups:
                yield s[i]
                for group in groups:
                    yield ","
                    yield group
                break
            else:
                yield s[i]
        i += 1


def format(x):
    s = str(x)
    if "." in s:
        i, f = s.split(".", 1)
        if i.isdigit() and f.isdigit():
            return "%s.%s" % ("".join(generate_format(i)), f)
    elif s.isdigit():
        return "".join(generate_format(s))

print(format(1))
print(format(12))
print(format(123))
print(format(1234))
print(format(12345))
print(format(123456))
print(format(12345678))
print(format(123456789))
print(format(123456789.1234))
