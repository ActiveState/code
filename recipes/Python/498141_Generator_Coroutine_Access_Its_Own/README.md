## Generator Coroutine Access to Its Own Handle

Originally published: 2006-09-27 07:32:12
Last updated: 2006-09-27 07:32:12
Author: Doug Fort

I really like the Python 2.5 generator extensions. I have cases where I want a generator to pass a reference to itself to another generator, or to store it in a queue etc. Here's how a generator can get its own handle.