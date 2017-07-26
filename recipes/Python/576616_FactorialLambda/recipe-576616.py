#On the name of ALLAH and may the blessing and peace of Allah 
#be upon the Messenger of Allah Mohamed Salla Allahu Aliahi Wassalam.
#Author : Fouad Teniou
#Date : 13/01/09
#version :2.4

import random

class NegativeNumberError(ArithmeticError):
    """ attempted imporper operation on negative number"""
    
    pass

class ZeroNumberException(ArithmeticError):
    """ attempted operation on zero with an agreed solution"""
    
    pass

def errors(number):
    """ Raises NegativeNumberError if number less than 0, and
    raises ZeroNumberException if number is equal to 0."""
    
    if number < 0:
        raise NegativeNumberError,\
            "\n<The number must be greater or equal to 0 \n"
    elif number == 0:
        raise ZeroNumberException,\
            "\n<It is agreed per convention that 0!= 1 \n"
    elif number >0:
        pass 
    
    return number

while 1:
    #get users answer to use Factorial program or exit the while loop 
    Answer = raw_input("\n<Would you like to use Factorial program, yes or no?:\t")

    if Answer == "yes":
      
        print '\n\t\t\t','','\5'*49
        print '\t\t\t\t  Welcome to Factorial n! Program'
        print '\t\t\t','','\5'*49,'\n'
    
        try:
            #get users entered numbers and compute factorial 
            userValue = float(raw_input('<Please enter a number :\t'))
            errors(userValue)

            Y=random.randrange(int(userValue)+1)

            mult = lambda d:reduce(lambda x,y:x*y,range(1,int(Y)+1))

            print '\n<A random list of factorial between 0 and %s will be displayed' % int(userValue)
            print '\n\t\t',str(0)+'!=',int(1),'\n'
            for Y in range(1,int(Y)+1):
                print '\n\t\t',str(Y)+'!=',mult(int(Y)),'\n'
                
        #Factorial raise ValueError if input is not numerical
        except ValueError:
            print "\n<The entered value is not a number"
        
        #Factorial raises Negative number exception
        except NegativeNumberError,exception:
            print exception
        
        #Factorial raises zero number exception
        except ZeroNumberException,exception:
            print exception 
      
    elif Answer == "no":
        break

#############################################################################
#c:\hp\bin\Python>python "C:\Documents\Programs\classes\Factorial7
#
#<Would you like to use Factorial program, yes or no?:   yes
#
#                         ?????????????????????????????????????????????????
#                                  Welcome to Factorial n! Program
#                         ?????????????????????????????????????????????????
#
#<Please enter a number :        7
#
#<A random list of factorial between 0 and 7 will be displayed
#
#                0!= 1
#
#
#                1!= 1
#
#
#                2!= 2
#
#
#<Would you like to use Factorial program, yes or no?:   yes
#
#                         ?????????????????????????????????????????????????
#                                  Welcome to Factorial n! Program
#                         ?????????????????????????????????????????????????
#
#<Please enter a number :        -7
#
#"\n<The number must be greater or equal to 0 \n"
#
#
#<Would you like to use Factorial program, yes or no?:   yes
#
#                         ?????????????????????????????????????????????????
#                                  Welcome to Factorial n! Program
#                         ?????????????????????????????????????????????????
#
#<Please enter a number :        0
#
#<It is agreed per convention that 0!= 1
#
#
#<Would you like to use Factorial program, yes or no?:   yes
#
#                         ?????????????????????????????????????????????????
#                                  Welcome to Factorial n! Program
#                         ?????????????????????????????????????????????????
#
#<Please enter a number :        test
#
#<The entered value is not a number
#
#<Would you like to use Factorial program, yes or no?:   yes
#
#                         ?????????????????????????????????????????????????
#                                  Welcome to Factorial n! Program
#                         ?????????????????????????????????????????????????
#
#<Please enter a number :        7
#
#<A random list of factorial between 0 and 7 will be displayed
#
#                0!= 1
#
#
#                1!= 1
#
#
#                2!= 2
#
#
#                3!= 6
#
#
#               4!= 24
#
#
#                5!= 120
#
#
#<Would you like to use Factorial program, yes or no?:   no
#
#c:\hp\bin\Python>
########################### Factorial ref FT (2 D A Missr)
#########################################################################################

#Version : Python 3.2

#import random
#from functools import reduce

#class NegativeNumberError(ArithmeticError):
#    """ attempted imporper operation on negative number"""
#    
#    pass

#class ZeroNumberException(ArithmeticError):
#    """ attempted operation on zero with an agreed solution"""
#    
#    pass
#
#def errors(number):
#    """ Raises NegativeNumberError if number less than 0, and
#    raises ZeroNumberException if number is equal to 0."""
#    
#    if number < 0:
#        raise NegativeNumberError("\n<The number must be greater or equal to 0 \n")
#    elif number == 0:
#        raise ZeroNumberException("\n<It is agreed per convention that 0!= 1 \n")
#    elif number >0:
#        pass 
#    
#    return number
#while 1:
#    #get users answer to use Factorial program or exit the while loop 
#    Answer = input("\n<Would you like to use Factorial program, yes or no?:\t")
#    if Answer == "yes":
#      
#        print('\n\t\t\t','','\5'*49)
#        print('\t\t\t\t  Welcome to Factorial n! Program')
#        print('\t\t\t','','\5'*49,'\n')
#    
#        try:
#            #get users entered numbers and coompute factorial 
#            userValue = float(input('<Please enter a number :\t'))
#
#            errors(userValue)
#            Y=random.randrange(int(userValue)+1)
#            mult = lambda d:reduce(lambda x,y:x*y,list(range(1,int(Y)+1)))
#
#            print('\n<A random list of factorial between 0 and %s will be displayed' % #int(userValue))
#            print('\n\t\t',str(0)+'!=',int(1),'\n')
#            for Y in range(1,int(Y)+1):
#                print('\n\t\t',str(Y)+'!=',mult(int(Y)),'\n')
#                
#        #Factorial raise ValueError if input is not numerical
#        except ValueError:
#            print("\n<The entered value is not a number")
#        
#        #Factorial raises Negative number exception
#        except NegativeNumberError as exception:
#            print(exception)
#        
#        #Factorial raises zero number exception
#        except ZeroNumberException as exception:
#            print(exception) 
#      
#    elif Answer == "no":
#        break
