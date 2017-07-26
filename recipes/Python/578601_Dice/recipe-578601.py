while again:
    print" Pick a dice: "
    print"4, 6, 12"
    userinput = input("Pick a dice: ")
    if userinput == 4: 
        randomnumber = random.randint(1,4)
        print randomnumber

    if userinput == 6:
        randomnumber = random.randint(1,6)
        print randomnumber

    if userinput == 12:
        randomnumber = random.randint(1,12)
        print randomnumber
   
