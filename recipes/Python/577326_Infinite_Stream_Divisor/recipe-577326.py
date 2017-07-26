def infinite_stream_divisor(base, divisor, stream):
	k = -1
	fsa = {}
	for state in range(divisor): # Does the trick :)
		fsa[state] = []
		for input in range(base):
			k = (k+1) % divisor
			fsa[state].append(k)

	state = 0
	for symbol in stream:
		state = fsa[state][int(symbol)]

	if state == 0:
		return True
	return False
