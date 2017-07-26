## Create a unique CVS/RCS/SCCS keyword line  
Originally published: 2001-03-12 13:52:48  
Last updated: 2001-03-12 13:52:48  
Author: Ken Goldstein  
  
Unlike interpreted languages such as Perl and Python,\nthe keyword line must NOT be commented out in .c or .h files.\nThe keyword string is defined as a static char so that it\nremains unchanged in the compiled executable.\nThis program will display a complete keyword line\nwhere the number after CVSid is always unique.\nYou can then cut and paste the line into\nyour .c or .h file. The diplayed line will look like:\nstatic char *CVSid432422157="@(#) $Header$ ";