def mcd(a,b):
    r=a
    while (r):
        r=a%b; a=b; b=r 
    return a   

print mcd(120,95)
