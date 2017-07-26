##################################################################################
##
##	Author:		Premshree Pillai
##	Date:		15/07/03	
##	File Name:	urn.py
##	Description:    -Unique Random Numbers
##                      -Returns a list of specified number of elements from
##                       another list such that each element in the returned
##                       list is unique and random.
##                       See e.g. below.
##	Website:	http://www.qiksearch.com
##
##################################################################################

from random import Random

def pickNums(nums, numArr):
    if(nums > len(numArr)):
        return 0
    pickArr = []
    tempArr = numArr
    i = 0
    while(i < nums):
        g = Random()
        pickArr.append(tempArr[int(round((len(tempArr) - 1) * g.random()))])
        temp = pickArr[len(pickArr)-1]
        count = 0
        for x in tempArr:
            if(x == temp):
                tempArr[count] = 'null'
                tempArr2 = []
                for y in tempArr:
                        if(y != 'null'):
                                tempArr2.append(y)
                tempArr=tempArr2;
                break
            count = count + 1
        i = i + 1
    return pickArr

##
## Create a list
##
myArr = ['1','2','3','4','5','6','7']

##
## The following function call will return a 2-element list, the elements
## of which are derived from myArr. The elements of the returned
## list (say, retArr) are such that each is unique. i.e. if  
## retArr[i] = myArr[j] then no other element of retArr will
## be equal to myArr[j]
##
print pickNums(2,myArr)

##
## You may also call the function like this:
##    
print pickNums(2,['1','2','3','4','5','6','7'])
