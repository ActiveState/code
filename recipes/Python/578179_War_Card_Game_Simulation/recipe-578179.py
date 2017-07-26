import random

################################################################################

def main():
    table = Table(['Matthew', 'Mark', 'Luke', 'John'])
    table.deal_cards()
    table.play_all()

def print_underline(string, line):
    print('\n{}\n{}'.format(string, line * len(string)))

################################################################################

class Table:

    def __init__(self, players):
        self.players = [Player(name, Hand()) for name in players]
        self.deck = Deck()
        self.rounds = 0

    def deal_cards(self):
        self.deck.shuffle()
        self.deck.setup_hands(self.players)
        for player in self.players:
            player.show_hand()

    def play_once(self, tied=None):
        if tied is None:
            self.count_round()
        collection = Pot()
        for player in (self.players if tied is None else tied):
            player.drop_card(collection)
            if tied:
                player.drop_bonus(collection, 3)
        winner = collection.winner
        if winner is not None:
            collection.reward(winner)
        else:
            winner = self.play_once(collection.tied)
            collection.reward(winner)
        return winner

    def count_round(self):
        self.rounds += 1
        print_underline('Starting round {}'.format(self.rounds), '=')

    def play_all(self):
        while not self.finished:
            self.play_once()
        self.show_winner()

    def show_winner(self):
        for player in self.players:
            if player.hand.has_cards:
                print()
                print(player.name, 'wins!')
                break

    @property
    def finished(self):
        return sum(bool(player.hand.cards) for player in self.players) == 1

################################################################################

class Player:

    def __init__(self, name, hand):
        self.name, self.hand = name, hand

    def drop_card(self, collection):
        if self.hand.has_cards:
            collection.add_card(self.hand.take_top(), self)

    def drop_bonus(self, collection, count):
        collection.add_bonus(self.hand.cards[:count])
        self.hand.cards = self.hand.cards[count:]

    def give_cards(self, cards):
        self.hand.add_all(cards)

    def show_hand(self):
        print(self.name, 'has', self.hand)

################################################################################

class Hand:

    def __init__(self):
        self.cards = []

    def __str__(self):
        return ', '.join(map(str, self.cards))

    def add_card(self, card):
        self.cards.append(card)

    def take_top(self):
        return self.cards.pop(0)

    def add_all(self, cards):
        self.cards.extend(cards)

    @property
    def has_cards(self):
        return bool(self.cards)

################################################################################

class Deck:

    def __init__(self):
        self.cards = [Card(s, r) for s in Card.SUITE for r in Card.RANKS]

    def shuffle(self):
        random.shuffle(self.cards)

    def setup_hands(self, players):
        hands = [player.hand for player in players]
        while len(self.cards) >= len(players):
            for hand in hands:
                hand.add_card(self.cards.pop())
        return hands

################################################################################

class Card:

    SUITE = 'H D S C'.split()
    RANKS = '2 3 4 5 6 7 8 9 10 J Q K A'.split()

    def __init__(self, suite, rank):
        self.suite, self.rank = suite, rank

    def __str__(self):
        return '{}-{}'.format(self.rank, self.suite)

    @property
    def value(self):
        return self.RANKS.index(self.rank)

################################################################################

class Pot:

    def __init__(self):
        self.cards = []
        self.players = []
        self.bonus = []

    def add_card(self, card, player):
        self.cards.append(card)
        self.players.append(player)

    def add_bonus(self, cards):
        self.bonus.extend(cards)

    @property
    def winner(self):
        self.show_pot()
        values = [card.value for card in self.cards]
        self.best = max(values)
        if values.count(self.best) == 1:
            return self.players[values.index(self.best)]

    def show_pot(self):
        for player, card in zip(self.players, self.cards):
            print('{} laid down a {}.'.format(player.name, card))

    def reward(self, player):
        player.give_cards(self.cards)
        player.give_cards(self.bonus)

    @property
    def tied(self):
        for card, player in zip(self.cards, self.players):
            if card.value == self.best:
                yield player

################################################################################

if __name__ == '__main__':
    main()
