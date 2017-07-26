## XML Lexing ("shallow parsing") 
Originally published: 2001-06-12 15:00:49 
Last updated: 2001-06-13 21:24:21 
Author: Paul Prescod 
 
Sometimes you want to work more with the form of an XML document than with the structural information it contains. For instance if you wanted to change a bunch of entity references or element names. Also, sometimes you have slightly incorrect XML that a traditional parser will choke on. In that case you want an XML lexer or "shallow parser". This is a Python implementation.