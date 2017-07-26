#---------------------------------------------------------------------

# Recursice computation of list length:

def rec_list_len(lis):
    if not lis:
        return 0
    #print "calling rec_list_len with lis = {}".format(lis)
    return 1 + rec_list_len(lis[1:])

print "Recursive computation of list length:"
print
for lis_siz in range(5):
    lis = range(lis_siz)
    lis_len = rec_list_len(lis)
    print 'List: {}   Length: {}'.format(lis, lis_len)
    print

# Also test rec_list_len on other kinds of sequences than lists:

s = 'hello there'
print 'String: "{}"   Length: {}'.format(s, rec_list_len(s))
print
s = 'the quick brown fox'
print 'String: "{}"   Length: {}'.format(s, rec_list_len(s))
print

student = ('Jack', 25, 'New York')
print 'Tuple: {}   Length: {}'.format(student, rec_list_len(student))
print
student = ('Jill', 27, 'Paris', 'France')
print 'Tuple: {}   Length: {}'.format(student, rec_list_len(student))
print

#---------------------------------------------------------------------

# Recursive list sum computation.
# Assumes list items are numbers.

def rec_list_sum(lis):
    if not lis:
        return 0
    return lis[0] + rec_list_sum(lis[1:])

for r in range(5):
    lis = range(r)
    print "Sum:", rec_list_sum(lis), "List:", lis

#---------------------------------------------------------------------

# Recursive list product computation.
# Assumes list items are numbers.

def rec_list_product(lis):
    if not lis:
        return 1
    return lis[0] * rec_list_product(lis[1:])

for r in range(1, 7):
    lis = range(1, r)
    print "Product:", rec_list_product(lis), "List:", lis

#---------------------------------------------------------------------
