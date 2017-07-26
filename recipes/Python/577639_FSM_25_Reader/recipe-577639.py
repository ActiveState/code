import sys
import os

FILE = os.path.basename(sys.argv[0])

def main():
    identity = get_identity()
    text = get_messages(identity)
    print_messages(text)

def get_identity():
    try:
        return sys.argv[1]
    except IndexError:
        print('Usage: {} <identity>'.format(FILE))
        sys.exit()

def get_messages(identity):
    for name in os.listdir('.'):
        if os.path.isfile(name) and name != FILE:
            with open(name) as file:
                title, text = file.read().split('\0', 1)
                if title == identity:
                    return text
    print(repr(identity), 'not found.')
    sys.exit()

def print_messages(text):
    message = iter(text.split('\0'))
    try:
        while True:
            try:
                print('[{}] {}'.format(next(message), next(message)))
            except UnicodeEncodeError:
                pass
    except StopIteration:
        pass

if __name__ == '__main__':
    main()
