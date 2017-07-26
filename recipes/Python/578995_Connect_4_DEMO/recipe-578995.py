from random import choice
from time import sleep
class Game:
    def __init__(self):
        self.map = []
        self.p1 = 0
        self.p2 = 0
        self.game = False
    def set_up(self):
        a = 0
        self.game = True
        self.map = [[],[],[],[],[],[]]
        while a < len(self.map):
            while len(self.map[a]) < 6:
                self.map[a].append(' ')
            a +=1
        user = input('What piece do you want to be represented by: R or Y ? ').lower()
        if user=='r':
            self.p1 ='R'
            self.p2 = 'Y'
        elif user=='y':
            self.p1 = 'Y'
            self.p2 = 'R'
        else:
            self.p1 = 'R'
            self.p2 = 'Y'
    def display(self,n):
        a = str(n).replace("[",'')
        b = a.replace(',','|')
        c = b.replace("'","")
        d = c.replace(']','')
        print('|',d,'|')
    def display2(self):
        print('  0  1  2  3  4  5')
        print('-'*20)
        for i in self.map:
            self.display(i)
            print('-'*20)
    def play1(self):
        self.display2()
        col = 0
        try:
            col = eval(input('Pick a column: '))
        except:
            NameError
            TypeError
            ValueError
            SyntaxError
            print('Try Again')
            self.play1()
        if col not in range(0,6):
            print('Out of range')
            self.play1()
        else:
            if self.game==True:
                self.insert(col,self.p1)
    def check_full(self):
        c = 0
        a = 0
        r = 0
        while a <  6:
            while r < 6:
                if self.map[a][r] in ['R','Y']:
                    c +=1
                r +=1
            r = 0
            a+=1
        if c >=36:
            print('FULL')
            self.game = False
            self.set_up()
    def check_map(self,n):
        a = 0  #row
        b = 0 #space
        c = 0 #counting
        while a < 6:
            while b < 6:
                if self.map[a][b]==n:
                    c +=1
                else:
                    c = 0
                if c >=4:
                    self.game = False
                b +=1
            b = 0
            a +=1
        a = 0  #row
        b = 0 #space
        while b < 6:
            while a < 6:
                if self.map[a][b]==n:
                    c +=1
                else:
                    c = 0
                if c>=4:
                    self.game = False
                a +=1
            b +=1
        a = 0
        b = 0
    def insert(self,n,u):
        a = 5
        p = False
        while a !=-1:
            if self.map[a][n] not in ['R','Y']:
                if p==False:
                    self.map[a][n] = u
                    p = True
            a -=1
        self.check_full()
        if self.game==True:
            self.check_map(u)
    def play1_com(self):
        n = choice([0,1,2,3,4,5])
        print(n)
        sleep(1)
        if self.game==True:
            self.display2()
            self.insert(n,self.p1)
    def play2(self):
        n = choice([0,1,2,3,4,5])
        print(n)
        sleep(1)
        if self.game==True:
            self.display2()
            self.insert(n,self.p2)
    def cycle(self):
        self.set_up()
        mode = input('1.YOU vs COM\n2.COM vs COM: ')
        if mode=='2':
            while self.game==True:
                self.play1_com()
                self.play2()
        else:
            while self.game==True:
                self.play1()
                self.play2()
        print('GAME OVER')

game = Game()
game.cycle()
