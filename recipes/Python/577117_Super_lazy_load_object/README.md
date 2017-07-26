## Super lazy load object  
Originally published: 2010-03-16 05:00:31  
Last updated: 2010-03-16 05:02:12  
Author: Russell   
  
A really light implementation of lazy load technique, yet powerful and conveniet. 

Simply call this:

    var1 = superlazy('key', default_value)

Your var1 will be loaded in load_setting(key) when accessed first time.

That's it. No subclassing is needed, no declaration is needed. Value type is auto detected and handled gracefully. str, int, list, dict can all be lazily loaded from anywhere you want now.