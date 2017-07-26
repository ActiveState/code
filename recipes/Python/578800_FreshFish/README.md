## FreshFish  
Originally published: 2013-12-29 15:34:24  
Last updated: 2013-12-29 15:38:33  
Author: Justin Shaw  
  
FreshFish is a function decorator for functions with no arguments (hardware query).\n\nThe first time the function is called, the wrapper caches the result (the fish).  Subsequent calls to the wrapped function simply return the cached result as long as the fish is still fresh.  When the fish goes stale, FreshFish calls the underlying function again for FreshFish.\n\nI used this on a BeagleBone project to monitor heart rate, speed, and cadence.\n  