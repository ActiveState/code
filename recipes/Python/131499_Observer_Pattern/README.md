## Observer Pattern  
Originally published: 2002-06-05 08:47:40  
Last updated: 2003-01-13 09:38:15  
Author: Jørgen Cederberg  
  
This is a Python implementation of the observer pattern described by Gamma et. al. It defines a one-to many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically.

The example should output:
Setting Data 1 = 10
DecimalViewer: Subject Data 1 has data 10
HexViewer: Subject Data 1 has data 0xa
Setting Data 2 = 15
HexViewer: Subject Data 2 has data 0xf
DecimalViewer: Subject Data 2 has data 15
Setting Data 1 = 3
DecimalViewer: Subject Data 1 has data 3
HexViewer: Subject Data 1 has data 0x3
Setting Data 2 = 5
HexViewer: Subject Data 2 has data 0x5
DecimalViewer: Subject Data 2 has data 5
Detach HexViewer from data1 and data2.
Setting Data 1 = 10
DecimalViewer: Subject Data 1 has data 10
Setting Data 2 = 15
DecimalViewer: Subject Data 2 has data 15