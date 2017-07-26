def number(number):
    ran=input("range  >")
    ran=ran+1
    from random import randrange
    guessed=[]
    guess=randrange(ran)
    print guess
    guessed.append(guess)
    guesses=1
    guessed=[]
    while guess !=number:
        guess=randrange(ran)
        if guess not in guessed:
            guessed.append(guess)
            guesses=guesses+1
            print guess
        
    print"i got the number",number,"in",guesses,"guesses"
        
    
        
def num(number):
    r=input("range >")+1
    if r<number:
        r=number+1
    guess=r/2
    print guess
    guesses=1
    min = 0
    max = r
    while guess!=number:
        if guess < number:
            min = guess
        else:
            max = guess
        guess = (min + max) / 2
        guesses += 1
        print guess
    print "i got the number",number,"in",guesses,"guesses"   
