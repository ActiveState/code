#without using the operator module you can map a list of integers to their
#absolute value with the following 5 methods 
a= [1,-2,3]

#first 3 use older non-iterative approach
b=[]
for i in a: b.append(abs(i))
print b

print [abs(i) for i in a ]
print map(lambda i:abs(i),a) 
>>> [1, 2, 3]  #all produce this result

#The next 2 use an approach in which the entire
#list is not returned, instead elements are returned one at a time
#which can offer substantial memory savings

#python 2.3 itertools
for j in itertools.imap(lambda i:abs(i),a): 
    print j,
#python 2.4 generator
for j in (abs(i) for i in a ):
    print j,

#both produce this result, note no list [] 
>>> 1 2 3

#if you want a list, wrap with list():
print list(itertools.imap(lambda i:abs(i),a))
>>> [1, 2, 3]

#The operator module allows you to use python's operators as a function:
#instead of a+b you would use add(a,b). To show off the operator module,
#for these examples, I use map. If memory is a concern, with python 2.3
#you can use itertools.imap

#abs: equivalent use to the previous 5 examples 
print map(operator.abs,[1,2,3])
>>> [1, 2, 3]

#add:  add the integers some lists together you can do:
print map(operator.add,[1,2,3],[4,5,6])
>>> [5, 7, 9]

#contains: check for membership
data=( ('fred','jane','ted'),('bill','jane','amy'),('sam','jane','matt'))
#look for groups which have fred
print map(operator.contains,data, ('fred','fred','fred'))
>>> [True, False, False]

#getslice: slice the first 2 elements from each group
print map(operator.getslice,data,(0,0,0),(2,2,2))
>>> ('fred', 'jane'), ('bill', 'jane'), ('sam', 'jane')]

#getslice: The problem with the 2 previous example is obviously the repetition
#you can deal with it by doing the following
print map(operator.getslice,data,(0,)*len(data),(2,)*len(data))
>>> [('fred', 'jane'), ('bill', 'jane'), ('sam', 'jane')]

#getitem: to get the 2nd element from each group
print map(operator.getitem,data,(1,)*len(data))
>>> ['jane', 'jane', 'jane']

#getitem: get elements 1,3,5 from the list 'a'
a=['a','b','c','d','e','f']
b=[1,3,5]

print map(operator.getitem,[a]*len(b),b)
>>> ['b', 'd', 'f']

#itemgetter: an even better alternative to getitem
data=( ('fred','jane','ted'),('bill','jane','amy'),('sam','jane','matt'))
print map(operator.itemgetter(1),data)
>>> ['jane', 'jane', 'jane']

#itemgetter: also of course works with dictionaries
data= ( {'name':'fred','score':50},{'name':'betty','score':75})
print map(operator.itemgetter('name'),data)
>>> ['fred', 'betty']

#setitem:initialize a dictionary 
#in this case imagine if you have 2 columns of data, one with people
#and the other with their scores
people=(('fred','sam','jane','betty'),(1,2,3,4))

p_dict = {}
map(operator.setitem, [p_dict]*len(people[0]), people[0],people[1])
print p_dict
>>> {'jane': 3, 'betty': 4, 'sam': 2, 'fred': 1}

#setitem: map one dictionary to another: same keys, different values
d1={'a':1,'b':2}
d2={}
old_keys = d1.keys()
new_vals = map(chr, d1.values())
map(operator.setitem, [d2]*len(old_keys), old_keys, new_vals)
print d1
print d2
>>> {'a': 1, 'b': 2}
>>> {'a': '\x01', 'b': '\x02'}
