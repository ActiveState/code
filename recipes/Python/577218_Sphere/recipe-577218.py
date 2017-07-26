#On the name of ALLAH and may the blessing and peace of Allah 
#be upon the Messenger of Allah Mohamed Salla Allahu Aliahi Wassalam.
#Author : Fouad Teniou
#Date : 06/05/10
#version :2.6

"""
Sphere class represents a geometric sphere and a completing_the_squares
function is used for the purpose, while an utility _checksign function
is used to check the sign of all the coefficients and return an empty string 
for a positive number and a minus character for a negative number.
A string representation function for the three different outcome
possibilities is used to print the solution of the sphere equation.
"""

from math import sqrt
class Sphere(object):
    """
    class that represents a geometric Sphere
    """
    def __init__(self,coef_A = 0,coef_B = 0, coef_C = 0, coef_D= 0, coef_E = 0, coef_F = 0, coef_G = 0):
        """ Sphere Construction takes coef_A,coef_B,coef_C,coef_D,coef_E,coef_F,coef_G constants """
        
        self._A = coef_A
        self._B = coef_B
        self._C = coef_C
        self._D = coef_D
        self._E = coef_E
        self._F = coef_F
        self._G = coef_G

        self._a = self._checkSign(self._D)
        self._b = self._checkSign(self._E)
        self._c = self._checkSign(self._F)
        
        self._d = pow((self._D/2.0)/self._A,2)
        self._e = pow((self._E/2.0)/self._B,2)
        self._f = pow((self._F/2.0)/self._C,2)
        
        self._g = chr(253)
       
        self._h = (-self._G/self._A + self._d + self._e + self._f)
        
    def _checkSign(self,value):
        """ Utility method to check the values' sign
        and return a sign string"""
        
        if value >= 0:
            return "+"
        else :
            return ""
        
    def completing_the_squares(self):
        """
        completing the squares function 
        """
        
        c_squares = "(x%s %s%sx + %s) + (y%s %s%sy + %s) + (z%s %s%sz + %s) = %s" % \
        (self._g,self._a,self._D/self._A,self._d,
        self._g,self._b,self._E/self._B,self._e,
        self._g,self._c,self._F/self._C,self._f,self._h)
        
        return c_squares
    
    def __str__(self):
        """
        String representation of a sphere
        """
        print ("\n(x%s%s)%s + (y%s%s)%s + (z%s%s)%s = %s") % \
               (self._a,(self._D/2.0)/self._A,self._g,self._b,(self._E/2.0)/self._B,
                self._g,self._c,(self._F/2.0)/self._C,self._g,self._h)
        if self._h > 0:
                return "\n<The graph of this equation is a sphere with centre (%s,%s,%s) and radius %s\n" % \
                       (-1*self._D/2.0,-1*self._E/2.0,-1*self._F/2.0,"%2.3f" % (sqrt(self._h)))
        elif self._h == 0:
            return "\n<this sphere has radius = 0 and the graph is a single point(%s,%s,%s)\n " % \
                       (-1*self._D/2.0,-1*self._E/2.0,-1*self._F/2.0,float(m.sqrt(self._h)))
        else :
            return "\n<There is no graph for such equation "
        
if __name__ == "__main__":
    
    sphere = Sphere(1,1,1,-2,-4,8,17)
    print sphere.completing_the_squares()
    print sphere
    sphere1 = Sphere(1,1,1,10,4,2,-19)
    print sphere1.completing_the_squares()
    print sphere1
    sphere2 = Sphere(2,2,2,-2,-3,5,-2)
    print sphere2.completing_the_squares()
    print sphere2
####C:\Windows\python "C:\Users\MyComputer\Documents\Pyt\Sphere7.py"

#(x² -2x + 1.0) + (y² -4y + 4.0) + (z² +8z + 16.0) = 4.0

#(x-1.0)² + (y-2.0)² + (z+4.0)² = 4.0

#<The graph of this equation is a sphere with centre (1.0,2.0,-4.0) #and radius 2.000

#(x² +10x + 25.0) + (y² +4y + 4.0) + (z² +2z + 1.0) = 49.0

#(x+5.0)² + (y+2.0)² + (z+1.0)² = 49.0

#<The graph of this equation is a sphere with centre (-5.0,-2.0,-1.0) #and radius 7.000

#(x² -1x + 0.25) + (y² -2y + 0.5625) + (z² +2z + 1.5625) = 3.375

#(x-0.5)² + (y-0.75)² + (z+1.25)² = 3.375

#<The graph of this equation is a sphere with centre (1.0,1.5,-2.5) #and radius 1.837
#################################################################
