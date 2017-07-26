an unordered list of numbers
the_list=[903, 10, 35, 69, 933, 485, 519, 379, 102, 402, 883, 1]

#standard list.sort() techniques
#to get lowest element which is 1, sort and pop
the_list.sort()
print the_list.pop(0)
>>> 1

#if you get more data, you need to sort again before popping
the_list.append(0)
print the_list.pop(0)
>>> 10 -- oops not zero, didn't sort

#a heap solves this problem, by always being ordered
#to create a heap you push with heapq.heappush onto a list
import heapq
the_heap = []
for i in the_list: heapq.heappush(the_heap, i)
print the_heap
#note how zero is first, but the heap isn't fully ordered
>>> [0, 35, 102, 379, 69, 485, 519, 883, 903, 933, 402]

#if you add some more zeros, the fact that it is not fully sorted
#becomes more obvious, look at where the zeros are at

heapq.heappush(the_heap,0)
heapq.heappush(the_heap,0)
print the_heap
>>> [0, 35, 0, 379, 69, 0, 519, 883, 903, 933, 402, 485, 102]

#But, you will still get data back in an ordered way when you pop
print heapq.heappop(the_heap)
>>> 0
print heapq.heappop(the_heap)
>>> 0
print the_heap
>>> [0, 35, 102, 379, 69, 485, 519, 883, 903, 933, 402]

#The method heapreplace is a combination of a pop and a push.
#In this case the smallest element 0 is popped off and 200 is inserted at
#some other place into the heap
print heapq.heapreplace(the_heap, 200) 
>>> 0
print the_heap
>>> [35, 69, 102, 379, 200, 485, 519, 883, 903, 933, 402]

#Ask for 5 largest or smallest-- does an actual sort for this
print heapq.nlargest(5,the_heap) #[933, 903, 883, 519, 485]
print heapq.nsmallest(5,the_heap) #[35, 69, 102, 200, 379]

#Popping everything off of the heap will give sorted results
while 1:
    try:
        print heapq.heappop(the_heap),
    except IndexError:
        break

>>> 35 69 102 200 379 402 485 519 883 903 933
