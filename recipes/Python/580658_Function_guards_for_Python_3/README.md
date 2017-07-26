## Function guards for Python 3  
Originally published: 2016-05-01 13:08:56  
Last updated: 2016-05-01 13:11:05  
Author: Dmitry Dvoinikov  
  
This module implements a function guard - facility to redirect the the call to one of several function implementations at run time based on the actual call arguments.

Wrap each of the identically named functions in a @guard decorator and provide a _when parameter with a default value set to guarding expression.

See samples at the top of the module.