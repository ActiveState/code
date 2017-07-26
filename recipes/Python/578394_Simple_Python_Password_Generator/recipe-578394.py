import random
import sys

def main(argv):

	if (len(sys.argv) != 2):
		sys.exit('Usage: simple_pass.py <password_length>')
    
	password = ''
	for i in range(int(argv[0])):
		password += chr(random.randint(33,126))
	
	print 'You new password is: ' + password

if __name__ == "__main__":
	main(sys.argv[1:])
