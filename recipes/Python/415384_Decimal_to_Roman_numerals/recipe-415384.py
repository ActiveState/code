"""
Victor Yang, pythonrocks@yahoo.com

Convert decimals to Roman numerials.
I use a recursive algorithm here since it reflects the thinking clearly in code.
A non-recursive algothrithm can be done as well.

usage: python roman.py 
It will run the test case against toRoman function
"""

import sys
import unittest


# these two lists serves as building blocks to construt any number
# just like coin denominations.
# 1000->"M", 900->"CM", 500->"D"...keep on going 
decimalDens=[1000,900,500,400,100,90,50,40,10,9,5,4,1]
romanDens=["M","CM","D","CD","C","XC","L","XL","X","IX","V","IV","I"]


def toRoman(dec):
	"""
	Perform sanity check on decimal and throws exceptions when necessary
	"""		
        if dec <=0:
	  raise ValueError, "It must be a positive"
         # to avoid MMMM
	elif dec>=4000:  
	  raise ValueError, "It must be lower than MMMM(4000)"
  
	return decToRoman(dec,"",decimalDens,romanDens)

def decToRoman(num,s,decs,romans):
	"""
	  convert a Decimal number to Roman numeral recursively
	  num: the decimal number
	  s: the roman numerial string
	  decs: current list of decimal denomination
	  romans: current list of roman denomination
	"""
	if decs:
	  if (num < decs[0]):
	    # deal with the rest denomination
	    return decToRoman(num,s,decs[1:],romans[1:])		  
	  else:
	    # deduce this denomation till num<desc[0]
	    return decToRoman(num-decs[0],s+romans[0],decs,romans)	  
	else:
	  # we run out of denomination, we are done 
	  return s


class DecToRomanTest(unittest.TestCase):

	def setUp(self):
		print '\nset up'
	def tearDown(self):
		print 'tear down'
	
	def testDens(self):
		
	   for i in range(len(decimalDens)):
		r=toRoman(decimalDens[i])
		self.assertEqual(r,romanDens[i])

	def testSmallest(self):
		self.assertEqual('I',toRoman(1))

	def testBiggest(self):
		self.assertEqual('MMMCMXCIX',toRoman(3999))

	def testZero(self):
		self.assertRaises(ValueError,toRoman,0)

	def testNegative(self):
		
		self.assertRaises(ValueError,toRoman,-100)


	def testMillonDollar(self):
		
		self.assertRaises(ValueError,toRoman,1000000)

		

if __name__ == "__main__":
	
	unittest.main()
