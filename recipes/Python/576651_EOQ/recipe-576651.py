#On the name of ALLAH
#Author : Fouad Teniou
#Date : 12/02/09
#version :2.4

""" Economic order quantity model can help reducing the total cost of (Ch,holding cost)
and (Co, ordering cost) of stock. However, an annual demand (D), cost per item (Ci),
quantity of order (X), and discount (S) are used to compute the
EOQ and savings """

import math

#The user try a value equal to zero
class MyZeroException(ArithmeticError): pass

#The user try a negative value
class MyNegativeException(ArithmeticError): pass
 
def myError(value):
    """ Raises MyZeroException and MyNegativeException exceptions."""
     
    if value == 0:
        raise MyZeroException,\
              "<\nQuantity and discount rate should not be equal to zero "
    elif value < 0:
        raise MyNegativeException,\
              "<\nQuantity and discount rate values should be greater than zero "
        
class EOQ:
    """ Class that represent Economic Order Quantity """
    
    def __init__(self,D=0,Ch=0,Co=0,Ci=0,X=0,S=0):
        """ Constructor for class EOQ """
        
        myError(D)
        myError(Ch)
        myError(Co)
        myError(Ci)
        myError(X)
        myError(S)
        
        self.D = D
        self.Ch = Ch
        self.Co = Co
        self.Ci = Ci
        self.X = X 
        self.S = S

        try:
            
            f = [(lambda D,Ch,Co: "%2.2f" %math.sqrt(math.fabs(2*Co*D/Ch))),
                 (lambda Ch,Co,D: "%2.2f" %((Ch*self.A/2)+(Co*D/self.A))),
                 (lambda Ch,Co,D,X: "%2.2f" %((Ch*X/2)+(Co*D/X))),
                 (lambda Ci,D,S : "%2.2f" %(Ci*D*S/100))]
            self.A = float(f[0](D,Ch,Co))
            self.B = f[1](Ch,Co,D) 
            self.C = "%2.0f" %(float(f[2](Ch,Co,D,X)))
            self.E = float(self.C)-float(self.B)
            self.F = float(f[3](Ci,D,S))
            self.G = "%2.0f" %(Ch*X/2)
            self.H = "%2.0f" %(Co*D/X)
            self.I = "%2.0f" %(((self.A/2)*Ch)+((D/self.A)*Co))
            self.J = "%2.0f" %(-(float(self.C) - float(self.I)) + (float(self.F)*100))

        #EOQ raise ValueError if input is not numerical
        except ZeroDivisionError:
            print "Holding cost should not be equal to zero "
            
        except MyZeroException, exception:
            print exception
            
        except MyNegativeException, exception:
            print exception
                       
    def compare(self,K,L):
        """ Compare a different quantity and discount rate """

        myError(K)
        myError(L)
        
        self.K = K
        self.L = L
        
        try:
            g =[(lambda Ch,Co,D,K: "%2.2f" %((self.Ch*K/2)+(self.Co*self.D/K))),
                (lambda Ci,D,L : "%2.2f" %(self.Ci*self.D*L/100))]
            self.M = float(g[0](self.Ch,self.Co,self.D,K))
            self.N = float(g[1](self.Ci,self.D,L))
            self.O = "%2.0f" %(-(float(self.M) - float(self.I)) + (float(self.N)*100))
            self.P = float(self.O)- float(self.J)
            print "\n<The total cost of ordering batches of %s is: %s " % (self.K,int(self.M))

            if self.P >= 0:
                return "\n<The extra saving of ordering batches of %s is %s " % (K,int(self.P))
            else:
                return "\n<The extra loss of ordering batches of %s is %s " % (K,int(self.P))
                
        except MyZeroException, exception:
            print exception
            
        except MyNegativeException, exception:
            print exception
            
    def __str__(self):
         """ String representation of the EOQ, annual order and holding cost,
         total annual inventory cost to obtain discount and using EOQ, and the
         annual profit or loss arise """
         
         print "\n<EOQ = %2.0f \n \
                \n<The annual order cost = %s\n \
                \n<The annual holding cost = %s\n \
                \n<The total annual inventory cost to obtain discount  = %s\n\
                \n<The total annual inventory cost using EOQ  is = %s" \
                % (self.A,self.H,self.G,self.C,self.I)
         
         if int(self.J)> 0:
            return "\n<The annual profit of ordering in batches of %s is %s " % (self.X,self.J) 
         else:
            return "\n<The annual loss of ordering in batches of %s is %s " % (self.X,self.J)
                  
if __name__ == "__main__":
    
    test = EOQ(37000,0.70,300,3.4,3000,0.005)
    print test
    print test.compare(7000,0.0075)
#############################################################    
#c:\hp\bin\Python>python "C:\Fouad #Teniou\Documents\Programs\EOQModel7.py"

#<EOQ = 5632

#<The annual order cost = 3700

#<The annual holding cost = 1050

#<The total annual inventory cost to obtain discount  = 4750

#<The total annual inventory cost using EOQ  is = 3942

#<The annual loss of ordering in batches of 3000 is -179

#<The total cost of ordering batches of 7000 is: 4035

#<The extra saving of ordering batches of 7000 is 1030


#c:\hp\bin\Python>
