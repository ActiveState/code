#On the name of ALLAH and may the blessing and peace of Allah 
#be upon the Messenger of Allah Mohamed Salla Allahu Aliahi Wassalam.
#Author :Fouad Teniou
#Date : 08/10/08
#Version : 2.4

""" Class of an equation of a circle of the form Ax^2 + Ay^2 + Dx + Ey + F = 0 (A !=0)
it represents a circle or a point or has no graph , depending of the radius value. And a class
of an equation for the circle of radius r and centred at point (x0,y0). """

import math

class Circle(object):
    """ Class that represent an equation of  a circle
    with A,D,E,F constants properties """

    def __init__(self, Avalue,Dvalue,Evalue,Fvalue):
        """ Circle construction takes A,D,E,F Constants """
		
	self.__A = float(Avalue)
	self.__D = float(Dvalue)
	self.__E = float(Evalue)
	self.__F = float(Fvalue)

	self._b = chr(253)
	self._a = self._checkSign(self.__A)
	self._d= self._checkSign(self.__D)
	self._e = self._checkSign(self.__E)
	self._f = self._checkSign(self.__F)
	self._g = ((self.__D/self.__A)/2)
	self._g1= self.__D/2
	self._h =((self.__E/self.__A)/2)
	self._h1 = self.__E/2
	self._i = self._checkSign(self._g)
	self._j = self._checkSign(self._h)
	self._k = (-self.__F/self.__A + self._g**2 +self._h**2)
	self._k1= (-self.__F + self._g1**2 +self._h1**2)
	self._l = "%2.2f" % math.sqrt(abs(self._k))
	self._l1 = "%2.2f" % math.sqrt(abs(self._k1))
	self._m = "(x%s%s)%s+(y%s%s)%s = %s" % \
			     (self._i,self._g,self._b,self._j,self._h,self._b,self._k)
	self._m1 = "(x%s%s)%s+(y%s%s)%s = %s" % \
			     (self._i,self._g1,self._b,self._j,self._h1,self._b,self._k1)
	self._n = "(%s,%s)" % (-self._g,-self._h)
	self._n1 = "(%s,%s)" % (-self._g1,-self._h1)
    def __str__(self):
	""" String representation of the circle equation,
	standard form , centre and radius """
		
        try:
	    math.sqrt(self._k)
	    #Circle raises zero degenerate case
	    assert math.sqrt(self._k) != 0,"The graph is the single point %s" % \
		   Circle.centre(self)
	    if self.__A == 0:
			
		return "\n<Equation of a circle : x%s + y%s %s %sx %s %sy %s %s = 0 \
			\n\n%s %35s %25s \n\n%s %22s %24s\n" %\
			(self._b,self._b,self._d,int(self.D),self._e, \
			int(self.E),self._f,int(self.F),
			'Standard form','Centre(x0,y0)','Radius r' \
			self._m1,Circle.centre(self),Circle.radius(self))
	    else:
		return "\n<Equation of a circle : %sx%s + %sy%s %s %sx %s %sy %s %s = 0 \
			\n\n%s %35s %25s \n\n%s %22s %24s\n" %\
			(int(self.A)self._b,int(self.A),self._b,self._d,int(self.D),self._e, \
			int(self.E),self._f,int(self.F),
			'Standard form', 'Centre(x0,y0)','Radius r' \
			self._m,Circle.centre(self),Circle.radius(self))

	#Circle raises Negative number degenerate case
        except ValueError:
		raise ValueError,\
			" r%s < 0 : Degenerate case has no graph" % self._b

    def getA(self):
	""" Get method for A attribute """

	if self.__A != 0:
	    return self.__A
	else:
	    raise ValueError,\
		  " A value should be different than zero "
	
    def setA(self,value):
	""" Set method for A attribute """

	self.__A = value

    def delA(self):
	""" Delete method for A attribute """

	del self.__A

    #Create A property
    A = property(getA,setA,delA,"A constant")
		
    def getD(self):
	""" Get method for D attribute """

	return self.__D
	
    def setD(self,value):
	""" Set method for D attribute """

	self.__D = value

    def delD(self):
	""" Delete method for D attribute """

	del self.__D

    #Create D property
    D = property(getD,setD,delD,"D constant")

    def getE(self):
	""" Get method for E attribute """

	return self.__E
	
    def setE(self,value):
	""" Set method for E attribute """

	self.__E = value

    def delE(self):
	""" Delete method for E attribute """

	del self.__E
	
    #Create E property
    E = property(getE,setE,delE,"E constant")

    def getF(self):
	""" Get method for F attribute """

	return self.__F
	
    def setF(self,value):
	""" Set method for F attribute """

	self.__F = value

    def delF(self):
	""" Delete method for F attribute """

	del self.__F
	
    #Create F property
    F = property(getF,setF,delF,"F constant")

    def _checkSign(self,value):
	""" Utility method to check the values’ signs and return a sign string """

	if value >= 0:
	    return "+"
	else:
	    return ""

    def radius(self):
	""" Compute radius of a circle """

	if self.__A == 1:
	    return self._l1
	else:
	    return self._l

    def centre(self):
	""" Compute centre(x0,y0) of a circle """

	if self.__A == 1:
	    return self._n1
	else:
	    return self._n

