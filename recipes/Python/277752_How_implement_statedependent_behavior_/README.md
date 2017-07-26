## How to implement state-dependent behavior - State-Pattern  
Originally published: 2004-04-12 04:43:05  
Last updated: 2004-04-12 12:58:10  
Author: Elmar Bschorer  
  
An object in a program frequently has an internal "state", and the behavior of the object needs to change when its state changes.\nAs someone who tends to think of objects as "data structures on steroids", it came as quite a shock when Netscape's Steve Abell pointed out that an object need not contain any values at all -- it can exist merely to provide behaviors, in the form of methods.\nThis recipe demonstrates a networkcard that depends on its internal state connected/disconnected - to send/receive data.