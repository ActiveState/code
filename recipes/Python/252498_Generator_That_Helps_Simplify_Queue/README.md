## A Generator That Helps Simplify Queue Consumers  
Originally published: 2003-12-04 17:29:35  
Last updated: 2003-12-04 17:29:35  
Author: Jimmy Retzlaff  
  
My Queue usage typically involves a producer thread and a consumer thread. The producer calls queue.put(value) until it's done at which point it calls queue.put(sentinel). My consumers almost always look like this:

while True:
&nbsp;&nbsp;&nbsp;&nbsp;value = queue.get()
&nbsp;&nbsp;&nbsp;&nbsp;if value != sentinel:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# do something with value
&nbsp;&nbsp;&nbsp;&nbsp;else:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;break

That logic can be abstracted away into a generator function that allows consumer code to look like this instead:

for value in iterQueue(queue, sentinel):
&nbsp;&nbsp;&nbsp;&nbsp;# do something with value