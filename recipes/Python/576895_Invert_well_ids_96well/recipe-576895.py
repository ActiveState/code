#!/usr/bin/python
#for inverting the plate order when mixups occur!

##e.g. input file looks like
##B1	B3	B5	B7	B9	B11	B13	B15	B17	B19	B21	B23
##D1	D3	D5	D7	D9	D11	D13	D15	D17	D19	D21	D23
##F1	F3	F5	F7	F9	F11	F13	F15	F17	F19	F21	F23
##H1	H3	H5	H7	H9	H11	H13	H15	H17	H19	H21	H23
##J1	J3	J5	J7	J9	J11	J13	J15	J17	J19	J21	J23
##L1	L3	L5	L7	L9	L11	L13	L15	L17	L19	L21	L23
##N1	N3	N5	N7	N9	N11	N13	N15	N17	N19	N21	N23
##P1	P3	P5	P7	P9	P11	P13	P15	P17	P19	P21	P23

input=open('xa','r')
L=input.readlines() #reads lines into list
L.reverse() #reverse rows
for row in L:
##    print row
    splitrow = row.split("\t")
    splitrow.reverse() #reverse column
    newwell=[]
    newwell.extend(splitrow)
    print newwell
        
