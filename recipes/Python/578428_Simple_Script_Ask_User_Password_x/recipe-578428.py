import sys

def main():

	print '\nPassword Request Program v.02\n'

	
	password = 'abcd'
	pass_try = 0 
	x = 3
	
	while pass_try < x:
		user_input = raw_input('Please Enter Password: ')
		if user_input != password:
			pass_try += 1
			print 'Incorrect Password, ' + str(x-pass_try) + ' more attempts left\n'
		else:
			pass_try = x + 1
			
	if pass_try == x and user_input != password:
		sys.exit('Incorrect Password, terminating... \n')

	print 'User is logged in!\n'		
			
if __name__ == "__main__":
	main()
