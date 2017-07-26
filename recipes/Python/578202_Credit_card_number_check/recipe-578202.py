cc_patterns = { # '<cc_type>' : { dict of valid lengths : [list of associated prefixes] }
    'amex' : { (15) : ('34', '37') },
    'carteblanche' : { (14) : ('300', '301', '302', '303', '304', '305', '36', '38') },
    'dinersclub' : { (14) : ('300', '301', '302', '303', '304', '305', '36', '38') },
    'discover' : { (16) : ('6011') },
    'enroute' : { (15) : ('2014', '2149') },
    'jcb' : { (15) : ('2131', '1800'), (16) : ('3') },
    'mastercard' : { (16) : ('51', '52', '53', '54', '55') },
    'visa' : { (13, 16) : ('4') }
}

def cc_check( cc_num, cc_type ):
    ''' 
        Returns a touple of (isValidated, strReason) 
    
        * All doctest cc#s are random and do not reflect real world numbers *
        >>> result = cc_check('5235235879456682', 'MASTERCARD')
        >>> result[0]
        True
        >>> result = cc_check('5235235879456683', 'MASTERCARD')
        >>> result[0]
        False
        >>> result[1].find('Invalid check sum')
        0
        >>> result = cc_check('523523583', 'MASTERCARD')
        >>> result[0]
        False
        >>> result[1].find('Invalid length')
        0
        >>> result = cc_check('3235235879456683', 'MASTERCARD')
        >>> result[0]
        False
        >>> result[1].find('Invalid prefix')
        0
    '''
    cc_type = cc_type.strip().lower().replace(' ', '')
    cc_num = str(cc_num)
    
    
    if cc_type in cc_patterns.keys():
        # Perform length check
        valid_lengths = cc_patterns[cc_type].keys()
        if len(cc_num) not in valid_lengths:
            return (False, 'Invalid length (%s) for %s' % \
                (str(valid_lengths).strip('[]'), cc_type))
                
        # Perform prefix check
        valid_prefixes = cc_patterns[cc_type][len(cc_num)]
        prefix_match = False
        for prefix in valid_prefixes:
            prefix_length = len(prefix)
            if cc_num[:prefix_length] == prefix:
                prefix_match = True
        if not prefix_match:
            return (False, 'Invalid prefix (not in %s)' % \
                ','.join(valid_prefixes))
                
        # Perform mod 10 check
        if cc_type == 'enroute':
            pass # Only cc_type that doesn't do a mod 10 check
        else:
            check_digits = []
            is_even = False
            for i, digit in enumerate(cc_num):
                is_even = (i % 2 == 1)
                if is_even:
                    check_digits.append(int(digit))
                else:
                    mult_digits = str(int(digit) * 2)
                    check_digits.append(int(mult_digits[0]))
                    if len(mult_digits) == 2:
                        check_digits.append(int(mult_digits[1]))
            
            check_sum = sum(check_digits)
            if check_sum % 10 != 0:
                return (False, 'Invalid check sum (%d)' % check_sum)
                
        return (True, '')
    else:
        return (False, 'Invalid cc type (%s)' % cc_type)
    
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
    
