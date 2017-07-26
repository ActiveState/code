#On the name of ALLAH and may the blessing and peace of Allah 
#be upon the Messenger of Allah Mohamed Salla Allahu Aliahi Wassalam.
#Author : Fouad Teniou 
#Date : 24/07/08
#versionl :2.4

import math as m 
import re

#################################################################################################### 
# Degree measure: There are 360 degrees in an angle of one revolution.
# Degrees are divided into 60 minutes and minutes are divided into 60 seconds.
# Radian measure: 360 degrees is equal to 2(Pi) radians and 180 degrees is equal to Pi(3.14159rad) 
# Sine, Cosine ,Tangent , Cosecant, Secant, and Cotangent are trigonometric functions which could be
# calculated for a given angle	.
####################################################################################################
 

class Pycol:
    def __init__(self,other,name='',value=0)      #Initialize                  
       self.other = other
       self.name  = name
       self.value = value
    def switch(self):
       cable = {30:(chr(244)+'/6'), 45:(chr(244 )+'/4'),60:( chr(244 )+ '/3'),
              90:(chr(244)+'/2'), 120 :('2'+chr(244)+'/3'),135 :('3'+ chr(244) +'/4'),
              150:('5'+chr(244)+'/6'), 180:(chr(244)),270:('3'+chr(244)+'/2'),360:('2'+chr(244))}		 #Make a dictionary
       if cable.has_key(self.other):			 #Step through rest and fetch dictionary values by their keys
	  return cable [self.other]			 #Return Keys values
    def __mul__(self}:
	return self.value * self.other
    def __repr__(self):			 #test and Print
       if self.__class__.__name__ == "Degrees" or self.__class__.__name__  == "Radians":
	  return ("\n <Pycol : Express %s %s into (Degrees + minutes + seconds) and %s " %
	(self.other,self.__class__.__name__,self.name))
       else:
           if Pycol.switch(self):			#Test if self.other in dictionary keys
	        return ("\n <Pycol : Compute %s function \t %s (%s) <--> %s(%s) = %s" %
	(self.__class__.__name__,self.__class__.__name__,self.other,self.__class__.__name__,str(Pycol.switch(self)[:]),self.compute))
           else:
	         return ("\n <Pycol : Compute %s function \t %s (%s) = %s" %
	                   (self.__class__.__name__,self.__class__.__name__,self.other,self.compute))

class Degrees(Pycol):
    def __init__(self,other):	#Inherit .
	Pycol.__init__(self,other,'Radians',m.pi/180)	#Run Pycol init
    def adapt(self):
         a = re.match(r"(?P<int>\d+)\.(\d*)", str("%2.2f" % self.other))
         b = re.match(r"(?P<int>\d+)\.(\d*)", "%2.2f" % float(str(float(a.group(2))*0.6)))
         c = re.match(r"(?P<int>\d+)\.(\d*)", "%2.2f" % float(str(float(b.group(2))*0.6)))
         if Pycol.switch(self):
            print ('\n\t\t\t' + str(self.other)+ " deg" +" = " + a.group(1)+chr(248)+' '+b.group(1)+"'"+ ' '+ c.group(1)+'"'+"=" +("%2.5f" % float(Pyeol.__mul__(self)))+"rad"+" <--> "+ str(Pycol.switch(self)[:]))
         else:
            print ('\n\t\t\t' + str(self.other)+ " deg"+" = " + a.group(1)+chr(248)+' '+b.group(1)+"'"+' ' + c.group(1)+'"'+" = " +("%2.5f" % float(Pycol.__mul__(self)))+"rad")

