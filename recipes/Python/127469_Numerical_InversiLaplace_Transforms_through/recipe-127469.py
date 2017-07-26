#################################################################
#   Function Zakian(t), numerically inverts a Laplace transform #
#   F(s) into f(t) for a specific time "t" using the Zakian     #
#   algorithm.                                                  #
#                                                               #
#   Function F(s) is defined in separate as Fs(s) (see code     #
#   below). In the present case, F(s) = 1/(s-1), whose          #
#   analytical inversion is f(t) = exp(t), and t=1.0 thus       #
#   yielding f(1) = 2.71828180837 what is "e" with an error     #
#   of -7.4e-007%. Oscillatory systems may become innacurate    #
#   after the second cycle, though.                             #
#                                                               #
#   Fs(s) has to be changed accordingly everytime the user      #
#   wants to invert a different function.                       #
#                                                               #
#   Creator: Fausto Arinos de Almeida Barbuto (Calgary, Canada) #
#   Date: May 16, 2002                                          #
#   E-mail: fausto_barbuto@yahoo.ca                             #
#                                                               #
#   Reference:                                                  #
#   Huddleston, T. and Byrne, P: "Numerical Inversion of        #
#   Laplace Transforms", University of South Alabama, April     #
#   1999 (found at http://www.eng.usouthal.edu/huddleston/      #
#   SoftwareSupport/Download/Inversion99.doc)                   #
#                                                               #
#   Usage: just invoke Zakian(t), where t>0.                    #
#                                                               #
#################################################################

#   We need cmath because F(s) is a function operating on the
#   complex argument s = a + bj
from cmath import *

def Zakian(t):
#   Tupple "a", of five complex members.
    a = 12.83767675+1.666063445j, 12.22613209+5.012718792j,\
    10.93430308+8.409673116j, 8.776434715+11.92185389j,\
    5.225453361+15.72952905j

#   Tupple "K", of five complex members.
    K = -36902.08210+196990.4257j, 61277.02524-95408.62551j,\
    -28916.56288+18169.18531j, +4655.361138-1.901528642j,\
    -118.7414011-141.3036911j

    sum = 0.0

#   Zakian's method does not work for t=0. Check that out.
    if t == 0:
        print "\n"
        print "ERROR:   Inverse transform can not be calculated for t=0"
        print "WARNING: Routine zakian() exiting. \n"
        return ("Error");

#   The for-loop below is the heart of Zakian's Inversion Algorithm.
    for j in range(0,5):
        sum = sum + (K[j]*Fs(a[j]/t)).real
 
    return (2.0*sum/t)

#   The Laplace function F(s) is defined here.
def Fs(s):
    return 1.0/(s-1.0)

#   Function Zakian(t) is invoked.
print Zakian(1.0)
