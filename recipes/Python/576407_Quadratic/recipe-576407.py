#On the name of ALLAH and may the blessing and peace of Allah 
#be upon the Messenger of Allah Mohamed Salla Allahu Aliahi Wassalam.
#Author : Fouad Teniou
#Date : 05/08/08
#Version : 2.4

import cmath as c
import math as m

################################################################## 
# x**2 = -1 an equation which does not have a solution in the real number field
# i = Square-Root (-1)  < -- > i**2 = -1 made it possible to develop the complex numbers
# of the form a + bj
################################################################### 

class Quadratic:
	def __call__(self,**args):
	      self.args = args
	      if (len(args) == 3 and self.args.has_key('a') and self.args.get('a') !=0 
                       and self.args.has_key('b') and self.args.has_key('c')):
       	            if ((self.args.get('b'))**2-(4*(self.args.get('a'))*(self.args.get('c'))))>=0:
		         self.compute1 = "%2.2f" % float(((self.args.get('b')*(-1))+(m.sqrt((self.args.get('b'))**
					2-(4*(self.args.get('a'))*(self.args.get('c'))))))/(2*self.args.get('a')))
		         self.compute2 = "%2.2f" % float(((self.args.get('b')*(-1))-(m.sqrt((self.args.get('b'))**
					2-(4*(self.args.get('a'))*(self.args.get('c'))))))/(2*self.args.get('a')))
                    elif ((self.args.get('b'))**2-(4*(self.args.get('a'))*(self.args.get('c'))))<0:
		         self.compute1 = "%2.2f" % float(((self.args.get('b')*(-1))+(c.sqrt((self.args.get('b'))**
					2-(4*(self.args.get('a'))*(self.args.get('c'))))))/(2*self.args.get('a')))
		         self.compute2 = "%2.2f" % float(((self.args.get('b')*(-1))-(c.sqrt((self.args.get('b'))**
					2-(4*(self.args.get('a'))*(self.args.get('c'))))))/(2*self.args.get('a')))
	       else:
		   self.args = 0
                
               return (self.compute1,self.compute2)

	def __str__(self):
	      if self.args == 0:
		return '\n<Quadratic : Equation should be of the form of ax%+bx+c (a=?,b=?,c=?) and a !=0' % chr(253)
	      else:
		   if self.compute1==self.compute2:
		        return ('\n<Quadratic : Equation of the form %sx%s +(%s)x+(%s) = 0 \n\n<Solutions : x = %s\n\t'
			% (self.args.get('a'),chr(253),self.args.get('b'),self.args.get('c'),self.compute1))
		   else:     
                        return ('\n<Quadratic : Equation of the form %sx%s +(%s)x+(%s) = 0 \n\n<Solutions : x = %s\n\t       x = %s'
			% (self.args.get('a'),chr(253),self.args.get('b'),self.args.get('c'),self.compute1,self.compute2))

if __name__ =='__main__':
	y = Quadratic()
	y(a=7,b=-2,c=-2)
	print y
	y(a=-1,b=4,c=-5)
	print y
	y(a=4,b=-4,c=1)
	print y
	y(a=0,b=3,c=3)
	print y
########################################################################################## 
#Version : Python 3.2
#import cmath as c
#import math as m

#class Quadratic:
#    def __call__(self,**args):
#        self.args = args
#        if (len(args)==3 and 'a' in self.args and self.args.get('a')!=0
#            and 'b' in self.args and 'c' in self.args):
#            if ((self.args.get('b'))**2-(4*(self.args.get('a'))*(self.args.get('c'))))#>=0:
#                self.compute1 = "%2.2f" % float(((self.args.get('b')*(-1))+( m.sqrt((self.args.get('b'))**
#                               2-(4*(self.args.get('a'))*(self.args.get('c'))))))/(2*self.args.get('a')))
#               self.compute2 = "%2.2f" % float(((self.args.get('b')*(-1))-( m.sqrt((self.args.get('b'))**
#                                2-(4*(self.args.get('a'))*(self.args.get('c'))))))/(2*self.args.get('a')))
#            elif ((self.args.get('b'))**2-(4*(self.args.get('a'))*(self.args.get('c'))))<0:
#                self.compute1 = ((self.args.get('b')*(-1))+( c.sqrt((self.args.get('b')**
#                                2-(4*(self.args.get('a'))*(self.args.get('c'))))))/(2*self.args.get('a'))
#                self.compute2 = ((self.args.get('b')*(-1))-(c.sqrt((self.args.get('b'))**
#                                2-(4*(self.args.get('a'))*(self.args.get('c'))))))/(2*self.args.get('a'))
#        else:
#            self.args = 0
            
#        return (self.compute1,self.compute2)
#    def __str__(self):
#        if self.args == 0:
#            return '\n<Quadratic : Equation should be of the form of ax%s+bx+c (a=?,b=?,c=?) and a != 0' % chr(178)
#        else:
#            if self.compute1==self.compute2:
#                return ('\n<Quadratic : Equation of the form %sx%s + (%s)x + (%s) = 0 #\n\n<Solutions : x = %s\n\t'
#                    % (self.args.get('a'),chr(178),self.args.get('b'),self.args.get('c'),self.compute1))
#            else:
#                return ('\n<Quadratic : Equation of the form %sx%s + (%s)x + (%s) = 0 #\n\n<Solutions : x = %s\n\t     x = %s'
#                    % (self.args.get('a'),chr(178),self.args.get('b'),self.args.get('c'),self.compute1,self.compute2))
         2)
#if __name__=='__main__':
#    y = Quadratic()
#    y(a=1,b=-0.2,c=-0.4)
#    print(y)
#    y(a=-1,b=4,c=-5)
#    print(y)
#    y(a=4,b=-4,c=1)
#    print(y)
#    y(a=0,b=3,c=3)
#    print(y)
#    y(a=-1900,b=177,c=333)
#    print(y)
#
