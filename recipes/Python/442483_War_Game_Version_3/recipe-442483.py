================================================================================
war_game_3.py
================================================================================
from random import randint, seed
from time import time
# region: change
from window import *
from cards import *
card_list = [card_0, card_1, card_2, card_3, card_4, card_5, card_6, card_7, card_8, card_9]
# endregion

def game():
    print 'Welcome to WAR V3!'
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
                table_window = window_v1(len(table) * 6, longest_name + 13)
                for card in range(len(table)):
                    name_page = page_v1(1, len(names[table[card][0]]) + 9)
                    name_page.mutate(0, 0, names[table[card][0]] + ' played')
                    table_window.append(name_page, [card * 6, 0])
                    table_window.append(card_list[table[card][1]], [card * 6, len(names[table[card][0]]) + 8])
                print table_window
            print 'These are your playing cards:'
            playing_window = window_v1(7, len(hands[now_play][0]) * 6)
            for index in range(len(hands[now_play][0])):
                playing_window.append(card_list[hands[now_play][0][index]], [1, index * 6 + 1])
            print playing_window
            if len(hands[now_play][1]) > 0:
                hands[now_play][1].sort()
                print 'These are your captured cards:'
                capture_window = window_v1(7, len(hands[now_play][1]) * 6)
                for index in range(len(hands[now_play][1])):
                    capture_window.append(card_list[hands[now_play][1][index]], [1, index * 6 + 1])
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
        table_window = window_v1(len(table) * 6, longest_name + 13)
        for card in range(len(table)):
            name_page = page_v1(1, len(names[table[card][0]]) + 9)
            name_page.mutate(0, 0, names[table[card][0]] + ' played')
            table_window.append(name_page, [card * 6, 0])
            table_window.append(card_list[table[card][1]], [card * 6, len(names[table[card][0]]) + 8])
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
    for player in range(players):
        print names[scores[player][0]] + ' received ' + str(scores[player][1]) + ' points.'
    print
    for index in range(10):
        raw_input('GAME OVER ... ' + str(9 - index))

if __name__ == '__main__':
    game()

================================================================================
window.py
================================================================================
# This is the first version of the page class.
class page_v1:

    def __init__(self, rows, columns, default = None):
        # (page_v1, int, int, str)
        if default is None:
            default = ' '
        self.__page = list()
        for index in range(rows):
            self.__page.append(list(default[0] * columns))

    def mutate(self, row, column, string):
        # (page_v1, int, int, str)
        try:
            if row >= 0:
                for index in range(len(string)):
                    if column + index >= 0:
                        self.__page[row][column + index] = string[index]
        except:
            pass

    def access(self, row, column, length = 1):
        # (page_v1, int, int, int)
        string = str()
        try:
            for index in range(length):
                string += self.__page[row][column + index]
        except:
            pass
        return string

    def internal(self):
        # (page_v1)
        array = list()
        for row in self.__page:
            array.append(row[:])
        return array

    def __str__(self):
        # (page_v1)
        string = str()
        for row in self.__page:
            for character in row:
                string += character
            string += '\n'
        return string[:-1]

# This is the first version of a theoretical window.
class window_v1:

    def __init__(self, height, width, border = None, background = None):
        # (window_v1, int, int, str, str)
        self.__height = height
        self.__width = width
        self.__border = border
        self.__background = background
        self.__draw = True
        self.__buffer = None
        self.__contents = list()

    def append(self, instance, position, visible = True, index = None):
        # (window_v1, page_v1 OR window_v1, [int, int], bool, int)
        self.__draw = True
        if index is None:
            self.__contents.append([instance, position, visible])
        else:
            self.__contents.insert(index, [instance, position, visible])

    def remove(self, instance):
        # (window_v1, page_v1 OR window_v1)
        for index in range(len(self.__contents)):
            if instance is self.__contents[index][0]:
                self.__draw = True
                del self.__contents[index]

    def __getitem__(self, index):
        # (window_v1, int)
        self.__draw = True
        return self.__contents[index]

    def __delitem__(self, index):
        # (window_v1, int)
        self.__draw = True
        del self.__contents[index]

    def size(self, height = None, width = None):
        # (window_v1, int, int)
        if height is not None:
            self.__draw = True
            self.__height = height
        if width is not None:
            self.__draw = True
            self.__width = width
        if height is None and width is None:
            return self.__height, self.__width

    def look(self, border = 0, background = 0):
        # (window_v1, str, str)
        if border is not 0:
            self.__draw = True
            self.__border = border
        if background is not 0:
            self.__draw = True
            self.__background = background
        if border is 0 and background is 0:
            return self.__border, self.__background

    def __update(self):
        # (window_v1)
        if self.__draw:
            self.__draw = False
            self.__buffer = page_v1(self.__height, self.__width, self.__background)
            for item in self.__contents:
                if item[2]:
                    internal = item[0].internal()
                    for row in range(len(internal)):
                        for column in range(len(internal[0])):
                            self.__buffer.mutate(row + item[1][0], column + item[1][1], internal[row][column])
            if self.__border is not None:
                self.__buffer.mutate(0, 0, self.__border[0] * self.__width)
                self.__buffer.mutate(self.__height - 1, 0, self.__border[0] * self.__width)
                for row in range(1, self.__height - 1):
                    self.__buffer.mutate(row, 0, self.__border[0])
                    self.__buffer.mutate(row, self.__width - 1, self.__border[0])

    def internal(self):
        # (window_v1)
        self.__update()
        return self.__buffer.internal()

    def __str__(self):
        # (window_v1)
        self.__update()
        return str(self.__buffer)

