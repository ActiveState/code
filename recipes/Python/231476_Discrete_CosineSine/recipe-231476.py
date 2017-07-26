##################################################################################
##
##	Author:		Premshree Pillai
##	Date:		27/10/03	
##	File Name:	dct-dst.py
##	Description:	-Discrete Cosine/Sine Transformations
##	Website:	http://www.qiksearch.com
##	Category:	Math
##
##################################################################################

from math import *

n = 4.0
a = [[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0]]
alpha = [0.0,0.0,0.0,0.0]

tempCount = 0
while(tempCount < 4):
    if(tempCount == 0):
        alpha[tempCount] = (1.0 / n)**0.5
    else:
	alpha[tempCount] = (2.0 / n)**0.5
    tempCount = tempCount + 1

i = 0
option = raw_input("Enter choice (DCT=0, DST=1): ")
while(i < 4):
    j = 0
    while(j < 4):
        a[i][j] = alpha[j] * cos(((2.0 * i + 1.0) * j * pi) / (2.0 * n))
        if(option == 1):
		a[i][j] = (2.0 / (n + 1.0)) * sin((i + 1.0) * (j + 1.0) * pi/(n + 1.0))**0.5
	j = j + 1
    i = i + 1

i = 0
while(i < 4):
    j = 0
    while(j < 4):
        u = 0
	print "\nPattern[",i,",",j,"]\n"
	while(u < 4):
            v = 0
            buf = ['']
	    while(v < 4):
		buf.append(a[u][i] * a[v][j])
                v = v + 1
                continue
            print buf[1],"\t",buf[2],"\t",buf[3],"\t",buf[4]
            u= u + 1
        if(i == 3 and j == 3):
            break
        while(raw_input()):
            continue
	j = j + 1
    print "\n"
    i = i + 1
