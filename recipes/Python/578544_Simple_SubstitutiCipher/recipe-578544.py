import sys

def main(argv):
	if (len(sys.argv) != 2):
		sys.exit('Usage: sub.py <k>')
		
	plaintext = list(raw_input('Enter message: '))
	alphabet = list('abcdefghijklmnopqrstuvwxyz')
	k = int(sys.argv[1])
	cipher = ''
		
	for c in plaintext:
		if c in alphabet:
			cipher += alphabet[(alphabet.index(c)+k)%(len(alphabet))]
		
	print 'Your encrypted message is: ' + cipher
	

if __name__ == "__main__":
	main(sys.argv[1:])
