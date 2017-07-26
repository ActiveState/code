## Numerical type with units (dimensions.py)  
Originally published: 2010-07-24 17:19:27  
Last updated: 2010-07-24 17:24:13  
Author: David Klaffenbach  
  
I implemented dimensions.py perhaps eight years ago as an exercise and have used it occasionally ever since.

It allows doing math with dimensioned values in order to automate unit conversions (you can add m/s to mile/hour) and dimensional checking (you can't add m/s to mile/lightyear).  It specifically does not convert 212F to 100C but rather will convert 9F to 5C (valid when converting temperature differences).

It is similar to unums (http://home.scarlet.be/be052320/Unum.html) but with a significant difference:
  
I used a different syntax Q(25,'m/s') as opposed to 100*m/s (I recall not wanting to have all the base SI units directly in the namespace).  I'm not entirely sure which approach is really better.

I also had a specific need to have fractional exponents on units, allowing the following:
>>> km=Q(10,'N*m/W^(1/2)')
>>> km
Q(10.0, 'kg**0.5*m/s**0.5')

Looking back I see a few design decisions I might do differently today, but I'll share it anyway.

Some examples are in the source below the line with if __name__ == "__main__":

Note that I've put two files into the code block below, dimensions.py and dimensions.data, so please cut them apart if you want to try it.