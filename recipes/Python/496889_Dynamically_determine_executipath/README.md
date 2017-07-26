## Dynamically determine execution path of a file

Originally published: 2006-07-14 16:20:17
Last updated: 2006-07-14 16:20:17
Author: adam smith

I ran into a dilemma when writing a PyUnit test case that read in sample data from a text file in the same package as the test. How I could successfully reference the relative location of the file changed depending on how I executed the code. So for example, when I ran the unit test in isolation, it passed, but when I ran the test as part of a suite, it failed, because the code was being executed from a different location. I needed to find a way to determine the relative location of the file at run-time no matter how it was executed.