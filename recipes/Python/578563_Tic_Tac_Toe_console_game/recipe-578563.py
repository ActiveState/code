import random


class TTTGame(object):

    _coords = [(x, y) for y in range(3) for x in range(3)]
    _num_to_coord = dict([(n+1, c) for n, c in enumerate(_coords)])
    _win_ways = (# Horizontal
                 set([1, 2, 3]),
                 set([4, 5, 6]),
                 set([7, 8, 9]),
                 # Verticle
                 set([1, 4, 7]),
                 set([2, 5, 8]),
                 set([3, 6, 9]),
                 # Diagonal
                 set([1, 5, 9]),
                 set([3, 5, 7]))

    def __init__(self, game=None):
        if not game:
            self.board = map(list, ['___'] * 3)
            self.avail = set(xrange(1, 10))
            self.xnums = set()
            self.onums = set()
        else:
            self.board = map(list, game.board)
            self.avail = set(game.avail)
            self.xnums = set(game.xnums)
            self.onums = set(game.onums)

    def __str__(self):
        rows = [' | '.join(row).replace('_',' ')
                for row in self.board[::-1]]
        divs = ['\n---+---+---\n', '\n---+---+---\n', '\n']
        return ' ' + ' '.join(map(''.join, zip(rows, divs)))

    def winner(self):
        """Return 'X' or 'O' or 'T' else False if game not over."""
        for way in self._win_ways:
            if way.issubset(self.xnums):
                return 'X'
            if way.issubset(self.onums):
                return 'O'
        if len(self.xnums) + len(self.onums) == 9:
            return 'T'
        return False

    def play(self, n, piece=None):
        """
        Place piece at spot numbered n and ammend attributes.
        if piece is None, remove the piece at cell n and ammend attributes.
        """
        x, y = self._num_to_coord[n]
        if piece:
            self.board[y][x] = piece
            (self.xnums if piece == 'X' else self.onums).add(n)
            self.avail.remove(n)
        else:
            self.board[y][x] = '_'
            self.avail.add(n)
            (self.xnums if n in self.xnums else self.onums).remove(n)

    def next_move(self, piece):
        """
        Return the next best move for piece as cell number.
        """
        if all(map(lambda x: len(set(x)) == 1, self.board)):
            return random.choice((1, 3, 7, 9)) # Corners are best first play.
        scores = []
        avail = list(self.avail)
        for n in avail:
            node = TTTGame(self)
            node.play(n, piece)
            scores.append(node._evaluate(piece))
        best = max(enumerate(scores), key=lambda x: x[1])[0]
        return avail[best]

    def _evaluate(self, piece):
        """
        Return a score for how favourable the current board is towards piece.
        """
        state = self.winner()
        if state:
            return (1 if state == piece else 0 if state == 'T' else -1)
        scores = []
        apponent = 'OX'.replace(piece, '')
        for n in self.avail:
            self.play(n, apponent)
            scores.append(0-self._evaluate(apponent))
            self.play(n) # reverse play
        safest = min(scores)
        return safest



class CLI(object):
    # - Note that game_loop() is not concerned with any of the display
    #   attributes or refreshing the screen.
    # - Each method is responsible for
    #   handling it's own display characteristics, for now, with the use of
    #   the message attribute and refresh().
    # - Methods which modify the message attribute should assign an empty 
    #   string to message attribute before returning, except in cases like
    #   coin_toss().
    # - Methods may communicate with each other via return values, not
    #   via message or any other display attribute.

    def __init__(self):
        # Display variables.
        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.message = ''
        # Piece assignments.
        self.player = ''
        self.computer = ''
        # TTTGame instance.
        self.game = None
        # Players turn or not.
        self.turn = None

    def refresh(self):
        screen = '\n' * 100 # Clear screen.
        screen += "TicTacToe\n"
        screen += ("wins:%s\tlosses:%s\tties:%s\n\n" %
                   (self.wins, self.losses, self.ties))
        screen += str(self.game) if self.game else '\n' * 4 # The game board.
        screen += '\n' + self.message + '\n'
        print screen

    def coin_toss(self):
        """Assigns player a piece at random, Returns None."""
        while True: # until user enters valid input
            self.refresh()
            option = raw_input("Heads or Tails (or just hit enter)? ")
            if option.lower() in ['', 'heads', 'h', 'tails', 't']:
                self.player = random.choice(['X', 'O'])
                self.computer = 'XO'.replace(self.player, '')
                break
            else:
                self.message = "That's not a valid choice!"
        self.message = "You go first" if self.player == 'X' else ''

    def player_turn(self):
        while True: # until user enters valid input
            self.refresh()
            option = raw_input("cell number: ").strip().lower()
            if option == 'hint':
                self.message = str(self.game.next_move(self.player))
            elif not (option.isdigit() and 1 <= int(option) <= 9):
                self.message = "That's not a valid option!"
            elif int(option) not in self.game.avail:
                self.message = "That cell is already occupied!"
            else:
                break
        self.game.play(int(option), self.player)
        self.message = ''

    def computer_turn(self):
        self.refresh()
        best = self.game.next_move(self.computer)
        self.game.play(best, self.computer)
        self.message = ''

    def play_again(self):
        """Gives user the chance to quit the program or continue."""
        while True: # until user enters valid input
            self.refresh()
            option = raw_input("Play again (enter) or n? ").strip().lower()
            if not option:
                self.message = ''
                return
            elif option in ["no", 'n']:
                import sys
                sys.exit()
            else:
                self.message = "That's not a valid option!"

    def game_loop(self):
        """Simple game loop."""
        while True:
            self.game = TTTGame()
            self.coin_toss()
            self.turn = (self.player == 'X') # X always goes first.
            while not self.game.winner():
                if self.turn:
                    self.player_turn()
                else:
                    self.computer_turn()
                self.turn = not self.turn
            winner = self.game.winner()
            if winner == 'T':
                self.message = "You tied."
                self.ties += 1
            elif winner == self.player:
                self.message = "You won!"
                self.wins += 1
            else:
                self.message = "You lost."
                self.losses += 1
            self.play_again()


if __name__ == '__main__':
    print '\n' * 100
    print ("Welome to TicTacToe\n\n" +
           "Cells are numbered 1 to 9 and correspond directly\n" +
           "with keys on your keyboards numpad.\n\n" +
           "To make a play, type the relevent number and hit enter\n\n" +
           "You can also type hint when it's your turn to play.\n\n" +
           "BTW, the computer is unbeatable. Which means your win\n" +
           "statistic will never show anything other than 0.\n" +
           "Have fun ;)\n\n")
    raw_input(".... (hit enter) ...")
    user_interface = CLI()
    user_interface.game_loop()
