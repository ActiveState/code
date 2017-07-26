def base(num,base):
    """
    Input: num can be any base 10 integer, base can be any positive integer<=10.

    Output: num is returned as a string in the specified base integer.
    """
    from math import log
    
    # Create a list of all possible digits
    digits=[x for x in range(base)]
    
    # Solve for highest base power
    highestExponent=int(log(num,base))

    # Create base expansion list from greatest to least
    baseExpansionList=[base**x for x in range(highestExponent+1)]
    baseExpansionList.reverse()

    # Get digits in base
    newDigits=[]
    for x in baseExpansionList:
        tmp=getDigits(num,x,digits)
        num=num-(tmp*x)
        newDigits.append(tmp)

    # Convert newDigits to str format
    numStr=""
    for x in newDigits:
        numStr+=str(x)
    return numStr
            
def getDigits(num,baseNum,digitsList):
    """
    Input: num, baseNum, and digitsList must all come from base(num,base) as is
    currently specified.

    Output: returns each digit in the output number of base(num,base).
    """
    tmpList=[]
    for x in digitsList:
        if x*(baseNum)>num:
            tmpList.append(x)
    
    return max((set(digitsList)-set(tmpList)))  
