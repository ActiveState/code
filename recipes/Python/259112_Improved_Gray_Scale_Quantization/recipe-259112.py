"""
Improved Gray Scale (IGS) Quantization implementation
IGS codes are used for the elimination of false contouring in images,
and image compression.
This Python program generates the IGS codes for a set of input
gray level values.

(c) 2003 Premshree Pillai (24/12/03)
http://www.qiksearch.com/
"""

import sys

def dec2bin(num):
	out = []
	while(num != 0):
		out.append(num % 2)
		num = num / 2
	out = pad(out)
	return out

def pad(the_list):
	while(len(the_list) != pix_depth):
		the_list.append(0)
	return the_list

def bin2dec(the_list):
	sum = 0
	i = 0
	while(i < len(the_list)):
		sum = sum + pow(2,i) * the_list[i]
		i = i + 1
	return sum

def rev(the_list):
	i = 0
	while(i < len(the_list)/2):
		temp = the_list[i]
		the_list[i] = the_list[len(the_list) - i - 1]
		the_list[len(the_list) - i - 1] = temp
		i = i + 1
	return the_list

def extractHigherBits(the_list):
	out = []
	i = 0
	while(len(out) != igs_len):
		out.append(the_list[len(the_list) - 1 - i])
		i = i + 1
	return(rev(out))

def extractLowerBits(the_list):
	out = []
	i = 0
	while(len(out) != igs_len):
		out.append(the_list[i])
		i = i + 1
	return(out)

def add(list1,list2):
	out = []
	carry = 0
	i = 0
	while(i < len(list1)):
		out.append(list1[len(list1) - 1 - i] ^ list2[len(list1) - 1 - i] ^ carry)
		if(list1[len(list1) - 1 - i] == list2[len(list1) - 1 - i] == 1):
			carry = 1
		else:
			carry = 0
		i = i + 1
	return rev(out)

def allOnes(the_list):
	if(0 in the_list):
		return 0
	else:
		return 1
	
def main():
	global pix_depth,igs_len
	pix_depth = int(raw_input("Enter pixel depth (i.e., bits per pixel): "))
	igs_len = pix_depth / 2
	num_pixels = int(raw_input("Enter number of pixels: "))
	pixels = []
	igs = []
	i = 0
	while(len(pixels) != num_pixels):
		print "Enter pixel ",(i + 1),":"
		pixels.append(int(raw_input()))
		if(pixels[i] > pow(2,pix_depth) - 1):
			print "With a pixel depth of", pix_depth,", maximum allowable gray level is", pow(2,pix_depth) - 1
			print "Please run the program again!"
			sys.exit()
		pixels[i] = dec2bin(pixels[i])
		i = i + 1
	pixels2 = []
	pixels2 = pixels
	sum = []
	sum = pad(sum)
	sum = pixels[0]
	sum = rev(sum)
	igs.append(extractLowerBits(sum))
	i = 1
	while(len(igs) != num_pixels):
		toAdd = rev(pad(extractLowerBits(rev(sum))))
		if(not(allOnes(extractHigherBits(pixels2[i - 1])))):
			sum = add(rev(pixels[i]),toAdd)
		else:
			sum = rev(pixels[i])
		igs.append(extractLowerBits(sum))
		i = i + 1
	j = 0
	print "\nDecimal\t\tGray Level\t\t\tIGS Code"
	print "-------------------------------------------------------------"
	while(j < len(igs)):
		if(j == 0):
			num = bin2dec(pixels[j])
		else:
			num = bin2dec(rev(pixels[j]))
		print num, "\t\t", rev(pixels[j]), "\t", igs[j]
		j = j + 1

main()

print "\nPress <enter> to exit..."
if(raw_input()):
	exit
