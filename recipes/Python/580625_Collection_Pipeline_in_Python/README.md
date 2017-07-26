## Collection Pipeline in Python  
Originally published: 2016-03-16 14:45:01  
Last updated: 2016-03-16 14:45:02  
Author: Steven D'Aprano  
  
A powerful functional programming technique is the use of pipelines of functions. If you have used shell scripting languages like `bash`, you will have used this technique. For instance, to count the number of files or directories, you might say: `ls | wc -l`. The output of the first command is piped into the input of the second, and the result returned.

We can set up a similar pipeline using Lisp-like Map, Filter and Reduce special functions. Unlike the standard Python `map`, `filter` and `reduce`, these are designed to operate in a pipeline, using the same `|` syntax used by bash and other shell scripting languages:

>>> data = range(1000)
>>> data | Filter(lambda n: 20 < n < 30) | Map(float) | List
[21.0, 22.0, 23.0, 24.0, 25.0, 26.0, 27.0, 28.0, 29.0]


The standard Python functional tools is much less attractive, as you have to write the functions in the opposite order to how they are applied to the data. This makes it harder to follow the logic of the expression.

>>> list(map(float, filter(lambda n: 20 < n < 30, data)))
[21.0, 22.0, 23.0, 24.0, 25.0, 26.0, 27.0, 28.0, 29.0]


We can also end the pipeline with a call to `Reduce` to collate the sequence into a single value. Here we take a string, extract all the digits, convert to ints, and multiply:

>>> from operator import mul
>>> "abcd12345xyz" | Filter(str.isdigit) | Map(int) | Reduce(mul)
120

