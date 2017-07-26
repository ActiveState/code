password  = 'password ' 
upperCount = 0
lowerCount = 0
digitCount = 0
strength = 0



passwordstrength = 'passwordstrength'
x = 0
while x == 0:
   userInput = raw_input ('Enter in a password: ')
   if len(userInput) < 6: # If the passowrd has less the 6 chartacter, it will say Access Denied.
        print "Not valid"

   elif len(userInput) > 12:
        print "Access Denied" # If the password is more than 12 characters, it will say Access Denied.

   else:
        print "Access Accepted" # If the password has more than 6 and less than 12 characters then th password will be accepted.
        x = 1

for password in userInput:
    if password.isupper():
        upperCount = upperCount + 1
    elif password.islower():
        lowerCount = lowerCount + 1
    elif password.isdigit():
        digitCount = digitCount + 1
print "upper case =" +str(upperCount)
print "lower case =" +str(lowerCount)
print "digits=" +str(digitCount)

if upperCount >0:
    strength = strength + 1
if lowerCount >0:
    strength = strength + 1
if digitCount >0:
    strength = strength + 1
    
if strength == 1:
    print "Weak"
  
elif strength == 2:
    print "Medium"

else:
    print "Strong"
