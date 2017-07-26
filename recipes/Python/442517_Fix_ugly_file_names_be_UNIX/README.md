## Fix ugly file names to be UNIX shell-friendly.  
Originally published: 2005-11-02 07:30:53  
Last updated: 2005-11-02 07:30:53  
Author: Micah Elliott  
  
You have files named with funky characters lying around in your
filesystem.  Ugly files like "My Document #3 - (2005)[1].txt" are
common when you're sharing directories with Windows users, but you
would like to have them renamed to something like
"my_document_3_-_2005-1-.txt" so that your shell and other unix
utilities won't have to deal with special characters.