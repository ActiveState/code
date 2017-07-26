# clipbrd.py

"""
# Examples:

>>> import clipbrd as cb
>>> D = [range(5) for i in range(3)]
>>> D
[[0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4]]
>>> print cb._buildstr(D)
0	1	2	3	4
0	1	2	3	4
0	1	2	3	4
>>> print cb._buildstr(D, transpose=True)
0	0	0
1	1	1
2	2	2
3	3	3
4	4	4
>>> cb.clipboard_put(D, transpose=True)
# Now paste into your favourite spread sheet, probably by ctrl-v.

>>> print cb._buildstr(458.78, replace=('.', ','))
458,78
>>> print cb._buildstr(range(5))
0	1	2	3	4
>>> print cb._buildstr(range(5), transpose=True)
0
1
2
3
4
>>> print cb._buildstr([('1A', '1B'), ('2A', '2B')])
1A	1B
2A	2B
>>> print cb._buildstr([('1A', '1B'), ('2A', '2B')], transpose=True)
1A	2A
1B	2B

"""

import Tkinter as tk

def _buildstr(D, transpose=False, replace=None):
    """Construct a string suitable for a spreadsheet.

    D: scalar, 1d or 2d sequence
        For example a list or a list of lists.

    transpose: Bool
        Transpose the data if True.

    replace: tuple or None
        If tuple, it is two strings to pass to the replace
        method. ('toreplace', 'replaceby')

    """

    try:
        D[0]
    except (TypeError, IndexError):
        D = [D]
    try:
        D[0][0]
    except (TypeError, IndexError):
        D = [D]

    if transpose:
        D = zip(*D)
        
    if not replace:
        rows = ['\t'.join([str(v) for v in row]) for row in D]
    else:
        rows = ['\t'.join([str(v).replace(*replace)
                           for v in row]) for row in D]
    S = '\n'.join(rows)
    return S

def clipboard_put(D, transpose=False, replace=None):
    """Construct a string suitable for a spreadsheet and put it into the
    clipboard.

    D: scalar, 1d or 2d sequence
        For example a list or a list of lists.

    transpose: Bool
        Transpose the data if True.

    replace: tuple or None
        If tuple, it is two strings to pass to the replace
        method. ('toreplace', 'replaceby')

    """
    s = _buildstr(D, transpose, replace)
    r = tk.Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(s)
    r.destroy()
