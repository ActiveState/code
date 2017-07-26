## Real Mixins 
Originally published: 2006-09-22 08:00:17 
Last updated: 2006-09-22 14:58:53 
Author: tomer filiba 
 
This code here creates real mixed-in classes: it actually merges one class into another (c-python specific), taking care of name-mangling, some complications with __slots__, and everything else. As a side-effect, you can also use it to mix modules into classes. Similar to ruby's include statement.