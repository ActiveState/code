################################################################
# program name: least common multiple and gratest common facter
# author: max baseman
# email: dos.fool@gmail.com
# date: 01/16/07
# description: a program to find the LCM
#   and gcf of three given numbers
#
# 
################################################################
print
print
print"enter three numbers to get the LCM and gcf of"
num1=input("number 1 >")
num2=input("number 2 >")
num3=input("number 3 >")
#find the lowest number
if num1 < num2 and num1 < num3:
    low = num1
elif num2 < num1 and num2< num3:
    low = num2
elif num3 < num1 and num3 < num2:
    low = num3
# find the highest number
if num1 > num2 and num1 > num3:
    high=num1
elif num2 > num1 and num2 > num3:
    high=num2
elif num3 > num1 and num3 > num2:
    high=num3
# start at the largest number because the LCM cant be smaller then the highist number
number=high
#loop till finds the lowest number
while 1:
    numtest=number+.0
    if numtest/num1 == number/num1:
        if numtest/num2 == number/num2:
            if numtest/num3 == number/num3:
                break
    number=number+1
LCM=number
#apply number to LCM so that i can keep useing number for GCF
number=2
while number <=  low:
    numtest=number+.0
    if num1/numtest == num1/number:
        if num2/numtest == num2/number:
            if num3/numtest == num3/number:
                break
    number=number+1
else:
    number=1
GCF=number
print
print
print"the LCM was",LCM,"and the GCF was",GCF
