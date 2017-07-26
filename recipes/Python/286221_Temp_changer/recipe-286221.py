# Temp changer by Josh Bailey (Riddle)
# July 10 '04

def print_options():
	print "Options:"
	print " 'p' print options"
	print " 'c' convert celsius to fahrenheit"
	print " 'f' convert fahrenheit to celsius"
	print " 'k' convert celsius to kelvin"
	print " 'x' convert fahrenheit to kelvin"
	print " 'q' quit the program"

	
def celsius_to_fahrenheit(c_temp):
	return (9.0/5.0*c_temp+32)
def fahrenheit_to_celsius(f_temp):
	return (f_temp - 32.0)*5.0/9.0
def celsius_to_kelvin(k_temp):
        return (temp + 273)
def fahrenheit_to_kelvin(k_temp2):
        return (temp -32.0)*5.0/9.0 + 273

choice = "p"
while choice != "q":
	if choice == "c":
		temp = input("Celsius temp:")
		print "Fahrenheit:",celsius_to_fahrenheit(temp)
	elif choice == "f":
		temp = input("Fahrenheit temp:")
		print "Celsius:",fahrenheit_to_celsius(temp)
	elif choice == "k":
                temp = input ("Celsius temp:")
                print "Kelvin:",celsius_to_kelvin(temp)
        elif choice == "x":
                temp = input ("Fahrenheit temp:")
                print "Kelvin:",fahrenheit_to_kelvin(temp)
	elif choice != "quit":
		print_options()
	choice = raw_input("option:")
