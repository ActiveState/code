from decimal import Decimal

# replaces default range function to allow more functionality
def range(start, stop=None, step=1):
	if stop==None: stop = start; start = 0
	x = []
	while start < stop:
		x.append(Decimal(str(start)))
		start += Decimal(str(step))
	return x
