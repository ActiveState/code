import re

def tokeniser( text, tokenpat=None, blockchar='()[]{}' ):
	'Lightweight text tokeniser for simple structured text'
	defpat = r'''
		(-?\d+\.?\d*)|  # find -nn.nnn or -nnn or nn numbers
		(\w+)|          # look for words (identifiers) next
		(".*?")|        # look for double-quoted strings
		('.*?')|        # look for single quoted strings
		([ \t]+)|       # gather white space (but not new lines)
		(\n)|           # check for a new line character
		(.)             # capture any other text as single characters'''
	openchar, closechar = blockchar[0::2], blockchar[1::2]
	blockpair = dict( zip( closechar, openchar ) )
	stack = []
	block = []
	synpat = re.compile( tokenpat or defpat, re.M + re.S + re.X )
	for token in synpat.split( text ):
		if token:
			if token in openchar:
				block.append( [] )
				stack.append( block )
				block = block[-1]
			block.append( token )
			if token in closechar:
				assert block[0] == blockpair[ token ], 'Block end mismatch'
				assert stack, 'Block start mismatch'
				block = stack.pop()
	assert stack == [], 'Block not closed'
	return block

def showtokens( tokens, indent=0 ):
	for token in tokens:
		if type( token ) == list:
			showtokens( token, indent+1 )
		else:
			print '%sToken: %s' % ('    '*indent, `token`)

if __name__ == '__main__':
	example = '''
for x in xseq[2:]:
	print fn( x*-5.5, "it\'s big", "", {'g':[0]} )
end
	'''.strip()
	result = tokeniser( example )
	showtokens( result )
