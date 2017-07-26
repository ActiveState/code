# explicit if
for i in range(1,3):
    if i == 1:
        plural = ''
    else:
        plural = 's'
    print "The loop ran %d time%s" % (i, plural)

# selecting from tuple
for i in range(1,3):
    print "The loop ran %d time%s" % (i, ('','s')[i != 1])

# short-circuited logical expression
for i in range(1,3):
    print "The loop ran %d time%s" % (i, i != 1 and 's' or '')

# Output of all loops:
# The loop ran 1 time
# The loop ran 2 times
