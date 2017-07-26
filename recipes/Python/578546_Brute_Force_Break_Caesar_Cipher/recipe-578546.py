import sys 

def decrypt(k,cipher):
	plaintext = ''
	
	for each in cipher:
		p = (ord(each)-k) % 126
	
		if p < 32:
			p+=95
						
		plaintext += chr(p)
		
	print plaintext

def main(argv):
	if (len(sys.argv) != 1):
		sys.exit('Usage: brute_ceaser.py')
		
	cipher = raw_input('Enter message: ')
		
	for i in range(1,95,1):
		decrypt(i,cipher)

if __name__ == "__main__":
	main(sys.argv[1:])
