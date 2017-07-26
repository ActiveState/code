###############################
#  old_password_generator.py  #
###############################

import string, random, sys

SELECT = string.ascii_letters + string.punctuation + string.digits
SAMPLE = random.SystemRandom().sample

def main():
    while True:
        size = get_size()
        password = generate_pw(size)
        print_pause(password)

def get_size():
    while True:
        try:
            size = int(input('Size: '))
        except ValueError:
            print('Please enter a number.')
        except EOFError:
            sys.exit()
        else:
            if 1 <= size <= 80:
                return size
            print('Valid number range is 1 - 80.')

def generate_pw(size):
    password = ''.join(SAMPLE(SELECT, size))
    while not approved(password):
        password = ''.join(SAMPLE(SELECT, size))
    return password

def approved(password):
    group = select(password[0])
    for character in password[1:]:
        trial = select(character)
        if trial is group:
            return False
        group = trial
    return True

def select(character):
    for group in (string.ascii_uppercase,
                  string.ascii_lowercase,
                  string.punctuation,
                  string.digits):
        if character in group:
            return group
    raise ValueError('Character was not found in any group!')

def print_pause(*values, sep=' ', end='\n', file=sys.stdout):
    print(*values, sep=sep, end=end, file=file)
    try:
        input()
    except EOFError:
        pass

if __name__ == '__main__':
    main()

###############################
#  new_password_generator.py  #
###############################

from random import SystemRandom
from string import ascii_lowercase, ascii_uppercase, digits, punctuation

CHOICE = SystemRandom().choice
GROUPS = ascii_lowercase, ascii_uppercase, digits, punctuation

def main():
    while True:
        print('Code:', make_password(get_size()))

def get_size():
    while True:
        try:
            size = int(input('Size: '))
        except ValueError:
            print('Please enter a number.')
        except EOFError:
            raise SystemExit()
        else:
            if 10 <= size <= 80:
                return size
            print('Valid number range is 10 - 80.')

def make_password(size):
    while True:
        password = ''
        pool = using = tuple(map(set, GROUPS))
        while True:
            selection = CHOICE(using)
            character = CHOICE(tuple(selection))
            password += character
            if len(password) == size:
                return password
            selection.remove(character)
            if not selection:
                break
            using = tuple(group for group in pool if group is not selection)

if __name__ == '__main__':
    main()
