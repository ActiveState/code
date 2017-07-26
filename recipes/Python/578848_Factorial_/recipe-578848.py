def fact():
    number=eval(input("Enter a number to get the factorial: "))
    initialvalue=1
    if number>0:
        for number in range(number,1,-1):
            initialvalue=initialvalue*number
        print(initialvalue)
    elif number==0:
        print(1)
    elif number<0:
            for number in range(number, -1, 1):
                initialvalue=initialvalue*number
            print(-initialvalue)
fact()
