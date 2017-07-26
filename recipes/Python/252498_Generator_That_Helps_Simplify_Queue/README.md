## A Generator That Helps Simplify Queue Consumers 
Originally published: 2003-12-04 17:29:35 
Last updated: 2003-12-04 17:29:35 
Author: Jimmy Retzlaff 
 
My Queue usage typically involves a producer thread and a consumer thread. The producer calls queue.put(value) until it's done at which point it calls queue.put(sentinel). My consumers almost always look like this:\n\nwhile True:\n&nbsp;&nbsp;&nbsp;&nbsp;value = queue.get()\n&nbsp;&nbsp;&nbsp;&nbsp;if value != sentinel:\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# do something with value\n&nbsp;&nbsp;&nbsp;&nbsp;else:\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;break\n\nThat logic can be abstracted away into a generator function that allows consumer code to look like this instead:\n\nfor value in iterQueue(queue, sentinel):\n&nbsp;&nbsp;&nbsp;&nbsp;# do something with value