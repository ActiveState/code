#On the name of ALLAH
#Author : Fouad Teniou
#Date : 07/03/09
#version :2.6.1

""" New in python 2.6 namedtuple function is used in my program IRR-Versus-NPV
    with a PresentValue as a typename, and discount rates r_1, r_2 and
    number of periods until payments n as fieldnames (PresentValue('r_1','r_2','n'))
    IRR-Versus-NPV program provide an NPV and IRR (linear interpolation) 
    calculations by entering the outflows/inflows values for a project
    with 2 different rates r_1 and r_2, and only an NPV if r_2 is equal to zero
    The program also returns any value or a series of values from the Present Value
    Annuity Tables
"""
    
import itertools
import operator
import collections
import math as m

class MinusSignError(ArithmeticError):
    """ user attempt an operation on negative number"""
    pass

class PresentValue(collections.namedtuple('PresentValue', 'r_1,r_2,n')):
    """PresentValue a subclass of namedtuple Python class
    with two rates values (r_1,r_2) and a period number n """
    
    #set __slots__ to an empty tuple keep memory requirements low
    __slots__ = () 

    @property
    def DF(self):
        """Compute the discount factor of two values"""
        
        if self.r_1<0 or self.r_2 < 0 or self.n<0:
            raise MinusSignError,\
              "\n<Rates values and period number should be positive "
        
        try:
            discount_factor_1 = "%2.3f" % m.pow((1+self.r_1),-self.n)
            discount_factor_2 = "%2.3f" % m.pow((1+self.r_2),-self.n)
        
            return (discount_factor_1,discount_factor_2)

        #DF raises Negative number error
        except MinusSignError,exception:
            print exception

    @property
    def AF(self):
        """Compute the annuity factor of two values"""
        
        if self.r_1<0 or self.r_2 < 0 or self.n<0:
            raise MinusSignError,\
              "\n<Rates values and period number should be positive"
        try:
            
            annuity_factor_1 = "%2.3f" %((1-((m.pow((1+self.r_1),-self.n))))/self.r_1)
            annuity_factor_2 = "%2.3f" %((1-((m.pow((1+self.r_2),-self.n))))/self.r_2)

            return (annuity_factor_1,annuity_factor_2)

        #AF raises Zero division number error 
        except ZeroDivisionError:
            print "\n<Please choose a rate value greater than zero"

        #AF raises Negative number error    
        except MinusSignError,exception:
            print exception

    def npvTable(self,*args):
        """Compute the NPV and IRR values of a project with two different rates"""
        
        try:
            #You need at least one rate to compute an NPV
            assert self.r_1 !=0,"The first rate should not be equal to zero "

            res_1 = []
            res_2 = []
            item_1 =[]
            item_2 =[]
            count_1 = -1
        
            for arg in args:
     	
                count_1 +=1

                #outflows/inflows starting at year 0                 
                pv_set = PresentValue(r_1=self.r_1,r_2=self.r_2,n = count_1)
                res_1.append(pv_set.DF[0]) # Trigger the Discount factor at rate r_1 and append the res_1
                res_2.append(pv_set.DF[1]) # Trigger the Discount factor at rate r_2 and append the res_2            
            print "\n years \tCash flows \t DF at %s\t PV" %(str(int(self.r_1*100))+'%')

            count_2 = -1

            for (x_1,y) in (itertools.izip(res_1,args)):    #for loop return PV set item_1
                item_1.append((float(x_1)*y))

                count_2  +=1
            
                print "\n  %s\t%s\t\t %s\t\t%s" %(count_2,y,x_1,int(float(x_1)*y))

                npv_1 =(reduce(operator.add,item_1))    #Compute the npv_1 total
            
            print '\n\t\t\t\t NPV =  %s\n' % int(npv_1)
        
            if self.r_2 == 0:   #user attempt only one NPV calculation 
            
                print "<No NPV calculation %s=%s" % pv_set._asdict().items()[1]

            else:
            
                print "\n years \tCash flows \t DF at %s\t PV" %(str(int(self.r_2*100))+'%')

                count_3 = -1
            
                for (x_2,y) in (itertools.izip(res_2,args)):    #for loop return PV set item_2
                    item_2.append((float(x_2)*y))
                    count_3 +=1
                
                    print "\n  %s\t%s\t\t %s\t\t%s" %(count_3,y,x_2,int(float(x_2)*y))

                    npv_2 = (reduce(operator.add,item_2))   #Compute the npv_2 total 
                
                print '\n\t\t\t\t NPV =  %s\n ' % int(npv_2)

                #The IRR computation will depend of the rates and npvs (higher and lower values)               
                if self.r_1 > self.r_2:
                
                    print "<The IRR = %2.1f" % ((self.r_2+(npv_2/(npv_2-npv_1))*(self.r_1-self.r_2))*100)+' %\n'

                else:
                
                    print "<The IRR = %2.1f" % ((self.r_1+(npv_1/(npv_1-npv_2))*(self.r_2-self.r_1))*100)+' %\n'       
                print "<The project will be recommended on finanacial grounds, while "
                print "ignoring risk, if the IRR is greater than the target rate of "
                print "return, otherwise the project will be rejected.\n"

        #npvTable raises Negative number error
        except MinusSignError,exception:
            print exception
    
        
