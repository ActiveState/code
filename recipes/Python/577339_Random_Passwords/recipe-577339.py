import random
import string
import time

def mkpass(size=16):
    chars = []
    chars.extend([i for i in string.ascii_letters])
    chars.extend([i for i in string.digits])
    chars.extend([i for i in '\'"!@#$%&*()-_=+[{}]~^,<.>;:/?'])
    
    passwd = ''
    
    for i in range(size):
        passwd += chars[random.randint(0,  len(chars) - 1)]
        
        random.seed = int(time.time())
        random.shuffle(chars)
        
    return passwd
