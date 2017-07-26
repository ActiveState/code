import win32api

#make long integers are used
neg_gig2=-2147483648L
gig2=2147483648L
gig4=4294967296L

#additional stores every whole group of 4 gigs
#base stores the remainder as an (unfortunately)signed int
#ignore the rest of what is returned in the array
file='c:/pagefile.sys'
(additional,base)=win32api.FindFiles(file)[0][4:6]

size=base

#if you get a negative size, that means the size is between 2 and 4 gigs
#The more negative the smaller the file
if base<0L:
 size=long(abs(neg_gig2-base))+gig2

#For every additional you add 4 gigs 
if additional:
 size=size+(additional*gig4)

print size,'bytes or ',size/1024,'kb'
