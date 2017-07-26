#!/usr/bin/env python
"""
2012-03-05, weeee!

This is a really simple script, the docs are WAY longer, that
dices a date-string returning a list of integers or a dict if
key-words are supplied.

... IT SLICES, IT DICES, IT HAS SHARP EDGES!
    ===============================================
    Not production-ready, 'nless you like to play with razors.
    There is no type-checking, no assertion for field-order etc.
    This simply, blindly and unintelligently guts the string.   
    If the order changes, it bites... you get the idea.

Some examples, more plus arg-defs b'low

    TEST_DATE = "2012-03-05 13:05:14.453728"
    
    # return list of int's in original order
    cheap_date(TEST_DATE)
    [2012, 3, 5, 13, 5, 14, 453728]
    
    ISO_KEYS = ['t_year','t_mon','...'t_sec','t_usec']

    # return same list, mapped into a dict
    cheap_date(TEST_DATE, ISO_KEYS)
    {'t_mon': 3, 't_min': 5, 't_sec': 14, 't_hour': 13,
              't_day': 5, 't_year': 2012, 't_usec': 453728}
    
    # Keep the decimal t'gether using non-default regex
    # Note: list is str's, int("12.34") razors a ValueError
    cheap_date(TEST_DATE, [], DIG_N_DEC, str)
    ['2012', '03', '05', '13', '05', '14.453728']
    
    # dict's and format strings, naturally sweeeeet
    FMT_STR % cheap_date(TEST_DATE, ISO_KEYS, DIG_N_DEC, PAT)
    2012-03-05T13:05:14.454
    
    FMT_STR2 % cheap_date(TEST_DATE, ISO_KEYS, val_conv = str)
    13:05-03/05/2012

"""

import re

def cheap_date(dt_str, kw_list = [], reg_xp = r'\D', val_conv = int):
    """ Cheap incremental date parser preserving ISO microseconds

    dt_str:     String representing source date
           pass "2012-03-05 13:05:14.453728"
        returns [2012, 3, 5, 13, 5, 14, 453728]

      optional- ['2012', '03', '05', '13', '05', '14.453728']
        returns {'tm_year': 2012, 'tm_mday': 5, 'tm_mon': 3 ... }

    Optional arguments:

    kw_list:    Ordered list of return-dictionary keys
    reg_xp:     Regular expression used to split the string
    val_conv:   List-processor for data-conversion i.e. str --> int

    >>> cheap_date(TEST_DATE)
    [2012, 3, 5, 13, 5, 14, 453728]
    >>> cheap_date(TEST_DATE, ISO_KEYS[:3])
    {'t_mon': 3, 't_day': 5, 't_year': 2012}
    >>> FMT_STR2 % cheap_date(TEST_DATE, ISO_KEYS, val_conv = str)
    '13:05-03/05/2012'
    """
    # shake the numbers out with re ['2012', '03'...]
    tm_list = re.split(reg_xp, dt_str)
    
    # juice 'em: apply function to each list-value [2012, 03...]
    # you _could_ test if val_conv == str an omit this step
    tm_list = map(val_conv, tm_list)

    # Existence of this list, enables return of a dictionary
    if kw_list:
        # fabricate list of key-value pairs [['yr',2012],[....],]
        tm_list = zip(kw_list, tm_list)
        
        # map the key-val pairs into a dict to be proud of
        tm_list = dict(tm_list)
    
    return tm_list


def cheaper_date(dt_str, kw_list = [], reg_xp = r'\D', val_conv = int):
    """ Cheaper date parser, with a few less teeth

    >>> FMT_STR2 % cheaper_date(TEST_DATE, ISO_KEYS, val_conv = str)
    '13:05-03/05/2012'
    """
    # The functionality above, tucked in a thin blankie.
    try:
        tm_list = map(val_conv, re.split(reg_xp, dt_str))
    except ValueError, e:
        print "Conversion proc (int?) spewed a matched value"
        print e
        raise
        
    if kw_list:
        tm_list = dict(zip(kw_list, tm_list))

    return tm_list

if __name__ == '__main__':
    import doctest

    # Some Q&D convenience, ta get 'r done.
    TEST_DATE = "2012-03-05 13:05:14.453728"

    # Keys match  number-seq. order of date to parse
    ISO_KEYS = ['t_year','t_mon','t_day','t_hour','t_min','t_sec','t_usec']

    # Slow lrner moi! Ages till I grep'd the non-obv. & betwix da lines.
    # A.K.A: "To select or not select? TITQ!" I mean "\d" to "\D" 

    # The following exp. splits, and discards, NON-number sequences.
    DIGITS_ONLY = r'\D' # DEFAULT, digits only: 12.56-> ['12','56']

    # \d is inverse|not \D, [^....] inverse|not's the match 
    DIG_N_DEC = r'[^\d\.]' # retain decmal no's 34.78-> ['34.78',]
    
    # With a dict[ionary] and format strings, it happens eh?
    FMT_STR = "T".join(["%(t_year)d-%(t_mon)02d-%(t_day)02d",
                                "%(t_hour)02d:%(t_min)02d:%(t_sec)0.3f"])
    # Same info, just shuffled for my simple-minded amusement
    FMT_STR2 = "%(t_hour)s:%(t_min)s-%(t_mon)s/%(t_day)s/%(t_year)s"
    
    # Pick-A-Type... for demo. Its stupid, assumes a string of digits only.
    # There are safer/elegantisher ways to do this... more calories though.
    def PAT(s): 
        try:
            return int(s)
        except ValueError:
            return float(s)

    doctest.testmod()
