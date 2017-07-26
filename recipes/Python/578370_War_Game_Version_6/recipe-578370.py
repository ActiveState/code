from random import randint, seed
from time import time
# region: change
# from window import *
from Zpaw import *
from cards import *
card_list = [card_0, card_1, card_2, card_3, card_4, card_5, card_6, card_7, card_8, card_9]
# endregion

# page & window dimensions have been corrected.
def game():
    print 'Welcome to WAR V6!'
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
    # region: change
    longest_name = 0
    for name in range(players):
        names.append(raw_input('What is the name of player ' + str(name + 1) + '? '))
        if len(names[-1]) > longest_name:
            longest_name = len(names[-1])
    # endregion
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
        hand[0].sort()
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
            # region: change
            if len(table) == 0:
                print 'There are no cards on the table.\n'
            else:
                table_window = window(longest_name + 13, len(table) * 6)
                for card in range(len(table)):
                    # name_page = page(1, len(names[table[card][0]]) + 9)
                    # name_page.mutate(0, 0, names[table[card][0]] + ' played')
                    # table_window.append(name_page, [card * 6, 0])
                    # table_window.append(card_list[table[card][1]], [card * 6, len(names[table[card][0]]) + 8])
                    # table_window += struct(True, card * 6, 0, name_page)
                    # table_window += struct(True, card * 6, len(names[table[card][0]]) + 8, card_list[table[card][1]])
                    table_window += page(len(names[table[card][0]]) + 9, 1) \
                                    .mutate(0, 0, names[table[card][0]] + ' played').y(card * 6)
                    table_window += page(0, 0).link(card_list[table[card][1]]) \
                                    .x(len(names[table[card][0]]) + 8).y(card * 6)
                print table_window
            print 'These are your playing cards:'
            playing_window = window(len(hands[now_play][0]) * 6, 7)
            for index in range(len(hands[now_play][0])):
                # playing_window.append(card_list[hands[now_play][0][index]], [1, index * 6 + 1])
                # playing_window += struct(True, 1, index * 6 + 1, card_list[hands[now_play][0][index]])
                playing_window += page(0, 0).link(card_list[hands[now_play][0][index]]).x(index * 6 + 1).y(1)
            print playing_window
            if len(hands[now_play][1]) > 0:
                hands[now_play][1].sort()
                print 'These are your captured cards:'
                capture_window = window(len(hands[now_play][1]) * 6, 7)
                for index in range(len(hands[now_play][1])):
                    # capture_window.append(card_list[hands[now_play][1][index]], [1, index * 6 + 1])
                    # capture_window += struct(True, 1, index * 6 + 1, card_list[hands[now_play][1][index]])
                    capture_window += page(0, 0).link(card_list[hands[now_play][1][index]]).x(index * 6 + 1).y(1)
                print capture_window
            # endregion
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
        #region: change
        table_window = window(longest_name + 13, len(table) * 6)
        for card in range(len(table)):
            # name_page = page(1, len(names[table[card][0]]) + 9)
            # name_page.mutate(0, 0, names[table[card][0]] + ' played')
            # table_window.append(name_page, [card * 6, 0])
            # table_window.append(card_list[table[card][1]], [card * 6, len(names[table[card][0]]) + 8])
            # table_window += struct(True, card * 6, 0, name_page)
            # table_window += struct(True, card * 6, len(names[table[card][0]]) + 8, card_list[table[card][1]])
            table_window += page(len(names[table[card][0]]) + 9, 1) \
                            .mutate(0, 0, names[table[card][0]] + ' played').y(card * 6)
            table_window += page(0, 0).link(card_list[table[card][1]]) \
                            .x(len(names[table[card][0]]) + 8).y(card * 6)
        print table_window
        # endregion
        hand_out = []
        for index in range(players):
            if table[index][1] == high_card:
                hand_out.append(table[index][0])
        while len(table) > 0:
            hands[hand_out[randint(0, len(hand_out) - 1)]][1].append(table[0][1])
            del table[0]
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
            for index in range(len(scores)):
                if total > scores[index][1]:
                    scores.insert((player, total))
                    break
    try:
        for player in range(players):
            # Next line of code has a problem (IndexError).
            print names[scores[player][0]] + ' received ' + str(scores[player][1]) + ' points.'
        print
        for index in range(10):
            raw_input('GAME OVER ... ' + str(9 - index))
    except Exception, bug:
        print
        print 'Oops!'
        print '\t', bug
        raw_input()

# NOTE:
# Am considering re-writing this game.
if __name__ == '__main__':
    game()
