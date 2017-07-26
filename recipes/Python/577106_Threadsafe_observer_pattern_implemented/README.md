## Threadsafe observer pattern implemented as descriptorOriginally published: 2010-03-13 12:17:10 
Last updated: 2010-03-13 12:17:11 
Author: Rodney Drenth 
 
This is a threadsafe version of recipe 576979. A publish-subscribe (observer) pattern is implemented as a descriptor.  Assigning a value notifies the observers.\nUses recipe 577105 as synchlock.py and recipe 576979 as Observer.py