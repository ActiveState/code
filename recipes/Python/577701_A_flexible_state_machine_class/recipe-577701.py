class StateMachine:
	'A class that implements a flexible state machine'
	def __init__( self, transitions, first=None ):
		if type( transitions ) == dict:
			self.sm = transitions
		else:
			self.first = first or transitions.split(',')[0]
			smtext = [ term.split(':') for term in transitions.split() ]
			self.sm = dict( [ tuple(a.split(',')), tuple(b.split(',')) ] 
				for a,b in smtext )
		self.setstate()
	def setstate( self, state=None ):
		self.state = state or self.first
	def __call__( self, event ):
		return self.signal( event )
	def signal( self, event ):
		change = self.sm.get( (self.state,event) )
		change = change or self.sm.get( (self.state,'*') )
		change = change or self.sm.get( ('*',event) )
		change = change or self.sm.get( ('*','*') )
		emit, newstate = change or ('**ERROR**',self.first)
		if newstate == '*':
			newstate = self.state
		elif newstate == '':
			newstate = self.first
		if callable( emit ):
			result = emit( self.state, event, newstate )
		else:
			result = ( emit, newstate )
		self.state = newstate
		return result

if __name__ == '__main__':
	# Example for demonstration and test.
	transitions = '''
		garden,climb:go-up-to-roof,roof 
		roof,jump:fall-through,cottage
		cottage,leave:unlock-door,garden 
		*,need-help:can-choose-climb-jump-leave,*
		*,jump:feel-tired,* 
		*,sleep:feel-refreshed,* 
		*,*:cannot-do,*
		'''
	houseguy = StateMachine( transitions, first='garden' )
	print 'I start at location: %s' % houseguy.state
	actionlist = 'sleep jump need-help climb jump jump leave climb climb'.split()
	for action in actionlist:
		result, newstate = houseguy( action )
		print 'I %s. I %s. Location: %s.' % (action, result, newstate)