class Radians(Pycol):                           #Inherit     
    def __init__(self,other):
       Pycol.__init__(self,other,'Degrees', 180/m.pi)     #Run Pycol init
    def adapt(self):
        a = re.match(r"(?P<int>\d+)\.(\d*)" , str( "%2.2f" % float(Pycol.__mul__(self))))
        b = re.match(r"(?P<int>\d+)\.(\d*)" ,"%2.2f" % float(str(float(a.group(2))*0.6)))
        c = re.match(r"(?P<int>\d+)\.(\d*)" , "%2.2f" % float(str(float(b.group(2))*0.6)))
        print ('\n\t\t\t' + "%2.5f" % float(str(self.other)) + " rad" + " = "+"%2.2f" % float(Pycol.__mul__(self))+ " deg"+" = " + a.group(1)+chr(248)+' '+b.group(1)+"'"+'' +c.group(1)+ '"')

class sin(Degrees):                      #Inherit
    def __init__(self,other}:
	Degrees.__init__(self,other)
	if self.other % 180 == 0 :#sin(X)=sin(X + 2Pi)=sin(X-2Pi),sin(0)=sin(180)=...
	   self.compute = 0.0
	else:
	     self.compute = m.sin(Pycol.__mul__(self))	# sin(X)=Side opposite(X)/hypotenuse
			                                #X: given angle in degrees
class sec(sin):
    def __init__(self,other):
       Degrees.__init__(self,other)
       if m.sqrt((1-((m.sin(Pycol.__mul__(self))**2)))) == 0: #sin**2(X) +cos**2(X)=1
	  self.compute = 'Division by Zero indefinebale'	#Obtained from applying Theorem of Pythagoras
       else:	                                        #and using the sin(X) and cos(X) defInitions
	    self.compute = 1/m.cos(Pycol.__mul__(self))	# sec(X)=1/cos(X)

class cos(sec):
    def __init__(self,other):          #Inherit
       Degrees.__init__(self,other)     
       if self.other %90 == 0 and self.other %180 !=0:#cos(X)=cos(X +2Pi)=cos(X-2Pi),cos(90)=cos(270) =...
	  self.compute = 0.0
       else:
	    self.compute = m.cos(Pycol.__mul__(self))# cos(X)= side adjacent to (X)/hypotcnus

class csc(cos):
    def __init__(self,other):
      Degrees.__init__(self,other)
	if m.sqrt((1-((m.cos(Pycol.__mul__(self))**2)))) == 0:
	   self.compute = 'Division by zero indefineable'
	else :
             self.compute = 1/m.sin(Pycol.__mul__(self))  #csc(X)= 1/sin(X)
   
class tan(csc):
     def __init__(self,other}:
	Degrees.__init__(self,other)
	if self.other % 180 == 0 :
	   self.compute = 0.0
	elif m.sqrt((1-((m.sin(Pycol.__mul__(self))**2)))) == 0: # sin**2(X) +cos**2(X)=1
	    self.compute = 'Division by zero indefinebale'	  # Obtained from applying Theorem of Pythagoras
	else:	                                                  #and using the sin(X} and cos(X) definitions
            self.compute = m.sin(Pycol.__mul__(self))/m.cos(Pycol.__mul__(self))    #tan(X)=sin(X)/cos(X)

class cot(tan):
    def __init__(self,other):
	Degrees.__init__(self,other)
	   if m.sqrt((1-((m.cos(Pyco1.__mul__(self))**2))))==0:                   # sin**2(X) +cos**2(X)=1
	      self.compute = 'Division by zero indefinebale'
	   elif self.other %90 ==0 and self.other % 180 !=0:
	      self.compute = 0.0
	   else:
	      self.compute =1/(m.sin(Pycol.__mul__(self))/m.cos(Pycol.__mul__(self))) #cot(X)= 1/tan(X)

if  __name__ == '__main__':
   for i in (0,30,45,60,90,120,135,150,180,270,360): 
       a = Degrees (i)
       print a
       a.adapt()
       b = Radians (6.283185307)
       print b
       b.adapt()
   for i in range(0,105,15):
       print sin(i)
       print cos(i)
       print tan(i) 
       print csc(i) 
       print sec(i) 
       print cot(i)
----------------------------------------------------------------------------------

