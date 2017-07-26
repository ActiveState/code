##########
# load1.py
##########

import boards
import util
import time

def main():
    screen = util.Screen(boards.boards[0])
    screen.update()
    time.sleep(2)
    row, col = 1, 9
    while True:
        character = screen.read(row, col)
        if character == '_' or character == '*':
            col += 1
        elif character == '|':
            row -= 1
        elif character == ' ':
            if screen.read(row + 1, col) == '|':
                col += 1
            else:
                row += 1
        else:
            break
        screen.write(row, col, '^')
        screen.update()
        time.sleep(.1)
    screen.update()
    time.sleep(2)

if __name__ == '__main__':
    main()

##########
# load2.py
##########

import boards
import util
import time
import ttyWindows

################################################################################

class Player:

    def __init__(self, screen, row=0, column=9, face='^'):
        self.screen = screen
        self.row = row
        self.column = column
        self.face = face[0]
        self.direction = 0, 0

    def setDirection(self, key):
        if key == '\xE0H':
            self.direction = 0, -1
        elif key == '\xE0P':
            self.direction = 0, +1
        elif key == '\xE0K':
            self.direction = -1, 0
        elif key == '\xE0M':
            self.direction = +1, 0

    def move(self):
        character = self.screen.read(self.row, self.column)
        x, y = self.direction
        if character == '_' or character == '*':
            self.column += x
        elif character == '|':
            self.row += y
        elif character == ' ':
            if self.screen.read(self.row + 1, self.column) != '|' or y == 1:
                self.row += 1
            else:
                self.column += x
        self.screen.write(self.row, self.column, self.face)

################################################################################

def main():
    screen = util.Screen(boards.boards[0])
    screen.update()
    player = Player(screen)
    while screen.read(player.row, player.column):
        time.sleep(.1)
        key = ttyWindows.readLookAhead()
        player.setDirection(key)
        player.move()
        screen.update()
    time.sleep(2)

if __name__ == '__main__':
    main()

##########
# load3.py
##########

import boards
import util
import time
import ttyWindows

################################################################################

class Player:

    def __init__(self, screen, face, row=1, column=10):
        self.screen = screen
        self.face = face
        self.row = row
        self.column = column
        self.vector = 0, 0

    def move(self):
        global playing, you
        string = self.screen.read(self.row, self.column)
        left = self.screen.read(self.row, self.column - 1)
        right = self.screen.read(self.row, self.column + 1)
        x, y = self.vector
        x_move = False
        if string == '_':
            self.column += x
            x_move = True
        elif string == '|':
            self.row += y
        elif string == ' ':
            if self.screen.read(self.row + 1, self.column) != '|' or y == 1:
                self.row += 1
            else:
                self.column += x
        if not x_move:
            if left == '_' and x == -1:
                self.column -= 1
            elif right == '_' and x == 1:
                self.column += 1
        self.screen.write(self.row, self.column, self.face)
        if self is you and self.screen.read(self.row, self.column) is None:
            playing = False

################################################################################

class You(Player):

    def setDirection(self, key):
        if key == '\xE0H':
            self.vector = 0, -1
        elif key == '\xE0P':
            self.vector = 0, +1
        elif key == '\xE0K':
            self.vector = -1, 0
        elif key == '\xE0M':
            self.vector = +1, 0

class Robot(Player):

    def setDirection(self, key):
        global playing, you
        if you.row == self.row and you.column == self.column:
            playing = False
        if self.row == you.row:
            if self.column > you.column:
                self.vector = -1, 0
            else:
                self.vector = +1, 0
        else:
            context = self.screen.read(self.row, self.column)
            if context == '|':
                if self.row > you.row:
                    self.vector = 0, -1
                elif self.row < you.row:
                    self.vector = 0, +1

################################################################################

def main():
    global playing, you
    screen = util.Screen(boards.boards[0])
    you = You(screen, '^')
    screen.update()
    players = [you]
    clock = 0
    playing = True
    time.sleep(2)
    while playing:
        clock += 1
        if clock == 40:
            players.append(Robot(screen, '&'))
        time.sleep(.1)
        key = ttyWindows.readLookAhead()
        for player in players:
            player.setDirection(key)
            player.move()
        screen.update()
    screen.update()
    time.sleep(2)

if __name__ == '__main__':
    main()

##########
# load4.py
##########

import boards
import util
import time
import ttyWindows

################################################################################

