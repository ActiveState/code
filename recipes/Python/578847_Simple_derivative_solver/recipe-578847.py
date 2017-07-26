def deri():
    coeff=eval(input("Enter the coefficient assuming there is one: "))
    exp=eval(input("Enter the exponent of the coefficient: "))
    if coeff<0 and exp<0:
        print("The derivative is:", abs(coeff*exp),"/(x^", abs((exp-1)),")")
    elif exp>1:
        print("The derivative is:", coeff*exp,"x^", exp-1)
    elif exp==1:
        print("The derivative is:",coeff)
    elif exp==0:
        print("The derivative is: 0")
    elif coeff<0:
        print("The derivative is:", coeff*exp,"x^", exp-1)
    elif coeff==0:
        print("The derivative is: 0")
    elif exp<0:
        print("The derivative is:",coeff*exp,"/(x^",abs(exp-1),")")
deri()
