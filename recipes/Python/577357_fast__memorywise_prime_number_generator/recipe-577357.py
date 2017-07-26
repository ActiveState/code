import numpy
def primesgen2(n):
    """ Input n>=30, Generates all primes < n """
    sieve01 = numpy.ones(n/30+1, dtype=numpy.bool)
    sieve07 = numpy.ones(n/30+1, dtype=numpy.bool)
    sieve11 = numpy.ones(n/30+1, dtype=numpy.bool)
    sieve13 = numpy.ones(n/30+1, dtype=numpy.bool)
    sieve17 = numpy.ones(n/30+1, dtype=numpy.bool)
    sieve19 = numpy.ones(n/30+1, dtype=numpy.bool)
    sieve23 = numpy.ones(n/30+1, dtype=numpy.bool)
    sieve29 = numpy.ones(n/30  , dtype=numpy.bool)
    sieve01[0] = False
    yield 2; yield 3; yield 5;
    for i in xrange(int(n**0.5)/30+1):
        if sieve01[i]:
            k=30*i+1; yield k;
            sieve01[     (k*k)/30::k] = False
            sieve07[(k*k+ 6*k)/30::k] = False
            sieve11[(k*k+10*k)/30::k] = False
            sieve13[(k*k+12*k)/30::k] = False
            sieve17[(k*k+16*k)/30::k] = False
            sieve19[(k*k+18*k)/30::k] = False
            sieve23[(k*k+22*k)/30::k] = False
            sieve29[(k*k+28*k)/30::k] = False
        if sieve07[i]:
            k=30*i+7; yield k;
            sieve01[(k*k+ 6*k)/30::k] = False
            sieve07[(k*k+24*k)/30::k] = False
            sieve11[(k*k+16*k)/30::k] = False
            sieve13[(k*k+12*k)/30::k] = False
            sieve17[(k*k+ 4*k)/30::k] = False
            sieve19[     (k*k)/30::k] = False
            sieve23[(k*k+22*k)/30::k] = False
            sieve29[(k*k+10*k)/30::k] = False
        if sieve11[i]:
            k=30*i+11; yield k;
            sieve01[     (k*k)/30::k] = False
            sieve07[(k*k+ 6*k)/30::k] = False
            sieve11[(k*k+20*k)/30::k] = False
            sieve13[(k*k+12*k)/30::k] = False
            sieve17[(k*k+26*k)/30::k] = False
            sieve19[(k*k+18*k)/30::k] = False
            sieve23[(k*k+ 2*k)/30::k] = False
            sieve29[(k*k+ 8*k)/30::k] = False
        if sieve13[i]:
            k=30*i+13; yield k;
            sieve01[(k*k+24*k)/30::k] = False
            sieve07[(k*k+ 6*k)/30::k] = False
            sieve11[(k*k+ 4*k)/30::k] = False
            sieve13[(k*k+18*k)/30::k] = False
            sieve17[(k*k+16*k)/30::k] = False
            sieve19[     (k*k)/30::k] = False
            sieve23[(k*k+28*k)/30::k] = False
            sieve29[(k*k+10*k)/30::k] = False
        if sieve17[i]:
            k=30*i+17; yield k;
            sieve01[(k*k+ 6*k)/30::k] = False
            sieve07[(k*k+24*k)/30::k] = False
            sieve11[(k*k+26*k)/30::k] = False
            sieve13[(k*k+12*k)/30::k] = False
            sieve17[(k*k+14*k)/30::k] = False
            sieve19[     (k*k)/30::k] = False
            sieve23[(k*k+ 2*k)/30::k] = False
            sieve29[(k*k+20*k)/30::k] = False
        if sieve19[i]:
            k=30*i+19; yield k;
            sieve01[     (k*k)/30::k] = False
            sieve07[(k*k+24*k)/30::k] = False
            sieve11[(k*k+10*k)/30::k] = False
            sieve13[(k*k+18*k)/30::k] = False
            sieve17[(k*k+ 4*k)/30::k] = False
            sieve19[(k*k+12*k)/30::k] = False
            sieve23[(k*k+28*k)/30::k] = False
            sieve29[(k*k+22*k)/30::k] = False
        if sieve23[i]:
            k=30*i+23; yield k;
            sieve01[(k*k+24*k)/30::k] = False
            sieve07[(k*k+ 6*k)/30::k] = False
            sieve11[(k*k+14*k)/30::k] = False
            sieve13[(k*k+18*k)/30::k] = False
            sieve17[(k*k+26*k)/30::k] = False
            sieve19[     (k*k)/30::k] = False
            sieve23[(k*k+ 8*k)/30::k] = False
            sieve29[(k*k+20*k)/30::k] = False
        if sieve29[i]:
            k=30*i+29; yield k;
            sieve01[     (k*k)/30::k] = False
            sieve07[(k*k+24*k)/30::k] = False
            sieve11[(k*k+20*k)/30::k] = False
            sieve13[(k*k+18*k)/30::k] = False
            sieve17[(k*k+14*k)/30::k] = False
            sieve19[(k*k+12*k)/30::k] = False
            sieve23[(k*k+ 8*k)/30::k] = False
            sieve29[(k*k+ 2*k)/30::k] = False
    for i in xrange(i+1,n/30):
            if sieve01[i]: yield 30*i+1
            if sieve07[i]: yield 30*i+7
            if sieve11[i]: yield 30*i+11
            if sieve13[i]: yield 30*i+13
            if sieve17[i]: yield 30*i+17
            if sieve19[i]: yield 30*i+19
            if sieve23[i]: yield 30*i+23
            if sieve29[i]: yield 30*i+29
    if n%30 > 1:
        if sieve01[i+1]: yield 30*i+1
    if n%30 > 7:
        if sieve07[i+1]: yield 30*i+7
    if n%30 > 11:
        if sieve11[i+1]: yield 30*i+11
    if n%30 > 13:
        if sieve13[i+1]: yield 30*i+13
    if n%30 > 17:
        if sieve17[i+1]: yield 30*i+17
    if n%30 > 19:
        if sieve19[i+1]: yield 30*i+19
    if n%30 > 23:
        if sieve23[i+1]: yield 30*i+23
