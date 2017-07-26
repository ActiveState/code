# Scramble word re-arrange characters of word by using simple string manipulation and Random.
import random
s= raw_input("Give Word:")
n=0
st=[]
while n<>len(s):
    st.append(s[n])
    n=n+1
print st
n=0
rst=[]
while n<>len(s):
    rno=random.randint(0,len(s)-1)
    if rst.count(rno)==0:
        rst.append(rno)
        n=n+1
print rst
n=0
ost=''
while n<>len(s):
    ost=ost+ st[rst[n]]
    n=n+1
print ost