================================================================================
cards.py
================================================================================
from window import page_v1

card_0 = page_v1(5, 5)
card_0.mutate(0, 0, '+---+')
card_0.mutate(1, 0, '|   |')
card_0.mutate(2, 0, '| 0 |')
card_0.mutate(3, 0, '|   |')
card_0.mutate(4, 0, '+---+')

card_1 = page_v1(5, 5)
card_1.mutate(0, 0, '+---+')
card_1.mutate(1, 0, '|   |')
card_1.mutate(2, 0, '| 1 |')
card_1.mutate(3, 0, '|   |')
card_1.mutate(4, 0, '+---+')

card_2 = page_v1(5, 5)
card_2.mutate(0, 0, '+---+')
card_2.mutate(1, 0, '|   |')
card_2.mutate(2, 0, '| 2 |')
card_2.mutate(3, 0, '|   |')
card_2.mutate(4, 0, '+---+')

card_3 = page_v1(5, 5)
card_3.mutate(0, 0, '+---+')
card_3.mutate(1, 0, '|   |')
card_3.mutate(2, 0, '| 3 |')
card_3.mutate(3, 0, '|   |')
card_3.mutate(4, 0, '+---+')

card_4 = page_v1(5, 5)
card_4.mutate(0, 0, '+---+')
card_4.mutate(1, 0, '|   |')
card_4.mutate(2, 0, '| 4 |')
card_4.mutate(3, 0, '|   |')
card_4.mutate(4, 0, '+---+')

card_5 = page_v1(5, 5)
card_5.mutate(0, 0, '+---+')
card_5.mutate(1, 0, '|   |')
card_5.mutate(2, 0, '| 5 |')
card_5.mutate(3, 0, '|   |')
card_5.mutate(4, 0, '+---+')

card_6 = page_v1(5, 5)
card_6.mutate(0, 0, '+---+')
card_6.mutate(1, 0, '|   |')
card_6.mutate(2, 0, '| 6 |')
card_6.mutate(3, 0, '|   |')
card_6.mutate(4, 0, '+---+')

card_7 = page_v1(5, 5)
card_7.mutate(0, 0, '+---+')
card_7.mutate(1, 0, '|   |')
card_7.mutate(2, 0, '| 7 |')
card_7.mutate(3, 0, '|   |')
card_7.mutate(4, 0, '+---+')

card_8 = page_v1(5, 5)
card_8.mutate(0, 0, '+---+')
card_8.mutate(1, 0, '|   |')
card_8.mutate(2, 0, '| 8 |')
card_8.mutate(3, 0, '|   |')
card_8.mutate(4, 0, '+---+')

card_9 = page_v1(5, 5)
card_9.mutate(0, 0, '+---+')
card_9.mutate(1, 0, '|   |')
card_9.mutate(2, 0, '| 9 |')
card_9.mutate(3, 0, '|   |')
card_9.mutate(4, 0, '+---+')

card_10 = page_v1(5, 5)
card_10.mutate(0, 0, '+---+')
card_10.mutate(1, 0, '|   |')
card_10.mutate(2, 0, '|1 0|')
card_10.mutate(3, 0, '|   |')
card_10.mutate(4, 0, '+---+')

card_A = page_v1(5, 5)
card_A.mutate(0, 0, '+---+')
card_A.mutate(1, 0, '|   |')
card_A.mutate(2, 0, '| A |')
card_A.mutate(3, 0, '|   |')
card_A.mutate(4, 0, '+---+')

card_J = page_v1(5, 5)
card_J.mutate(0, 0, '+---+')
card_J.mutate(1, 0, '|   |')
card_J.mutate(2, 0, '| J |')
card_J.mutate(3, 0, '|   |')
card_J.mutate(4, 0, '+---+')

card_Q = page_v1(5, 5)
card_Q.mutate(0, 0, '+---+')
card_Q.mutate(1, 0, '|   |')
card_Q.mutate(2, 0, '| Q |')
card_Q.mutate(3, 0, '|   |')
card_Q.mutate(4, 0, '+---+')

card_K = page_v1(5, 5)
card_K.mutate(0, 0, '+---+')
card_K.mutate(1, 0, '|   |')
card_K.mutate(2, 0, '| K |')
card_K.mutate(3, 0, '|   |')
card_K.mutate(4, 0, '+---+')
