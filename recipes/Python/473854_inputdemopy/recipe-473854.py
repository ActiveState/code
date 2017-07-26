from msvcrt import kbhit, getch
from os import system
from time import sleep

x = 0
y = 0

def show(ch):
    system('cls')
    for z in range(y):
        print
    print ' ' * x + ch

while True:
    sleep(0.03)
    if kbhit():
        if getch() == '\xe0':
            ch = getch()
            if ch == 'H':
                y -= 1
                show('^')
            elif ch == 'M':
                x += 1
                show('>')
            elif ch == 'P':
                y += 1
                show('V')
            elif ch == 'K':
                x -= 1
                show('<')
