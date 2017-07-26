# Text Twister
# Nik Uzelac
# Octoer 29, 2009
# This program is self explanitory, if you dont kno what it does by the name.... the ur just retarted.

import time
import random
import os

os.system ('color a')

################## File2List Begin: This code is to read a file into a list ##
## Copy and paste the below code into your program if you wish ##
filein = open("TEXTTWIST_words.txt", "r")
line_list = filein.readlines()

c = 0
while c < len(line_list): # This will go through each item of the list and resave it without the new line character
    line_list[c]=line_list[c].replace('\n', '')  # replaces the newline character by a blank
    c = c + 1
## Copy all the way until here ##
################## File2List End ##########################################
    
print "Type 'start' to play the game and 'exit' to leave  the game"
game = raw_input()
os.system('CLS')

while game == "start" :     
    print "Instructions will be shown momentarily"
    time.sleep(3)
    os.system('CLS')
    
    print "                             INSTRUCTIONS"       
    time.sleep(3)
    print "             you will recive a bunch of scrambled letters"
    time.sleep(4)
    print " rearrange the letters till you get the word that the computer is thinking of"
    time.sleep(6)
    print "           you will get 10 trys before you get the game over"
    time.sleep(4)
    print "                               NOW PLAY"
    time.sleep(2)
    os.system('CLS')
    
    
    randwrd = line_list[random.randint(0,len(line_list)-1)]
    
    time.sleep(23)
          
    
    
    
    
    
    


if game != "start" :
    print "Game closing"
    time.sleep(3)
    
