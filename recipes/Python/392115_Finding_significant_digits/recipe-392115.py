import unittest

def makeSigDigs(num, digits, debug=False):
    """Return a numeric string with significant digits of a given number.
    
    Arguments:
      num -- a numeric value
      digits -- how many significant digits (int)
      debug -- boolean; set to True for verbose mode
    """
    notsig = ['0', '.', '-', '+', 'e'] # not significant
    pad_zeros_left = '' # zeros to pad immed. left of the decimal
    pad_zeros_right = '' # zeros to pad immed. right of the decimal
    pad_zeros_last = '' # zeros to pad after last number after decimal
    str_left = '' # string to prepend to left of zeros and decimal
    str_right = '' # string to append to right of decimal and zeros
    dec = '.' # the decimal
    e_idx = None
    e_str = ''
    num = float(num)
    if debug: print "%s at %s digits:" % (repr(num), digits)
    for n in repr(num):
        if n not in notsig: # ignore zeros and punctuation
            first_idx = repr(num).find(n) # index of first digit we care about
            if debug: print "\tfirst digit at %s" % (first_idx)
            break
    try: first_idx # If it doesn't exist, then we're looking at 0.0
    except UnboundLocalError:
        return '0.0'
    try: e_idx = repr(num).index('e') # get index of e if in scientific notation
    except: pass
    if debug: print "\te at: %s" % (e_idx)
    dec_idx = repr(num).find('.') # index of the decimal
    if debug: print "\tdecimal at %s" % (dec_idx)
    if dec_idx < first_idx:
        """All sigdigs to right of decimal '0.033'
        """
        if debug: print "\tdigits are right of decimal."
        last_idx = first_idx + digits -1
        if last_idx+1 > len(repr(num)[0:e_idx]): # in case we need extra zeros at the end
            pad_zeros_last = '0'*(last_idx+1 - len(repr(num)[0:e_idx]))
        if e_idx and last_idx >= e_idx: # fix last_idx if it picks up the 'e'
            last_idx = e_idx-1
        pad_zeros_left = '0'*1
        pad_zeros_right = '0'*(first_idx - dec_idx - 1)
        str_right = repr(num)[first_idx:last_idx+1]
    elif dec_idx > first_idx + digits - 1:
        """All sigdigs to left of decimal. '3300.0'
        """
        if debug: print "\tdigits are left of decimal."
        last_idx = first_idx + digits - 1
        if e_idx and last_idx >= e_idx: # fix last_idx if it picks up the 'e'
            last_idx = e_idx-1
        str_left = repr(num)[first_idx]
        str_right = repr(num)[first_idx+1:last_idx+1]+'e+'+str(dec_idx-1-first_idx)
    else:
        """Sigdigs straddle the decimal '3.300'
        """
        if debug: print "\tnumber straddles decimal."
        last_idx = first_idx + digits # an extra place for the decimal
        if last_idx+1 > len(repr(num)[0:e_idx]): # in case we need extra zeros at the end
            pad_zeros_last = '0'*(last_idx+1 - len(repr(num)[0:e_idx]))
        if e_idx and last_idx >= e_idx: # fix last_idx if it picks up the 'e'
            last_idx = e_idx-1
        str_left = repr(num)[first_idx:dec_idx]
        str_right = repr(num)[dec_idx+1:last_idx + 1]
    if e_idx:
        e_str = repr(num)[e_idx:]
    if debug: print "\tlast digit at %s" % (last_idx)
    if debug: print "\t%s %s %s %s %s %s %s" % (str_left or '_',
                                                pad_zeros_left or '_',
                                                dec or '_',
                                                pad_zeros_right or '_',
                                                str_right or '_',
                                                pad_zeros_last or '_',
                                                e_str or '_')
    sig_string = str_left+pad_zeros_left+dec+pad_zeros_right+str_right+pad_zeros_last+e_str
    if debug: print "\tsignificant: %s\n" % (sig_string)
    return sig_string



class utMakeSigDigs(unittest.TestCase):
    knownValues = [[333.333, 4, '333.3'],
                   [33.0, 2, '3.3e+1'],
                   [333.33, 2, '3.3e+2'],
                   [33300.00, 4, '3.330e+4'],
                   [0.0033333, 3, '0.00333'],
                   [3.3e-10, 2, '3.3e-10'],
                   [0.0001, 2, '0.00010'],
                   [3.3e-10, 3, '3.30e-10'],
                   [1.0000000, 6, '1.00000'],
                   [1.00000001591, 6, '1.00000'],
                   [33330000000000000000.0, 6, '3.33300e+19'],
                   [33330000000000000000.03, 6, '3.33300e+19']
                   ]
    def testKnownValues(self):
        """MakeSigDigs should return known values for known inputs.
        """
        for el in self.knownValues:
            self.assertEqual(makeSigDigs(el[0], el[1], debug=True), el[2])

if __name__ == "__main__":
    unittest.main()
