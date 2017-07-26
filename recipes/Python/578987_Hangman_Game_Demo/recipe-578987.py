from random import choice, randrange as rrange, shuffle
from time import sleep, ctime
from sys import getsizeof

class Game:
    def __init__(self):
        self.create_word = ''
        self.word_hint = ''
        self.life = 0
        self.bank = []
        self.fill_word = []
    def set_up(self):
        self.fill_word = []
        self.life = 5
        if self.bank ==[]:
            print("First you need to create some questions")
            self.create()
        else:
            self.main()
    def display1(self,w,n):
        #For view, edit, and delete
        a = str(w).replace('[','')
        b = a.replace(',',':')
        c = b.replace("'",'')
        d = c.replace(']','')
        print(n,d)
    def create(self):
        print("")
        self.create_word = input("What is the word? ")
        self.word_hint = input("Type a hint or description of the word: ")
        print(self.create_word,':',self.word_hint)
        en = input("Does this seem accurate? ").lower()
        if en in ['no','n','nope']:
            self.create()
        else:
            self.bank.append([self.create_word,self.word_hint])
            self.main()
    def view(self):
        print()
        a = 0
        for i in self.bank:
            self.display1(i,a)
            a +=1
    def display2(self,w):
        #For play
        while len(self.fill_word) < len(w):
            self.fill_word.append('_')
        a = str(self.fill_word).replace('[','')
        b = a.replace(',','')
        c = b.replace("'",'')
        d = c.replace(']','')
        print(d)
    def play(self):
        game = True
        word = self.bank[0]
        f = False
        while game==True:
            print("Life Left: ",self.life)
            f = False
            print('Hint: ',word[1])
            self.display2(word[0])
            letter = input(": ")
            a = 0
            while a < len(word[0]):
                if word[0][a]==letter:
                    self.fill_word[a]= letter
                    f = True
                a +=1
            if f==False:
                self.life -=1
            if self.life <0:
                self.game = False
            if '_' not in self.fill_word:
                game = False
        print(word[0])
        print('GAME OVER')

    def main(self):
        print()
        user = input('1.PLAY\n2.CREATE\n3.EDIT\n4.DELETE\n5.VIEW')
        if user=='1':
            self.play()
        elif user=='2':
            self.create()
        elif user=='3':
            pass
        elif user=='4':
            pass
        elif user=='5':
            self.view()
        else:
            print(len(self.bank[0][0]))
            self.display2(self.bank[0][0])
game = Game()
game.set_up()
