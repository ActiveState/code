## Python code minifier  
Originally published: 2009-03-31 14:20:30  
Last updated: 2014-05-25 16:23:55  
Author: Dan McDougall  
  
**Update 05/25/2014:** Pyminifier 2.0 has been released and now lives on Github: https://github.com/liftoff/pyminifier (docs are here: http://liftoff.github.io/pyminifier/).  The code below is very out-of-date but will be left alone for historical purposes.

Python Minifier:  Reduces the size of Python code for use on embedded platforms.  Performs the following:

1. Removes docstrings.
2. Removes comments.
3. Removes blank lines.
4. Minimizes code indentation.
5. Joins multiline pairs of parentheses, braces, and brackets (and removes extraneous whitespace within).
6. Preserves shebangs and encoding info (e.g. "# -*- coding: utf-8 -*-")
7. **NEW:** Optionally, produces a bzip2 or gzip-compressed self-extracting python script containing the minified source for ultimate minification.

**Update 09/23/2010:** Version 1.4.1:  Fixed an indentation bug when operators such as @ and open parens started a line.

**Update 09/18/2010:** Version 1.4:
* Added some command line options to save the result to an output file.
* Added the ability to save the result as a bzip2 or gzip-compressed self-extracting python script (which is kinda neat--try it!).
* Updated some of the docstrings to provide more examples of what each function does.

**Update 06/02/2010:** Version 1.3:  Rewrote several functions to use Python's built-in tokenizer module (which I just discovered despite being in Python since version 2.2).  This negated the requirement for pyparsing and improved performance by an order of magnitude.  It also fixed some pretty serious bugs with dedent() and reduce_operators().

PLEASE POST A COMMENT IF YOU ENCOUNTER A BUG!