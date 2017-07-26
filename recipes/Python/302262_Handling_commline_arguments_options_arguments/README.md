## Handling of command line arguments: options, arguments, file(s) content iterator  
Originally published: 2004-08-27 08:46:10  
Last updated: 2004-08-28 21:02:14  
Author: Peter Kleiweg  
  
Handles arguments for small scripts that need to:
- read some command line options
- read some command line positional arguments
- iterate over all lines of some files given on the command line, or stdin if none given
- give usage message if positional arguments are missing
- give usage message if input files are missing and stdin is not redirected