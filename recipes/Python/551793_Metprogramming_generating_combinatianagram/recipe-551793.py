import string
#the string that we want to test the combination
strng = "131"
#the size of the string
size = len(strng)
#the string that will contain the program generated
prog = ""
#here we will stock the tabulation
tab = ""
#the variable that will count and b used for the meta variable
i = 0
#the first str meta variable must be initialised
str0 = strng
# a meta variable that will stock the sum of the l meta variable
result = ""


while i < size :
    #we generate a for with l in str meta variable string
    prog+= """%sfor l%s in str%s:\n"""%(tab,i,i)
    if (i+1 != size):
        #then we substract one letter in the sequence
        prog+= """%sstr%s = string.replace(str%s,l%s,"",1)\n"""%(tab+"    ",i+1,i,i)
    # here we stock the sum of the meta variable ex : l0+l1 etc ...
    result += "l%s+"%i
    prog += "%sprint %s\n"%(tab+"    ",result[0:len(result)-1])
    #at the end of the loop
    tab += "    "
    i = i +1

#we print the program
print prog
#we execute the program
exec(prog)
print "the end"

#please note that there could be some doublon in the resultat
