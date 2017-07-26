# Author: Sam Erickson
# Date: 2/23/2016
#
# Program Description: This program gives the integer coefficients x,y to the
# equation ax+by=gcd(a,b) given by the extended Euclidean Algorithm. 

def extendedEuclid(a,b):
    """
    Preconditions - a and b are both positive integers.
    Posconditions - The equation for ax+by=gcd(a,b) has been returned where
                    x and y are solved.
    Input - a : int, b : int
    Output - ax+by=gcd(a,b) : string
    """
    b,a=max(a,b),min(a,b)
    # Format of euclidList is for back-substitution
    euclidList=[[b%a,1,b,-1*(b//a),a]]
    while b%a>0:
        b,a=a,b%a 
        euclidList.append([b%a,1,b,-1*(b//a),a])
    if len(euclidList)>1:
        euclidList.pop()
        euclidList=euclidList[::-1]
        for i in range(1,len(euclidList)):
            euclidList[i][1]*=euclidList[i-1][3]
            euclidList[i][3]*=euclidList[i-1][3]
            euclidList[i][3]+=euclidList[i-1][1]
        
    expr=euclidList[len(euclidList)-1]
    strExpr=str(expr[1])+"*"+str(expr[2])+" + "+str(expr[3])+"*"+str(expr[4]) \
                +" = "+str(euclidList[0][0])
    return strExpr
