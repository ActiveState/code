# http://akiscode.com/articles/gcd_of_a_list.shtml
# Copyright (c) 2010 Stephen Akiki
# MIT License (Means you can do whatever you want with this)
#  See http://www.opensource.org/licenses/mit-license.php
# Error Codes:
#   None

def GCD(a,b):
	""" The Euclidean Algorithm """
	a = abs(a)
	b = abs(b)
        while a:
                a, b = b%a, a
        return b
        
        
def GCD_List(list):
	""" Finds the GCD of numbers in a list.
	Input: List of numbers you want to find the GCD of
		E.g. [8, 24, 12]
	Returns: GCD of all numbers
	"""
	return reduce(GCD, list)
