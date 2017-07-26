import sys 

def encrypt(k):
	plaintext = raw_input('Enter plain text message: ')
	cipher = ''
	
	for each in plaintext:
		c = (ord(each)+k) % 126
		
		if c < 32: 
			c+=31
			
		cipher += chr(c)
		
	print 'Your encrypted message is: ' + cipher

def decrypt(k):
	cipher = raw_input('Enter encrypted message: ')
	plaintext = ''
	
	for each in cipher:
		p = (ord(each)-k) % 126
	
		if p < 32:
			p+=95
						
		plaintext += chr(p)
		
	print 'Your plain text message is: ' + plaintext

def main(argv):
	if (len(sys.argv) != 3):
		sys.exit('Usage: ceaser.py <k> <mode>')
		
	if sys.argv[2] == 'e':
		encrypt(int(sys.argv[1]))
	elif sys.argv[2] == 'd':
		decrypt(int(sys.argv[1]))
	else:
		sys.exit('Error in mode type')


if __name__ == "__main__":
	main(sys.argv[1:])
