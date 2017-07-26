import random
import sys
import string

def main(argv):

	if (len(sys.argv) != 5):
		sys.exit('Usage: simple_pass.py <upper_case> <lower_case> <digit> <special_characters>')
    
	password = ''
	
	for i in range(len(argv)):
		for j in range(int(argv[i])):
			if i == 0:
				password += string.uppercase[random.randint(0,len(string.uppercase)-1)]
			elif i == 1:
				password += string.lowercase[random.randint(0,len(string.lowercase)-1)]
			elif i == 2:
				password += string.digits[random.randint(0,len(string.digits)-1)]
			elif i == 3:
				password += string.punctuation[random.randint(0,len(string.punctuation)-1)]
	
	print 'You new password is: ' + ''.join(random.sample(password,len(password)))

if __name__ == "__main__":
	main(sys.argv[1:])
