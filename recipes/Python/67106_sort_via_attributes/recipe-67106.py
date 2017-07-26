#!/usr/bin/env python

# This is a class designed to sort things via an index or an attribute.
# Thus, you can sort lists of classes or lists of dicts or lists of tuples
# without much trouble.
class Sorter :

	# Initialize self.__attribute .  It will be abused later.
	def __init__ (self) :
		self.__attribute = None

	# Notice how __compare is dependant upon self.__attribute
	def __compare (self, x, y) :
		return cmp(x[self.__attribute], y[self.__attribute])

	# Pass the sort function the __compare function defined above.
	def __call__ (self, data, attribute = None) :
		if attribute == None :
			data.sort()

		else :
			self.__attribute = attribute
			data.sort(self.__compare)

			# This is useful if you want to inline things.
			# I don't know how much innefficiency it introduces.
			# Is this just a new reference?  (that would be cool.)
			return data
			

# Instanciate the Sorter class once in the module.
# All calls will subsequently abuse this instance.
sort = Sorter()


if __name__ == '__main__' :

	list = [(1, 2), (4, 8), (0, 3)]
	dict = [{'a': 3, 'b': 4}, {'a': 5, 'b': 2}, {'a': 0, 'b': 0}, {'a': 9, 'b': 9}]
	dumb = [1, 4, 6, 7, 2, 5, 9, 2, 4, 6]

	print

	print 'list normal:', list
	sort(list, 0)
	print 'sort by [0]:', list
	sort(list, 1)
	print 'sort by [1]:', list

	print
	print

	print "dict normal:", dict
	sort(dict, 'a')
	print "sort by 'a':",  dict
	sort(dict, 'b')
	print "sort by 'b':",  dict

	print
	print

	print 'dumb normal:', dumb
	sort(dumb)
	print 'normal sort:', dumb

	print
