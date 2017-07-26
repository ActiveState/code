#return data which has groups of a name following by 2 scores.
def get_data():
    return [('fred',10,1),('bill',3,0),('betty',5,8),('jim',0,4)]

####basic older sorting approaches

#By default list's sort method will first sort the names, then the numbers
a=get_data()
a.sort()
print a
>>>[('betty', 5, 8), ('bill', 3, 0), ('fred', 10, 1), ('jim', 0, 4)]


#Now use a special function to sort by only the 1st score. This happens to be
element 1 of the 3 member tuple, so we reference elements a[1] and b[1] Notice
that betty is not first now, jim who has the lowest 1st score is now first
def cmp1(a,b):
    if a[1]<b[1]: return -1
    if a[1]==b[1]: return 0
    if a[1]>b[1]: return 1

#Even better, you can use of python's builtin cmp
def cmp1(a,b): return cmp(a[1],b[1])
    
a=get_data()
a.sort(cmp1)
print a
>>>[('jim', 0, 4), ('bill', 3, 0), ('betty', 5, 8), ('fred', 10, 1)]

#If you know you are only going to be sorting numbers, you can make the special 
function small enough so using an anonymous function lambda makes sense
a=get_data()
a.sort(lambda a, b: a[1]-b[1])
print a
>>>[('jim', 0, 4), ('bill', 3, 0), ('betty', 5, 8), ('fred', 10, 1)]


#Transform approach which does the same as above, except has the advantage of
avoiding the special function to which speeds up list.sort()
In this case we build a list whose 1st element is the part of the
data structure we want to be sorted.
a=get_data()
b=[]
for i in a:
    b.append((i[1],i))
b.sort()    
a=[ j[1] for j in b ]
print a
>>>[('jim', 0, 4), ('bill', 3, 0), ('betty', 5, 8), ('fred', 10, 1)]

#####Using the datastructure itself to do the sorting
#####python 2.4 adds: heapq and bisect implemented in C

#The default sort with bisect is simple, once the data is inserted into the list
#it is already sorted. No need to do a list.sort()
import bisect
a=[]
for i in get_data(): bisect.insort(a,i)
print a 
>>>[('betty', 5, 8), ('bill', 3, 0), ('fred', 10, 1), ('jim', 0, 4)]

#If you want to sort based off of the 1st score at element one,
#we insert pairs of data, in which the element zero of the pair
#is the item we want the sort to be based off of and then convert
#the data back to the original
import bisect
a=[]
for i in get_data():
        bisect.insort(a,(i[1],i))
#map out the original data, now it starts with jim instead of betty
print [ j[1] for j in a ]
>>> [('jim', 0, 4), ('bill', 3, 0), ('betty', 5, 8), ('fred', 10, 1)]

#The heapq is similar but it only guarantees element 0 always has the smallest
#item in the list. It has less overhead than bisect, but to get a sorted result,
#you have to pop from the heap, since the data at higher indexes isn't fully #sorted
import heapq
heaped_list=[]
for i in get_data():
        heapq.heappush(heaped_list,(i[1],i))
while 1:
    try:
        print heapq.heappop(heaped_list)[1],
    except IndexError:
        break
>>> ('jim', 0, 4) ('bill', 3, 0) ('betty', 5, 8) ('fred', 10, 1)

#####python 2.4 sorting approaches. 
#adds: cmp,key, and reverse keywords to list.sort()
#adds: operator.itemgetter which helps limit use of functions

#reverse argument, will do highest to lowest, jim then fred now
a=get_data()
a.sort(reverse=True)
print a
>>>[('jim', 0, 4), ('fred', 10, 1), ('bill', 3, 0), ('betty', 5, 8)]

#keyword argument cmp for the comparison function as above
a=get_data()
a.sort(cmp=cmp1)
print a
>>>[('jim', 0, 4), ('bill', 3, 0), ('betty', 5, 8), ('fred', 10, 1)]

#The keyword argument key is an easy way to do the Transform. You simply provide
#a function which returns the part of the data structure that you want the
#sort to be based off of, instead of creating a list yourself to house it like
#we do above.

This enables a really easy way to do a numberical sort of strings. Note: I use the new python 2.4 sorted function:
>>> j=['100','11','17','1000']
>>> sorted(j)
['100', '1000', '11', '17']
>>> sorted(j,key=int)
['11', '17', '100', '1000']
>>> 

a=get_data()
#anonymous function lambda returns index one, which is a score
a.sort(key=lambda i:i[1]) 
print a
>>>[('jim', 0, 4), ('bill', 3, 0), ('betty', 5, 8), ('fred', 10, 1)]



#This can be further enhanced with a new addition to the operator
#module called itemgetter. It let's you avoid the function entirely to get an
#index (check out operator.attrgetter for attributes).
import operator
a=get_data()
a.sort(key=operator.itemgetter(1)) #get index 1 of the item for sorting
print a
>>>[('jim', 0, 4), ('bill', 3, 0), ('betty', 5, 8), ('fred', 10, 1)]


#You can also use the 2 keywords together. This would be useful
#if for example you want to sort based off of the SUM of the scores
#rather than an individual one

#In this function we add the 2 scores together to enable a sort based off
#of both values. Bill who has the lowest sum is now first, not jim
#who had the lowest 1st score.
def cmp2(a,b):
    sum1=a[0]+a[1]
    sum2=b[0]+b[1]
    return cmp(sum1,sum2)

#The anonymous function lambda returns everything but the 1st element
#to avoid the name. We only want scores for summing.
a=get_data()
a.sort(key=lambda i:i[1:],cmp=cmp2)

print a 
>>>[('bill', 3, 0), ('jim', 0, 4), ('fred', 10, 1), ('betty', 5, 8)]
