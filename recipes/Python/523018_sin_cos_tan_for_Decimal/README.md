## sin, cos, tan for DecimalOriginally published: 2007-07-04 14:18:54 
Last updated: 2007-07-05 19:49:49 
Author: Alain Mellan 
 
Implementation of sine, cosine, tangent functions for Decimal arithmetic, using Taylor series expansion. It uses simple numerator and denominator generators.\n\nThe nice part is, the code is independent from the Decimal library. Feed it a float, it works just the same as if you feed it a Decimal (apart from the precision :-)