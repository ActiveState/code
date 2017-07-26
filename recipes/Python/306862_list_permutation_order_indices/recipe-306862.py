# Based on a post by Peter Otten on comp.lang.python 2004/09/04.
# This uses the 'key' option to sort and the 'sorted' function, both
# new in Python 2.4.

def permutation_indices(data):
     return sorted(range(len(data)), key = data.__getitem__)

if __name__ == "__main__":
     import sys
     chars = "Sing a song of six-pence."
     print chars
     print   "0         1         2     "
     print   "01234567890123456789012345"
     print
                    
     indices = permutation_indices(chars)
     for i in indices:
          print "%4s %r" % (i, chars[i])

# Sing a song of six-pence.
# 0         1         2     
# 01234567890123456789012345
# 
#    4 ' '
#    6 ' '
#   11 ' '
#   14 ' '
#   18 '-'
#   24 '.'
#    0 'S'
#    5 'a'
#   22 'c'
#   20 'e'
#   23 'e'
#   13 'f'
#    3 'g'
#   10 'g'
#    1 'i'
#   16 'i'
#    2 'n'
#    9 'n'
#   21 'n'
#    8 'o'
#   12 'o'
#   19 'p'
#    7 's'
#   15 's'
#   17 'x'
