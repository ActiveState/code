#Dont know if this has been done
#a lot before, but I
#got inspired from the web site
#http://p-nand-q.com/python/stupid_lambda_tricks.html
#and tried to write a lambda that
#is a complete program, except for
#the import.
#Sure a lot of fun to write.
#
import sys #For the write function


#All variables are inside of the lambda
#
(lambda dbg=1, n=(lambda:0):

   #start main lambda body
   (
     #List of characters that we filter out
     #of user input
     setattr(n, 'letrs', ['a', 'b', 'c', 'd', 'e',
     'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
     'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
     'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
     'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
     'W', 'X', 'Y', 'Z', 
     '.', ',', ';', ':', '*', '-', '_', '#', '@', '$', '%',
     '^', '&', '(', ')', '{', '}', '[', ']', '+', '=',
     '<', '>', '/', '?', ' ' ]),
     
     #make functions n.prit, n.fac, etc.
     #Use write function from p-nand-q.com web site
     
     setattr(n, 'prit', lambda *s:
        sys.stdout.write(' '.join(map(str, s) + ['\n'] ))),
     
     setattr(n, 'fac', lambda m, ak:
       ((m < 1 and [ak]) or [n.fac(m-1, m*ak)] )[0]),

     
     #Variable to test whether we get out of loop
     setattr(n, 'outvr', 1),

     #Use list comprehension to loop thru tuple
     #until input is 0, or preset number of
     #times thru the loop
     
     [(
     
     #Get user input
     setattr(n, 'b', raw_input('Enter a number: ')),

     #Filter out letters from string
     setattr(n, 'c', [i for i in n.b if not i in n.letrs]),

     #Join list back to string
     setattr(n, 'dt', ''.join(n.c)),

     #Check if we get the empty string
     setattr(n, 'd', (n.dt == '' and '0' or n.dt)),

     #For debug
     (dbg and n.prit('n.d:',n.d)),
    
     #If len of string is 0, return 1, else return int of string
     setattr(n, 'e', ( len(n.d) <= 0 and 0 or int(n.d))),

     #Set variable to see if we get out of loop
     setattr(n, 'outvr', n.e),
     #For debug
     (dbg and n.prit('n.outvr:', n.outvr)),
     
     #Find factorial
     setattr(n, 'f', n.fac(n.e, 1)),
     n.prit('Factorial of', n.e, 'is:', n.f),

     
     #Make lists of factorials 
     setattr(n, 'faclis', [(i, n.fac(i,1)) for i in range(n.e+1)] ),
     
     #print lists of facs 
     n.prit('Fac list:', n.faclis),
          
     
    ) for j in range(100) if n.outvr > 0 ] #end loop

   )#end main lambda 


)(dbg=0) #Call lambda program
