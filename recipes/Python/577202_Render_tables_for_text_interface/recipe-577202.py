# -*- coding: Windows-1251 -*-
'''
texttable -- render text tables for console, log files etc
'''
__author__ = 'Denis Barmenkov <denis.barmenkov@gmail.com>'
__source__ = 'http://code.activestate.com/recipes/577202-render-tables-for-text-interface/'

import types

# Align center is not supported because of the terrible form :)
ALIGN_RIGHT   = 0x0001
ALIGN_LEFT    = 0x0002
PADDING_LEFT  = 0x0010
PADDING_RIGHT = 0x0020
PADDING_ALL   = PADDING_LEFT | PADDING_RIGHT

def _rpad_to_maxlen(slist, padchar=' '):
    maxlen = max(map(len, slist))
    res = map(lambda s: s + padchar * (maxlen - len(s)), slist)
    return res

def _lpad_to_maxlen(slist, padchar=' '):
    maxlen = max(map(len, slist))
    res = map(lambda s: padchar * (maxlen - len(s)) + s, slist)
    return res

def test_mask(mask, flag):
    '''
    tests mask for all bits of flag set
    '''
    return mask & flag == flag

def _align_para(para, mode):
    if test_mask(mode, ALIGN_RIGHT):
        para = _lpad_to_maxlen(para) # little confusing: right align == left padding
    elif test_mask(mode, ALIGN_LEFT):
        para = _rpad_to_maxlen(para)
    else:
        raise ValueError, "NO ALIGN SPECIFIED!"

    if test_mask(mode, PADDING_LEFT):
        para = map(lambda x: ' ' + x, para)
    if test_mask(mode, PADDING_RIGHT):
        para = map(lambda x: x + ' ', para)

    return para

def _glue_cols(col1, col2):
    return map(lambda x: '%s|%s' % (x[0], x[1]), zip(col1, col2))

def _has_column_headers(cols):
    fail_count = 0
    for c in cols:
        try:
            a = c[2]
        except IndexError:
            fail_count += 1
    return fail_count == 0

def _join_to_list(*arguments):
    '''
    join all parameters to one list, 
    expanding lists and tuples
    '''
    res = list()
    for arg in arguments:
        if isinstance(arg, types.ListType):
            res.extend(arg)
        elif isinstance(arg, types.TupleType):
            res.extend(list(arg))
        else:
            res.append(arg)
    return res

def format_table(cols):
    # 1. aligning data
    if len(cols) == 0:
        return list()

    header_present = _has_column_headers(cols)
    if header_present:
        # prefix all data with headers // TODO: alignment set to center 
        cols = map(lambda x: [_join_to_list(x[2], x[0]), x[1] ], cols)

    cols2 = map(lambda x: _align_para(x[0], x[1]), cols)
    if len(cols2) == 0:
        return list()

    empty_vert_border = [ '' ] * len(cols2[0])

    cols2.append(empty_vert_border)
    cols2.insert(0, empty_vert_border)

    glued_cols = reduce(_glue_cols, cols2)
    if len(glued_cols) == 0:
        return list()

    border = '=' * len(glued_cols[0])
    glued_cols.insert(0, border)
    glued_cols.append(border)
    if header_present:
        glued_cols.insert(2, border)  # insert delimiter berween header and values        

    return glued_cols

def demo():
    nums = [ '1', '2', '3', '4' ]
    speeds = [ '100', '10000', '1500', '12' ]
    desc = [ '', 'label 1', 'none', 'very long description' ]
    lines = format_table( [(nums, ALIGN_RIGHT|PADDING_ALL, 'NUM'), 
                           (speeds, ALIGN_RIGHT|PADDING_ALL, 'SPEED'), 
                           (desc, ALIGN_LEFT|PADDING_ALL, 'DESC')] )

    print '\n'.join(lines)


if __name__ == '__main__':
    demo()
