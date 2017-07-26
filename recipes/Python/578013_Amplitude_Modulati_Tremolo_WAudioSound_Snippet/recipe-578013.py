# SomeSound.py

audio=file('/dev/dsp', 'wb')
def main():
	for a in range(0,25,1):
		for b in range(15,112,1):
			for c in range(0,1,1):
				audio.write(chr(127+b)+chr(127+b)+chr(127+b)+chr(127+b)+chr(127-b)+chr(127-b)+chr(127-b)+chr(127-b))
		for b in range(112,15,-1):
			for c in range(0,1,1):
				audio.write(chr(127+b)+chr(127+b)+chr(127+b)+chr(127+b)+chr(127-b)+chr(127-b)+chr(127-b)+chr(127-b))
main()
audio.close()



# The modified code below, that you can experiment with. Be aware of wordwrapping, etc...



# SomeSound.py

audio=file('/dev/dsp', 'wb')
def main():
	# "a" is unimportant!
	for a in range(0,25,1):
		f=15
		g=112
		h=1
		i=0
		j=1
		k=1
		l=112
		m=15
		n=-1
		o=0
		p=1
		q=1
		for b in range(f,g,h):
			for c in range(i,j,k):
				audio.write(chr(127+b)+chr(127+b)+chr(127+b)+chr(127+b)+chr(127-b)+chr(127-b)+chr(127-b)+chr(127-b))
		for d in range(l,m,n):
			for e in range(o,p,q):
				audio.write(chr(127+d)+chr(127+d)+chr(127+d)+chr(127+d)+chr(127-d)+chr(127-d)+chr(127-d)+chr(127-d))
main()
audio.close()
