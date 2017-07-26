## Stateful Objects use Mix-ins to define behaviour  
Originally published: 2002-11-02 06:41:05  
Last updated: 2002-11-02 06:41:05  
Author: Dave Haynes  
  
You want to implement stateful objects, which have a different
set of behaviours according to what state they are in.

This requirement can be achieved with the use of mix-ins. A mix-in
is a class which is dynamically inherited by an object. The methods
of the mix-in class are thus accessible through the object. This is a
clean way of providing objects with standard interfaces.

Chuck Esterbrook has written a discussion of mix-ins, and their
implementation in Python, which can be found here:
http://www.linuxjournal.com/article.php?sid=4540

The recipe draws from the famous "Lumberjack Song". If you're not
familiar with it, all you need to know is that the passage of time
modifies the Lumberjack's behaviour.