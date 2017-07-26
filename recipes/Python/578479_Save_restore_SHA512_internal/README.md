## Save and restore SHA-512 internal state  
Originally published: 2013-03-03 18:05:41  
Last updated: 2013-03-03 18:05:42  
Author: Dima Tisnek  
  
If you have a very long input to hash, you may want to save your progress.

CPython doesn't normally let you, but it's easy to hack around via ctypes