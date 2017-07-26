import sys

def main(argv):

	if len(argv) != 1:
		sys.exit('Usage: pass_auth3.py <file_name>')

	print '\nPassword Request Program v.03\n'

	try:
		file_conn = open(sys.argv[1])
		password = file_conn.readline()[:-1]
		file_conn.close()
	except:
		sys.exit('There was a problem reading the file!')
		
	pass_try = 0 
	x = 3
	
	while pass_try < x:
		user_input = raw_input('Please Enter Password: ')
		if user_input != password:
			pass_try += 1
			print 'Incorrect Password, ' + str(x-pass_try) + ' more attempts left\n'
		else:
			pass_try = 4
			
	if pass_try == x and user_input != password:
		sys.exit('Incorrect Password, terminating... \n')

	print 'User is logged in!\n'		
			
if __name__ == "__main__":
	main(sys.argv[1:])
