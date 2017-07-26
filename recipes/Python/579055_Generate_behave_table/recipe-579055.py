import string

def as_behave_table(data):
    """ nosetests --with-doctest --with-coverage report_table.py

    >>> from report_table import as_behave_table
    >>> data = [('what', 'how', 'who'),
    ...         ('lorem', 'that is a long value', 3.1415),
    ...         ('ipsum', 89798, 0.2)]

    >>> print as_behave_table(data)
    | what  | how                  | who    |
    | lorem | that is a long value | 3.1415 |
    | ipsum |                89798 |    0.2 |

    """
    table = []
    # max size of each column
    sizes = map(max, zip(*[[len(str(elt)) for elt in member]
                           for member in data]))
    num_elts = len(sizes)

    start_of_line = '| '
    vertical_separator = ' | '
    end_of_line = ' |'
    meta_template = vertical_separator.join(['{{{{{0}:{{{0}}}}}}}'.format(i)
                                             for i in range(num_elts)])
    template = '{0}{1}{2}'.format(start_of_line,
                                  meta_template.format(*sizes),
                                  end_of_line)

    for d in data:
        table.append(template.format(*d))
    return '\n'.join(table)
