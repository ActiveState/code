#!/usr/bin/python3

print('''Welcome to Temperature Calculator. You have three temperature option, 'Celsius', 'Fahrenhet' and 'Kelvin';
or if you wish to exit the program then type exit at any dialog box.''')

def tempCalc():
    selectionType = input('Select type of conversion: \n\na)"Celsius to Fahrenheit" or \n\nb)"Celsius to Kelvin" or \n\nc)"Fahrenheit to Celsius" or \n\nd)"Fahrenheit to Kelvin" or \n\ne)"Kelvin to Celsius" or \n\nf)"Kelvin to Fahrenheit" \n\nEnter Here:')
    if selectionType == ("Celsius to Fahrenheit") or selectionType == ("celsius to fahrenheit") or selectionType == ("CELSIUS TO FAHRENHEIT"):
        c_f = eval(input("\nEnter temperature in Fahrenheit to find Celsius: "))
        print ((1.8 * c_f) + 32)
    elif selectionType == ("Celsius to Kelvin") or selectionType == ("celsius to kelvin") or selectionType == ("CELSIUS TO KELVIN"):
        c_k = eval(input("Enter temperature in Celsius to find Kelvin: "))
        print(c_k + 273)
    elif selectionType == ("Fahrenheit to Celsius") or selectionType == ("fahrenheit to celsius") or selectionType == ("FAHRENHEIT TO CELSIUS"):
        f_c = eval(input("Enter temperature in Fahrenheit to find Celsius: "))
        print((f_c - 32) *(5/9))
    elif selectionType == ("Fahrenheit to Kelvin") or selectionType == ("fahrenheit to kelvin") or selectionType == ("FAHRENHEIT TO KELVIN"):
        f_k = eval(input("Enter temperature in Fahrenheit to Kelvin: "))
        print((5/9 * (f_k - 32) + 273))
    elif selectionType == ("Kelvin to Celsius") or selectionType == ("kelvin to celsius") or selectionType == ("KELVIN TO CELSIUS"):
        k_c = eval(input("Enter temperature in Kelvin to find Celsius: "))
        print(k_c - 273)
    elif selectionType == ("Kelvin to Fahrenheit") or selectionType == ("Kelvin to Fahrenheit") or selectionType == ("KELVIN TO FAHRENHEIT"):
        k_f = eval(input("Enter temperature in Kelvin to find Fahrenheit: "))
        print(((k_f - 273) * 1.8 ) + 32)
    elif selectionType == ('') or selectionType == (' '):
        print("Please make a selection. A blank input is not acceptable")
        tempCalc()
    elif selectionType == ("exit") or selectionType == ("Exit") or selectionType == ("EXIT") or selectionType == ("Quit") or selectionType == ("QUIT") or selectionType == ("quit"):
         exit()
    else:
        print("PLEASE RECHECK THE SPELLING, AND ENTER YOUR CHOISE AGAIN. THANK YOU")
        tempCalc()


tempCalc()

def loop():
    restartProgram = input('''
Would you like to try again?:''')
    while restartProgram == ("Yes") or restartProgram == ("yes") or restartProgram == ("YES"):
        return tempCalc()
    while restartProgram != ("Yes") or restartProgram != ("yes") or restartProgram != ("YES") or restartProgram != ("No") or restartProgram != ("no") or restartProgram != ("NO"):
        print ("Please reselect your decision again.")
        tempCalc()
    else:
        while restartProgram == ("No") or restartProgram == ("no") or restartProgram == ("NO"):
            print("thank you for using our calculator, hope to see you agin later")
            exit()


while True:
    loop()
