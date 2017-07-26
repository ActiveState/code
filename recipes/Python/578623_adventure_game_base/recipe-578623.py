## bctg.py
## by andrew wayne teesdale jr.
class LL:
    def __init__(self, ll, name):
        import random
        self.randnum=random.choice(['True', 'False'])
        self.msg=random.choice(['I dont know.', 'Oh, Yes '+ll, 'I think '+name+' knows.'])
    def say_to(self, msg):
        ## msging system
        print msg
    def fight_thing(self, moolaugh, things):
        import random
        bg=random.choice(things)
        print 'You see a '+bg+' It attacks you'
        if self.randnum == 'True':
            fmsg='Died!'
        else:
            fmsg='Killed it'
            moolaugh=moolaugh+random.randint(1, 40)
        print 'You '+fmsg
    def reply_to(self, msg):
        print 'The person says:'
        print msg
## player class
## is related
## to monster
## class.
class Player(LL):
    def __init__(self, name1):
        LL.__init__(self, "None", "None")
        self.name=name1
        self.money=0
        self.weapons=['sword']
        self.keys=[]
    def say(self, s):
        print 'You say:'
        self.say_to(s)
    def fight(self):
        self.fight_thing(self.money)
    def pickup(self, thing):
        things=[['coin', 'ruby'], ['key'], ['shield', 'bow', 'arrows']]
        if thing in things[2]:
            self.weapons.append(thing)
            print 'You got a '+thing
        elif thing in things[0]:
            if thing == 'coin':
                self.money=self.money+1
                print 'you got a '+thing
            elif thing == 'ruby':
                self.money=self.money*2
            else:
                print "weird not a kind of currency I've seen before."
        elif thing in things[1]:
            print 'cool a key.'
            self.keys.append(thing)
        else:
            print 'what is it!'
            print 'ill keep it'
            self.weapons.append(thing)
    def sell(self, price, thing):
        self.weapons.remove(thing)
        self.money=self.money+price
    def show_stat(self):
        self.say(self.money)
        self.say(self.weapons)

## Npc class is a subclass of LL
## It is the non player class

class Npc(LL):
    def __init__(self, info, keyto, kinfo, list):
        LL.__init__(self, "None", "None")
        self.info=info
        self.keyto=keyto
        self.kinfo=kinfo
        self.list=list
    def talk(self):
        import random
        print 'my names '+random.choice(['Neec', 'Nal', 'Zeenosx', 'Teelal', 'Meron', 'Peelal'])
        if self.keyto in self.list:
            self.say_to('ooh could i have that')
            if raw_input('y-n?]') == 'y':
                self.list.remove(self.keyto)
                self.say_to('Thankyou!')
                self.say_to('Hey by the way')
                self.say_to(self.kinfo)
            else:
                self.say_to('Ok-Ok! Fine keep it')
        else:
            self.say_to(self.info)
class Door:
    def __init__(self, key, lst):
        self.key = key
        self.list = lst
        self.exst = '0'
    def check(self):
        if self.key in self.list:
            self.list.remove(self.key)
            self.exst="1"
        else:
            print "you don't have the right key for this door"
        ## check if key is in inventory
        if self.exst == '1':
            return True
        else:
            return False
        
## Shell parser syntax
import time
class ascii:
    def __init__(self):
        self.version=1.0
    def clear(self):
        print "\n"*1000
    def pause(self, i):
        time.sleep(i)
    def roll_film(self, film, repi=1):
        for k in range(1, repi):
            for j in film:
                print j
                self.pause(1)
                self.clear()
            self.clear()
    def example(self):
        listf=['.  ',  ' . ', '  .']
        self.roll_film(listf, 100)
    def create_film(self, film):
        return film
    
def prompt():
    return raw_input('?]')
def test_game_funcs():
    print 'Name:'
    player=Player(prompt())
    player.fight()
    player.pickup('key')
    player.say('hello my name is bobby the busybody')
    npc=Npc('I know you', 'sword', 'I know evrybody', player.weapons)
    npc.talk()
    door=Door('key', player.keys)
    print door.check()
def small_text_game():
    print "name please:"
if __name__ == "__main__":
    test_game_funcs()
