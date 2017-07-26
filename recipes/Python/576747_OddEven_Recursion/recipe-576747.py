#On the name of ALLAH
#Author : Fouad Teniou
#Date : 9/05/09
#version :2.4

""" 

OddEvenRecursion program uses a recursion function
to calculate the sum of odd or even numbers less or equal
to the odd or the even number entered by the user
and it produce a set of these numbers. 

"""

# Starting with an empty list.
list_A = []

def OddEvenRecursion(number):
    """ Returns a set and a sum of numbers in the set using recursion """
    
    try:
        #Append the list with odd or even numbers
        list_A.append(number)
    
        if number == 0 or number == 1 or number == -1:
            # Display the even numbers' set and the sum of these numbers
            print "\n<The numbers' set : %s \n\n<And the sum is :" % \
              list_A
            return number
        elif number < 1:
            return number + OddEvenRecursion(number + 2)
        else:
            return number + OddEvenRecursion(number - 2)

    except TypeError:
        print 'Please enter an integer.'
    
if __name__ == "__main__":
    
    # testing an odd value.
    odd = OddEvenRecursion(7) 
    print odd
    # Empty the list
    del list_A[:]
    # testing a negative odd  value.
    negativeOdd = OddEvenRecursion(-7) 
    print negativeOdd
    # Empty the list
    del list_A[:]    
    # testing an even value.
    even = OddEvenRecursion(8) # testing an even value.
    print even
    # Empty the list
    del list_A[:]
    # testing a negative even value.
    negativeEven = OddEvenRecursion(-8) # testing an even value.
    print negativeEven

-----------------------------------------------------------------------------------------------

# c:\Python26>python "C:\Users\Fouad Teniou\OddEvenR7

# <The numbers' set : [7, 5, 3, 1]

# <And the sum is :
# 16

# <The numbers' set : [-7, -5, -3, -1]

# <And the sum is :
# -16

# <The numbers' set : [8, 6, 4, 2, 0]

# <And the sum is :
# 20

# <The numbers' set : [-8, -6, -4, -2, 0]

# <And the sum is :
# -20

# c:\Python26> 
# Ref XM + DA
