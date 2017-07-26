#On the name of ALLAH and may the blessing and peace of Allah 
#be upon the Messenger of Allah Mohamed Salla Allahu Aliahi Wassalam.
#Author : Fouad Teniou
#Date : 9/02/10
#version :2.6

"""
My program Binary_Decimal_Systems Recursion uses a Recursion method
in both binary_function and decimal_function, whether converting a
number from decimal to binary or vice versa, and in both functions it
applies mathematics' operations on the number entered by the user
until it reaches its base case value, where the function returns a
final value and the recursion stops and produce whether a binary or a
decimal number.
"""

import re

# Starting with an empty list.
binary_list = []

def binary_function(value):
    """
    It converts a decimal number into a binary number by using
    a recursion function.
    """
      
    try:
        binary_string = ''
        
        #Append binary_list 
        binary_list.append(value%2) 

        # recursion base cases 
        if value == 0 or value == 1 or value == -1:
            binary_list.reverse()
        
            for item in binary_list:
                #Append binary_string 
                binary_string += str(item)
                
            # Convert string to an int.
            return int(binary_string)
              
        else:
            if value > 0:
                return binary_function(value/2)
        
            else:
                return binary_function(-value/2)*-1
            
    #Raise TypeError if input is not numerical
    except TypeError:
        print 'Please enter an integer.'
        
def decimal_function(number):
    """
    It converts a binary number into a decimal number by using
    a re and a recursion function.
    """

    decimal_sum = 0
    #regular expression substitution
    transform = re.sub("(]?\w+)(\w{1})", '\g<1>.\g<2>',str(number))

    for arg in str(number):
        
        if  arg[0] != '-' and arg != '.' and int(arg) != 0 and int(arg)!= 1 :
            raise TypeError,\
              "\n<binary numbers should be composed of 0 and 1 digits only "
     
    try:   
        # recursion base case
        if number == transform:
            for item in xrange((len(number)-1)/2,-2,-1):
                for res in xrange(0,len(number)):
                    if transform[res].isdigit():
                        next_item = 2**item * int(transform[res])
                        item -= 1
                        decimal_sum += next_item

                return decimal_sum
        else:
            if number > 0:
                return decimal_function(transform)
        
            else:
                return decimal_function(transform)*-1
            
    #Raise TypeError if input is not a binary number          
    except TypeError,exception:
        print exception
     
if __name__ == '__main__':
    
    convert_binary = binary_function(37)
    print convert_binary
    del binary_list[:]
    convert_decimal = decimal_function(100101)
    print convert_decimal
    convert_binary1 = binary_function(-37)
    print convert_binary1
    del binary_list[:]  
    convert_decimal = decimal_function(-100101)
    print convert_decimal

##############

# FTpython "C:\Users\binary_decimal_Sys.py"
# 100101
# 37
# -100101
# -37

# FT