class Equation(Circle):
    """Class that represent a radius and the centre of a circle """

    def __init__(self,x,y,radius):
	"""Equation construction takes centre(xValue,yValue
	and radius"""

	self.__x = float(x)
	self.__y = float(y)
	self.__radius = float(radius)

	self._o = chr(253)
	self._p = self.__radius**2
	self._q = self._checkSign(-self.__x)
	self._r = self._checkSign(-self.__y)
	self._s = "(x%s%s)%s + (y%s%s)%s = %s " % \
		   (self._q,-self.__x,self._o,self._r,-self.__y,self._o,self._p)
	self._t = self.__x**2 + self.__y**2 -self._p
	self._u = self._checkSign(self._t)
	self._v = "x%s + y%s %s %sx %s %sy %s %s = 0 " % \
		  (self._o,self._o,self._q,-self.__x*2,self._r,-self.__y*2,self._u,self._t)

    def __str__(self):
	""" String representation of the circle equation, standard form ,centre and radius """

	#Equation raises radius value < 0
	assert self.__radius > 0, "<Radius value should be greater than zero"

	return ( "\n<Equation for the circle of radius (%s)\
		centred at (%s,%s) is : \n\n%s < -- > %s" ) % \
		(self.__radius,self.__x,self.__y,self._s,self._v)

if __name__ == "__main__":

    circle1 = Circle(16,40,16,-7)
    print circle1

    #Though students might use only values of radius and circle
    print radius.circle1()
    print centre.circle1()

    circle2 = Circle(2,24,0,-81)
    print circle2

    del circle2.A
	
    circle2.A = 1
    print circle2

    equation = Equation(2,5,3)
    print equation 
    
    for doc in (Circle.A,Circle.D,Circle.E,Circle.F):
        print doc.__doc__,doc.fget.func_name,doc.fset.func_name,doc.fdel.func_name

########################################################################################

#Version : Python 3.2


#import math

