## Compile-time regex's and pattern-based dispatching  
Originally published: 2001-10-18 15:05:18  
Last updated: 2001-10-31 23:11:35  
Author: Michael Robin  
  
Although python has no literal representation for compiled
regular expressions (which is good) you can compile them
at Python read/compile-time. You can also use regexs to
match strings and automatically call funtions with arguments
that are based on the groups of the matched strings.