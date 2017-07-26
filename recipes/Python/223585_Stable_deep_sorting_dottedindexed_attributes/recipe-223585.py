def sortByAttrs(seq, attrs):

	listComp = ['seq[:] = [(']

	for attr in attrs:
		listComp.append('seq[i].%s, ' % attr)

	listComp.append('i, seq[i]) for i in xrange(len(seq))]')

	exec('%s' % ''.join(listComp))

	seq.sort()

	seq[:] = [obj[-1] for obj in seq]

	return

#
# begin test code
#

from random import randint

class a:
	def __init__(self):
		self.x = (randint(1, 5), randint(1, 5))

class b:
	def __init__(self):
		self.x = randint(1, 5)
		self.y = (a(), a())

class c:
	def __init__(self, arg):
		self.x = arg
		self.y = b()

if __name__ == '__main__':

	aList = [c(1), c(2), c(3), c(4), c(5), c(6)]

	print '\n...to be sorted by obj.y.y[1].x[1]'
	print '    then, as needed, by obj.y.x'
	print '    then, as needed, by obj.x\n\n     ',

	for i in range(6):
		print '(' + str(aList[i].y.y[1].x[1]) + ',',
		print str(aList[i].y.x) + ',',
		print str(aList[i].x) + ') ',

	sortByAttrs(aList, ['y.y[1].x[1]', 'y.x', 'x'])

	print '\n\n...now sorted by listed attributes.\n\n     ',

	for i in range(6):
		print '(' + str(aList[i].y.y[1].x[1]) + ',',
		print str(aList[i].y.x) + ',',
		print str(aList[i].x) + ') ',
	print

#
# end test code
#