#class Circle(object):
#    """ Class that represent an equation of a circle
#    with A,D,E,F constants properties"""
#
#    def __init__(self,Avalue,Dvalue,Evalue,Fvalue):
#        """ Circle constructor takes A,D,F,E constants """
#        
#        self.__A = float(Avalue)
#        self.__D = float(Dvalue)
#        self.__E = float(Evalue)
#        self.__F = float(Fvalue)
#        
#        self._b = chr(178)
#        self._a = self._checkSign(self.__A)
#        self._d = self._checkSign(self.__D)
#        self._e = self._checkSign(self.__E)
#        self._f = self._checkSign(self.__F)
#        self._g = ((self.__D/self.__A)/2)
#        self._g1 = self.D/2
#        self._h = ((self.__E/self.__A)/2)
#        self._h1 = self.E/2
#        self._i = self._checkSign(self._g)
#        self._j = self._checkSign(self._h)
#        self._k = (-self.__F/self.__A +self._g**2 + self._h**2)
#        self._k1= (-self.__F +self._g1**2 + self._h1**2)
#        self._l = "%2.2f" % math.sqrt(abs(self._k))
#        self._l1= "%2.2f" % math.sqrt(abs(self._k1))
#        self._m = "(x%s%s)%s+(y%s%s)%s = %s" % \
#                  (self._i,self._g,self._b,self._j,self._h,self._b,self._k)
#        self._m1 ="(x%s%s)%s+(y%s%s)%s = %s" % \
#                  (self._i,self._g1,self._b,self._j,self._h1,self._b,self._k1)
#        self._n = "(%s,%s)" % (-self._g,-self._h)
#        self._n1= "(%s,%s)" % (-self._g1,-self._h1)
#
#        
#    def squared(self):
#        self._w =(-self.__F/self.__A +((self.__D/self.__A)/2)**2 + ((self.__E/self.__A)/2)**2)
#        return self._w
#    def standardForm(self):
#        return "(x%s%s)%s+(y%s%s)%s = %s" % \
#                  (self._checkSign(((self.__D/self.__A)/2)),((self.__D/self.__A)/2),chr(178),self._checkSign(((self.__E/self.__A)/2)),((self.__E/self.__A)/2),chr(178),(-self.__F/self.__A +((self.__D/self.__A)/2)**2 + ((self.__E/self.__A)/2)**2))
#        
#    def __str__(self):
#        """ String representation of the circle equation,
#        standard form, centre and radius"""
#        
#        try:
#            math.sqrt(Circle.squared(self))
#
#            #Circle raises zero degenerate case 
#            assert math.sqrt(Circle.squared(self)) != 0,"The graph is the single point %s" % \
#                   Circle.centre(self)
#            if self.__A == 1:
#                
#                return "\n<Equation of a circle : x%s + y%s %s %sx %s %sy %s %s = 0 \
#                        \n\n%s %35s %25s \n\n%s %22s %24s\n" %\
#                        (self._b,self._b,self._d,int(self.D),self._e,\
#                         int(self.E),self._f,int(self.F),
#                        "Standard form","Center(x0,y0)","Radius r",\
#                        self._m1,Circle.centre(self),Circle.radius(self))
#            else:
#                return "\n<Equation of a circle : %sx%s + %sy%s %s %sx %s %sy %s %s = 0 \
#                        \n\n%s %35s %25s \n\n%s %22s %24s\n" %\
#                        (int(self.A),self._b,int(self.A),self._b,self._d,int(self.D),self._e,\
#                         int(self.E),self._f,int(self.F),
#                        "Standard form","Center(x0,y0)","Radius r",\
#                        Circle.standardForm(self),Circle.centre(self),Circle.radius(self))
#                
#        #Circle raises Negative number degenerate case    
#        except ValueError:
#            raise ValueError("r%s < 0 : Degenerate case has no graph" % self._b)  
#            
#    def getA(self):
#        """ Get method for A attribute """
#        if self.__A !=0:
#            return self.__A
#        else:
#            raise ValueError("A value should be differtent than zero")
#       
#    def setA(self,value):
#        """ Set method for A attribute """
#       
#        self.__A = value
#        
#    def delA(self):
#        """Delete method for A attrobute"""
#        
#        del self.__A
#
#    #Create a property
#    A = property(getA,setA,delA,"A constant")
#
#    def getD(self):
#        """ Get method for D attribute """
#
#        return self.__D
#
#    def setD(self,value):
#        """ Set method for D attribute """
#        
#        self.__D = value
#        
#    def delD(self):
#        """Delete method for D attrobute"""
#        del self.__D
#
#    #Create a property
#    D = property(getD,setD,delD,"D constant")

