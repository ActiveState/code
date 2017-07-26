from random import choice, randrange as rrange, shuffle
from time import sleep, ctime
from sys import getsizeof
from decimal import Decimal

class Game:
    def __init__(self):
        self.empty = ''
        self.create_word = ''
        self.word_hint = ''
        self.life = 0
        self.bank = []
        self.count = 0
        self.fail = 0
        self.os = True
        self.fill_word = []
    def set_up(self):
        self.fill_word = []
        u = input("Memory Size:\n1.Low\n2.Medium\n3.Normal\n4.High\n5.Maximum")
        if u=='1':
            n = 1
        elif u=='2':
            n = 5
        elif u=='3':
            n = 10
        elif u=='4':
            n = 20
        elif u=='5':
            n = 50
        else:
            n = 10
        self.fill_memory(n)
        self.life = 5
        if self.empty ==True:
            print("First you need to create some questions")
            self.create()
        else:
            self.main()
    def clear(self):
        a = 0
        while a < 2:
            print()
            a +=1
    def fill_memory(self,n):
        print("Loading...")
        while getsizeof(self.bank) < 1024*1024*n:
            self.bank.append(['none','none'])
        self.clear()
    def display1(self,w,n):
        #For view, edit, and delete
        a = str(w).replace('[','')
        b = a.replace(',',':')
        c = b.replace("'",'')
        d = c.replace(']','')
        print(n,d)
    def check_bank(self):
        a = 0
        c = 0
        print('Checking...')
        while a < len(self.bank):
            if 'none' not in self.bank[a]:
                c +=1
            a +=1
        self.empty = c
        self.clear()
        print(self.empty,' words found')
    def create(self):
        self.clear()
        self.create_word = input("What is the word? ")
        self.word_hint = input("Type a hint or description of the word: ")
        print(self.create_word,':',self.word_hint)
        en = input("Does this seem accurate? ").lower()
        if en in ['no','n','nope']:
            self.create()
            self.clear()
        else:
            self.bank[self.count] = [self.create_word,self.word_hint]
            self.count +=1
            self.clear()
            self.main()
    def clear_all_memory(self):
        a = 0
        print("Clearing memory...")
        while a < len(self.bank):
            p = Decimal(a) / len(self.bank)
            p *=100
            self.bank[a] = [0,0]
            a+=1
    def delete_word(self):
        try:
            self.view(0)
            d = eval(input("Delete? "))
        except:
            NameError
            TypeError
            SyntaxError
            ValueError
            print("Error!")
            self.main()
        self.bank[d] = ['none','none']
        self.clear()
        self.main()

    def view(self,u):
        print()
        a = 0
        while a < len(self.bank):
            if 'none'not in self.bank[a]:
                self.display1(self.bank[a],a)
            a +=1
        e = input()
        if u=='main':
            self.main()
    def display2(self,w):
        #For play
        while len(self.fill_word) < len(w):
            self.fill_word.append('_')
        a = str(self.fill_word).replace('[','')
        b = a.replace(',','')
        c = b.replace("'",'')
        d = c.replace(']','')
        print(d)
    def edit(self):
        a = 0
        d = 0
        self.view(0)
        try:
            d = eval(input('Edit? '))
        except:
            NameError
            ValueError
            TypeError
            SyntaxError
            print('Error!')
            self.main()
        if d in range(0,len(self.bank)):
            if 'none' not in self.bank[d]:
                word = self.bank[d]
                print(word[0],':',word[1])
                w = input('New hint for this?')
                self.bank[d][1] = w
            else:
                print('No word stored here')
        else:
            print('OUT OF RANGE')
        self.clear()
        self.main()

    def play(self):
        game = True
        s = 0
        print('Please wait...')
        shuffle(self.bank)
        while 'none' in self.bank[s]:
            self.fail +=1
            s = rrange(0,len(self.bank))
        print(self.fail)
        word = self.bank[s]
        f = False
        while game==True:
            print("Life Left: ",self.life)
            f = False
            print('Hint: ',word[1])
            self.display2(word[0])
            letter = input(": ")
            if word[0]==letter:
                print("WOW")
                game = False
            else:
                a = 0
                while a < len(word[0]):
                    if word[0][a]==letter:
                        self.fill_word[a]= letter
                        f = True
                    a +=1
            if f==False:
                self.life -=1
            if self.life < 0:
                game = False
            if '_' not in self.fill_word:
                game = False
        print(word[0])
        print('GAME OVER')
        self.clear()
        self.main()

    def main(self):
        self.check_bank()
        print('Memory being used:',int(getsizeof(self.bank)/1024/1024),'MB')
        user = input('1.PLAY\n2.CREATE\n3.EDIT\n4.DELETE\n5.VIEW\n6.EXIT')
        if user=='1':
            self.play()
        elif user=='2':
            self.create()
        elif user=='3':
            self.edit()
        elif user=='4':
            self.delete_word()
        elif user=='5':
            self.view('main')
        elif user=='6':
            self.clear_all_memory()
            print('System shutting down...')
        else:
            self.main()
game = Game()
game.set_up()
