## Python Vectors  
Originally published: 2009-09-22 12:45:11  
Last updated: 2009-11-25 04:50:10  
Author: Stephen Chappell  
  
This recipe implements vectors in pure Python and does not use "C" for speed enhancements. As a result, much effort has gone towards optimizing the instructions for the class methods. There are a few things that have yet to be improved, but it is being posted as an RFC. Comments on the structure, method names, and coding technique are requested for change. Once this code is standardized, work may commence on writing Vector3, Vector4, and VectorX. Please note that there is a difference between the "direction" and "degrees" properties.