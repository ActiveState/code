# Relativistic Rocket Kinematics
# FB - 20130609
import math
print "Coordinate Time passed (for observer) to reach given speed (velocity):"
print "v0 = 0"
g = float(raw_input("Constant Proper Acceleration in g: "))
a = g * 9.8 # meters / second ** 2
a = a / 3e8 # light-second / second ** 2
a = a * 3.15e7 # light-year / year ** 2
# a = float(raw_input("Constant Proper Acceleration: "))
v = float(raw_input("Speed in c: ")) 
tc = v / a / math.sqrt(1.0 - v * v)
print str(tc) + " years"
print
print "Proper Time passed for the traveller:"
print "v0 = 0"
# g = float(raw_input("Constant Proper Acceleration in g: "))
# a = g * 9.8 # meters / second ** 2
# a = a / 3e8 # light-second / second ** 2
# a = a * 3.15e7 # light-year / year ** 2
# a = float(raw_input("Constant Proper Acceleration: "))
# tc = float(raw_input("Coordinate Time passed for the observer in years: "))
tp = math.asinh(a * tc) / a
print str(tp) + " years"
##print
##print "Distance travelled at given time:"
##print "v0 = 0"
##a = float(raw_input("Constant Proper Acceleration: "))
##t = float(raw_input("Time: "))
##x = (math.sqrt(1.0 + a * a * t * t) - 1.0) / a
##print x
##print
##print "Coordinate Time passed for distant observer:"
##print "v0 = 0"
##a = float(raw_input("Constant Proper Acceleration: "))
##t = float(raw_input("Proper Time passed for the traveller: "))
##tc = math.sinh(a * t) / a
##print tc
##print
##print "Coordinate Time passed to reach given distance:"
##print "v0 = 0"
##a = float(raw_input("Constant Proper Acceleration: "))
##x = float(raw_input("Distance: "))
##tc = (math.sqrt(1.0 + a * a * x * x) - 1.0) / a
##print tc
##print
##print "Speed at given time:"
##print "v0 = 0"
##a = float(raw_input("Constant Proper Acceleration: "))
##t = float(raw_input("Time: ")) 
##v = a * t / math.sqrt(1.0 + a * a * t * t)
##print v
##print
##print "Speed at given time under constant force:"
##print "v0 = 0"
##f = float(raw_input("Force: "))
##m = float(raw_input("Mass: "))
##t = float(raw_input("Time: "))
##v1 = f * t / math.sqrt(m * m - (f * t / c) ** 2.0)
##v2 = f * t / m / math.sqrt(1.0 + (f / m / c) ** 2.0 * t * t) 
##print v1, v2
##print
##print "Distance travelled at given time under constant force:"
##print "v0 = 0"
##f = float(raw_input("Force: "))
##m = float(raw_input("Mass: "))
##t = float(raw_input("Time: "))
##x = c * (m * c / f) * (math.sqrt(1.0 + (f / m / c) ** 2.0 * t * t) - 1.0)
##print x
##print
##print "Acceleration at given time under constant force:"
##print "v0 = 0"
##f = float(raw_input("Force: "))
##m = float(raw_input("Mass: "))
##t = float(raw_input("Time: "))
##a = f / m / math.sqrt(1.0 + (f / m / c) ** 2.0 * t * t) ** 3.0
##print a
##print
##print "Time it takes to reach given speed (velocity) under constant force:"
##print "v0 = 0"
##f = float(raw_input("Force: "))
##m = float(raw_input("Mass: "))
##v = float(raw_input("Speed: ")) 
##t = math.sqrt(v * v * m * m * c * c / (f * f * (c * c - v * v)))
##print t
##print
##print "Time to travel given distance under constant force:"
##print "v0 = 0"
##f = float(raw_input("Force: "))
##m = float(raw_input("Mass: "))
##x = float(raw_input("Distance: ")) 
##t = math.sqrt(((x * f / m + 1.0) ** 2.0 - 1.0) * m * m * c * c / f * f )
##print t
