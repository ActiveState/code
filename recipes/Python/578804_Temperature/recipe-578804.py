def c2f(t):
	return (t*9/5.0)+32

def c2k(t):
	return t+273.15

def f2c(t):
	return (t-32)*5.0/9

def f2k(t):
	return (t+459.67)*5.0/9

def k2c(t):
	return t-273.15

def k2f(t):
	return (t*9/5.0)-459.67

def get_user_input():

	user_input = 0
	while type(user_input) != type(1.0): 
		user_input = raw_input("Enter degrees to convert: ")
		try:
			user_input = float(user_input)
		except:
			print user_input + " is not a valid entry"
	return user_input

def main():

	menu = "\nTemperature Convertor\n\n"+\
	 	"1. Celsius to Fahrenheit\n"+\
		"2. Celsius to Kelvin\n"+\
		"3. Fahrenheit to Celsius\n"+\
		"4. Fahrenheit to Kelvin\n"+\
		"5. Kelvin to Celsius\n"+\
    		"6. Kelvin to Fahrenheit\n"+\
		"7. Quit"
		

	user_input = 0
	while user_input != 7: 
		print menu
		user_input = raw_input("Please enter a valid selection: ")

		try:
			user_input = int(user_input)
		except:
			print user_input + " is not a valid selction, please try again\n"

		if user_input == 1:
			t = get_user_input()
			print str(t) + " degree Celsius is " + str((c2f(t))) + " degree Fahrenheit" 
		elif user_input == 2:
			t = get_user_input()
			print str(t) + " degree Celsius is " + str((c2k(t))) + " degree Kelvin" 
		elif user_input == 3:
			t = get_user_input()
			print str(t) + " degree Fahrenheit is " + str((f2c(t))) + " degree Celsius" 
		elif user_input == 4:
			t = get_user_input()
			print str(t) + " degree Fahrenheit is " + str((f2K(t))) + " degree Kelvin" 
		elif user_input == 5:
			t = get_user_input()
			print str(t) + " degree Kelvin is " + str((k2c(t))) + " degree Celsius" 
		elif user_input == 6:
			t = get_user_input()
			print str(t) + " degree Kelvin is " + str((k2f(t))) + " degree Fahrenheit" 
		elif user_input == 7:
			quit()
		else: 
			print str(user_input) + " is not a valid selection, please try again\n"
	
if __name__ == "__main__":
	main()
