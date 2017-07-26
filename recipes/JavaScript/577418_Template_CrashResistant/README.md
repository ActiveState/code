## A Template for Crash-Resistant Toggle-Macros  
Originally published: 2010-10-07 00:51:41  
Last updated: 2010-10-07 00:51:42  
Author: Eric Promislow  
  
If you've followed my postings here lately (http://code.activestate.com/recipes/users/4166930/), you'll see that I've been playing with what I call "toggle macros", macros that toggle a state on and off, with different behaviors for each state.  Unfortunately I found that it was easy to get Komodo to crash on shutdown.  Meanwhile I wanted to build a framework to make it easier to build these.

This recipe accomplishes both. It looks like putting a listener on a view object can trigger this crash, but so can storing a method on a view object, even with a unique name.
So while I wanted to use the "view.view_closing" event, I can't, and I notice no other core Komodo code is. The template instead uses a global hash, ko.extensions.togglers,
to store the code objects. And now I'm not getting a crash.