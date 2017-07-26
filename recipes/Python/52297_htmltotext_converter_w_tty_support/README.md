## htmltotext converter w/ tty support for bold/underline  
Originally published: 2001-03-22 15:13:10  
Last updated: 2004-01-30 16:44:42  
Author: Brent Burley  
  
This is a complete program that reads an html doc and converts it to
plain ASCII text.  In the spirit of minimalism, this operates as a
standard unix filter.
E.g. htmltotext < foo.html > foo.txt

If the output is going to a terminal, then bold and underline are
displayed on the terminal.  Italics in HTML are mapped to underlining
on the tty.  Underlining in HTML is ignored (mostly due to laziness).