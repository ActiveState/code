import math as m
import cmath as c

class Complex:
    """
      Author: César Otero
      Description: A complex number class which can do complex arithmetic
                   in both Cartesian and polar coordinates, or a mix of the two
    """
  
    def __init__(self, num=0, phase=0):
        if type(num) == complex:
            # cnum is in Cartesian form
            self.cnum      = num
            self.magnitude = abs(num)
            phaseRad = m.atan2(num.imag, num.real)
            self.phase     = m.degrees(phaseRad)
            
        else:
            # cnum is in polar form
            self.cnum      = m.cos(phase) + complex(0,m.sin(phase))
            self.magnitude = num
            self.phase     = phase

    def __str__(self):
        return str(self.magnitude) + " /_ (" + str(self.phase) + ") deg"

    def __add__(self,n):
        if type(n) == int:
            re = self.cnum.real + n
            im = self.cnum.imag
        elif type(n) == float:
            re = self.cnum.real + n
            im = self.cnum.imag
        else:
            re = self.cnum.real + n.cnum.real
            im = self.cnum.imag + n.cnum.imag
            
        z = re+complex(0,im)
        return Complex(z)
    
    def __radd__(self,n):
        if type(n) == int:
            re = self.cnum.real + n
            im = self.cnum.imag
        elif type(n) == float:
            re = self.cnum.real + n
            im = self.cnum.imag
        else:
            re = self.cnum.real + n.cnum.real
            im = self.cnum.imag + n.cnum.imag
            
        z = re+complex(0,im)
        return Complex(z)

    def __div__(self,n):
        magnitude = self.magnitude / n.magnitude
        phase = self.phase - n.phase
        return Complex(magnitude, phase)

    def __rdiv__(self,n):
        magnitude = n.magnitude / self.magnitude
        phase = n.phase - self.phase 
        return Complex(magnitude, phase)

if __name__=="__main__":
        ----------r=90 Ohms--------L = 160j Ohms ----------|        
        |                                                                            
      pSource = 750 /_ 30 deg                             C = -40j Ohms
        |                     |                                                                                                                                                                   
        |--------------------------------------------------|                
    
    pSource = Complex(750,30) # power source, in polar form 
                              # with a magnitude of 750 volts, and angle of 30 
                              # degrees.
    r = 90                    # Ohms ( real part only )
    L = Complex(0+160j)       # Ohms ( Cartesian form )
    C = Complex(0-40j)        # Ohms ( Cartesian form )
    Z = r+L+C                 # total impedance    
    print "Impedance is ", Z
    
    I = pSource / Z
    print "Phase current is ", I
    
