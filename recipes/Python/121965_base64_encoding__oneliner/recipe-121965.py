#generate Base64 Alphabet in one line
b64list = reduce(lambda v,a:v+[chr(ord(a[0])+i) for i in range(a[1])],[('A',26),('a',26),('0',10)],[])+['+','/','=']

#now convert each 24 bit field into 4 pieces
s ='anuraguniyal.'
##bytes = [ord(ch) for ch in s]
##print b64list[bytes[0]>>2]
##print b64list[((bytes[0]&3)<<4)+(bytes[1]>>4)]
##print b64list[((bytes[1]&15)<<2)+(bytes[2]>>6)]
##print b64list[bytes[2]&63]
#this can be written in short as
#one line to convert three bytes to 4 base64 chars
en = lambda a,b,c,l = b64list:''.join([l[a>>2]]+[l[i or 64] for i in [((a&3)<<4)+(b>>4),((b&15)<<2)+(c>>6),c&63]])

#use en function to convert aribirary legth strings
l = [ord(c) for c in s]+[0,0,0]
ll = []
for i in range(0,len(s),3):
    ll.extend(en(l[i],l[i+1],l[i+2]))

#this can be written in one ilne
encode = lambda s,l=[[]]:''.join([l.pop(0),l.append([ord(c) for c in s]+[0,0,0]),[en(l[0][i],l[0][i+1],l[0][i+2]) for i in range(0,len(s),3)]][2])

#combining en and encode
encode = lambda s,l=[[]]:''.join([l.pop(0),l.append([ord(c) for c in s]+[0,0,0]),[apply(lambda a,b,c,l = b64list:''.join([l[a>>2]]+[l[i or 64] for i in [((a&3)<<4)+(b>>4),((b&15)<<2)+(c>>6),c&63]]),(l[0][i],l[0][i+1],l[0][i+2])) for i in range(0,len(s),3)]][2])

#base64 Alphabet is not integrated in this oneliner as it will evaluate it each time
#that may slow this function
#but just to write one liner base 64 converter
#here it is...10 times slower 
encode = lambda s,l=[[]]:''.join([l.pop(0),l.append([ord(c) for c in s]+[0,0,0]),[apply(lambda a,b,c,l = reduce(lambda v,a:v+[chr(ord(a[0])+i) for i in range(a[1])],[('A',26),('a',26),('0',10)],[])+['+','/','=']:''.join([l[a>>2]]+[l[i or 64] for i in [((a&3)<<4)+(b>>4),((b&15)<<2)+(c>>6),c&63]]),(l[0][i],l[0][i+1],l[0][i+2])) for i in range(0,len(s),3)]][2])
print '-----------------------'
import base64
print encode(s)
print base64.encodestring(s)
