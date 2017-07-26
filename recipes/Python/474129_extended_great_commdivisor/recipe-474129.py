 I am new to programing so Is this code ok? how can i make it faster?


def egcd(a,b):  # a > b > 0  
    """ Extended great common divisor, returns x , y
        and gcd(a,b) so ax + by = gcd(a,b)       """
    
    if a%b==0: return (0,1,b)
    q=[]
    while a%b != 0:
        q.append(-1*(a//b))
        (a,b)=(b,a%b)
    (a,b,gcd)=(1,q.pop(),b)
    while q:(a,b)=(b,b*q.pop()+a)
    return (a,b,gcd)
