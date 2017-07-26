## simple, cooperative multitasking using generators  
Originally published: 2006-01-05 12:44:52  
Last updated: 2006-01-16 12:18:27  
Author: Maciej Obarski  
  
Cooperative multitasking offers an alternative to using threads. It can be harder to use in some cases (blocking IO) but in other it can be much easier (sharing data between tasks). This recipe shows how to use generators to achieve simple, cooperative multitasking, that allows thousends of 'simultaneously' running tasks.