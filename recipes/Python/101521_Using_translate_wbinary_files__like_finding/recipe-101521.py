import string

#Translate in python has 2 pieces, a translation table and the translate call.
#The translation table is a list of 256 characters. Changing the order of the #characters is used for mapping

norm = string.maketrans('', '') #builds list of all characters
print len(norm) #256 characters

print string.maketrans('', '')[100] #is the letter d
print string.maketrans('', '')[101] #is the letter e
print string.maketrans('d','e')[100] #is now  also the letter e

#The second piece of translate, is the translate function itself.
#The translate function has 3 parts:

#1)string to translate
#2)translation table  -- always required
#3)deletion list

#Let's start simple and build 
#use translate to get groups of characters
#This can be done because translate's 3rd arg is to delete characters

#build list of all characters
norm = string.maketrans('', '') 

#delete letters
non_letters = string.translate(norm, norm, string.letters) 

#then take the list of non_letters and remove digits
non_alnum = string.translate(non_letters, all_chars, string.digits) 

#You'll notice the length shrinks appropriately as we delete
print len(all_chars),'\t256-(26*2 letters)=',len(non_letters),'\t204-10 digits=',len(non_alnum)

#Norm is a handy list to have around if all you are going to do is delete 
#characters. It would be nice if translate assumed Norm if the translation table arg was null.

#To translate all non-text to a '#', you have to have a one to one mapping for #each character in translate.
#Thus we make use of the python * operator to make a string of '#'
#of the appropriate length
trans_nontext=string.maketrans(non_alnum,'#'*len(non_alnum))

#A full program to examine strings in a binary file for Regents
# would look like this. We use regular expressions to convert all groups
# of '#' to a single '#'

import string,re

norm = string.maketrans('', '') #builds list of all characters
non_alnum = string.translate(norm, norm, string.letters+string.digits) 

#now examine the binary file. If Regents is in it. It contains the copyright
ftp_file=open('f:/tmp/ftp.exe','rb').read()

trans_nontext=string.maketrans(non_alnum,'#'*len(non_alnum))
cleaned=string.translate(ftp_file, trans_nontext)
for i in  re.sub('#+','#',cleaned).split('#'):
    if i.find('Regents')!=-1:
        print 'found it!',i
        break
    if i>5:
        print i
