#!/usr/bin/python3
# Author: pantuts

binary = []
def strBin(s_str):
	for s in s_str:
	    if s == ' ':
	        binary.append('00100000')
	    else:
	        binary.append(bin(ord(s)))
s_str = input("String: ")
strBin(s_str)

b_str = '\n'.join(str(b_str) for b_str in binary) # print as type str
# replace '\n' to '' to output in one line without spaces, ' ' if with spaces

print(b_str.replace('b',''))
