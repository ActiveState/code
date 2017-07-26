###Stateful Objects use Mix-ins to define behaviour

Originally published: 2002-11-02 06:41:05
Last updated: 2002-11-02 06:41:05
Author: Dave Haynes

You want to implement stateful objects, which have a different\nset of behaviours according to what state they are in.\n\nThis requirement can be achieved with the use of mix-ins. A mix-in\nis a class which is dynamically inherited by an object. The methods\nof the mix-in class are thus accessible through the object. This is a\nclean way of providing objects with standard interfaces.\n\nChuck Esterbrook has written a discussion of mix-ins, and their\nimplementation in Python, which can be found here:\nhttp://www.linuxjournal.com/article.php?sid=4540\n\nThe recipe draws from the famous "Lumberjack Song". If you're not\nfamiliar with it, all you need to know is that the passage of time\nmodifies the Lumberjack's behaviour.