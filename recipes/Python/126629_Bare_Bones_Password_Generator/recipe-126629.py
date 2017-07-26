import string
import whrandom

def generatePassword(minlen=5, maxlen=10):
 chars = string.letters + string.digits
 passwd = ""
 
 # determine password size (randomly, but between the given range)
 passwd_size = whrandom.randint(minlen, maxlen)

 for x in range(passwd_size):
  # choose a random alpha-numeric character
  passwd += whrandom.choice(chars)

 return passwd

print generatePassword()
