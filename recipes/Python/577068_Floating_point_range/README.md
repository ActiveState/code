## Floating point range  
Originally published: 2010-02-24 07:12:53  
Last updated: 2010-02-24 07:12:55  
Author: Steven D'Aprano  
  
Generator that produces floats, equivalent to range for integers, minimising rounding errors by using only a single multiplication and addition for each number, and no divisions.

This generator takes an optional argument controlling whether it produces numbers from the open, closed, or half-open interval.