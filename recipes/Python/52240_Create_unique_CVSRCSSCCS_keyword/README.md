## Create a unique CVS/RCS/SCCS keyword line  
Originally published: 2001-03-12 13:52:48  
Last updated: 2001-03-12 13:52:48  
Author: Ken Goldstein  
  
Unlike interpreted languages such as Perl and Python,
the keyword line must NOT be commented out in .c or .h files.
The keyword string is defined as a static char so that it
remains unchanged in the compiled executable.
This program will display a complete keyword line
where the number after CVSid is always unique.
You can then cut and paste the line into
your .c or .h file. The diplayed line will look like:
static char *CVSid432422157="@(#) $Header$ ";