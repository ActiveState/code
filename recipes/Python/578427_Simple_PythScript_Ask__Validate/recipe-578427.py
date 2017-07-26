import sys

def main():

	print '\nPassword Request Program v.01\n'
	
	password = 'abcd'
	user_input = raw_input('Please Enter Password: ')
	
	if user_input != password:
		sys.exit('Incorrect Password, terminating... \n')
		
	print 'User is logged in!\n'
	
if __name__ == "__main__":
	main()
