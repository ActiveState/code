"""A simple money counting game for kids."""

import random
import sys


class Money:
    def __init__(self):
        pass

    @staticmethod
    def display_intro():
        """Display the introduction at the start of program execution."""
        print('*' * 75)
        print('This is a simple money countinggame to help kids learn '
              'to count money.')
        print('The program helps kids learn various change amounts in US '
              'currency.')
        print('*' * 75)

    def start(self):
        """Randomly display an amount of change and ask how many of each coin
        type are needed to equal the amount displayed.
        """
        self.display_intro()
        currency_amt = random.randint(1, 99)
        print('\nHow much change is needed to equal .{0} cents?\n'
              .format(str(currency_amt)))
        your_total_amt = get_input_values(currency_amt)

        if sum(your_total_amt) == 0:
            print('Thank you for playing.')
            sys.exit(0)
        else:
            if your_total_amt[0] > 1 or your_total_amt[0] == 0:
                quarter_spelling = 'quarters'
            else:
                quarter_spelling = 'quarter'

            if your_total_amt[1] > 1 or your_total_amt[1] == 0:
                dime_spelling = 'dimes'
            else:
                dime_spelling = 'dime'

            if your_total_amt[2] > 1 or your_total_amt[2] == 0:
                nickel_spelling = 'nickels'
            else:
                nickel_spelling = 'nickel'

            if your_total_amt[3] > 1 or your_total_amt[3] == 0:
                penny_spelling = 'pennies'
            else:
                penny_spelling = 'penny'

            print('\nCorrect! You entered {0:d} {1}, {2:d} {3},'
                  ' {4:d} {5} and {6:d} {7}.'.format(your_total_amt[0],
                                                     quarter_spelling,
                                                     your_total_amt[1],
                                                     dime_spelling,
                                                     your_total_amt[2],
                                                     nickel_spelling,
                                                     your_total_amt[3],
                                                     penny_spelling))
            print('Which equals .{0} cents. Nice job!'
                  .format(str(currency_amt)))
            
            response = input('\nWould you like to try again? ')
            if response.lower() != 'y':
                print('Thanks for playing.')
                sys.exit(0)
            self.start()


def get_input_values(currency_amt):
    """Main logic of the program that tallies the value of each entered
    coin. Validation on the values entered is also performed.
    """
    quarter = 25
    dime = 10
    nickel = 5
    penny = 1
    total_amt = 0
    total_quarters = 0
    total_dimes = 0
    total_nickels = 0
    total_pennies = 0

    print('Enter change in the form of (25 = quarter, 10 = dime,'
          ' 5 = nickel, 1 = penny)')
    coin_value = input('Enter coin amount: ')

    while len(coin_value) > 0:        
        try:
            coin_amt = int(coin_value)
            if not coin_amt not in (quarter, dime, nickel, penny):
                if coin_amt < currency_amt or coin_amt < total_amt:
                    if (coin_amt + total_amt) <= currency_amt:
                        if (coin_amt + total_amt) != currency_amt:
                            if coin_amt == 25:
                                total_quarters += 1
                                total_amt += quarter
                            elif coin_amt == 10:
                                total_dimes += 1
                                total_amt += dime
                            elif coin_amt == 5:
                                total_nickels += 1
                                total_amt += nickel
                            elif coin_amt == 1:
                                total_pennies += 1
                                total_amt += penny
                            else:
                                print('This is not a valid amount!\n')
                            print('Enter change in the form of (25 = quarter,'
                                  ' 10 = dime,  5 = nickel, 1 = penny)')
                            coin_value = input('\nEnter coin amount: ')
                        else:
                            if coin_amt == 25:
                                total_quarters += 1
                            elif coin_amt == 10:
                                total_dimes += 1
                            elif coin_amt == 5:
                                total_nickels += 1
                            elif coin_amt == 1:
                                total_pennies += 1
                            break
                    else:
                        print('You have entered more than I currently have'
                              ' totalled up!')
                        print('\nI currently have a total of .{0} and need to get to .{1}'
                              .format(str(total_amt), str(currency_amt)))
                        print('Enter change in the form of (25 = quarter,'
                              ' 10 = dime,  5 = nickel, 1 = penny)')
                        coin_value = input('\nEnter coin amount: ')
                else:
                    if (coin_amt + total_amt) > currency_amt:
                        print('You entered more than what I need')
                        print('Enter change in the form of (25 = quarter,'
                              ' 10 = dime,  5 = nickel, 1 = penny)')
                        coin_value = input('\nEnter coin amount: ')

                    if (coin_amt + total_amt) != currency_amt:
                        print('\nEnter change in the form of (25 = quarter,'
                              ' 10 = dime,  5 = nickel, 1 = penny)')
                        coin_value = input('\nEnter coin amount: ')
                    else:
                        if coin_amt == 25:
                            total_quarters += 1
                        elif coin_amt == 10:
                            total_dimes += 1
                        elif coin_amt == 5:
                            total_nickels += 1
                        elif coin_amt == 1:
                            total_pennies += 1
                        break
            else:
                print('This is not a valid amount!\n')
                print('\nEnter change in the form of (25 = quarter,'
                      ' 10 = dime,  5 = nickel, 1 = penny)')
                coin_value = input('\nEnter coin amount: ')
        except ValueError:
            print('This is not a valid amount!')
            coin_value = input('\nEnter coin amount: ')

    currency_totals = (total_quarters, total_dimes, total_nickels,
                       total_pennies)
    return currency_totals


if __name__ == '__main__':
    money_game = Money()
    money_game.start()
