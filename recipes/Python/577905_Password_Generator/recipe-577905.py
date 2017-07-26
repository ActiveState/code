##Author: ATC
##Please score this on activestate

import string, random

print "How many characters would you like the password to have?"
print "Must be nine or more"
length = input ()


password_len = length

password = []

for group in (string.ascii_letters, string.punctuation, string.digits):
    password += random.sample(group, 3)

password += random.sample(
                 string.ascii_letters + string.punctuation + string.digits,
                 password_len - len(password))

random.shuffle(password)
password = ''.join(password)


print password