#alternatively students can use DOS and run the following 
# if __name__=='__main__""" instead of the above to compute their trigonometric
# functions or converting methods 
if __name__ =='__main__':
   while 1:
     y=raw_input("\nPlease enter the function's name,'sin,cos,tan,sec,csc,cot'\nor a converting method 'deg,rad'\nor any key to exit\n")
     x=raw_input("Please enter the angle's value.\n")
     if y=='deg':
        a = Degrees(float(x))
        a.adapt()
     elif y=='rad':
        a = Radians(float(x))
        a.adapt()
     elif y=='sin':
          print sin(int(x))
     elif y=='cos':
          print cos(int(x))
     elif y=='tan':
          print tan(int(x))
     elif y=='sec':
          print sec(int(x))
     elif y=='csc':
          print csc(int(x))
     elif y=='cot':
          print cot(int(x))
     else:
          break


#########################################################################################
#Version : Python 3.2


#import math as m
#import re


#class Pycol:
#    def __init__(self,other,name='',value=0):                       #Initialize
#        self.other = other      
#        self.name = name
#        self.value = value
#    def switch(self):
#        cable = {30:(chr(182)+'/6'),45:(chr(182)+'/4'),60:(chr(182)+'/3'),
#                 90:(chr(182)+'/2'),120:('2'+chr(182)+'/3'),135:('3'+chr(182)+'/4'),
#                 150:('5'+chr(182)+'/6'),180:(chr(182)),
#                 270:('3'+chr(182)+'/2'),360:('2'+chr(182))}        #Make a dictionary
#        if self.other in cable:                             #Step through test and fetch #dictionary values by their keys 
#            return cable [self.other]                               #Return Keys values
#    def __mul__(self):
#        return self.value * self.other
#    def __repr__(self):                                             #test and Print
#        if self.__class__.__name__ == "Degrees" or self.__class__.__name__ == "Radians":
#           return ("\n <Pycol : Express %s  %s into (Degrees + minutes + seconds)and %#s " %
#        (self.other,self.__class__.__name__,self.name))
#        else:
#            if Pycol.switch(self):                                  #Test if selfother #in dictionary keys
#               return ("\n <Pycol : Compute %s function \t %s (%s) <--> %s (%s) = %s "  %
#            (self.__class__.__name__,self.__class__.__name__,self.other,self.__class__.__name__,str(Pycol.switch(self)[:]),self.compute)) 
#            else :
#                return ("\n <Pycol : Compute %s function \t %s (%s) = %s"  %
#            (self.__class__.__name__,self.__class__.__name__,self.other,self.compute))
#class Degrees(Pycol):
#    def __init__(self,other):                                       #Inherit
#        Pycol.__init__(self,other,'Radians',m.pi/180)               #Run Pycol init
#    def adapt(self):
#        a = re.match(r"(?P<int>\d+)\.(\d*)", str( "%2.2f" % self.other))
#        b = re.match(r"(?P<int>\d+)\.(\d*)","%2.2f" % float(str(float(a.group(2))*0.6)))
#        c = re.match(r"(?P<int>\d+)\.(\d*)", "%2.2f" % float(str(float(b.group(2))*0.6)))
#        if Pycol.switch(self):
#            print(('\n\t\t\t' + str(self.other)+ " deg" +" = " + a.group(1)+chr(176)#+' '+b.group(1)+"'"+' ' +
#                   c.group(1)+'"'+" = " +("%2.5f" % float(Pycol.__mul__(self)))+"rad"+" #<--> "+ str(Pycol.switch(self)[:])))
#        else :
#            print(('\n\t\t\t' + str(self.other)+ " deg" +" = " + a.group(1)+chr(176)#+' '+b.group(1)+"'"+' ' +
#                   c.group(1)+'"'+" = " +("%2.5f" % float(Pycol.__mul__(self)))+"rad"))
#            
#class Radians(Pycol):                                               #Inherit
#    def __init__(self,other):
#        Pycol.__init__(self,other,'Degrees',180/m.pi)               #Run Pycol init
#    def adapt(self):
#        a = re.match(r"(?P<int>\d+)\.(\d*)", str( "%2.2f" % float(Pycol.__mul__(self))))
#        b = re.match(r"(?P<int>\d+)\.(\d*)","%2.2f" % float(str(float(a.group(2))*0.6)))
#        c = re.match(r"(?P<int>\d+)\.(\d*)", "%2.2f" % float(str(float(b.group(2))*0.6)))
#        print(('\n\t\t\t' + "%2.5f" % float(str(self.other)) + " rad" + " = "+"%2.2f" % #float(Pycol.__mul__(self))+
#               " deg"+" = " + a.group(1)+chr(176)+' '+b.group(1)+"'"+' ' +c.group(1)#+'"'))
#class sin(Degrees):                                                 #Inherit
#    def __init__(self,other):   
#        Degrees.__init__(self,other)
#        if self.other % 180 == 0 :                                  #sin(X)=sin(X + 2Pi)#=sin(X-2Pi),sin(0)=sin(180)=...
#            self.compute = 0.0
#        else:
#            self.compute = m.sin(Pycol.__mul__(self))               # sin(X)=Side #opposite(X)/hypotenuse 
#                                                                    #X: given angle in #degrees
#class sec(sin):                                                     #Inherit
#    def __init__(self,other):
#        Degrees.__init__(self,other)
#        if  m.sqrt((1-((m.sin(Pycol.__mul__(self))**2)))) == 0:     # sin**2(X) +cos**2(X)=1
#            self.compute = 'Division by zero indefinebale'          #Obtained from #applying Theorem of Pythagoras
#        else :                                                      #and using the sin(X) and cos(X) definitions
#            self.compute = 1/m.cos(Pycol.__mul__(self))             # sec(X)=1/cos(X)
#
#class cos(sec):                                                     #Inherit           
#    def __init__(self,other):
#        Degrees.__init__(self,other)
#        if self.other %90 ==0 and self.other %180 !=0:              #cos(X)=cos(X + 2Pi)#=cos(X-2Pi),cos(90)=cos(270) =...
#             self.compute = 0.0
#        else :
#             self.compute = m.cos(Pycol.__mul__(self))              # cos(X)= side #adjacent to (X)/hypotenus

