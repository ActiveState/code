# Filename: perfect.py
a = True
n = 0
while a == True:                           #  To loop the following commands 
    running = True
    while running == True:
        r = 0
        n =  n+ 1
        for x in range(1,n + 1):
            if n%x == 0:                   #  To determine the factors of n
                r = r + x
                if x == n:
                    if  r == 2*n:
                        print n
                        running = False
                    else:
                        running = False
                        
                                 
            
            
