#!/usr/bin/env python
from string import split

first_name = split("""
chet
frank
olga
ethel
norman
chuck
velma
cleo
""")

last_name = split("""
milquetoast
roth
bumstead
toodles
menderchuck
""")

er = split("""
killer
slayer
smiter
destroyer
defenestrator
""")

p = split("""
of
""")

adj = split("""very small
tiny
non-combatant
defenseless""",'\n')

n = split("""reindeer
bunnies
probate-attorneys
inanimate objects
fruit""",'\n')
          
name = [first_name,last_name,[','],er,p,adj,n]

if __name__ == '__main__':
    import random
    try:
        i = hash(raw_input('enter your name:'))
    except:
        i = 35

    random.seed(i)
    print 'your viking name is',

    for i in map(lambda list: random.choice(list), name):
        print i,
