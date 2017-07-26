## A simple text file pager in Python  
Originally published: 2017-02-10 21:34:44  
Last updated: 2017-02-10 21:34:45  
Author: Vasudev Ram  
  
This recipe shows how to create a simple text file pager in Python. It allows you to view text content a page at a time (with a user-definable number of lines per page). Like standard Unix utilities, it can either take a text file name as a command-line argument, or can read the text from its standard input, which can be redirected to come from a file, or to come from a pipe. The recipe is for Windows only, though, since it uses the msvcrt.getch() function, which is Windows-specific. However, the recipe can be modified to work on Unix by using things like tty, curses, termios, cbreak, etc.

More details here:

https://jugad2.blogspot.in/2017/02/tp-simple-text-pager-in-python.html
