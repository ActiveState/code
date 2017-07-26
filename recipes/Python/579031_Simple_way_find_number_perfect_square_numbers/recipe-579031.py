#
# Question: given a range a,b, find the total number of perfect square numbers in the given range.
#

import cmath

def find_perfect_square_count(a, b, verbose=False):
    '''    
        The strategy here is not to iterate through the set of possible integer values and check for is_perfect_square()
        each time but to translate the upper and lower values to either complex or real space of square numbers.
        
        # O(n) complexity
        len([x for x in range(0, 100) if x!= 0 and float(math.sqrt(x)).is_integer()])
        
        so if a and b positive then we count the number of integer values between upper and lower sqrt() values
        if either a or b are negative then we need to use the complex number space for the sqrt() results. In this case
        we are still counting integer values either along the imaginary or real axis, the result is then a simple sum
        if both a and b are negative we need to make sure that when walking down the same imaginary axis we dont count
        the same inteters twice, in this case we can take the min(a,b) to get max distinct set of integer values.
    
        a : float
            represents either start or end of range
            
        b : float
            represents either start or end of range
            
        return : integer or NaN
            returns total number of perfect square numbers between (a,b) or NaN if not available.
            
        complexity:
            O(a) scalar complexity
    
    '''
    
    # protect against silly type errors
    try:
        float(a)
        float(b)
    except:
        return NaN
    
    # protect against something that might be nothing
    if (a or b) in [None]:
        return NaN
    
    # nothing to do here, fail quickly no range, what if a and b are a square?
    if b==a  :
        return 0
    
    # do we need to handle complex numbers?
    if a < 0 or b < 0:
        if verbose:
            print 'complex'
        # case when a img and b real
        if a < 0 and b >= 0: 
            return np.sum([math.ceil(cmath.sqrt(complex(a,0)).imag), math.ceil(cmath.sqrt(complex(b,0)).real)])-2
        # case when a real b imag
        if a >= 0 and b < 0: 
            return np.sum([math.ceil(cmath.sqrt(complex(b,0)).imag), math.ceil(cmath.sqrt(complex(a,0)).real)])-2
        # special case when both negative, both vectors are aligned to the 
        # i axis, in this case we only need the min(a,b) otherwise we will double count
        if a < 0 and b < 0: 
            return np.sum([math.ceil(cmath.sqrt(complex(min(a,b),0)).imag)])-1
    
    if a >= b:
        count = 2*(ceil(math.sqrt(abs(a))) - ceil(math.sqrt(abs(b))))
        if count > 0:
            return count-2
        else:
            return 0
    
    if b >= a:
        # check to make sure we dont remove zero adjustment from zero count
        # incorrectly gives a negative count.
        count = 2*(ceil(math.sqrt(abs(b))) - ceil(math.sqrt(abs(a))))
        if count > 0:
            return count-2
        else:
            return 0
    
    # else return NaN
    return NaN



# some preflight checks
assert(find_perfect_square_count(0, 100) == 18)
assert(isnan(find_perfect_square_count('ff', 1.2))) 
assert(isnan(find_perfect_square_count('ff', None)))

# lets fully test
import random
number_of_tests = 5
value = 1e4
for (a,b) in zip([random.randint(-value,value) for x in arange(number_of_tests)]
                 , [random.randint(-value,value) for x in arange(number_of_tests)]):
    print '%d\t between \t[%d, %d]'%(find_perfect_square_count(a,b), a, b)
