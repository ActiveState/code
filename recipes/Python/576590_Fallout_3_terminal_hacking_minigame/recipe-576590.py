#!/usr/bin/python

#
#  Copyright Bill Sharer 2008
#  Distributed under the terms of the GNU General Public License v2 or later
#

#
#  crackerhacker.py is a script I wrote as a Python learning exercise to help
#  solve Fallout 3's "terminal hacking" minigame.  Many of you may already be
#  aware of this annoying mind challenge after playing the popular waste of
#  time from Bethesda Softworks on your favorite pc or console.
#
#  The minigame presents a "green screen" like terminal with what apparently
#  is a dump of some mainframe's password program file.  In amongst the noise
#  are a set of words that are all the same length.  As you hover your mouse
#  over each of these words, that word becomes a guess that you may take on
#  the command line.  The following ascii excerpt of an example screen is
#  taken from DrAgRoS' terminal hacking guide from gamespot.com (I was too
#  lazy to type one on my own)
#
# ---------------------------------------------------------
# ROBCO INDUSTRIES (TM) TERMLINK PROTOCOL                  |
# ENTER PASSWORD NOW                                       |
#                                                          |
# 4 ATTEMPT(S) LEFT : [] [] [] []                          |
#                                                          |
# 0xF92C %*-}'!.-[)#! 0xF9F8 :($-?!!}'%_(                  |
# 0xF938 (>!];-/\[=(, 0xFA04 /?;_;#"]!!:,                  |
# 0xF944 @PARTNERSHIP 0xFA10 %'%{.@@}#?|+                  |
# 0xF950 S=\]%,*?++:] 0xFA1C ="||^<@-|PUR                  |
# 0xF96C #\--(??%=^\? 0xFA28 IFICATION(^S                  |
# 0xF978 ]$/!]'|]=}"| 0xFA34 ECLUSIONIST>                  |
# 0xF984 REPRIMANDING 0xFA40 .,"CONSTRUCT                  |
# 0xF980 :(%CIVILIZAT 0xFA4C ION@'_'=':'>                  |
# 0xF99C ION:(]=%?|{A 0xFA58 =!.;/'+.@'/D                  |
# 0xF908 PPRECIATION' 0xFA64 ISAPPEARING%                  |
# 0xF9A4 :*CONVERSATI 0xFA70 ,]%?<TRANSMI                  |
# 0xF9B0 ON=.:="+$@#< 0xFA7C SSION,}"/'},                  |
# 0xF9BC ['<'%':}!%;+ 0xFA88 \"%\^?<(|APP                  |
# 0xF9C8 '('#'?,.%*!+ 0xFA94 REHENSIVE}<+                  |
# 0xF9D4 =\.\?/(!|#?< 0xFAA0 "<\^+].^^'._                  |
# 0xF9E0 |[)???@?%{CI 0xFAAC ;++}{=/'\ENC                  |
# 0xF9EC RCUMSTANCE_= 0xFAB8 OUNTERING*}; >[]              |
# ---------------------------------------------------------
# 
# 						   ------
# 						   |    |
# 					    POWER  ------
#
#
#  You only have four guesses (although as the guide mentions, there may be ways
#  to reset the challenge).  When you make an incorrect guess, the terminal
#  shows the number of characters that matched the correct guess.  This match
#  count is a character by character comparison of the guess against the correct
#  password.
#
#  You will be permanently locked out of the terminal after four incorrect
#  guesses, but using the script, I have yet to not have the list narrowed down
#  to a single choice by the fourth attempt.
#

words = []
while True :
    line = raw_input("word> ")
    if line != "" :
        words.append(line)
    else :
        break

word_matrix = {}
for word in words :
    word_matrix[word] = {}
    for key in word_matrix.keys() :
        match = 0
        i = 0
        while i < len(key) :
            if key[i] == word[i] :
                match += 1
            i += 1
        word_matches = word_matrix[key]
        word_matches[word] = match
        word_matches = word_matrix[word]
        word_matches[key] = match

for key in word_matrix.keys() :
    word_matches = word_matrix[key]
    nonzero = 0
    sum = 0
    for word in word_matches.keys() :
        if word != key :
            if word_matches[word] > 0 :
                nonzero += 1
                sum += word_matches[word]
    if nonzero > 0 :
        print key, "matches",  nonzero, " avg", sum/nonzero

narrowed = set(words)

while True :
    guesses = []
    guess = raw_input("guess> ")
    if guess == "" :
        break
    matches = input("matches> ")
    word_matches = word_matrix[guess]
    for word in word_matches.keys() :
        if word_matches[word] == matches :
            guesses.append(word)

    narrowed = narrowed & set(guesses)
    for word in narrowed :
        print word
