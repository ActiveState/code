## pending/blocking a signal  
Originally published: 2009-05-25 22:42:30  
Last updated: 2009-05-25 22:42:30  
Author: J Y  
  
http://www-h.eng.cam.ac.uk/help/tpl/unix/signals.html

do you want certain signals to be ignored or blocked? The sigaction(), sigprocmask(), siginterrupt(), and sigsuspend() functions control the manipulation of the signal mask, which defines the set of signals currently blocked. The manual pages give details. The following code shows how the response to signals can be delayed. 