import string
from textwrap import wrap

MIN = 1
UNBIASED = 2

def display_table(rows,             # List of tuples of data
                  headings=[],      # Optional headings for columns
                  col_widths=[],    # Column widths 
                  col_justs=[],     # Column justifications (str.ljust, etc)
                  screen_width=80,  # Width of terminal
                  col_spacer=2,     # Space between columns
                  fill_char=' ',    # Fill character
                  col_sep='=',      # Separator char
                  row_term='\n',    # row terminator (could be <br />)
                  norm_meth=MIN,    # Screen width normailization method
                  ):
 
    _col_justs = list(col_justs)
    _col_widths = list(col_widths)

    # String-ify everything
    rows = [tuple((str(col) for col in row)) for row in rows]
    
    # Compute appropriate col_widths if not given
    if not col_widths:
        if headings:
            _col_widths = [max(row) for row in (map(len, col) 
                           for col in zip(headings, *rows))]
        else:
            _col_widths = [max(row) for row in (map(len, col) 
                           for col in zip(*rows))]

    num_cols = len(_col_widths)
    col_spaces = col_spacer * (num_cols - 1)

    # Compute the size a row in our table would be in chars
    def _get_row_size(cw):
        return sum(cw) + col_spaces
    
    row_size = _get_row_size(_col_widths)
    
    def _unbiased_normalization():
        """ Normalize keeping the ratio of column sizes the same """
        __col_widths = [int(col_width * 
                           (float(screen_width - col_spaces) / row_size))
                       for col_width in _col_widths]

        # Distribute epsilon underage to the the columns
        for x in xrange(screen_width - _get_row_size(__col_widths)):
            __col_widths[x % num_cols] += 1
        return __col_widths

    def _min_normalization():
        """ Bring all columns up to the minimum """
        __col_widths = _unbiased_normalization()

        # A made up heuristic -- hope it looks good
        col_min = int(0.5 * min(row_size, screen_width) / float(num_cols))
       
        # Bring all the columns up to the minimum
        norm_widths = []
        for col_width, org_width in zip(__col_widths, _col_widths):
            if col_width < col_min: 
                col_width = min(org_width, col_min)
            norm_widths.append(col_width) 

        # Distribute epsilon overage to the the columns
        count = _get_row_size(norm_widths) - screen_width
        x = 0
        while count > 0:
            if norm_widths[x % num_cols] > col_min:
                norm_widths[x % num_cols] -= 1
                count -= 1
            x += 1

        return norm_widths

    if not col_widths:
        # Normalize columns to screen size
        if row_size > screen_width:
            if norm_meth is UNBIASED:
                _col_widths = _unbiased_normalization()
            else:
                _col_widths = _min_normalization()

    row_size = _get_row_size(_col_widths)

    # If col_justs are not specified then guess the justification from
    # the appearence of the first row of data
    # Numbers and money are right justified, alpha beginning strings are left
    if not _col_justs:
        for col_datum in rows[0]:
            if isinstance(col_datum, str):
                if col_datum.startswith(tuple(string.digits + '$')):
                    _col_justs.append(str.rjust)
                else:
                    _col_justs.append(str.ljust)
            else:
                _col_justs.append(str.rjust)

    # Calculate the minimum screen width needed based on col_spacer and number
    # of columns
    min_screen_width = num_cols + col_spaces
    
    assert screen_width >= min_screen_width, "Screen Width is set too small, must be >= %d" % min_screen_width

    row_size = _get_row_size(_col_widths)

    def _display_wrapped_row(row, heading=False):
        """ Take a row, wrap it, and then display in proper tabular format
        """
        wrapped_row = [wrap(col_datum, col_width)
                        for col_datum, col_width in zip(row, _col_widths)]
        row_lines = []
        for cols in map(None, *wrapped_row):
            if heading:
                partial = (str.center((partial_col or ''), col_width, fill_char)
                        for partial_col, col_width in zip(cols, _col_widths))
            else:
                partial = (col_just((partial_col or ''), col_width, fill_char)
                        for partial_col, col_width, col_just in zip(cols, 
                                                                    _col_widths,
                                                                    _col_justs))
            row_lines.append((fill_char * col_spacer).join(partial))

        print row_term.join(row_lines)

    if headings:
        # Print out the headings
        _display_wrapped_row(headings, heading=True)

        # Print separator
        print col_sep * row_size

    # Print out the rows of data
    for row in rows:
        _display_wrapped_row(row)
