"minesweeper"
from UserDict import UserDict

class Game(UserDict):

    def __init__(self, **kwargs):
        "initialize board"
        d = {"ROWS":8,"COLS":8,"BOMBS":10}
        d.update(kwargs)
        UserDict.__init__(self,d)
        self.reset()

    def random_bombs(self):
        "returns list of coordinates in tuple form"
        from random import choice
        coords = []
        for i in range(self['BOMBS']):
            while 1:
                row_idx = choice(range(self['ROWS']))
                col_idx = choice(range(self['COLS']))
                if not (row_idx,col_idx) in coords:
                    break
            coords.append((row_idx,col_idx))
        return coords

    def inc_neighbors(self,row_idx,col_idx):
        for r, c in [(r,c) for r in (-1,0,1) for c in (-1,0,1)]:
            try:
                ri = r + row_idx
                ci = c + col_idx
                if ri < 0 or ci < 0:
                    raise IndexError, "smaller than 0"
                v = self['BOARD'][ri][ci]
                self['BOARD'][ri][ci] = v + 1
            except:
                pass

    def reset(self):
        "reset board"
        self['BOARD'] = map ((lambda x,d=self: [0] * d['ROWS']),
                             range(self['COLS']))
        self['PLAYER'] = map ((lambda x,d=self: ['.'] * d['ROWS']),
                             range(self['COLS']))
        for (row,col) in self.random_bombs():
            self['BOARD'][row][col] = 'B'
            self.inc_neighbors(row,col)

    def to_string(self,board):
        str = ''
        for r in board:
            rstr = ''
            for c in r:
                rstr = rstr + '%s' % c
            str = str + '%s\n' % rstr
        return str
        
    def __repr__(self):
        board = self['BOARD']
        return self.to_string(board)

    def find_edges(self,row,col):
        "check up down left right"
        board = self['BOARD']
        player = self['PLAYER']
        to_explore = [(row,col)]
        try:
            if row < 0 or col < 0:
                raise IndexError, "smaller than 0"
            if player[row][col] is '.':
                v = board[row][col]
                player[row][col] = v
                ##print "updated,", row, col
                if v is 0:
                    for (r,c) in zip((0,0,-1,-1,-1,1,1,1),(-1,1,0,-1,1,0,-1,1)):
                        ri = row + r
                        ci = col + c
                        self.find_edges(ri,ci)
        except:
            pass

    def venture(self,row,col):
        msg = ''
        board = self['BOARD']
        player = self['PLAYER']
        v = board[row][col]
        
        if v is 'B':
            player[row][col] = 'X'
            msg = 'You lost!\n'
        elif v is 0:
            self.find_edges(row,col)
        else:
            player[row][col] = v
            if self.winp():
                msg = 'You won!\n'
        print msg + self.to_string(player)
        
    def winp(self):
        for (cb, cp) in zip(self['BOARD'], self['PLAYER']):
            cp = list(cp)
            for i in range(len(cp)):
                if cp[i] is '.': cp[i] = 'B'
            if tuple(cp) != tuple(cb):
                return 0
        return 1
        
if __name__ == '__main__':
    import string
    g = Game(ROWS=8,COLS=8, BOMBS=10)
        
    print '*' * 80
    print '*', "solution:"
    print '*' * 80
    print g

    while 1:
        try:
            r = string.atoi( raw_input('row:'))
            c = string.atoi( raw_input('col:'))
            g.venture(r,c)
        except:
            import sys
            print sys.exc_type, sys.exc_value
            if sys.exc_type is KeyboardInterrupt:
                raise KeyboardInterrupt
            print '*' * 80
            print '*', "solution:"
            print '*' * 80
            print g
