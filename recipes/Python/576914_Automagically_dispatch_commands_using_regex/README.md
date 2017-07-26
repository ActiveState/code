## Automagically dispatch commands using regex token classes 
Originally published: 2009-09-28 03:45:35 
Last updated: 2009-09-28 03:46:29 
Author: Mick Krippendorf 
 
The *(?P<...>...)* notation in Python's regular expressions can be viewed as a classification of matched tokens. The names of these classes can be used to dispatch tokens to appropriate handlers: