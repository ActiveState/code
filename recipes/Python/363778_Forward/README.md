## Forward  
Originally published: 2005-01-19 10:20:35  
Last updated: 2005-01-19 10:20:35  
Author: Shannon -jj Behrens  
  
Calling the "forward" method transfers processing to a new screen.
It never returns.  This code is taken from multiple places, so I haven't
bothered to keep the classes intact, I've just taken the meat.  More generally,
this is an example of state machine with a main loop.  At any point, you can
say, "I'm ready to change state.  Do it.  Go back to the loop.  Don't
return--just throw away my current stack."