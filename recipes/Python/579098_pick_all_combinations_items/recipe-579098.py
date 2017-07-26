#!/usr/bin/env python3

def of_bucket(lst, depth=0) :
	""" return all combinations of items in buckets """
	#dbg print("of_bucket({0}, {1})".format(lst, depth))
	for item in lst[0] :
		if len(lst) > 1 :
			for result in of_bucket(lst[1:], depth+1) :
				yield [item,] + result
		else :
			yield [item,]

if __name__ == '__main__' :
	bucket_lst = [["ba", "be", "bi"], ["ka", "ko", "ku", "ke"], ["to", "ty"]]
	for n, combination in enumerate(of_bucket(bucket_lst)) :
		print("{0:2d}. {1}".format(n, '-'.join(combination)))
