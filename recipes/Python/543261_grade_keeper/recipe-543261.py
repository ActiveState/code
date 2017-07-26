#! /usr/bin/python
# keep record of grades. Made by Caleb Herbert. 0.1-PUBLIC
# NOTE! All letter answers are to be written in quotes (including dates)!
print """############################################
# Welcome to Gradebook! v 0.1              # 
# YOUR LIGHT WEIGHT SCHOOL RECORD MANAGER! #
############################################"""              
subject = raw_input("What is your assignment's subject? ")
# ^^This asks your class subject; assigns it to 'subject'; and is used later. 
date = input('What is the date for your assignment? ')
# ^^This is pretty much the same: but asks the date.
amount = input('What is the number of questions? (NOTE: make all #s from now decimals. e.g.: "5.0" ')
# ^^^This is also the same, but make the number a DECIMAL!
correct = input('How many questions did you get correct? ')
# ^^^The same... make all DECIMALS!
calc = divmod(correct, amount)
#  This is a nice homework trick. Divides correct by amount, assigns to 'calc'
calcx = (correct / amount)
# divides correct by amount; assigns to 'calcx'
text = "***%s*** \n %s | %d out of %d | %s or %s \n" % (date, subject, correct, amount, calc, calcx) 
# creates what will be in your file. assigns to 'text'
print text
# prints what it will put in your file (or append).
fle = raw_input('What should I name the file to put the above data into? ')
# prompts for a filename 
A = input('Do you want this to be appended to an existing file? ') 
# decides to either append,or to create new file. assigns answer to 'A'
print 'Thanks! appending to file... '
if A is 'yes': #if you answered yes:
    fyl = open(fle, 'a')
# the phrase 'fyl' is used to combine open('fle, 'a') with future commands
    fyl.write(text)
# the command assigned to 'fyl' writes your data to the filename you said.
    fyl.close()
# closes the file; job is done.
elif A is 'no': # if you said no, this will happen:
    fyl = open(fle, 'w')
# same as before, but saves the file (see the 'w' instead of 'a'?)
    fyl.write(text)
# same
    fyl.close()
# same
else: # and if nothing was valid...
    print 'Error! Invalid transaction! '
# ...error message! 
print 'Done!'
# says it is done
raw_input("Press <RETURN> to quit.")
# makes you type <enter> to quit.
