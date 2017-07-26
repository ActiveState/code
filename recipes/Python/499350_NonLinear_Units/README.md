## Non-Linear Units  
Originally published: 2007-01-02 20:50:18  
Last updated: 2007-01-05 04:29:20  
Author: Justin Shaw  
  
This is a simple way of expressing non-linear scales (such as decibels) in python.  In stead of:
gain = 10 ** (12/10.)

Use
gain = 12 * dB