#class csc(cos):
#    def __init__(self,other):
#        Degrees.__init__(self,other)
#        if  m.sqrt((1-((m.cos(Pycol.__mul__(self))**2)))) == 0:
#            self.compute = 'Division by zero indefinebale'
#        else :
#            self.compute = 1/m.sin(Pycol.__mul__(self))             #csc(X)= 1/sin(X)
#class tan(csc):
#    def __init__(self,other):
#        Degrees.__init__(self,other)
#        if self.other % 180 == 0 :
#            self.compute = 0.0
#        elif m.sqrt((1-((m.sin(Pycol.__mul__(self))**2)))) == 0:    # sin**2(X) +cos**2(X)=1
#            self.compute = 'Division by zero indefinebale'          #Obtained from #applying Theorem of Pythagoras 
#        else:                                                       #and using the sin(X) and cos(X) definitions
#            self.compute = m.sin(Pycol.__mul__(self))/m.cos(Pycol.__mul__(self))    #tan(X)=sin(X)/cos(X)
#
#class cot(tan):
#    def __init__(self,other):
#        Degrees.__init__(self,other)
#        if  m.sqrt((1-((m.cos(Pycol.__mul__(self))**2)))) == 0:      # sin**2(X) +cos**2(X)=1
#            self.compute = 'Division by zero indefinebale'
#        elif self.other %90 ==0 and self.other %180 !=0:
#             self.compute = 0.0
#        else :
#            self.compute= 1/(m.sin(Pycol.__mul__(self))/m.cos(Pycol.__mul__(self))) #cot(X)=1/tan(X)
