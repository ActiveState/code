## Bounded Buffer Example (1)  
Originally published: 2006-03-29 09:59:42  
Last updated: 2006-03-29 09:59:42  
Author: Stephen Chappell  
  
The following recipe shows an example of the bounded buffer problem
and its solution. Fortunately in Python, this is very easily solved
with the Queue class from the Queue module. Even creating a buffer
with a maximum size limit becomes rather easy with the automatic
blocking feature (when trying to put when the Queue is full or when
trying to get when the Queue is empty). Overall, this is just a
simple example and approach to a classic problem.