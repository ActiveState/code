import string

star_list = ['Elizabeth Taylor',
             'Bette Davis',
             'Hugh Grant',
             'C. Grant']

star_list.sort(lambda x,y: (
   cmp(string.split(x)[-1], string.split(y)[-1]) or  # Sort by last name ...
   cmp(x, y)))                                       #  ... then by first name

print "Sorted list of stars:"
for name in star_list: 
    print name

#
# "cmp(X, Y)" return 'false' (0) when X and Y compare equal,
# so "or" makes the next "cmp()" to be evaluated.
# To reverse the sorting order, simply swap X and Y in cmp().
#
# This can also be used if we have some other sorting criteria associated with
# the elements of the list.  We simply build an auxiliary list of tuples
# to pack the sorting criteria together with the main elements, then sort and
# unpack the result.
#

def sorting_criterium_1(data):
    return string.split(data)[-1]   # This is again the last name.

def sorting_criterium_2(data):
    return len(data)                # This is some fancy sorting criterium.

# Pack the auxiliary list:
aux_list = map(lambda x: (x, 
                          sorting_criterium_1(x), 
                          sorting_criterium_2(x)),
               star_list)
# Sort:
aux_list.sort(lambda x,y: (
   cmp(x[1], y[1])  or       # Sort by criteria 1 (last name)...
   cmp(y[2], x[2])  or       #  ... then by criteria 2 (in reverse order) ...
   cmp(x, y)))               #  ... then by the value in the main list.
# Unpack the resulting list:
star_list = map(lambda x: x[0], aux_list)

print "Another sorted list of stars:"
for name in star_list: 
    print name
