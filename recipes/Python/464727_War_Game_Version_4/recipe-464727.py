================================================================================
war_game_4.py
================================================================================
from random import randint, seed
from time import time
# region: change
# from window import *
from Zpaw import *
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
                table_window = window(len(table) * 6, longest_name + 13)
                for card in range(len(table)):
                    name_page = page(1, len(names[table[card][0]]) + 9)
                    name_page.mutate(0, 0, names[table[card][0]] + ' played')
                    # table_window.append(name_page, [card * 6, 0])
                    # table_window.append(card_list[table[card][1]], [card * 6, len(names[table[card][0]]) + 8])
                    table_window += struct(True, card * 6, 0, name_page)
                    table_window += struct(True, card * 6, len(names[table[card][0]]) + 8, card_list[table[card][1]])
                print table_window
            print 'These are your playing cards:'
            playing_window = window(7, len(hands[now_play][0]) * 6)
            for index in range(len(hands[now_play][0])):
                # playing_window.append(card_list[hands[now_play][0][index]], [1, index * 6 + 1])
                playing_window += struct(True, 1, index * 6 + 1, card_list[hands[now_play][0][index]])
            print playing_window
            if len(hands[now_play][1]) > 0:
                hands[now_play][1].sort()
                print 'These are your captured cards:'
                capture_window = window(7, len(hands[now_play][1]) * 6)
                for index in range(len(hands[now_play][1])):
                    # capture_window.append(card_list[hands[now_play][1][index]], [1, index * 6 + 1])
                    capture_window += struct(True, 1, index * 6 + 1, card_list[hands[now_play][1][index]])
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
        table_window = window(len(table) * 6, longest_name + 13)
        for card in range(len(table)):
            name_page = page(1, len(names[table[card][0]]) + 9)
            name_page.mutate(0, 0, names[table[card][0]] + ' played')
            # table_window.append(name_page, [card * 6, 0])
            # table_window.append(card_list[table[card][1]], [card * 6, len(names[table[card][0]]) + 8])
            table_window += struct(True, card * 6, 0, name_page)
            table_window += struct(True, card * 6, len(names[table[card][0]]) + 8, card_list[table[card][1]])
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
Zpaw.py
================================================================================
import copy
from Zam import *

class struct:

    def __init__(self, visible, x, y, value):
        self.__assert_type((bool, visible), (int, x), (int, y))
        self.__visible = visible
        self.__x = x
        self.__y = y
        self.__value = value

    def get_visible(self):
        return self.__visible

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_value(self):
        return self.__value

    def set_visible(self, visible):
        self.__assert_type((bool, visible))
        self.__visible = visible

    def set_x(self, x):
        self.__assert_type((int, x))
        self.__x = x

    def set_y(self, y):
        self.__assert_type((int, y))
        self.__y = y

    def set_value(self, value):
        self.__value = value
    
    def __assert_type(self, *tuples):
        for types, objects in tuples:
            if type(objects) is not types:
                raise TypeError

class page:

    def __init__(self, rows, columns, value=''):
        self.__assert_type((int, rows), (int, columns), (str, value))
        if value:
            self.__data = matrix(rows, columns, value[0])
        else:
            self.__data = matrix(rows, columns, ' ')

    def access(self, row, column, length=1):
        self.__assert_type((int, row), (int, column), (int, length))
        string = str()
        for index in range(length):
            try:
                string += self.__data[row][column + index]
            except:
                pass
        return string

    def mutate(self, row, column, value):
        self.__assert_type((int, row), (int, column), (str, value))
        for index in range(len(value)):
            try:
                self.__data[row][column + index] = value[index]
            except:
                pass

    def data(self):
        return copy.deepcopy(self.__data)

    def __str__(self):
        return '\n'.join([''.join(row) for row in self.__data])

    def __assert_type(self, *tuples):
        for types, objects in tuples:
            if type(objects) is not types:
                raise TypeError

