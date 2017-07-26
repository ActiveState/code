def primeSieve(x):
    '''
       Generates a list of odd integers from 3 until input, and crosses
       out all multiples of each number in the list.

       Usage:

       primeSieve(number) -- Finds all prime numbers up until number.

       Returns: list of prime integers (obviously).

       Time: around 1.5 seconds when number = 1000000.

       '''
    
    numlist = range(3, x+1, 2)
    counter = 0 # Keeps count of index in while loop
    backup = 0 # Used to reset count after each iteration and keep count outside of while loop
    for num in numlist:
        counter = backup
        if num != 0:
            counter += num
            while counter <= len(numlist)-1: # Sifts through multiples of num, setting them all to 0
                    numlist[counter] = 0
                    counter += num
        else: # If number is 0 already, skip
            pass
        backup += 1 # Increment backup to move on to next index
    return [2] + [x for x in numlist if x]
