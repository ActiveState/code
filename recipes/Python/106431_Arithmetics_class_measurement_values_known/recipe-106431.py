# measurement.py
#
# An arithmetics class for measurement values of known percentual error
# This class uses the error propagation formulae of physicists
# --------------------------
# arithmetics uses number tupels consisting of
# measurement value val and error perc (in percent)
# uses operator overloading of '+','-','*','/'
# use '/' only if val != 0 (division by 0 problem)
# --------------------------
# version 2001-12-19 by Mario Hilgemeier <hilgemeier@gmx.de>
# I'd like to hear of modifications or extensions, e.g.
# addition of other error types (absolute, last digit +-1, 
# last digit +-0.5 i.e. digit after last digit +-5)

import math

class Measurement:
  "arithmetics for measurement values with errors"
  
  def __init__(self,val,perc):
    self.val = val
    self.perc = perc
    self.abs = self.val * self.perc / 100.0 # absolute error

  def __repr__(self):
    return "Measurement(%s,%s)" % (self.val, self.perc)  
  
  def __str__(self):
    return "(%g,%g)" % (self.val, self.perc)  
  
  # Addition
  def __add__(self, other):
    result = self.val + other.val
    new_perc = 100.0 * (math.sqrt(self.abs*self.abs + other.abs*other.abs) / result)
    return Measurement(result, new_perc)

  # Subtraction
  def __sub__(self, other):
    result = self.val - other.val
    new_perc = 100.0 * (math.sqrt(self.abs*self.abs + other.abs*other.abs) / result)
    return Measurement(result, new_perc)

  # Multiplication
  def __mul__(self, other):
    result = self.val * other.val
    new_perc = math.sqrt(self.perc*self.perc + other.perc*other.perc)
    return Measurement(result, new_perc)

  # Division (incorrect, if 0 in divisor Measurement)
  def __div__(self, other):
    result = 1.0*self.val/other.val
    new_perc = math.sqrt(self.perc*self.perc + other.perc*other.perc)
    return Measurement(result, new_perc)


--------------------------------------


exemplary use:

execfile("measurement.py")

m1 = Measurement(100.0, 5.5) # i.e. a measured value of 100.0 with 5.5% error
m2 = Measurement(50, 2)
print "m1 = ", m1
print "m2 = ", m2
print "m1 + m2 = ", m1 + m2
print "m1 - m2 = ", m1 - m2
print "m1 * m2 = ", m1 * m2
print "m1 / m2 = ", m1 / m2
print "(m1+m2) * (m1-m2) = ", (m1+m2) * (m1-m2)
print "(m1-m2) / (m1+m2) = ", (m1-m2) / (m1+m2)

# results:
# m1 =  (100,5.5)
# m2 =  (50,2)
# m1 + m2 =  (150,3.72678)
# m1 - m2 =  (50,11.1803)
# m1 * m2 =  (5000,5.85235)
# m1 / m2 =  (2,5.85235)
# (m1+m2) * (m1-m2) =  (7500,11.7851)
# (m1-m2) / (m1+m2) =  (0.333333,11.7851)
