# HW.py
# Almost any version of standard text mode Python inside a terminal on Linux OS...
# IMPORTANT! The print() function MUST be a single line only so beware of wordwrapping, etc... etc...
# You may need to edit it if wordwrapping occurs...
# (C)2012, B.Walker, G0LCU...
#
# Edited on 02-04-2012 as per comment by S.D'Aprano.
#
# NOTE:- There is NO malicious intent in this code!!!
# I DO expect, however, that professionals _know_ how to manipulate Linux terminal colours through Python!

reset_term_colours="\033[0m"

f="\033[0;36;41m"
b="\033[0;31;46m"
lines=0

print(reset_term_colours)

for lines in range (0,50,1): print(b)

print(b+" "+f+" "+b+"   "+f+" "+b+"        "+f+" "+b+"     "+f+" "+b+"                "+f+" "+b+"   "+f+" "+b+"              "+f+" "+b+"        "+f+" "+b+"   "+f+" "+b+"\n "+f+" "+b+"   "+f+" "+b+"        "+f+" "+b+"     "+f+" "+b+"                "+f+" "+b+"   "+f+" "+b+"              "+f+" "+b+"        "+f+" "+b+"   "+f+" "+b+"\n "+f+" "+b+"   "+f+" "+b+"  "+f+"   "+b+"   "+f+" "+b+"     "+f+" "+b+"     "+f+"   "+b+"        "+f+" "+b+"   "+f+" "+b+"  "+f+"   "+b+"  "+f+" "+b+" "+f+"   "+b+"  "+f+" "+b+"     "+f+"    "+b+"   "+f+" "+b+"\n "+f+"     "+b+" "+f+" "+b+"   "+f+" "+b+"  "+f+" "+b+"     "+f+" "+b+"    "+f+" "+b+"   "+f+" "+b+"       "+f+" "+b+"   "+f+" "+b+" "+f+" "+b+"   "+f+" "+b+" "+f+"  "+b+"     "+f+" "+b+"    "+f+" "+b+"   "+f+" "+b+"   "+f+" "+b+"\n "+f+" "+b+"   "+f+" "+b+" "+f+"     "+b+"  "+f+" "+b+"     "+f+" "+b+"    "+f+" "+b+"   "+f+" "+b+"       "+f+" "+b+" "+f+" "+b+" "+f+" "+b+" "+f+" "+b+"   "+f+" "+b+" "+f+" "+b+"      "+f+" "+b+"    "+f+" "+b+"   "+f+" "+b+"   "+f+" "+b+"\n "+f+" "+b+"   "+f+" "+b+" "+f+" "+b+"      "+f+" "+b+"     "+f+" "+b+"    "+f+" "+b+"   "+f+" "+b+"       "+f+"  "+b+" "+f+"  "+b+" "+f+" "+b+"   "+f+" "+b+" "+f+" "+b+"      "+f+" "+b+"    "+f+" "+b+"   "+f+" "+b+"\n "+f+" "+b+"   "+f+" "+b+"  "+f+"    "+b+"   "+f+"   "+b+"   "+f+"   "+b+"  "+f+"   "+b+"        "+f+" "+b+"   "+f+" "+b+"  "+f+"   "+b+"  "+f+" "+b+"       "+f+"   "+b+"  "+f+"    "+b+"   "+f+" "+b+"\n\n\n\n\n Hello World!\n\n\n\n\033[0;30;46mPress Ctrl_C to Quit/Stop/Exit...")

print(reset_term_colours)

while 1: pass
