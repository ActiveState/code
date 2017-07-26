from random import *
from math import *

#GLOBAL VARIABLES

cards = range(0,52)

def randRange(in_lower,in_upper):
	""" generates a random number between in_lower and in_upper"""
	temp_range = in_upper - in_lower
	return int(round((temp_range)*random() + (in_lower)))


def popRandArray(in_list):
	return in_list.pop(randRange(0,len(in_list)-1))
	
def realDealCard():
	
	global cards
	if len(cards)==0:
		print "new deck"
		cards = range(0,52)
	return popRandArray(cards)


def cardAsString(in_card):
	
	value = ["ace","two","three","four","five","six","seven","eight","nine","ten","jack","queen","king"]
	suit = ["hearts","diamonds","spades","clubs"]
	return value[in_card%13]+ " of " + suit[in_card/13]
	
	

def cardScore(in_card):

	score = in_card%13+1
	if score > 10:
		score = 10
	return score

print "$Blackjack$"
player_reply="r"
while player_reply == "r" :
		#~ player is delt with two cards
		player_card1 = realDealCard()
		player_card2 = realDealCard()

		#~ show player the two cards
		print "your card1 is", cardAsString(player_card1)
		print "your card2 is", cardAsString(player_card2)

		#~ count score of player
		player_score = cardScore(player_card1) + cardScore(player_card2)

		#~ show playerthe score
		print "your score is", player_score

		#~ computer is delt with two cards
		computer_card1 = realDealCard()
		computer_card2 = realDealCard()

		#~ show player one of the two cards
		print "The card1 of computer is", cardAsString(computer_card1)

		#~ count score of computer
		computer_score = cardScore(computer_card1) + cardScore(computer_card2)

		#~ ask players action
		while True:
			player_action = str(raw_input("twist (t) or stick (s)?"))

		#~ if player chooses twist
			while player_action == "t" : 
				#~ player is delt with one more card
				player_card3 = realDealCard()
				#~ show player the third card
				print "your new card is", cardAsString(player_card3)
				#~ count current score of player
				player_score += cardScore(player_card3)
				#~ show player current score
				print "your score is", player_score
					#~ check bust
					#~ if current score of player > 21
				if player_score > 21 :
					#~ bust
					print "you bust"
					#~ player lose
					print "you lose and computer wins"
					break
				
				elif player_score == 21 :
					#~player has a blackjack
					print "blackjack!"
					#~win
					print "you win and computer loses"
					player_action = ""
				elif player_score < 21 :
					player_action = str(raw_input("twist (t) or stick (s)?"))
					
					
					#~ elif current score of player == 21	
				
			#~ elif player chooses stick
			if player_action == "s" :
			#~ dealers turn
				print "you choose stick"
				print "It is computers turn"
				
				#~ if first score of computer <= 18
				while computer_score <=18 :
					#~ computer chooses twist
					print "computer twist"
					#~computer is delt one more card
					computer_card3 = realDealCard()
					computer_score += cardScore(computer_card3)
						#~ check bust
						#~ if current score of computer > 21
				if computer_score > 21 :
							#~computer bust
					print "computer score is", computer_score
					print "computer bust and You win"
					break
				elif computer_score == player_score :
					print "computer score is", computer_score
					print "draw- No winner"
					break
				#~ elif first two score > 18
				elif computer_score > 18 :
					#~computer choose stick
					print "computer stick"
					#~ print "computer score is", computer_score
					#~compare score
				if computer_score < player_score :
					print "computer score is", computer_score
					print "you win and computer loses"
				elif computer_score > player_score :
					print "computer score is", computer_score
					print "you lose and computer wins"
					break
				break
			break	
		player_reply = str(raw_input("restart (r) or quit (q)?"))
