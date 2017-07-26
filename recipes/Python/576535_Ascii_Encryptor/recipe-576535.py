def encrypt(string):
    a = string
    new_string = ''
    for x in a:
        new_string = new_string+str(ord(x))+' '
    return new_string
def unencrypt(string):
    a = string
    new_string = ''
    b = a.split()
    for x in b:
        new_string = new_string+chr(int(x))
    return new_string
