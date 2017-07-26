def str_to_int(s):
    ctr = i = 0
    for c in reversed(s):
        i += (ord(c) - 48) * (10 ** ctr)
        ctr += 1
    return i

print
for s in ('0', '1', '2', '3', '12', '123', '234', '456', '567'):
    i = str_to_int(s)
    print "s = {}, i = {} |".format(s, i),

print
print

for i in range(50):
    s = str(i)
    j = str_to_int(s)
    print "s = {}, j = {} |".format(s, j), 
