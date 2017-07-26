#conversion functions
def Binary2Decimal(bin_num):
    """ Return the decimal representation of bin_num
    
        This actually uses the built-in int() function, 
        but is wrapped in a function for consistency """
    return int(bin_num, 2)


def Decimal2Binary(dec_num):
    """ Return the binary representation of dec_num """
    if dec_num == 0: return ''
    head, tail = divmod(dec_num, 2)
    return Decimal2Binary(head) + str(tail)

#input code: converts input into string
s= raw_input("Give Numbers:")
n=0
st=[]
while n<>len(s):
    st.append(s[n])
    n=n+1

#decoding
one = int("".join(st[:3]))
two = int("".join(st[3:6]))
three = int("".join(st[6:9]))
#Decimal two Binary
x = Decimal2Binary(one)
y = Decimal2Binary(two)
z = Decimal2Binary(three)
#Add the Binary together
a = (x+""+y+""+z)
#get additional numbers from Binary
b = a[:6]
c = Binary2Decimal(b)
d = a[6:12]
e = Binary2Decimal(d)
f = a[12:18]
g = Binary2Decimal(f)
h = a[18:24]
i = Binary2Decimal(h)
print c
print e
print g
print i
