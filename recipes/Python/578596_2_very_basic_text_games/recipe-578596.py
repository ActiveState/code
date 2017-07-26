############################################################
# - My version on the game "Dragon Realm".
# - taken from the book "invent with python" by Al Sweigart.
# - thanks for a great book Mr Sweigart.
# - this code takes advantage of python 3.
############################################################

#files.py
import random
import time
print('\n\n[--system--] one file is bad the other is good ..guess the right one.\n')
print('\n\nconnecting....')
time.sleep(1)
print('....')
time.sleep(1)
print('....')
time.sleep(1)
print('....')
time.sleep(1)
print('\nconnection established')

def displayIntro():
	print('------------')
	print('SYSTEM FILES')
	print('------------\n')
	print('1.) file.')
	print('2.) file.\n')
	
def chooseOption():
	option = ''
	while option != '1' and option != '2':
		print('which file to download? 1 or 2')
		option = input('user:> ')
		
	return option
	
def checkOption(chosenOption):
	print('\nintialising download....')
	time.sleep(1)
	print('accessing file....')
	time.sleep(1)
	print('downloading....')
	time.sleep(1)
	print('....')
	time.sleep(1)
	print('....')
	time.sleep(1)
	
	goodfile = random.randint(1, 2)
	
	if chosenOption == str(goodfile):
		print('\ndownload complete.')
		print('\nGAME OVER')
	else:
		print('\nfile corrupt')
		print('system infected.')
		print('\nGAME OVER')
		
		
playAgain = 'yes'
while playAgain == 'yes':
	displayIntro()
	optionNumber = chooseOption()
	checkOption(optionNumber)
	
	print('\ndownload again? .... (yes or no)')
	playAgain = input('user:> ')

############################################################
# - My version of the game "guess the number".
# - taken from the book "invent with python" by Al Sweigart.
# - thanks for a great book Mr Sweigart.
# - this code takes advantage of python 3.
############################################################

# -NOTE - this program will crash if a number is not typed.

#digitcode.py
import random
import time

guessesTaken = 0

print('\n\n\n\n\n[--system--] enter code in 15 trys to avoid lockout\n')
print('\nconnecting....')
time.sleep(1)
print('....')
time.sleep(1)
print('....')
time.sleep(1)
print('....')
time.sleep(1)
print('connection established\n')
print('---------------------')
print('  MAINFRAME - LOGIN  ')
print('---------------------')
print('\nenter 3 digit access code..')

number = random.randint(000, 999)
while guessesTaken < 15:
	print()
	guess = input('user:> ')
	guess = int(guess)
	
	guessesTaken = guessesTaken + 1
	
	if guess < number:
		print('\nACCESS - DENIED  -code to low')
		
	if guess > number:
		print('\nACCESS - DENIED  -code to high')
		
	if guess == number:
		break
		
if guess == number:
	guessesTaken = str(guessesTaken)
	print('\nverifying ....')
	time.sleep(1)
	print('\nauthenticating ....')
	time.sleep(1)
	print('....')
	time.sleep(1)
	print('....')
	time.sleep(1)
	print('\nACCESS - GRANTED')
	print('\nGAME OVER\n')
	exit(0)
	
if guess != number:
	number = str(number)
	print('\n....')
	time.sleep(1)
	print('\n....')
	time.sleep(1)
	print('\nSYSTEM LOCKED  -the code was ' + number)
	print()
	exit(0)
	
	
