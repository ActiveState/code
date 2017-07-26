def solve(eq, var=('x', 'y')):
    """ Solve a system of simultaneous equation in
    two variables of the form

    2*x + 5*y=c1; 3*x - 5*y=c2

    Example: solve('12*x - 3*y = 21; 9*x  - 18*y=0')

    Should work for negative constants as well.

    Example: solve('3*x - 5*y=-11; 12*x + 3*y=48')

    Returns a two tuple of (x, y) values.

    NOTE: Won't denegarate to the special case
    of solving for only one variable.
    
    """

    var_re = re.compile(r'(\+|\-)\s*(\d*)\s*\*?\s*(x|y)')
    const_re = re.compile(r'(\+|\-)\s*(\-?\d+)$')

    constants, eqns, coeffs, default  = [],[], {'x': [], 'y': []}, {'': '1'}

    for e in eq.split(';'):
        eq1 = e.replace("="," - ").strip()
        if not eq1.startswith('-'):
            eq1 = '+' + eq1
        eqns.append(eq1)

    var_eq1, var_eq2 = map(var_re.findall, eqns)

    constants = [-1*int(x[0][1]) for x in map(const_re.findall, eqns)]
    [coeffs[x[2]].append(int((x[0]+ default.get(x[1], x[1])).strip())) for x in (var_eq1 + var_eq2)]
    
    ycoeff = coeffs['y']
    xcoeff = coeffs['x']

    # Adjust equations to take out y and solve for x
    if ycoeff[0]*ycoeff[1] > 0:
        ycoeff[1] *= -1
        xcoeff[0] *= ycoeff[1]
        constants[0] *= -1*ycoeff[1]        
    else:
        xcoeff[0] *= -1*ycoeff[1]
        constants[0] *= ycoeff[1]
        
    xcoeff[1] *= ycoeff[0]
    constants[1] *= -1*ycoeff[0]

    # Obtain x
    xval = sum(constants)*1.0/sum(xcoeff)

    # Now solve for y using value of x
    z = eval(eqns[0],{'x': xval, 'y': 1j})
    yval = -z.real*1.0/z.imag

    return (xval, yval)
