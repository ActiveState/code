import passwordadvisor
import random
import string
import re
import sys 
import math

def ex1(num):

	password = ''
	for i in range(int(num)):
		password += chr(random.randint(33,126))
	
	return password
	
ex2 = lambda length, ascii =  string.ascii_letters + string.digits + string.punctuation: "".join([list(set(ascii))[random.randint(0,len(list(set(ascii)))-1)] for i in range(length)])

def ex3(argv):
    
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
	
	return ''.join(random.sample(password,len(password)))
		
def bit_strength(password):
	return str(math.floor(len(password)*math.log(94,2)))
		
def checker2(argv):

	example_1 = ex1(argv[1])
	print example_1 + ' ' + bit_strength(example_1)
	
	example_2 = ex2(int(argv[2]))
	print example_2 + ' ' + bit_strength(example_2)
	
	example_3 = ex3([argv[3],argv[4],argv[5],argv[6]])
	print example_3 + ' ' + bit_strength(example_3)

def main(argv):
	if (len(sys.argv) != 7):
		sys.exit('Usage: ex4.py <length1> <length2> <upper_case> <lower_case> <digit> <special_characters>')
		
	checker2(sys.argv)

if __name__ == "__main__":
	main(sys.argv[1:])
