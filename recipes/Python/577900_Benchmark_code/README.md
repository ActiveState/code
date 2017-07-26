## Benchmark code with the with statement  
Originally published: 2011-10-10 04:30:11  
Last updated: 2011-10-10 04:30:11  
Author: vleon   
  
Inspired by [this post](http://preshing.com/20110924/timing-your-code-using-pythons-with-statement) I wrote this context manager to benchmark code blocks or function calls.

Usage is incredibly simple:

    with Timer():
        ...  # code to benchmark goes here


The time taken (in seconds) will be printed when the code block completes. To capture the time taken programmatically is almost as easy:

    t = Timer()
    with t:
        ...  # code to benchmark goes here
    time_taken = t.interval


Due to the difficulties of timing small snippets of code *accurately*, you should only use this for timing code blocks or function calls which take a significant amount of time to process. For micro-benchmarks, you should use the `timeit` module.
