>>> len('a\\nb')
4
>>> len('a\\nb'.decode('string_escape'))
3
>>>

Or for unicode strings

>>> len(u'\N{euro sign}\\nB')
4
>>> len(u'\N{euro sign}\\nB'.encode('utf-8').decode('string_escape').decode('utf-8'))
3


This compares to naive approach to decode character escape by writing 
your own scanner in pure Python. For example:

def decode(s):
    output = []
    iterator = iter(s)
    for c in iterator:
      if c == '\\':
        ...enter your state machine and decode...
      else:
        output.append(c)
    return ''.join(output)

or

def decode(s):
    return s\
        .replace('\\n','\n')\
        .replace('\\t','\t')\
        ...and so on for the few escapes supported...

The navie approaches are expected to be much slower.
