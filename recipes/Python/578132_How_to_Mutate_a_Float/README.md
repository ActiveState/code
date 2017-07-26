## How to Mutate a Float 
Originally published: 2012-05-14 16:47:53 
Last updated: 2012-05-14 16:49:13 
Author: Stephen Chappell 
 
This is just an experiment to test my mental understanding of Python. It should not be used in any code as is violates the design principle that floats are to be immutable. The code also abuses `ctypes` and an understanding of how `floats` are currently arranged in memory. `set_float` is not guaranteed to work properly on any system, and may fail to work in the future if the data's arrangement changes.