class window:

    def __init__(self, height, width, border='  ', background='  '):
        self.__assert_type((int, height), (int, width), (str, border), (str, background))
        self.__height = height
        self.__width = width
        if len(border) < 2:
            self.__border = border
        else:
            self.__border = ''
        if len(background) < 2:
            self.__background = background
        else:
            self.__background = ''
        self.__draw = True
        self.__data = None
        self.__list = list()

    def size(self, height=0, width=0):
        self.__assert_type((int, height), (int, width))
        if height != 0:
            self.__draw = True
            self.__height = height
        if width != 0:
            self.__draw = True
            self.__width = width
        return self.__height, self.__width

    def option(self, border='  ', background='  '):
        self.__assert_type((str, border), (str, background))
        if len(border) < 2:
            self.__draw = True
            self.__border = border
        if len(background) < 2:
            self.__draw = True
            self.__background = background
        return self.__border, self.__background

    def data(self):
        self.__update()
        return self.__data.data()

    def __str__(self):
        self.__update()
        return str(self.__data)
            
    def __len__(self):
        return len(self.__list)
    
    def __getitem__(self, key):
        self.__assert_type((int, key))
        self.__draw = True
        return self.__list[key]
    
    def __setitem__(self, key, value):
        self.__assert_type((int, key))
        self.__draw = True
        self.__list[key] = value
        
    def __delitem__(self, key):
        self.__assert_type((int, key))
        self.__draw = True
        del self.__list[key]
        
    def __iter__(self):
        self.__draw = True
        return iter(self.__list)
    
    def __contains__(self, value):
        return value in self.__list

    def __iadd__(self, value):
        self.__draw = True
        self.__list.append(value)
        return self

    def __isub__(self, value):
        self.__draw = True
        while value in self.__list:
            self.__list.remove(value)
        return self
    
    def __update(self):
        if self.__draw:
            self.__draw = False
            self.__data = page(self.__height, self.__width, self.__background)
            for item in self.__list:
                if item.get_visible():
                    x = item.get_x()
                    y = item.get_y()
                    data = item.get_value().data()
                    rows = len(data) / len(data[0])
                    columns = len(data[0])
                    for row in range(rows):
                        for column in range(columns):
                            self.__data.mutate(row + x, column + y, data[row][column])
            if self.__border:
                self.__data.mutate(0, 0, self.__border * self.__width)
                self.__data.mutate(self.__height - 1, 0, self.__border * self.__width)
                for row in range(1, self.__height - 1):
                    self.__data.mutate(row, 0, self.__border)
                    self.__data.mutate(row, self.__width - 1, self.__border)

    def __assert_type(self, *tuples):
        for types, objects in tuples:
            if type(objects) is not types:
                raise TypeError

================================================================================
Zam.py
================================================================================
class array:
    
    def __init__(self, length, value=None):
        self.__data = range(length)
        for index in range(length):
            self.__data[index] = value
            
    def __len__(self):
        return len(self.__data)
    
    def __getitem__(self, key):
        return self.__data[key]
    
    def __setitem__(self, key, value):
        self.__data[key] = value
        
    def __delitem__(self, key):
        self.__data[key] = None
        
    def __iter__(self):
        return iter(self.__data)
    
    def __contains__(self, value):
        return value in self.__data

class matrix:
    
    def __init__(self, rows, columns, value=None):
        self.__data = array(rows)
        for index in range(rows):
            self.__data[index] = array(columns, value)
            
    def __len__(self):
        return len(self.__data) * len(self.__data[0])
    
    def __getitem__(self, key):
        return self.__data[key]
    
    def __setitem__(self, key, value):
        pass
    
    def __delitem__(self, key):
        self.__data[key] = array(len(self.__data[key]))
        
    def __iter__(self):
        return iter(self.__data)
    
    def __contains__(self, value):
        for item in self.__data:
            if value in item:
                return True
        return False

================================================================================
Zam.py
================================================================================
from Zpaw import page

card_0 = page(5, 5)
card_0.mutate(0, 0, '+---+')
card_0.mutate(1, 0, '|   |')
card_0.mutate(2, 0, '| 0 |')
card_0.mutate(3, 0, '|   |')
card_0.mutate(4, 0, '+---+')

