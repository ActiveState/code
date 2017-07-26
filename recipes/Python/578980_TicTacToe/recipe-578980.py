from random import choice, randrange as rrange
from time import sleep
class Game:
    def _init__(self):
        self.p1 = ''
        self.p2 = ''
        self.map = []
        self.game = True
        self.done = False #For CPU
        self.count = 0
    def set_up(self):
        self.done = False
        self.game = True
        self.count = 0
        self.p1 = choice(['X','O'])
        if self.p1 =='X':
            self.p2 = 'O'
        else:
            self.p2 = 'X'
        print("You are ",self.p1)
        sleep(2)
        self.map = [0,1,2,3,4,5,6,7,8]
        self.cycle()
    def display(self):
        a = str(self.map).replace("[",'')
        b = a.replace(',','|')
        c = b.replace("'",'')
        d = c.replace("]",'')
        print(d[:7])
        print('-'*8)
        print(d[9:16])
        print('-'*8)
        print(d[18:])
    def check_map(self,a,b,c):
        if self.map[a]==self.map[b]==self.map[c]:
            if self.map[a] ==self.p1:
                print("YOU WIN")
                sleep(3)
                self.game = False
            else:
                print("COM WINS")
                sleep(3)
                self.game = False
        if self.count >=9:
            self.game = False
        if self.game==False:
            self.set_up()
    def play1(self):
        self.display()
        space = 0
        try:
            space = eval(input("Pick a space: "))
        except:
            NameError
            SyntaxError
            TypeError
            ValueError
            print("Invalid!")
        if space > 8:
            print("TRY AGAIN")
            self.play1()
        elif self.map[space] in ['X','O']:
            print("Space is used")
            sleep(1)
            self.play1()
        else:
            self.map[space] = self.p1
        self.check_map(0,1,2)
        self.check_map(3,4,5)
        self.check_map(6,7,8)
        self.check_map(0,3,6)
        self.check_map(1,4,7)
        self.check_map(2,5,8)
        self.check_map(0,4,8)
        self.check_map(2,4,6)
        self.count +=1
    def AI(self,a,b,c):
        if self.done ==False:
            if self.map[a]==self.map[b]:
                if self.map[c] not in ['X','O']:
                    self.map[c] = self.p2
                print("COM picked ",c)
                self.done = True
    def play2(self):
        print("")
        sm = choice([True,False])
        if sm ==True:
            self.AI(0,1,2)
            self.AI(3,4,5)
            self.AI(6,7,8)
            self.AI(0,3,6)
            self.AI(1,4,7)
            self.AI(2,5,8)
            self.AI(2,4,6)
            self.AI(0,4,8)
            self.AI(6,4,2)
            self.AI(8,4,0)
            self.AI(5,4,3)
            self.AI(2,1,0)
            self.AI(8,7,6)
        else:
            cpu = rrange(0,9)
            if self.map[cpu] not in ['X','O']:
                self.map[cpu] = self.p2
                print("COM picked ",cpu)
                self.done = True
        while self.done !=True:
            cpu = rrange(0,9)
            if self.map[cpu] not in ['X','O']:
                self.map[cpu] = self.p2
                print("COM picked ",cpu)
                self.done =True
        self.check_map(0,1,2)
        self.check_map(3,4,5)
        self.check_map(6,7,8)
        self.check_map(0,3,6)
        self.check_map(1,4,7)
        self.check_map(2,5,8)
        self.check_map(0,4,8)
        self.check_map(2,4,6)
        self.count +=1
    def cycle(self):
        while self.game==True:
            self.done =False
            self.play1()
            self.play2()
            print()
game = Game()
game.set_up()
