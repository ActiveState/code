## dynamically changing encoder (for json) with metaclass (class factory) Originally published: 2013-10-24 11:31:44 
Last updated: 2013-10-24 11:31:44 
Author: -  
 
The *json.dumps* need to be feed with some class (cls =someClass)  but what if we want to change the class dynamically?\nThis example can be done by declaring the *listOfClasses* in class level of course, but the idea is to be changeable. This can be done by the class factory function *encoderFacory*\n