card_1 = page(5, 5)
card_1.mutate(0, 0, '+---+')
card_1.mutate(1, 0, '|   |')
card_1.mutate(2, 0, '| 1 |')
card_1.mutate(3, 0, '|   |')
card_1.mutate(4, 0, '+---+')

card_2 = page(5, 5)
card_2.mutate(0, 0, '+---+')
card_2.mutate(1, 0, '|   |')
card_2.mutate(2, 0, '| 2 |')
card_2.mutate(3, 0, '|   |')
card_2.mutate(4, 0, '+---+')

card_3 = page(5, 5)
card_3.mutate(0, 0, '+---+')
card_3.mutate(1, 0, '|   |')
card_3.mutate(2, 0, '| 3 |')
card_3.mutate(3, 0, '|   |')
card_3.mutate(4, 0, '+---+')

card_4 = page(5, 5)
card_4.mutate(0, 0, '+---+')
card_4.mutate(1, 0, '|   |')
card_4.mutate(2, 0, '| 4 |')
card_4.mutate(3, 0, '|   |')
card_4.mutate(4, 0, '+---+')

card_5 = page(5, 5)
card_5.mutate(0, 0, '+---+')
card_5.mutate(1, 0, '|   |')
card_5.mutate(2, 0, '| 5 |')
card_5.mutate(3, 0, '|   |')
card_5.mutate(4, 0, '+---+')

card_6 = page(5, 5)
card_6.mutate(0, 0, '+---+')
card_6.mutate(1, 0, '|   |')
card_6.mutate(2, 0, '| 6 |')
card_6.mutate(3, 0, '|   |')
card_6.mutate(4, 0, '+---+')

card_7 = page(5, 5)
card_7.mutate(0, 0, '+---+')
card_7.mutate(1, 0, '|   |')
card_7.mutate(2, 0, '| 7 |')
card_7.mutate(3, 0, '|   |')
card_7.mutate(4, 0, '+---+')

card_8 = page(5, 5)
card_8.mutate(0, 0, '+---+')
card_8.mutate(1, 0, '|   |')
card_8.mutate(2, 0, '| 8 |')
card_8.mutate(3, 0, '|   |')
card_8.mutate(4, 0, '+---+')

card_9 = page(5, 5)
card_9.mutate(0, 0, '+---+')
card_9.mutate(1, 0, '|   |')
card_9.mutate(2, 0, '| 9 |')
card_9.mutate(3, 0, '|   |')
card_9.mutate(4, 0, '+---+')

card_10 = page(5, 5)
card_10.mutate(0, 0, '+---+')
card_10.mutate(1, 0, '|   |')
card_10.mutate(2, 0, '|1 0|')
card_10.mutate(3, 0, '|   |')
card_10.mutate(4, 0, '+---+')

card_A = page(5, 5)
card_A.mutate(0, 0, '+---+')
card_A.mutate(1, 0, '|   |')
card_A.mutate(2, 0, '| A |')
card_A.mutate(3, 0, '|   |')
card_A.mutate(4, 0, '+---+')

card_J = page(5, 5)
card_J.mutate(0, 0, '+---+')
card_J.mutate(1, 0, '|   |')
card_J.mutate(2, 0, '| J |')
card_J.mutate(3, 0, '|   |')
card_J.mutate(4, 0, '+---+')

card_Q = page(5, 5)
card_Q.mutate(0, 0, '+---+')
card_Q.mutate(1, 0, '|   |')
card_Q.mutate(2, 0, '| Q |')
card_Q.mutate(3, 0, '|   |')
card_Q.mutate(4, 0, '+---+')

card_K = page(5, 5)
card_K.mutate(0, 0, '+---+')
card_K.mutate(1, 0, '|   |')
card_K.mutate(2, 0, '| K |')
card_K.mutate(3, 0, '|   |')
card_K.mutate(4, 0, '+---+')
