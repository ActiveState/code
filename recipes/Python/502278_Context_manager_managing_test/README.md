## Context manager for managing a test file  
Originally published: 2007-03-05 17:53:14  
Last updated: 2007-03-05 17:53:14  
Author: Brett Cannon  
  
This recipe helps to manage a temporary file used in a test.  It returns an open file so as to write the test data, and upon exiting the 'with' statement, makes sure that the created file is deleted.