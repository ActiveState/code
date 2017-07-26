# If you ever wanted to do something like:

for line in open('file').readlines().reverse():
   print line 

# you will have noticed that reverse is an "In-Place" method.
# it modifies the list itself and returns None.
# So the for loop sees just a (non-iterable) None.
# Even worse, you can't use reverse/sort/extend on tuples or strings.
# "hallo".reverse() or (3,1,5).sort() does not exist.  

# The obfuscated oneliner below solves these problems so that
# you can write 

for line in reverse(open('file').readlines()):
   print line # lines of the file in reverse order

# Additionally it allows you to use reverse/sort/extend 
# on tuples and strings and it always maintains Types.

sort([3,7,5])  # gives you a sorted list [3,5,7]

reverse("hallo") # returns reversed string "ollah"

extend( (1,2,3), (4,5) ) # returns (1,2,3,4,5)

# recursion/iteration of course works like usual:

print reverse(sort([7,3,5])) # prints [7,5,3]  

print extend(reverse(range(4)),([42],reverse('32')))
# will give you [3, 2, 1, 0, [42], '23']
# the last line shows, that types are really preserved!


# OK. Now on to the actual "Oneliner". I told you it's obfuscated 
# so don't complain. It actually has 275 characters so i
# split it here in four lines to make it (hopefully) "pastable"

for n,m in ( ('reverse(o)','n.reverse()'),('sort(o)','n.sort()'),\
 ('extend(o,o1)','n.extend(o1)')): exec "def %s:\n t=type\n to=t(o)\
\n if to in (t(''),t(())): n=list(o)\n else: n=to(o)\n %s\n return n and\
(to==t('') and ''.join(n) or to==t(()) and tuple(n) or n) or to()\n" % (n,m)

# paste this code into your interpreter or module 
# and the above examples should work. If you are interested in how
# it basically works (i hope so:-) read on




################
# Obviously you don't want me to talk about this code in compact form...
# (I have put an easily readable version at the end of the page)
# How does it work?
# It actually puts three functions into your current namespace. 
# Let me show you the first one, "reverse"

def reverse(o):
 t=type        # shortcut 
 to=t(o)       # store type of object to be reversed
 if to in (t(''),t(())): n=list(o)  # for tuples and strings construct list 
 else: n=to(o) # otherwise call copy-constructor
 n.reverse()   # now call the inplace method
 return n and (to==t('') and ''.join(n) or to==t(()) and tuple(n) or n) or to()

# The last line ensures that the result is of the same type as the input
# and that Results with length 0 are correctly returned.
# Actually reverse does not only work on strings, tuples and lists.
# It also works on any object which has an "Inplace-" reverse method, 
# a copy constructor and has the conversion into bool. 

# the generated "sort"-method is - apart from name - exactly like reverse.
# But "extend" is different because it needs another argument!
# If you look in the "for ... :"-part of the onliner you will 
# see that "extend" comes out slightly differently:

def extend(o,o1): # NOTE THIS LINE
 t=type
 to=t(o)
 if to in (t(''),t(())): n=list(o)
 else: n=to(o)
 n.extend(o1)  # NOTE THIS LINE
 return n and (to==t('') and ''.join(n) or to==t(()) and tuple(n) or n) or to()

# but actually it differs only in number of arguments: 
# - def extend(o,o1): has two arguments
# - n.extend(o1) gets the second argument

# If you want to play with it you should really use
# the following "longish" version of the code and put it in a module. 

signatures = (('reverse(o)','n.reverse()'),\
              ('sort(o)','n.sort()'), \
              ('extend(o,o1)','n.extend(o1)'))

functemplate="""
def %s:
    t=type
    to=t(o)
    if to in (t(''),t(())):
        n=list(o)
    else:
        n=to(o)
    %s
    return n and (to==t('') and ''.join(n) or to==t(()) and tuple(n) or n) or to()
"""

for n,m in signatures:
    #print functemplate % (n,m) # remove comment if you want to see
    exec functemplate % (n,m)