class Player:

    def __init__(self, screen, face, row=1, column=10):
        self.screen = screen
        self.face = face
        self.row = row
        self.column = column
        self.vector = 0, 0

    def move(self):
        global playing, you
        context = self.screen.read(self.row, self.column)
        left = self.screen.read(self.row, self.column - 1)
        right = self.screen.read(self.row, self.column + 1)
        x, y = self.vector
        x_move = False
        if context == '_':
            self.column += x
            x_move = True
        elif context == '|':
            self.row += y
        elif context == ' ':
            if self.screen.read(self.row + 1, self.column) != '|' or y == 1:
                self.row += 1
            else:
                self.column += x
        if not x_move and context != ' ':
            if left == '_' and x == -1:
                self.column -= 1
            elif right == '_' and x == 1:
                self.column += 1
        self.screen.write(self.row, self.column, self.face)
        if self is you and self.screen.read(self.row, self.column) is None:
            playing = False

################################################################################

class You(Player):

    def __init__(self, screen, face, row=1, column=10):
        Player.__init__(self, screen, face, row, column)
        self.score = 0

    def setDirection(self, key):
        context = self.screen.read(self.row, self.column)
        if context == '*':
            self.score += 10
            self.screen.cache_write(self.row, self.column, '_')
        if key == '\xE0H':
            self.vector = 0, -1
        elif key == '\xE0P':
            self.vector = 0, +1
        elif key == '\xE0K':
            self.vector = -1, 0
        elif key == '\xE0M':
            self.vector = +1, 0
        elif key == 'a':
            self.screen.cache_write(self.row, self.column - 1, ' ')
        elif key == 'd':
            self.screen.cache_write(self.row, self.column + 1, ' ')

class Robot(Player):

    def setDirection(self, key):
        global playing, you
        if you.row == self.row and you.column == self.column:
            playing = False
        if self.row == you.row:
            if self.column > you.column:
                self.vector = -1, 0
            else:
                self.vector = +1, 0
        else:
            context = self.screen.read(self.row, self.column)
            if context == '|':
                if self.row > you.row:
                    self.vector = 0, -1
                elif self.row < you.row:
                    self.vector = 0, +1

################################################################################

def main():
    global playing, you
    screen = util.Screen2(boards.boards[0])
    you = You(screen, '^')
    screen.update()
    players = [you]
    clock = 0
    playing = True
    time.sleep(2)
    while playing:
        clock += 1
        if clock == 90:
            players.append(Robot(screen, '&'))
        time.sleep(.1)
        key = ttyWindows.readLookAhead()
        for player in players:
            player.setDirection(key)
            player.move()
        screen.update()
        print 'Score: %s' % you.score
    screen.update()
    print 'Score: %s' % you.score
    time.sleep(2)

if __name__ == '__main__':
    main()

##########
# load5.py
##########

import boards
import random
import time
import ttyWindows
import util

################################################################################

class Player:

    def __init__(self, screen, face, row=1, column=10):
        self.screen = screen
        self.face = face
        self.row = row
        self.column = column
        self.vector = 0, 0

    def move(self):
        global playing, you, players
        context = self.screen.read(self.row, self.column)
        left = self.screen.read(self.row, self.column - 1)
        right = self.screen.read(self.row, self.column + 1)
        x, y = self.vector
        x_move = False
        if context == '_':
            self.column += x
            x_move = True
        elif context == '|':
            self.row += y
        elif context == ' ':
            if self.screen.read(self.row + 1, self.column) != '|' or y == 1:
                self.row += 1
            else:
                self.column += x
        if not x_move and context != ' ':
            if left == '_' and x == -1:
                self.column -= 1
            elif right == '_' and x == 1:
                self.column += 1
        self.screen.write(self.row, self.column, self.face)
        if self.screen.read(self.row, self.column) is None:
            if self is you:
                playing = False
            else:
                players.remove(self)

################################################################################

class You(Player):

    def __init__(self, screen, face, row=1, column=10):
        Player.__init__(self, screen, face, row, column)
        self.score = 0

    def setDirection(self, key):
        context = self.screen.read(self.row, self.column)
        if context == '*':
            self.score += 10
            self.screen.cache_write(self.row, self.column, '_')
        if key == '\xE0H':
            self.vector = 0, -1
        elif key == '\xE0P':
            self.vector = 0, +1
        elif key == '\xE0K':
            self.vector = -1, 0
        elif key == '\xE0M':
            self.vector = +1, 0
        elif key == 'a':
            self.screen.cache_write(self.row, self.column - 1, ' ')
        elif key == 'd':
            self.screen.cache_write(self.row, self.column + 1, ' ')

class Robot(Player):

    def __init__(self, screen, face, row=1, column=10):
        Player.__init__(self, screen, face, row, column)
        self.move_count = 0

    def move(self):
        if self.screen.read(self.row, self.column) == ' ':
            Player.move(self)
        else:
            self.move_count += 1
            if self.move_count % 2:
                Player.move(self)
            else:
                self.screen.write(self.row, self.column, self.face)

    def setDirection(self, key):
        global playing, you
        if you.row == self.row and you.column == self.column:
            playing = False
        if self.column > you.column:
            self.vector = -1, 0
        elif self.column < you.column:
            self.vector = +1, 0
        if self.row != you.row:
            context = self.screen.read(self.row, self.column)
            if context == '|':
                if self.row > you.row:
                    self.vector = 0, -1
                elif self.row < you.row:
                    self.vector = 0, +1

