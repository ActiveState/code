"""

Example script to try and replicate the Dobble game.

1. setup our decision variables, all symbols can potentially be allocated
to each card.

Card_0_Symbol_0_Card_1 = 0 (symbol is not the card 0)
Card_0_Symbol_0_Card_0 = 1 (symbol is on the card)

Author: Alexander Baker April 2016

"""
from collections import OrderedDict

# import PuLp modeler functions
from pulp import *

def check(card0, card1):
	return int(card0.split('_')[1]) != int(card1.split('_')[1])

#Create a prob variable to contain the problem data
prob = LpProblem('Dobble Card Game', LpMinimize)

# Set the number of symbols to 50
m = 50
# Set the number of cards to 55
n = 57
# Set the number of symbols per card
z = 8

Symbol = ['Symbol_%d'%(i) for i in xrange(0, m)]

# Setup Card list
Card = ['Card_%d'%(i) for i in xrange(0, n)]

card_symbol = []
for card0 in Card:
	for s in Symbol:
		for card1 in Card:
			if check(card0, card1):
				card_symbol.append('%s_%s_%s'%(card0,s,card1)) 

symbol_card_var = LpVariable.dicts("CardSymbolCard", \
                                card_symbol, \
                                lowBound=0, \
                                upBound=1, \
                                cat='Integer')

for c0 in Card:
	prob += lpSum([symbol_card_var['%s_%s_%s'%(c0, s, c1)] \
				for s in Symbol \
					for c1 in Card \
						if check(c0, c1)]) == z

for c0 in Card:
	for s in Symbol: \
		prob += lpSum([symbol_card_var['%s_%s_%s'%(c0, s, c1)] \
				for c1 in Card \
						if check(c0, c1)]) <= 1
						
for c0 in Card:
	#print c0
	for c1 in Card:
		#print s
		prob += lpSum([symbol_card_var['%s_%s_%s'%(c0, s, c1)] \
				 for s in Symbol\
					if check(c0, c1)]) <= 1
for c0 in Card:
	for s in Symbol:
		for c1 in Card:
			if check(c0, c1):
				y = LpVariable('dummy_%s_%s_%s'%(c0,s,c1),0,1,cat='Integer')
				prob += 1 <= symbol_card_var['%s_%s_%s'%(c0,s,c1)] + 10*y
		 		prob += symbol_card_var['%s_%s_%s'%(c1,s,c0)] <= 0 + 10*(1-y)

prob.writeLP('dobble.lp')
prob += 0, "Arbitrary Objective Function"
status = prob.solve()
print LpStatus[status]
results = OrderedDict()
for v in prob.variables():
		if 'dummy' in v.name:
			continue
		f = v.name.split('_')
		card0 = f[2]
		symbol = f[4]
		card1 = f[6]
		if v.varValue == 1:
			if 'C%s'%(card0) in results:
				if not 'S%s'%(symbol) in results['C%s'%(card0)]:
					results['C%s'%(card0)].append('%s(Card %s)'%(symbol, card1))
			else:
				results['C%s'%(card0)] = ['%s(Card %s)'%(symbol, card1)]
		
for k,v in results.items():
	print k, v

print prob.objective
print value(prob.objective)
