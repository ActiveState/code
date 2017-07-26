import sys
import hashlib
import getpass

def process_file(file_name):
	
	user_names = []
	passwords = []
	
	try:
		file_conn = open(file_name)
		data = file_conn.readlines()

		for i in range(len(data)): 
			if i%2 == 0:
				user_names.append(data[i][:-1])
			else:
				passwords.append(data[i][:-1])
			
		file_conn.close()
	except:
		sys.exit('There was a problem reading the file!')
		
	return user_names, passwords

def main(argv):

	if len(argv) != 1:
		sys.exit('Usage: user_pass.py <file_name>')

	print '\nUser & Password Authentication Program v.01\n'

	user_names, passwords = process_file(sys.argv[1])
		
	pass_try = 0 
	x = 3
	
	user = raw_input('Please Enter User Name: ')
	
	if user not in user_names:
		sys.exit('Unkown User Name, terminating... \n')
		
	while pass_try < x:
		user_input = hashlib.sha224(getpass.getpass('Please Enter Password: ')).hexdigest()
		if user_input != passwords[user_names.index(user)]:
			pass_try += 1
			print 'Incorrect Password, ' + str(x-pass_try) + ' more attemts left\n'
		else:
			pass_try = x+1
			
	if pass_try == x:
		sys.exit('Incorrect Password, terminating... \n')

	print 'User is logged in!\n'		
			
if __name__ == "__main__":
	main(sys.argv[1:])