if __name__ == "__main__":
    
    p = PresentValue('r_1','r_2','n')
    
    p = p._replace(r_1=0.27,r_2 = 0.13)# n is equal to the numbers of outflows/inflows
    p.npvTable(-70000,48000,24000,22000,13000,33000,15000,17000)
    
    s = p._replace(r_1=0.07,r_2 =0.05) #You can set r_2 to zero to get only an NPV but not r_1 since you need at least one rate for the NPV

    print " years\t\tDF at%2.0f%s\tAF at%2.0f%s\t DF at%2.0f%s\t AF at%2.0f%s \n" %\
          (s.r_1*100,'%',s.r_1*100,'%',s.r_2*100,'%',s.r_2*100,'%')

    for i in range(1,11): # you can do it individualy by setting r_1,r_2 and n (eg: PresentValue(r_1 = 0.17,r_2 = 0.07,n=7)
        s = p._replace(r_1=0.07,r_2 =0.05,n=i)
        print "  %s\t\t%s\t\t %s\t\t %s\t\t %s" % \
              (i,s.DF[0],s.AF[0],s.DF[1],s.AF[1])
    
    # Another method to display the npv,for the same outflows/inflows values
    # using different sets of rates and (n = to the number of outflows/inflows )
    # It will save you time to write the same inflows/outflows every time you  
    # alter the rates 
    
    # below is just an example and you can extend your set of values as you wish.

    a = [0.07,0.02,'n']
    b = [0.04,0.05,'n']
    c = [0.04,0.07,'n']
    
    for item in a,b,c:
        p = p._make(item)
        p.npvTable(-70000,48000,24000,22000,13000,37000)
    
    #Another way to retrieve Annuity factors and Discount factors
    #individually or in sets of (r_1,r_2)
    g = [0.04,0.07,17]
    p = p._make(g)
    print p.DF
    print p.AF
    print p.DF[0]
    print p.DF[1]
    print p.AF[0]
    print p.AF[1]
    
#########################################################################################

    
# c:\Python26>python "C:Fouad Teniou\Documents\IRRvNPV.py"

# years  Cash flows       DF at 27%       PV

#  0     -70000           1.000          -70000

#  1     28000            0.787          22036

#  2     24000            0.620          14880

#  3     22500            0.488          10980

#  4     13000            0.384          4992

#  5     33000            0.303          9999

#  6     15000            0.238          3570

#  7     17000            0.188          3196

#                                 NPV =  -347


# years  Cash flows       DF at 13%       PV

#  0     -70000           1.000          -70000

#  1     28000            0.885          24780

#  2     24000            0.783          18792

#  3     22500            0.693          15592

#  4     13000            0.613          7969

#  5     33000            0.543          17919

#  6     15000            0.480          7200

#  7     17000            0.425          7225

#                                 NPV =  29477

#<The IRR = 26.8 %

#<The project will be recommended on finanacial grounds, while
#ignoring risk, if the IRR is greater than the target rate of
#return, otherwise the project will be rejected.

# years          DF at 7%        AF at 7%         DF at 5%        AF at 5%

#  1             0.935            0.935           0.952           0.952
#  2             0.873            1.808           0.907           1.859
#  3             0.816            2.624           0.864           2.723
#  4             0.763            3.387           0.823           3.546
#  5             0.713            4.100           0.784           4.329
#  6             0.666            4.767           0.746           5.076
#  7             0.623            5.389           0.711           5.786
#  8             0.582            5.971           0.677           6.463
 # 9             0.544            6.515           0.645           7.108
#  10            0.508            7.024           0.614           7.722

#c:\Python26>

###########################################################################################
