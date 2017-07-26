# bstr_pos: only positive integers
# zero     -> ''
# negative -> ''

bstr_pos = lambda n: n>0 and bstr_pos(n>>1)+str(n&1) or ''

# bstr_nonneg: only non-negative integers
# zero     -> '0'
# negative -> ''

bstr_nonneg = lambda n: n>0 and bstr_nonneg(n>>1).lstrip('0')+str(n&1) or '0'

# bstr_sgn: all integers, signed
# zero -> '0'
# negative get a minus sign

bstr_sgn = lambda n: n<0 and '-'+binarystr(-n) or n and bstr_sgn(n>>1).lstrip('0')+str(n&1) or '0'

# bstr: all integers
# zero -> '0'
# negative represented as complements, 16-bit by default
# optional second argument specifies number of bits

bstr = lambda n, l=16: n<0 and binarystr((2L<<l)+n) or n and bstr(n>>1).lstrip('0')+str(n&1) or '0'
