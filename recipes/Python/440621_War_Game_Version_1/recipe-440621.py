import random, time

def main():
    '''Starts the game.

    This function is the first function that gets called.
    It shows a welcome message and then gets input.
    The input loop is designed to handle errors.
    The information gathered is the number of players playing the game.'''
    print 'Welcome to WAR!'
    loop = True
    while loop:
        try:
            players = int(raw_input('How many players are there? '))
            if players < 2:
                print 'There must be at least two players.'
            else:
                loop = False
        except:
            print 'You must enter a number.'
    launch_game(players)

def launch_game(players):
    '''Starts pre-game and game.

    This sets up the game.
    It then starts the game play.'''
    setup_game(players)
    play_game()

def setup_game(players):
    '''Creates deck and sets up players.

    This sets up a playing deck from which cards are to be distributed.
    The next function call then distributes the cards from the deck.'''
    create_deck(players)
    setup_players(players)

def create_deck(players):
    '''Creates the playing deck.

    The deck is global because all parts of the program should be able to access it.
    (Actually, just one fuction needs it, but its being visible everywhere else is fine.
    This was the line of code that was being avoided: setup_players(create_deck(players)).
    setup_game is most clear this way as to what gets done first.)
    The deck is composed of cards 0 - 9, one for each player in the game.'''
    global deck
    deck = []
    for number in range(10):
        for card in range(players):
            deck.append(number)

def setup_players(players):
    '''Prepares the data for the players.

    Hands is global because it needs to be seen during game play.
    Hands stores the cards of each player.
    The cards should be randomly picked from the deck and distributed.
    A hand is what each player has (regarding that person's cards).
    A card is selected, given to a players, and then deleted from the deck.
    Once a player's hand has been created, it is added to the list of hands.'''
    global hands
    hands = []
    random.seed(time.time())
    for player in range(players):
        hand = []
        for card in range(10):
            index = random.randint(0, len(deck) - 1)
            hand.append(deck[index])
            del deck[index]
        hands.append(hand)

def play_game():
    '''Is main game loop.

    Round keeps track of what round all players are currently on.
    (As you will see later, each "round" does not go around the players.)
    Table keeps track of what has been placed on the table during a round.
    The program needs to know who is playing so it asks for everyone's name.
    A loop is setup where the table is reset at the beginning of each round.
    The round number is also updated and a round is played.
    At the end of a round, the results of that round are calculated.
    When then game is over, post-game is taken care of.'''
    global round, table
    round = 0
    get_names()
    playing = True
    while playing:
        table = []
        round += 1
        play_round()
        playing = create_results()
    finish_game()

def get_names():
    '''Gets player's names.

    This lets the program say who is playing so that people do not need to know their number.
    names is global so that it can be seen during game play.
    This is just a simple input loop that stores names in the list called "names."'''
    global names
    names = []
    for name in range(len(hands)):
        names.append(raw_input('What is the name of player ' + str(name + 1) + '? '))

def play_round():
    '''Goes through a round.

    Players is a list of people who still need to play.
    Only those people who still have cards are going to play.
    A loop handles each playing person's turn.
    The screen is cleared for privacy during the game.
    A random playing player is selected and deleted from the list.
    The round number is printed for reference.
    The player that is up for play is notified and the game waits for the passing of program control.
    The table is shown for reference of the player.
    The player's current hand of cards is displayed for reference as well.
    The player's action is then requested.'''
    players = []
    for player in range(len(names)):
        if len(hands[player]) > 0:
            players.append(player)
    for turn in range(len(players)):
        clear_screen()
        index = random.randint(0, len(players) - 1)
        player = players[index]
        del players[index]
        print 'Round', round
        raw_input('It is ' + names[player] + "'s turn to play.")
        show_table()
        show_hand(player)
        get_action(player)        

def clear_screen():
    '''Clears screen.

    A loop prints out X number of new-lines.
    X should be the height of the viewing screen.'''
    for line in range(50):
        print

def show_table():
    '''Shows the current table.

    If there are no cards on the table yet, the condition is handled.
    Otherwise, what each player has played so far and the players' names are displayed.'''
    if len(table) == 0:
        print 'There are no cards on the table.'
    else:
        for card in range(len(table)):
            print names[table[card][0]] + ' played a ' + str(table[card][1]) + '.'

def show_hand(player):
    '''Displays a player's hand.

    The main action of this fuction is the formating of list of cards.
    "Player" selects a player's hand to be displayed (zero based).
    The list is converted to a string, and the brackets are removed.
    Notice that "and" is not inserted into the last part of the string.'''
    print 'These are your cards: ' + str(hands[player])[1:-1] + '.'

def get_action(player):
    '''Gets action of player.

    This is of similar design to the input loop found in main().
    A few more possibilities are handled.
    Note the inner-most logic.
    The line "hands[player].index(card)" is not needed because an exception is raised when trying to remove an item that does not exist.
    The line previosly mentioned has been left in place for historical purposes (documentation), and the line does not result in errors.
    Note "table.append((player, card))."
    A tuple on the table remembers who played what.'''
    asking = True
    while asking:
        try:
            card = int(raw_input('What card do you want to play? '))
            try:
                if card >= 0 and card <= 9:
                    hands[player].index(card)
                    hands[player].remove(card)
                    table.append((player, card))
                    asking = False
                else:
                    print 'Please enter a value between -1 and 10.'
            except:
                print 'You do not have that card.'
        except:
            print 'Please enter a number.'

def create_results():
    '''Calculates result of round.

    The table is displayed for all players to see.
    Variable "high_card" keeps track of the highest value card on the table.
    The first loop finds the highest-valued card.
    Variable "hand_out" keeps track of players who may have table cards distributed to them.
    The second loop finds those players who may received table cards.
    The third loop randomly distributes table cards to people on the hand_out list.
    The hands are shown, and the status of game play is found.
    The end of the round is noted for reference, and game play status is returned.'''
    show_round()
    high_card = 0
    for index in range(len(table)):
        if table[index][1] > high_card:
            high_card = table[index][1]
    hand_out = []
    for index in range(len(table)):
        if table[index][1] == high_card:
            hand_out.append(table[index][0])
    while len(table) > 0:
        hands[hand_out[random.randint(0, len(hand_out) - 1)]].append(table[0][1])
        del table[0]
    result = show_hands()
    print
    raw_input('End Of Round')
    return result

def show_round():
    '''Shows result of round.

    The screen is cleared for the last player's privacy.
    The table is shown to all players to see what was on the table at the end of the round.'''
    clear_screen()
    show_table()

def show_hands():
    '''Shows how many cards everyone has.

    Variable "players" keeps track of how many people are still in play.
    The loop goes through the hands of all those still playing and displays how many cards they have.
    If only one player has cards, then the game is over.'''
    players = 0
    print
    for player in range(len(names)):
        if len(hands[player]) > 0:
            players += 1
            print names[player] + ' has ' + str(len(hands[player])) + ' cards.'
    if players == 1:
        return False
    else:
        return True

def finish_game():
    '''Executes post-game.

    The screen is cleared for simplicity.
    The winner of the game is found.
    The winner is congratulated and the number of cards that were captured is displayed.
    End of game is noted.'''
    clear_screen()
    for player in range(len(names)):
        if len(hands[player]) != 0:
            winner = player
    print 'Congratulations go to ' + names[winner] + '! All ' + str(len(names) * 10) + ' cards were collected!'
    print
    raw_input('GAME OVER')

if __name__ == '__main__':
    main()
