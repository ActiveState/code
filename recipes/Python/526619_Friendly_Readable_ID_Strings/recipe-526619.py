from random import choice

def GetFriendlyID():
	"""
		Create an ID string we can recognise.
		(Think Italian or Japanese or Native American.)
	"""
	v = 'aeiou'
	c = 'bdfghklmnprstvw'
	
	return ''.join([choice(v if i%2 else c) for i in range(8)])

def GetUniqueFriendlyID(used_ids):
	"""
		Return an ID that is not in our list of already used IDs.
	"""
	# trying infinitely is a bad idea
	LIMIT = 1000

	count = 0
	while count < LIMIT:
		id = GetFriendlyID()
		if id not in used_ids:
			break
		count += 1
		id = ''
	return id

if __name__ == '__main__':
	from sets import Set

	print 'some sample unique IDs:'
	used_ids = Set()
	for i in xrange(50):
		id = GetUniqueFriendlyID(used_ids)
		if not id:
			print 'something broke'
			break
		used_ids.add(id)
		print id

		
