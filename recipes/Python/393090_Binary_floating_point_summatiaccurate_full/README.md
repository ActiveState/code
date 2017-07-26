###Binary floating point summation accurate to full precision

Originally published: 2005-03-28 18:48:06
Last updated: 2009-03-28 23:32:08
Author: Raymond Hettinger

Completely eliminates rounding errors and loss of significance due to catastrophic cancellation during summation.  Achieves exactness by keeping full precision intermediate subtotals.  Offers three alternative approaches, each using a different technique to store exact subtotals.