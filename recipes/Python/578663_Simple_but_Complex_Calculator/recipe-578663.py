done = False
while not done:

    import cmath
    import time
    import math
    import Audio_mac
    print "+--------------------------+"
    print "|RAW_CALCULATOR 0.6 (BASIC)|"
    print "|A)Addition                |"
    print "|B)Subtraction             |"
    print "|C)Multiplication          |"
    print "|D)Division                |"
    print "|E)Exponents               |"
    print "|F)Square Root             |"
    print "+--------------------------+"
    usr_choice = raw_input (">>")
    if usr_choice == "A" or usr_choice == "a":
        print "What is A?"
        a = input (">>")
        print "What is B?"
        b = input (">>")
        print "PROCESSING DATA"
        time.sleep(0.8)
        c = a + b
        print c
    if usr_choice == "B" or usr_choice == "b":
        print "What is A?"
        a = input (">>")
        print "What is B?"
        b = input (">>")
        print "PROCESSING DATA..."
        time.sleep(0.8)
        c = a - b
        print c
    if usr_choice == "C" or usr_choice == "c":
        print "What is A?"
        a = input (">>")
        print "What is B?"
        b = input (">>")
        print "PROCESSING DATA..."
        time.sleep(1.8)
        c = a * b
        print c
    if usr_choice == "D" or usr_choice == "d":
        print "What is A?"
        a = input (">>")
        print "What is B?"
        b = input (">>")
        print "PROCESSING DATA..."
        time.sleep(1.8)
        c = a/b
        print c
    if usr_choice == "E" or usr_choice == "e":
        print "What is A?"
        a = input (">>")
        print "What is B?"
        b = input (">>")
        print "PROCESSING DATA..."
        time.sleep(1.8)
        c = a**b
        print c
    if usr_choice == "F" or usr_choice == "f":
        print "What is A?"
        a = input (">>")
        print "PROCESSING DATA..."
        time.sleep(1.8)
        c = math.sqrt(a)
        print c
    if usr_choice == "42":
        print "The answer to the universe life and everything!"
        time.sleep(1.8)
        print "BLOODY FORTY TWO!"
    print ("Try Again? Y/N")
input = raw_input(">>")
if input == "N" or input == "n":
    done = True
