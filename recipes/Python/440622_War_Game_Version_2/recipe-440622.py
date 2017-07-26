from random import randint, seed
from time import time

def game():
    print 'Welcome to WAR V2!'
    print
    asking = True
    while asking:
        try:
            players = int(raw_input('How many players are there? '))
            if players < 2:
                print 'There must be at least two players.'
            else:
                asking = False
        except:
            print 'You must enter a number.'
    print
    names = []
    for name in range(players):
        names.append(raw_input('What is the name of player ' + str(name + 1) + '? '))
    deck = []
    for card in range(10):
        for player in range(players):
            deck.append(card)
    hands = []
    seed(time())
    for player in range(players):
        hand = ([], [])
        for card in range(10):
            index = randint(0, len(deck) - 1)
            hand[0].append(deck[index])
            del deck[index]
        hands.append(hand)
    for round in range(1, 11):
        table = []
        will_play = []
        high_card = 0
        for player in range(players):
            will_play.append(player)
        for turn in range(players):
            for line in range(50):
                print
            index = randint(0, len(will_play) - 1)
            now_play = will_play[index]
            del will_play[index]
            print 'Round', round
            raw_input('It is ' + names[now_play] + "'s turn to play.")
            print
            if len(table) == 0:
                print 'There are no cards on the table.'
            else:
                for card in range(len(table)):
                    print names[table[card][0]] + ' played a ' + str(table[card][1]) + '.'
            print
            print 'These are your playing cards: ' + str(hands[now_play][0])[1:-1] + '.'
            if len(hands[now_play][1]) > 0:
                print 'These are your captured cards: ' + str(hands[now_play][1])[1:-1] + '.'
            print
            asking = True
            while asking:
                try:
                    card = int(raw_input('What card do you want to play? '))
                    if card >= 0 and card <= 9:
                        try:
                            hands[now_play][0].remove(card)
                            table.append((now_play, card))
                            if card > high_card:
                                high_card = card
                            asking = False
                        except:
                            print 'You do not have that card.'
                    else:
                        print 'You must enter a value between -1 and 10.'
                except:
                    print 'You must enter a number.'
        for line in range(50):
            print
        for card in range(players):
            print names[table[card][0]] + ' played a ' + str(table[card][1]) + '.'
        hand_out = []
        for index in range(players):
            if table[index][1] == high_card:
                hand_out.append(table[index][0])
        while len(table) > 0:
            hands[hand_out[randint(0, len(hand_out) - 1)]][1].append(table[0][1])
            del table[0]
        print
        for player in range(players):
            if len(hands[player][1]) > 0:
                   print names[player] + ' has captured ' + str(len(hands[player][1])) + ' cards.'
        print
        raw_input('End Of Round ' + str(round))
    for line in range(50):
        print
    high_score = 0
    scores = []
    for player in range(players):
        total = 0
        for card in range(len(hands[player][1])):
            total += hands[player][1][card]
        if total > high_score:
            high_score = total
        if len(scores) == 0 or scores[len(scores) - 1][1] <= total:
            scores.append((player, total))
        else:
            for index in range(scores):
                if total > scores[index][1]:
                    scores.insert((player, total))
                    break
    for player in range(players):
        print names[scores[player][0]] + ' received ' + str(scores[player][1]) + ' points.'
    print
    raw_input('GAME OVER')

if __name__ == '__main__':
    game()