#    def getE(self):
#        """ Get method for E attribute """
#        return self.__E
#
#    def setE(self,value):
#        """ Set method for E attribute """
#        
#        self.__E = value
#        
#    def delE(self):
#        """Delete method for E attrobute"""
#
#        del self.__E
#
#    #Create a property
#    E = property(getE,setE,delE,"E constant")
#
#    def getF(self):
#        """ Get method for F attribute """
#
#        return self.__F
#
#    def setF(self,value):
#        """ Set method for F attribute """
#        
#        self.__F = value
#        
#    def delF(self):
#        """Delete method for F attrobute"""
#
#        del self.__F
#
#    #Create a property
#    F = property(getF,setF,delF,"F constant")
#    
#    def _checkSign(self,value):
#        """ Utility method to check the values's sign
#        and return a sign string"""
#        
#        if value >= 0:
#            return "+"
#        else :
#            return ""
#        
#    def radius(self):
#        """ Computes radius of a circle """
#        if self.__A ==1:
#            return self._l1
#        else:
#            return "%2.2f" % math.sqrt(abs(Circle.squared(self)))
#        
#    def centre(self):
#        """ Computes centre(x0,y0) of a circle """
#        if self.__A == 1:
#            return self._n1
#        else:
#            return "(%s,%s)" % (-((self.__D/self.__A)/2),-((self.__E/self.__A)/2))
#        
#    
#
#class Equation(Circle):
#    """ class that represent a radius and the centre of a circle """
#
#    def __init__(self,x,y,radius):
#        """ Equation construction takes centre(xValue,yValue)
#        and radius """
#
#        self.__x = float(x)
#        self.__y = float(y)
#        self.__radius = float(radius)
#        
#        self._o = chr(178)
#        self._p = self.__radius**2
#        self._q = self._checkSign(-self.__x)
#        self._r = self._checkSign(-self.__y)
#        self._s = "(x%s%s)%s+(y%s%s)%s = %s" % \
#                  (self._q,-self.__x,self._o,self._r,-self.__y,self._o,self._p)
#        self._t = self.__x**2 + self.__y**2 - self._p
#        self._u = self._checkSign(self._t)
#        self._v = "x%s + y%s %s%sx %s%sy %s%s = 0" % \
#                  (self._o,self._o,self._q,-self.__x*2,self._r,-self.__y*2,self._u,self._t)
#    
#    def __str__(self):
#        """ String representation of the circle equation, standard form,
#         centre and radius"""
#        
#        #Equation raises radius value < 0
#        assert self.__radius > 0, "<radius value should be greater than zero"
#
#        return ("\n<Equation for the circle of radius (%s)\
#        centred at(%s,%s) is :\n\n%s <--> %s") %\
#        (self.__radius,self.__x,self.__y,self._s,self._v )     
#    
#        
#if __name__ == "__main__":

#    circle1 =  Circle(10,40,16,-7)
#    print(circle1)
#    
#    print(circle1.radius())
#    print(circle1.centre())
#    circle1.delA
#    circle1.A=1
#    print(circle1)
#    circle3 =  Circle(5,24,0,-81)
#    print(circle3)
#    
#    circle3.E =80
#    print(circle3)
#    
#    equation = Equation(2,5,3)
#    print(equation)
#    
#    
#    for doc in (Circle.A,Circle.D,Circle.E,Circle.F):
#        print(doc.__doc__,"=",doc.fget.__name__,doc.fset.__name__,doc.fdel.__name__)
#######################################################################################

#<Equation of a circle : 10x² + 10y² + 40x + 16y  -7 = 0                         

#Standard form                       Center(x0,y0)                  Radius r 

#(x+2.0)²+(y+0.8)² = 5.34            (-2.0,-0.8)                     2.31

#2.31
#(-2.0,-0.8)

#<Equation of a circle : x² + y² + 40x + 16y  -7 = 0                         

#Standard form                       Center(x0,y0)                  Radius r 

#(x+20.0)²+(y+8.0)² = 471.0           (-20.0,-8.0)                    21.70


#<Equation of a circle : 5x² + 5y² + 24x + 0y  -81 = 0                         

#Standard form                       Center(x0,y0)                  Radius r 

#(x+2.4)²+(y+0.0)² = 21.96            (-2.4,-0.0)                     4.69


#<Equation of a circle : 5x² + 5y² + 24x + 80y  -81 = 0                         

#Standard form                       Center(x0,y0)                  Radius r 

#(x+2.4)²+(y+8.0)² = 85.96            (-2.4,-8.0)                     9.27


#<Equation for the circle of radius (3.0)        centred at(2.0,5.0) is :

#(x-2.0)²+(y-5.0)² = 9.0 <--> x² + y² -4.0x -10.0y +20.0 = 0
#A constant = getA setA delA
#D constant = getD setD delD
#E constant = getE setE delE
#F constant = getF setF delF
