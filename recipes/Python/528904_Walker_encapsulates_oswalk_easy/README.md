## Walker encapsulates os.walk for easy reuse  
Originally published: 2007-08-28 15:50:15  
Last updated: 2007-08-29 15:07:29  
Author: Jack Trainor  
  
Walker encapsulates os.walk's directory traversal as an object with the added features of excluded directories and a hook for calling an outside function to act on each file.\n\nWalker can easily be subclassed for more functionality, as with ReWalker which filters filenames in traversal by a regular expression.