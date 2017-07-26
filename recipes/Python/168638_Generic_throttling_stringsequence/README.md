## Generic throttling for string/sequence functions  
Originally published: 2002-12-11 12:34:55  
Last updated: 2002-12-11 12:34:55  
Author: Anon User  
  
This call wrapper class enables throttling of function calls. You can control how many characters (or sequence elements) per second your function processes (with granularity of one sequence). The calls are asynchronous and the actual function call is done when the last operation has lasted/waited long enough to satisfy the characters/second limit.