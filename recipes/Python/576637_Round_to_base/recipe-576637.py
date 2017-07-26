import builtins

def Round(a,base_place=0,base=10):
    '''
        implement Rounding to bases other than 10.

        known deficiencies:
            fails with decimal input
            fails with fractions input

        Beware of 0 < base < 1 since b**(-p) == (1/b)**(p)

        >>> [Round(x,-1,5) for x in (142,143,147,)]
        [140, 145, 145]
        >>>
        >>> [(p,Round(12.345,p,2)) for p in range(-3,3)]
        [(-3, 16.0), (-2, 12.0), (-1, 12.0), (0, 12.0), (1, 12.5), (2, 12.25)]
        >>>
        >>> # Use for base < 1
        >>> # one might want decimal input
        >>> # Round to the nearest US nickel
        >>> no_pennies = Round(12.07,-1,0.05)
        >>> print('{0:.2f}'.format(no_pennies))
        12.05
        >>> # The advertising game
        >>> price_per_gallon = Round(12.379999999999,-1,1/100)
        >>> print('{0:.2f}'.format(price_per_gallon))
        12.38
        >>>
        >>> # round to nearest multiple of square root of two
        >>> x = Round(12.379999999999,1/2,2)
        >>> print (x / 2**(1/2))
        9.0
        >>>
    '''
    # consider using sign transfer for negative a

    if base == 10:
        return builtins.round(a,base_place)

    if base <= 0:
        raise ValueError('base too complex')

    b = base**base_place
    return type(a)(int(a*b+0.5)/b)
