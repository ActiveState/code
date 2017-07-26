## Make the New Class Available During the Execution of its Body 
Originally published: 2011-06-10 04:25:04 
Last updated: 2011-08-12 23:44:46 
Author: Eric Snow 
 
When a class object is created, normally the class body is exec'ed first and then the class object is generated with that resulting namespace.  \n\nThis recipe lets you flip that around, and then make the class object available to the class body during execution. 