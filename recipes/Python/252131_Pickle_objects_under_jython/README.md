## Pickle objects under jython  
Originally published: 2003-11-17 06:11:21  
Last updated: 2003-11-17 06:11:21  
Author: Ferdinand Jamitzky  
  
Using the pickle module under jython is a rather slow method for storing data. Using the ObjectOutputStream speeds it up. You can save and restore objects (jython and java) with these functions.