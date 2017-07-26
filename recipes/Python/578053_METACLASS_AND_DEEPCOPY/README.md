## METACLASS AND DEEPCOPY  
Originally published: 2012-02-26 15:43:00  
Last updated: 2012-02-26 15:43:01  
Author: thonpy   
  
I would like to solve this excercise:
Traditionally object-oriented programming provides two different modes for cloning an instance or a structured data type: shallow and deep copy. The former has the effect to clone exclusively the external shell and not its content originating a quite fastidious aliasing effect. The latter, instead, copies the shell and its content recursively creating two completely separate copies of the instance.

As you know, Python's programs suffer of the aliasing effect when you copy an instance of a class or a structured type (e.g., a list) with the = operator. As showed in the following example:


l=[0,1,2]
mylist=l
mylist[2] = ’B’
mylist
[1, 2, ’B’]
l
[1, 2, ’B’


The exercise consists of defining a meta-class which implements the deep copy on the assignment operator and binding this to the standard class list. Such that the following behavior can be yielded