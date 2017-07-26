import random
import string

pass_gen = lambda length, ascii =  string.ascii_letters + string.digits + string.punctuation: "".join([list(set(ascii))[random.randint(0,len(list(set(ascii)))-1)] for i in range(length)])
