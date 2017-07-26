## Assertion that all base class initializers get called (metaclass solution)  
Originally published: 2003-09-26 02:54:29  
Last updated: 2003-09-29 19:46:17  
Author: Hannu Kankaanpää  
  
This code can be used in debugging phase to notice errors sooner. It is usually always desirable to visit all base class __init__-methods, but Python does nothing to ensure they will be visited. Set AssertInit as a metaclass in the base class of your class hierarchy, and all errors from not calling base class __init__s will be cleanly reported as AssertionErrors.

The solution should work properly with multiple inheritance and diamond-shaped inheritance graphs (see the example at the bottom of code).

It slows down object creation by a large amount (I'd assume but didn't do any tests).