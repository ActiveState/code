# radix.py

"""
Defines str(number,radix) -- reverse function to int(str,radix) and long(str,radix)

number -- signed int or long,
radix  -- 2 to 36

Usage:
import radix
str_repr = radix.str( number, radix )

print radix.str( 10, 16 ), radix.str( 1570137287, 36 ) # a python

"""


import string


def str( number, radix ):
   """str( number, radix ) -- reverse function to int(str,radix) and long(str,radix)"""

   if not 2 <= radix <= 36:
      raise ValueError, "radix must be in 2..36"

   abc = string.digits + string.letters

   result = ''

   if number < 0:
      number = -number
      sign = '-'
   else:
      sign = ''

   while True:
      number, rdigit = divmod( number, radix )
      result = abc[rdigit] + result
      if number == 0:
         return sign + result

   # never here because number >= 0, radix > 0, we repeat (number /= radix)


if __name__ == '__main__':
   src = 'qwertyuioplkjhgfdsazxcvbnm0987654321'
   dst = 79495849566202193863718934176854772085778985434624775545L

   num = int( src, 36 )
   assert num == dst
   res = str( num, 36 )
   assert res == src
   print "%s radix 36 is\n%d decimal" % (src, dst)


# EOF
