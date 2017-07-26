# Author: Hemanth Sethuram
# Email: hemanthps@gmail.com
# Date: 16 Sep 2005
# Modifications: 
# 27 Jul 2006
#    1. Changed ALPHABETS set. This follows the keyboard layout and their shifted versions.
#    2. Added CONST_STRING
#    3. Added a new password generation function for GeneratePassword() and
#    deprecated the random number based password generation.
#    4. Passphrase is now Identifier + Master Password + CONST_STRING
# 12 Nov 2006
#    1. Added a new Password generation method using base64 encoding. Just use the string
#       representation of the hash and encode it as base64. This becomes the password with
#      alphanumeric characters.
#    2. Renamed the old password generation function to GeneratePasswordWithCharSet()

import getpass, random, sha, string

#The character set used in the password
#!!!CAUTION!!!:
#Do not change this string. Else, you may not get back the same password again

# In every row from top to bottom, move from left to right
# Then in the same order all shifted characters are taken
ALPHABETS = r'''`1234567890-=qwertyuiop[]\asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'''

# if you want passwords containing only alphanumeric strings
ALPHABETS_ALPHANUM = r'''1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'''

ALPHABETS_LIMITED = r'''1234567890qwertyuiopasdfghjklzxcvbnm!@#$%^&<>?QWERTYUIOPASDFGHJKLZXCVBNM'''

CONST_STRING = r"""This is an arbitrary string present just to add some bytes to
the string that will be used to generate the hash. This constant string is added
to the identifier and the master password and fed to the hash function."""

def GetMasterPassword(prompt="Enter Master Password:"):
    """This is the only password that you need to remember. All other passwords
    are generated for you using your master password + the unique identifier for
    an account. This id can be public and need not be a secret."""
    s = getpass.getpass(prompt)
    return s
    
def GetIdentifier(prompt="Enter the Identifier:"):
    """This function gets the unique identifier you want to use for the account.
    e.g. myname@yahoo.com or login.yahoo.com, etc. This id can be public and need 
    not be a secret. You can typically use the site's webpage address or your
    account name as your Id."""
    s = raw_input(prompt)
    return s
    
def GetPasswordLength(prompt="Enter number of letters in the password:"):
    while 1:
        try:
            s = raw_input(prompt)
            n = string.atoi(s)
            if (n > 40):
                print "Only a maximum of 40 characters is allowed"
                continue
            else:
                return n
        except:
            print "Only digits allowed"
            continue

# as mentioned by Walker Hale, future implementation of Random may not generate
# the same number with the same seed. Not safe to use this method.
def GeneratePassword_Deprecated(charset, passString, passLength):
    """This function creates a pseudo random number generator object, seeded with
    the cryptographic hash of the passString. The contents of the character set
    is then shuffled and a selection of passLength words is made from this list.
    This selection is returned as the generated password."""
    l = list(charset)
    s = sha.new(passString)
    r = random.Random(long(s.hexdigest(),16))  
    #r.shuffle(l)
    return "".join(r.sample(l,passLength))

def GeneratePasswordWithCharSet(charset, passString, passLength):
    """This function creates a SHA-1 hash from the passString. The 40 nibbles of
    this hash are used as indexes into the charset from where the characters are
    picked. This is again shuffled by repeating the above process on this subset.
    Finally the required number of characters are returned as the generated
    password"""
    assert passLength <= 40   # because we want to use sha-1 (160 bits)
    charlen = len(charset)
    c1 = []
    n = 0
    s = sha.sha(passString).hexdigest() # this gives a 40 nibble string (160 bits)
    for nibble in s:
        n = (n + string.atoi(nibble,16)) % charlen
        c1.append(charset[n])  # this will finally generate a 40 character list
        
    # Repeat the above loop to scramble this set again
    n = 0
    c2 = []
    for nibble in s:
        n = (n + string.atoi(nibble,16)) % 40   # for 40 nibbles
        c2.append(c1[n])
    
    # Now truncate this character list to the required length and return
    return "".join(c2[-passLength:])
    
def GeneratePasswordBase64(passString, passLength):
    """This function creates a SHA-1 hash from the passString. The 40 nibbles of
    this hash are expressed in base64 format and the first passLength characters
    are returned as the generated password"""
    assert passLength <= 160/6  #because each base64 character is derived from 6 bits
    import base64
    return base64.b64encode(sha.sha(passString).hexdigest())[:passLength]

    
if __name__ == "__main__":
    i = GetIdentifier()
    m = GetMasterPassword()
    n = GetPasswordLength()
    print "Your password is:", GeneratePasswordBase64(i+m+CONST_STRING,n)
