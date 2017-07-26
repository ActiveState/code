def div(a,b,t):
      
    a1=str(a)
    if  "." in  a1:
        d1, d2 =a1.split(".")
        d2=d2.ljust(t,"0")    
    else:
        d1=a1
        d2="0"*t
           
    c=[];r1=0
    for i in d1:
            d11=int(str(r1)+i)
            c1=d11/b
            r1=d11%b
            c.append(c1);
    
    c.append(".")    
    for i in d2:
            d11=int(str(r1)+i)
            c1=d11/b
            r1=d11%b
            c.append(c1);
    
    
    c = "".join(map(str, c))
    while c[0] =="0": c =c[1:]
    if c[0]==".": c ="0"+c 
       
    return c 

print div(15,23,150)
