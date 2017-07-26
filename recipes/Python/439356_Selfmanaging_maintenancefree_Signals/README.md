## Self-managing, maintenance-free Signals implementation  
Originally published: 2005-08-17 12:22:47  
Last updated: 2005-08-18 14:21:18  
Author: Patrick Chasco  
  
This is a signals implementation for python. It is similar to the pydispatch module. This implementation enables you to create Signals as members of classes, as globals, or as locals. You may connect any number of functions or class methods to any signal. Connections manage themselves with the weakref module. Signals may also have arguments as long as all connected functions are callable with the same arguments.