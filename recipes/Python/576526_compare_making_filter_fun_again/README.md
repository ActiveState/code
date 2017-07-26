## compare(), making filter() fun again  
Originally published: 2008-10-04 14:27:27  
Last updated: 2008-10-04 12:40:42  
Author: Andreas Nilsson  
  
compare() takes a function parameter and returns a callable comparator when compared to a value. When called, the comparator returns result of comparing the result of calling the function and the value it was created with.

Basic usage:

    items = [1, 2, 3, 4, 5]

    def double(x):
        return x * 2

    for i in filter(compare(double) > 5, items):
        print i #Prints 3, 4 and 5