import random
#it just gets the octal representation of text and replace /
#by randomly 8 or 9 as octal doesn't have it
def OctalEncode(text):
    s = ''
    #convert to octal string representaion
    for ch in text:
        s = s +'\\%o'%(ord(ch))
    es = ''
    #replace / by 8 or 9
    for ch in s:
        if ch == '\\':
            if random.randrange(2) == 0:
                es=es+'8'
            else:
                es=es+'9'
        else:
            es=es+ch
    return es

#replace 8 and 9 by / and u have ur string back    
def OctalDecode(text):
    ds = text.replace('8','\\')
    ds = ds.replace('9','\\')
    exec 'ds ="'+ds+'"'
    return ds

#octal encode text and passwd and multiply
def Encrypt(text,passwd):
    etext = long(OctalEncode(text))
    epasswd = long(OctalEncode(passwd).replace('8','9'))#must be unique
    e = etext*epasswd
    return str(e)

#divide encode string by octal encode of passwd and u get ur string back
def Decrypt(etext,passwd):
    epasswd = long(OctalEncode(passwd).replace('8','9'))#must be unique
    e = long(etext)/epasswd
    return OctalDecode(str(e))

es = Encrypt('python rules','anurag')
print es
print Decrypt(es,'anurag')
