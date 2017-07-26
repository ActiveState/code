## lreplace() and rreplace(): Replace the beginning and ends of a strings  
Originally published: 2010-06-04 02:16:41  
Last updated: 2010-06-04 02:18:48  
Author: Dan McDougall  
  
Python newbies will often make the following mistake (I certainly have =):

    >>> test = """this is a test:
    ... tis the season for mistakes."""
    >>> for line in test.split('\n'):
    ...     print line.lstrip('this')
    ... 
     is a test
     the season for mistakes.

The mistake is assuming that lstrip() (or rstrip()) strips a string (whole) when it actually strips all of the provided characters in the given string.  Python actually comes with no function to strip a string from the left-hand or right-hand side of a string so I wrote this (very simple) recipe to solve that problem.  Here's the usage:

    >>> test = """this is a test:
    ... tis the season for mistakes."""
    >>> for line in test.split('\n'):
    ...     print lreplace('this', '', line)
    ... 
     is a test
    tis the season for mistakes.

I really wish Python had these functions built into the string object.  I think it would be a useful addition to the standard library.  It would also be nicer to type this:

    line.lreplace('this', '')

Instead of this:

    lreplace('this','',line)