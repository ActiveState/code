## Dynamic function parameters using annotations  
Originally published: 2012-02-22 22:29:11  
Last updated: 2012-02-22 22:31:02  
Author: pavel   
  
Python default values for keyword arguments are evaluated only once and not on every function call. For example following function will not work as user may expect:

    def printNow(l=[], now=datetime.now()):
        l.append(len(l))
        
        print('List:', l, ' id:', id(l))
        print('Now:', now)
    
    
    for i in range(3):
        printNow()
        print()

The "dynamic" decorator solves problem by evaluating callables, that are assigned to parameters using annotations syntax (see PEP 3107).