def split_uppercase(str):
	x = ''
	i = 0
	for c in str:
		print c, str[i-1]
		if i == 0: 
			x += c
		elif c.isupper() and not str[i-1].isupper():
			x += ' %s' % c
		else:
			x += c
		i += 1
	return x.strip()
