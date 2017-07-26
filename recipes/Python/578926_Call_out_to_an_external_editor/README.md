## Call out to an external editor  
Originally published: 2014-09-01 16:02:42  
Last updated: 2014-09-01 18:26:51  
Author: Steven D'Aprano  
  
Here's a function that lets you use Python to wrap calls to an external editor. The editor can be an command line editor, like venerable old "ed", or something more powerful like nano, vim or emacs, and even GUI editors. After the editor quits, the text you typed in the editor is returned by the function.

A simple example, using the (rather cryptic) 'ed' editor on Linux. For the benefit of those unfamiliar with 'ed', I have annotated the editor session with comments.

    >>> status, text = edit('ed')
    0                        ## ed prints the initial number of lines
    a                        ## start "append" mode
    Hello World!
    Goodbye now
    .                        ## stop appending
    w                        ## write the file to disk
    25                       ## ed prints the number of bytes written
    q                        ## quit ed and return to Python
    >>> status
    0
    >>> print text
    Hello World!
    Goodbye now

