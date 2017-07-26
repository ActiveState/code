"""Doctests for templates with bracketed placeholders

>>> s = 'People of [planet], take us to your leader.'
>>> d = dict(planet='Earth')
>>> print convert_template(s) % d
People of Earth, take us to your leader.

>>> s = 'People of <planet>, take us to your leader.'
>>> print convert_template(s, '<', '>') % d
People of Earth, take us to your leader.

"""

import re

def convert_template(template, opener='[', closer=']'):
    opener = re.escape(opener)
    closer = re.escape(closer)
    pattern = re.compile(opener + '([_A-Za-z][_A-Za-z0-9]*)' + closer)
    return re.sub(pattern, r'%(\1)s', template.replace('%','%%'))


if __name__ == '__main__':
    import doctest
    print 'Doctest results: ', doctest.testmod()
