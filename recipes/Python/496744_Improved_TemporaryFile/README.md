## Improved TemporaryFile  
Originally published: 2006-05-28 02:52:01  
Last updated: 2006-09-29 08:20:47  
Author: Andy Chambers  
  
From PEP 42...

I wonder if it would be a good idea to have a new kind of
temporary file that stored data in memory unless:

        - The data exceeds some size, or

        - Somebody asks for a fileno.

Then the cgi module (and other apps) could use this thing in a
uniform way.