################################################################################

SELECT = 1

def main():
    global playing, you, players
    screen = util.Screen2(boards.boards[SELECT])
    you = You(screen, '^')
    screen.update()
    players = [you]
    clock = 0
    playing = True
    time.sleep(2)
    while playing:
        clock += 1
        if clock > 40 and len(players) < 3:
            players.append(Robot(screen, '&', column=random.randrange(len(boards.boards[SELECT].board().splitlines()[1]))))
        time.sleep(.1)
        key = ttyWindows.readLookAhead()
        for player in players:
            player.setDirection(key)
            player.move()
        screen.update()
        print 'Score: %s' % you.score
    screen.update()
    print 'Score: %s' % you.score
    time.sleep(2)

if __name__ == '__main__':
    main()

##########################
# Extended Demo (Sound).py
##########################

import boards
import random
import time
import ttyWindows
import util
import winsound

################################################################################

class Player:

    def __init__(self, screen, face, row=1, column=10):
        self.screen = screen
        self.face = face
        self.row = row
        self.column = column
        self.vector = 0, 0

    def move(self):
        global playing, you, players
        context = self.screen.read(self.row, self.column)
        left = self.screen.read(self.row, self.column - 1)
        right = self.screen.read(self.row, self.column + 1)
        x, y = self.vector
        x_move = False
        if context == '_':
            self.column += x
            x_move = True
        elif context == '|':
            self.row += y
        elif context == ' ':
            if self.screen.read(self.row + 1, self.column) != '|' or y == 1:
                self.row += 1
            else:
                self.column += x
        if not x_move and context != ' ':
            if left == '_' and x == -1:
                self.column -= 1
            elif right == '_' and x == 1:
                self.column += 1
        self.screen.write(self.row, self.column, self.face)
        if self.screen.read(self.row, self.column) is None:
            if self is you:
                playing = False
            else:
                players.remove(self)
                winsound.Beep(400, 25)
                winsound.Beep(500, 25)

################################################################################

class You(Player):

    def __init__(self, screen, face, row=1, column=10):
        Player.__init__(self, screen, face, row, column)
        self.score = 0

    def setDirection(self, key):
        context = self.screen.read(self.row, self.column)
        if context == '*':
            self.score += 10
            self.screen.cache_write(self.row, self.column, '_')
            winsound.Beep(300, 50)
        if key == '\xE0H':
            self.vector = 0, -1
        elif key == '\xE0P':
            self.vector = 0, +1
        elif key == '\xE0K':
            self.vector = -1, 0
        elif key == '\xE0M':
            self.vector = +1, 0
        elif key == 'a':
            self.screen.cache_write(self.row, self.column - 1, ' ')
        elif key == 'd':
            self.screen.cache_write(self.row, self.column + 1, ' ')

class Robot(Player):

    def __init__(self, screen, face, row=1, column=10):
        Player.__init__(self, screen, face, row, column)
        self.move_count = 0

    def move(self):
        if self.screen.read(self.row, self.column) == ' ':
            Player.move(self)
        else:
            self.move_count += 1
            if self.move_count % 2:
                Player.move(self)
            else:
                self.screen.write(self.row, self.column, self.face)

    def setDirection(self, key):
        global playing, you
        if you.row == self.row and you.column == self.column:
            playing = False
        if self.column > you.column:
            self.vector = -1, 0
        elif self.column < you.column:
            self.vector = +1, 0
        if self.row != you.row:
            context = self.screen.read(self.row, self.column)
            if context == '|':
                if self.row > you.row:
                    self.vector = 0, -1
                elif self.row < you.row:
                    self.vector = 0, +1

################################################################################

SELECT = 1
ROBOTS = 3

def main():
    global playing, you, players
    screen = util.Screen2(boards.boards[SELECT])
    you = You(screen, '^')
    screen.update()
    players = [you]
    clock = 0
    playing = True
    time.sleep(2)
    note = False
    while playing:
        clock += 1
        if clock > 40 and len(players) - 1 < ROBOTS:
            players.append(Robot(screen, '&', column=random.randrange(len(boards.boards[SELECT].board().splitlines()[1]))))
        time.sleep(0.1)
        key = ttyWindows.readLookAhead()
        for player in players:
            player.setDirection(key)
            player.move()
        screen.update()
        print 'Score: %s' % you.score
        winsound.Beep(100 + 100 * note, 25)
        note = not note
    screen.update()
    print 'Score: %s' % you.score
    for x in range(4):
        time.sleep(0.1)
        winsound.Beep(700 - 100 * x, 25)
    time.sleep(2)

if __name__ == '__main__':
    main()
