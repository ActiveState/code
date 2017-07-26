## Observer Pattern  
Originally published: 2013-03-07 11:32:07  
Last updated: 2013-03-09 10:03:10  
Author: Mauro B. Bianc  
  
This is a Python implementation of the observer pattern described by Gamma et. al.
It defines a one-to many dependency between objects so that when one object changes state,
 all its dependents (i.e. observers) are notified and updated automatically.

My adaptation gets rid of the need to use specific functions to set the data (and to call Notify)
and allows you to be notified for ANY attribute you set.
It is possible to specify a list of attributes which should not trigger a notification.
In case you need the opposite, it is very easy to invert the behavior of the code.

The example should output:
Creating data1 without notification for attrs name & surname  
Creating data2 without notification for attr age  
Setting data1.name=Heather - Notification unnecessary  
Setting data1.num=333 - Notification expected  
Observer1: Subject Heather has updated attr num to 333  
Setting data2.name=Molly - Notification expected  
Observer2: Subject Molly has updated attr name to Molly  
Setting data2.age=28 - Notification unnecessary  
Setting data2.eyecolor=blue - Notification expected  
Observer2: Subject Molly has updated attr eyecolor to blue  

