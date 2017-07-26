#!/usr/bin/python

# Routine by Micah D. Cochran
# Submitted on 26 Aug 2005
# This routine is allowed to be put under any license Open Source (GPL, BSD, LGPL, etc.) License 
# or any Propriety License. Effectively this routine is in public domain. Please attribute where appropriate.

def strip_ml_tags(in_text):
	"""Description: Removes all HTML/XML-like tags from the input text.
	Inputs: s --> string of text
	Outputs: text string without the tags
	
	# doctest unit testing framework

	>>> test_text = "Keep this Text <remove><me /> KEEP </remove> 123"
	>>> strip_ml_tags(test_text)
	'Keep this Text  KEEP  123'
	"""
	# convert in_text to a mutable object (e.g. list)
	s_list = list(in_text)
	i,j = 0,0
	
	while i < len(s_list):
		# iterate until a left-angle bracket is found
		if s_list[i] == '<':
			while s_list[i] != '>':
				# pop everything from the the left-angle bracket until the right-angle bracket
				s_list.pop(i)
				
			# pops the right-angle bracket, too
			s_list.pop(i)
		else:
			i=i+1
			
	# convert the list back into text
	join_char=''
	return join_char.join(s_list)

if __name__ == '__main__':
	import doctest
	doctest.testmod()
