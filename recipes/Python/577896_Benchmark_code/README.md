## Benchmark code with the with statement 
Originally published: 2011-10-08 09:53:05 
Last updated: 2011-10-08 09:53:06 
Author: Steven D'Aprano 
 
Inspired by [this post](http://preshing.com/20110924/timing-your-code-using-pythons-with-statement) I wrote this context manager to benchmark code blocks or function calls.\n\nUsage is incredibly simple:\n\n    with Timer():\n        ...  # code to benchmark goes here\n\n\nThe time taken (in seconds) will be printed when the code block completes. To capture the time taken programmatically is almost as easy:\n\n    t = Timer()\n    with t:\n        ...  # code to benchmark goes here\n    time_taken = t.interval\n\n\nDue to the difficulties of timing small snippets of code *accurately*, you should only use this for timing code blocks or function calls which take a significant amount of time to process. For micro-benchmarks, you should use the `timeit` module.\n