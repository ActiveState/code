from tkinter import *
import random
import time

def MainMenu():
    self = Tk()

    #Objects
    self.lbDirections = Label(text="Choose a Game Mode",bg="black",fg="white")
    self.lbDirections.pack()
    self.btnSinglePlayer = Button(text="Single Player")
    self.btnSinglePlayer.pack()
    self.btnMultiPlayer = Button(text="Multi-Player")
    self.btnMultiPlayer.pack()
    self.btnTenWaveChallenge = Button(text="Ten Wave Challenge")
    self.btnTenWaveChallenge.pack()

    def SinglePlayerChooseDifficulty(event):
        self.lbDirections.config(text="Choose a Pace")
        self.btnSinglePlayer.destroy()
        self.btnMultiPlayer.destroy()
        self.btnTenWaveChallenge.destroy()
        self.btnDifficultyEasy = Button(text="Easy")
        self.btnDifficultyEasy.pack()
        self.btnDifficultyMedium = Button(text="Medium")
        self.btnDifficultyMedium.pack()
        self.btnDifficultyHard = Button(text="Hard")
        self.btnDifficultyHard.pack()
        self.btnMainMenu = Button(text="Main Menu")
        self.btnMainMenu.pack(side=BOTTOM)
        self.lbControls = Label(text="Use arrow keys to move and space bar to shoot",bg="black",fg="white")
        self.lbControls.pack()
        self.btnMainMenu.bind('<Button>',StartMainMenu)
        self.btnDifficultyEasy.bind('<Button>',StartSinglePlayerEasy)
        self.btnDifficultyMedium.bind('<Button>',StartSinglePlayerMedium)
        self.btnDifficultyHard.bind('<Button>',StartSinglePlayerHard)

    def MultiPlayerChooseDifficulty(event):
        self.lbDirections.config(text="Choose a Pace")
        self.btnSinglePlayer.destroy()
        self.btnMultiPlayer.destroy()
        self.btnTenWaveChallenge.destroy()
        self.btnDifficultyEasy = Button(text="Easy")
        self.btnDifficultyEasy.pack()
        self.btnDifficultyMedium = Button(text="Medium")
        self.btnDifficultyMedium.pack()
        self.btnDifficultyHard = Button(text="Hard")
        self.btnDifficultyHard.pack()
        self.btnMainMenu = Button(text="Main Menu")
        self.btnMainMenu.pack(side=BOTTOM)
        self.lbControls = Label(text="Player 1 - Use arrow keys to move and space bar to shoot"+'\n'+"Player 2 - Use 'wasd' keys to move and tab to shoot",bg="black",fg="white")
        self.lbControls.pack()
        self.btnMainMenu.bind('<Button>',StartMainMenu)
        self.btnDifficultyEasy.bind('<Button>',StartMultiPlayerEasy)
        self.btnDifficultyMedium.bind('<Button>',StartMultiPlayerMedium)
        self.btnDifficultyHard.bind('<Button>',StartMultiPlayerHard)

    def TenWaveChallengeChooseMode(event):
        self.lbDirections.config(text="Choose a Mode")
        self.btnSinglePlayer.destroy()
        self.btnMultiPlayer.destroy()
        self.btnTenWaveChallenge.destroy()
        self.btnTenWaveChallengeSinglePlayer = Button(text="Single Player")
        self.btnTenWaveChallengeSinglePlayer.pack()
        self.btnTenWaveChallengeMultiPlayer = Button(text="Multi-Player")
        self.btnTenWaveChallengeMultiPlayer.pack()
        self.btnMainMenu = Button(text="Main Menu")
        self.btnMainMenu.pack(side=BOTTOM)
        self.lbControls = Label(text="Player 1 - Use arrow keys to move and space bar to shoot"+'\n'+"Player 2 - Use 'wasd' keys to move and tab to shoot",bg="black",fg="white")
        self.lbControls.pack()
        self.btnMainMenu.bind('<Button>',StartMainMenu)
        self.btnTenWaveChallengeSinglePlayer.bind('<Button>',StartTenWaveChallengeSinglePlayer)
        self.btnTenWaveChallengeMultiPlayer.bind('<Button>',StartTenWaveChallengeMultiPlayer)

    def StartMainMenu(event):
        self.destroy()
        MainMenu()

    def StartTenWaveChallengeSinglePlayer(event):
        self.destroy()
        TenWaveChallengeSinglePlayerChooseEnemies()

    def StartTenWaveChallengeMultiPlayer(event):
        self.destroy()
        TenWaveChallengeMultiPlayerChooseEnemies()

    def StartSinglePlayerEasy(event):
        global pace
        pace = 14000
        self.destroy()
        SinglePlayer()

    def StartSinglePlayerMedium(event):
        global pace
        pace = 10000
        self.destroy()
        SinglePlayer()

    def StartSinglePlayerHard(event):
        global pace
        pace = 6000
        self.destroy()
        SinglePlayer()

    def StartMultiPlayerEasy(event):
        global pace
        pace = 14000
        self.destroy()
        MultiPlayer()

    def StartMultiPlayerMedium(event):
        global pace
        pace = 10000
        self.destroy()
        MultiPlayer()

    def StartMultiPlayerHard(event):
        global pace
        pace = 6000
        self.destroy()
        MultiPlayer()

    def Exit(event):
        self.destroy()

    #Bind
    self.btnSinglePlayer.bind('<Button>',SinglePlayerChooseDifficulty)
    self.btnMultiPlayer.bind('<Button>',MultiPlayerChooseDifficulty)
    self.btnTenWaveChallenge.bind('<Button>',TenWaveChallengeChooseMode)
    self.bind('<Escape>',Exit)
    
    #Frame settings
    self.geometry("830x700")
    self.title("Space Assault")
    self.configure(bg="black")
    
def SinglePlayer():
    self = Tk()

    #Variables
    global wave
    global Damage
    global Damage3
    global Damage5
    global Damage6
    global Xpos
    global Ypos
    global enXpos
    global enYpos
    global en2Xpos
    global en2Ypos
    global en3Xpos
    global en3Ypos
    global en4Xpos
    global en4Ypos
    global en5Xpos
    global en5Ypos
    global en6Xpos
    global en6Ypos
    global gameover
    global direction
    global start
    global created
    global created2
    global created3
    global created4
    global created5
    global destroy
    global summoned
    global waveTime
    global generated1
    global generated2
    global generated3
    global generated4
    global pause
    global pace
    wave = 0
    Damage = 0
    Damage3 = 0
    Damage5 = 0
    Damage6 = 0
    Xpos = 425
    Ypos = 350
    enXpos = 0
    enYpos = 0
    en2Xpos = 0
    en2Ypos = 0
    en3Xpos = 0
    en3Ypos = 0
    en4Xpos = 0
    en4Ypos = 0
    en5Xpos = 0
    en5Ypos = 0
    en6Xpos = 0
    en6Ypos = 0
    gameover = 0
    direction = "N"
    start = 0
    created = 0
    created2 = 0
    created3 = 0
    created4 = 0
    created5 = 0
    destroy = 0
    summoned = 0
    waveTime = 0
    generated1 = 1000
    generated2 = 1250
    generated3 = 1500
    generated4 = 1750
    pause = 0

    #Lists
    Shots = []
    ShotsXpos = []
    ShotsYpos = []
    ShotDir = []
    enShots = []
    enShotsXpos = []
    enShotsYpos = []
    enShotDir = []
    Enemies = []
    EnemiesDmg = []
    EnemiesXpos = []
    EnemiesYpos = []
    Enemies2 = []
    Enemies2Xpos = []
    Enemies2Ypos = []
    Enemies3 = []
    Enemies3Dmg = []
    Enemies3Xpos = []
    Enemies3Ypos = []
    Enemies4 = []
    Enemies4Xpos = []
    Enemies4Ypos = []
    Enemies5 = []
    Enemies5Dmg = []
    Enemies5Xpos = []
    Enemies5Ypos = []
    Enemies5Wall = []
    Enemies6 = []
    Enemies6Xpos = []
    Enemies6Ypos = []
    Enemies6Type = []
    Enemies6Dmg = []
    Explosions = []
    
    #Score
    self.lbScore = Label(text="Wave: "+str(wave)+"  Next Wave: "+str(pace/1000)+"sec  Press 'p' to pause",bg="black",fg="white")
    self.lbScore.place(x=165,y=680,width=500,height=20)

    #Player
    self.player = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
    self.player.place(x=Xpos,y=Ypos)
    self.player.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="green")

    #Functions
    def LeftKey(event):
        global Xpos
        global Ypos
        global direction
        global start
        self.player.delete("all")
        self.player.create_polygon(0,15,30,30,15,15,30,0,0,15,fill="green")
        if Xpos > 0:
            Xpos -= 25
        self.player.place(x=Xpos,y=Ypos)
        direction = "W"
        cycle = 0
        for enemy in Enemies:
            if Xpos == EnemiesXpos[cycle] and Ypos == EnemiesYpos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy2 in Enemies2:
            if Xpos == Enemies2Xpos[cycle] and Ypos == Enemies2Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy3 in Enemies3:
            if Xpos == Enemies3Xpos[cycle] and Ypos == Enemies3Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy4 in Enemies4:
            if Xpos == Enemies4Xpos[cycle] and Ypos == Enemies4Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy5 in Enemies5:
            if Xpos == Enemies5Xpos[cycle] and Ypos == Enemies5Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy6 in Enemies6:
            if Xpos == Enemies6Xpos[cycle] and Ypos == Enemies6Ypos[cycle]:
                GameOver()
            cycle += 1
        if start == 0:
            NextWave()
        start = 1

    def RightKey(event):
        global Xpos
        global Ypos
        global direction
        global start
        self.player.delete("all")
        self.player.create_polygon(30,15,0,30,15,15,0,0,30,15,fill="green")
        if Xpos < 800:
            Xpos += 25
        self.player.place(x=Xpos,y=Ypos)
        direction = "E"
        cycle = 0
        for enemy in Enemies:
            if Xpos == EnemiesXpos[cycle] and Ypos == EnemiesYpos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy2 in Enemies2:
            if Xpos == Enemies2Xpos[cycle] and Ypos == Enemies2Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy3 in Enemies3:
            if Xpos == Enemies3Xpos[cycle] and Ypos == Enemies3Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy4 in Enemies4:
            if Xpos == Enemies4Xpos[cycle] and Ypos == Enemies4Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy5 in Enemies5:
            if Xpos == Enemies5Xpos[cycle] and Ypos == Enemies5Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy6 in Enemies6:
            if Xpos == Enemies6Xpos[cycle] and Ypos == Enemies6Ypos[cycle]:
                GameOver()
            cycle += 1
        if start == 0:
            NextWave()
        start = 1

    def UpKey(event):
        global Xpos
        global Ypos
        global direction
        global start
        self.player.delete("all")
        self.player.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="green")
        if Ypos > 0:
            Ypos -= 25
        self.player.place(x=Xpos,y=Ypos)
        direction = "N"
        cycle = 0
        for enemy in Enemies:
            if Xpos == EnemiesXpos[cycle] and Ypos == EnemiesYpos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy2 in Enemies2:
            if Xpos == Enemies2Xpos[cycle] and Ypos == Enemies2Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy3 in Enemies3:
            if Xpos == Enemies3Xpos[cycle] and Ypos == Enemies3Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy4 in Enemies4:
            if Xpos == Enemies4Xpos[cycle] and Ypos == Enemies4Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy5 in Enemies5:
            if Xpos == Enemies5Xpos[cycle] and Ypos == Enemies5Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy6 in Enemies6:
            if Xpos == Enemies6Xpos[cycle] and Ypos == Enemies6Ypos[cycle]:
                GameOver()
            cycle += 1
        if start == 0:
            NextWave()
        start = 1

    def DownKey(event):
        global Xpos
        global Ypos
        global direction
        global start
        self.player.delete("all")
        self.player.create_polygon(15,30,30,0,15,15,0,0,15,30,fill="green")
        if Ypos < 650:
            Ypos += 25
        self.player.place(x=Xpos,y=Ypos)
        direction = "S"
        cycle = 0
        for enemy in Enemies:
            if Xpos == EnemiesXpos[cycle] and Ypos == EnemiesYpos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy2 in Enemies2:
            if Xpos == Enemies2Xpos[cycle] and Ypos == Enemies2Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy3 in Enemies3:
            if Xpos == Enemies3Xpos[cycle] and Ypos == Enemies3Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy4 in Enemies4:
            if Xpos == Enemies4Xpos[cycle] and Ypos == Enemies4Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy5 in Enemies5:
            if Xpos == Enemies5Xpos[cycle] and Ypos == Enemies5Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy6 in Enemies6:
            if Xpos == Enemies6Xpos[cycle] and Ypos == Enemies6Ypos[cycle]:
                GameOver()
            cycle += 1
        if start == 0:
            NextWave()
        start = 1

    def CreateEnemy():
        global Xpos
        global Ypos
        global enXpos
        global enYpos
        global Damage
        global created
        enXpos = random.randrange(0,33)*25
        enYpos = random.randrange(0,27)*25
        while abs(Xpos - enXpos) <= 75 and abs(Ypos - enYpos) <= 75:
            enXpos = random.randrange(0,33)*25
            enYpos = random.randrange(0,27)*25
        self.enemy = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
        self.enemy.place(x=enXpos,y=enYpos)
        self.enemy.polygon = self.enemy.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="darkviolet")
        Enemies.append(self.enemy)
        EnemiesDmg.append(Damage)
        EnemiesXpos.append(enXpos)
        EnemiesYpos.append(enYpos)
        created = 1

    def CreateEnemy2():
        global Xpos
        global Ypos
        global en2Xpos
        global en2Ypos
        global created2
        en2Xpos = random.randrange(0,33)*25
        en2Ypos = random.randrange(0,27)*25
        while abs(Xpos - en2Xpos) <= 75 and abs(Ypos - en2Ypos) <= 75:
            en2Xpos = random.randrange(0,33)*25
            en2Ypos = random.randrange(0,27)*25
        self.enemy2 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
        self.enemy2.place(x=en2Xpos,y=en2Ypos)
        self.enemy2.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="red")
        Enemies2.append(self.enemy2)
        Enemies2Xpos.append(en2Xpos)
        Enemies2Ypos.append(en2Ypos)
        created2 = 1

    def CreateEnemy3():
        global Xpos
        global Ypos
        global en3Xpos
        global en3Ypos
        global Damage3
        global created3
        en3Xpos = random.randrange(0,33)*25
        en3Ypos = random.randrange(0,27)*25
        while abs(Xpos - en3Xpos) <= 75 and abs(Ypos - en3Ypos) <= 75:
            en3Xpos = random.randrange(0,33)*25
            en3Ypos = random.randrange(0,27)*25
        self.enemy3 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
        self.enemy3.place(x=en3Xpos,y=en3Ypos)
        self.enemy3.polygon = self.enemy3.create_polygon(10,0,0,0,0,30,30,30,30,0,20,0,20,10,10,10,fill="navy")
        Enemies3.append(self.enemy3)
        Enemies3Dmg.append(Damage3)
        Enemies3Xpos.append(en3Xpos)
        Enemies3Ypos.append(en3Ypos)
        created3 = 1

    def CreateEnemy4():
        global Xpos
        global Ypos
        global en4Xpos
        global en4Ypos
        global created4
        en4Xpos = random.randrange(0,33)*25
        en4Ypos = random.randrange(0,27)*25
        while abs(Xpos - en4Xpos) <= 150 and abs(Ypos - en4Ypos) <= 150:
            en4Xpos = random.randrange(0,33)*25
            en4Ypos = random.randrange(0,27)*25
        self.enemy4 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
        self.enemy4.place(x=en4Xpos,y=en4Ypos)
        self.enemy4.create_polygon(15,0,5,15,12,15,5,30,25,30,17,15,25,15,fill="darkgreen")
        Enemies4.append(self.enemy4)
        Enemies4Xpos.append(en4Xpos)
        Enemies4Ypos.append(en4Ypos)
        created4 = 1

    def CreateEnemy5():
        global Xpos
        global Ypos
        global en5Xpos
        global en5Ypos
        global Damage5
        global created5
        wall = random.choice(["N","E","S","W"])
        if wall == "N":
            en5Xpos = random.randrange(0,33)*25
            en5Ypos = 0
            self.enemy5 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
            self.enemy5.place(x=en5Xpos,y=en5Ypos)
            self.enemy5.polygon = self.enemy5.create_polygon(0,0,10,15,10,30,20,30,20,15,30,0,fill="darkorange2")
        elif wall == "E":
            en5Xpos = 800
            en5Ypos = random.randrange(0,27)*25
            self.enemy5 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
            self.enemy5.place(x=en5Xpos,y=en5Ypos)
            self.enemy5.polygon = self.enemy5.create_polygon(30,0,15,10,0,10,0,20,15,20,30,30,fill="darkorange2")
        elif wall == "S":
            en5Xpos = random.randrange(0,33)*25
            en5Ypos = 650
            self.enemy5 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
            self.enemy5.place(x=en5Xpos,y=en5Ypos)
            self.enemy5.polygon = self.enemy5.create_polygon(30,30,20,15,20,0,10,0,10,15,0,30,fill="darkorange2")
        elif wall == "W":
            en5Xpos = 0
            en5Ypos = random.randrange(0,27)*25
            self.enemy5 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
            self.enemy5.place(x=en5Xpos,y=en5Ypos)
            self.enemy5.polygon = self.enemy5.create_polygon(0,30,15,20,30,20,30,10,15,10,0,0,fill="darkorange2")
        while abs(Xpos - en5Xpos) <= 75 and abs(Ypos - en5Ypos) <= 75:
            wall = random.choice(["N","E","S","W"])
            if wall == "N":
                en5Xpos = random.randrange(0,33)*25
                en5Ypos = 0
                self.enemy5 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
                self.enemy5.place(x=en5Xpos,y=en5Ypos)
                self.enemy5.polygon = self.enemy5.create_polygon(0,0,10,15,10,30,20,30,20,15,30,0,fill="darkorange2")
            elif wall == "E":
                en5Xpos = 800
                en5Ypos = random.randrange(0,27)*25
                self.enemy5 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
                self.enemy5.place(x=en5Xpos,y=en5Ypos)
                self.enemy5.polygon = self.enemy5.create_polygon(30,0,15,10,0,10,0,20,15,20,30,30,fill="darkorange2")
            elif wall == "S":
                en5Xpos = random.randrange(0,33)*25
                en5Ypos = 650
                self.enemy5 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
                self.enemy5.place(x=en5Xpos,y=en5Ypos)
                self.enemy5.polygon = self.enemy5.create_polygon(30,30,20,15,20,0,10,0,10,15,0,30,fill="darkorange2")
            elif wall == "W":
                en5Xpos = 0
                en5Ypos = random.randrange(0,27)*25
                self.enemy5 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
                self.enemy5.place(x=en5Xpos,y=en5Ypos)
                self.enemy5.polygon = self.enemy5.create_polygon(0,30,15,20,30,20,30,10,15,10,0,0,fill="darkorange2")
        Enemies5.append(self.enemy5)
        Enemies5Dmg.append(Damage5)
        Enemies5Xpos.append(en5Xpos)
        Enemies5Ypos.append(en5Ypos)
        Enemies5Wall.append(wall)
        created5 = 1

    def CreateEnemy6():
        global Xpos
        global Ypos
        global en6Xpos
        global en6Ypos
        en6Type = random.choice([1,2,3,4])
        en6Xpos = random.randrange(0,33)*25
        en6Ypos = random.randrange(0,27)*25
        while abs(Xpos - en6Xpos) <= 75 and abs(Ypos - en6Ypos) <= 75:
            en6Xpos = random.randrange(0,33)*25
            en6Ypos = random.randrange(0,27)*25
        self.enemy6 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
        self.enemy6.place(x=en6Xpos,y=en6Ypos)
        self.enemy6.oval = self.enemy6.create_oval(0,0,30,30,fill="gray20")
        Enemies6.append(self.enemy6)
        Enemies6Xpos.append(en6Xpos)
        Enemies6Ypos.append(en6Ypos)
        Enemies6Type.append(en6Type)
        Enemies6Dmg.append(Damage6)

    def EnemyMove():
        global Xpos
        global Ypos
        global gameover
        global created
        if gameover != 1:
            self.after(300,EnemyMove)
            if created == 1:
                cycle = 0
                for self.enemy in Enemies:
                    rndDir = random.choice(["X","Y"])
                    if EnemiesDmg[cycle] == 0:
                        EnemyColor = "darkviolet"
                    else:
                        EnemyColor = "violet"
                    if Xpos < EnemiesXpos[cycle] and Ypos < EnemiesYpos[cycle]:
                        self.enemy.delete("all")
                        if rndDir == "X":
                            EnemiesXpos[cycle] -= 25
                            self.enemy.polygon = self.enemy.create_polygon(0,15,30,30,15,15,30,0,0,15,fill=EnemyColor)
                        else:
                            EnemiesYpos[cycle] -= 25
                            self.enemy.polygon = self.enemy.create_polygon(15,0,30,30,15,15,0,30,15,0,fill=EnemyColor)
                    elif Xpos < EnemiesXpos[cycle] and Ypos > EnemiesYpos[cycle]:
                        self.enemy.delete("all")
                        if rndDir == "X":
                            EnemiesXpos[cycle] -= 25
                            self.enemy.polygon = self.enemy.create_polygon(0,15,30,30,15,15,30,0,0,15,fill=EnemyColor)
                        else:
                            EnemiesYpos[cycle] += 25
                            self.enemy.polygon = self.enemy.create_polygon(15,30,30,0,15,15,0,0,15,30,fill=EnemyColor)
                    elif Xpos > EnemiesXpos[cycle] and Ypos < EnemiesYpos[cycle]:
                        self.enemy.delete("all")
                        if rndDir == "X":
                            EnemiesXpos[cycle] += 25
                            self.enemy.polygon = self.enemy.create_polygon(30,15,0,30,15,15,0,0,30,15,fill=EnemyColor)
                        else:
                            EnemiesYpos[cycle] -= 25
                            self.enemy.polygon = self.enemy.create_polygon(15,0,30,30,15,15,0,30,15,0,fill=EnemyColor)
                    elif Xpos > EnemiesXpos[cycle] and Ypos > EnemiesYpos[cycle]:
                        self.enemy.delete("all")
                        if rndDir == "X":
                            EnemiesXpos[cycle] += 25
                            self.enemy.polygon = self.enemy.create_polygon(30,15,0,30,15,15,0,0,30,15,fill=EnemyColor)
                        else:
                            EnemiesYpos[cycle] += 25
                            self.enemy.polygon = self.enemy.create_polygon(15,30,30,0,15,15,0,0,15,30,fill=EnemyColor)
                    elif Xpos < EnemiesXpos[cycle] and Ypos == EnemiesYpos[cycle]:
                        self.enemy.delete("all")
                        self.enemy.polygon = self.enemy.create_polygon(0,15,30,30,15,15,30,0,0,15,fill=EnemyColor)
                        EnemiesXpos[cycle] -= 25
                    elif Xpos > EnemiesXpos[cycle] and Ypos == EnemiesYpos[cycle]:
                        self.enemy.delete("all")
                        self.enemy.polygon = self.enemy.create_polygon(30,15,0,30,15,15,0,0,30,15,fill=EnemyColor)
                        EnemiesXpos[cycle] += 25
                    elif Xpos == EnemiesXpos[cycle] and Ypos < EnemiesYpos[cycle]:
                        self.enemy.delete("all")
                        self.enemy.polygon = self.enemy.create_polygon(15,0,30,30,15,15,0,30,15,0,fill=EnemyColor)
                        EnemiesYpos[cycle] -= 25
                    elif Xpos == EnemiesXpos[cycle] and Ypos > EnemiesYpos[cycle]:
                        self.enemy.delete("all")
                        self.enemy.polygon = self.enemy.create_polygon(15,30,30,0,15,15,0,0,15,30,fill=EnemyColor)
                        EnemiesYpos[cycle] += 25
                    self.enemy.place(x=EnemiesXpos[cycle],y=EnemiesYpos[cycle])
                    if Xpos == EnemiesXpos[cycle] and Ypos == EnemiesYpos[cycle]:
                        GameOver()
                    cycle += 1

    def Enemy2Move():
        global Xpos
        global Ypos
        global gameover
        global created2
        if gameover != 1:
            self.after(300,Enemy2Move)
            if created2 == 1:
                cycle = 0
                for self.enemy2 in Enemies2:
                    if Xpos < Enemies2Xpos[cycle] and Ypos < Enemies2Ypos[cycle]:
                        self.enemy2.delete("all")
                        self.enemy2.create_polygon(0,0,30,15,15,15,15,30,0,0,fill="red")
                        Enemies2Xpos[cycle] -= 25
                        Enemies2Ypos[cycle] -= 25
                    elif Xpos < Enemies2Xpos[cycle] and Ypos > Enemies2Ypos[cycle]:
                        self.enemy2.delete("all")
                        self.enemy2.create_polygon(0,30,15,0,15,15,30,15,0,30,fill="red")
                        Enemies2Xpos[cycle] -= 25
                        Enemies2Ypos[cycle] += 25
                    elif Xpos > Enemies2Xpos[cycle] and Ypos < Enemies2Ypos[cycle]:
                        self.enemy2.delete("all")
                        self.enemy2.create_polygon(30,0,0,15,15,15,15,30,30,0,fill="red")
                        Enemies2Xpos[cycle] += 25
                        Enemies2Ypos[cycle] -= 25
                    elif Xpos > Enemies2Xpos[cycle] and Ypos > Enemies2Ypos[cycle]:
                        self.enemy2.delete("all")
                        self.enemy2.create_polygon(30,30,15,0,15,15,0,15,30,30,fill="red")
                        Enemies2Xpos[cycle] += 25
                        Enemies2Ypos[cycle] += 25
                    elif Xpos < Enemies2Xpos[cycle] and Ypos == Enemies2Ypos[cycle]:
                        self.enemy2.delete("all")
                        self.enemy2.create_polygon(0,15,30,30,15,15,30,0,0,15,fill="red")
                        Enemies2Xpos[cycle] -= 25
                    elif Xpos > Enemies2Xpos[cycle] and Ypos == Enemies2Ypos[cycle]:
                        self.enemy2.delete("all")
                        self.enemy2.create_polygon(30,15,0,30,15,15,0,0,30,15,fill="red")
                        Enemies2Xpos[cycle] += 25
                    elif Xpos == Enemies2Xpos[cycle] and Ypos < Enemies2Ypos[cycle]:
                        self.enemy2.delete("all")
                        self.enemy2.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="red")
                        Enemies2Ypos[cycle] -= 25
                    elif Xpos == Enemies2Xpos[cycle] and Ypos > Enemies2Ypos[cycle]:
                        self.enemy2.delete("all")
                        self.enemy2.create_polygon(15,30,30,0,15,15,0,0,15,30,fill="red")
                        Enemies2Ypos[cycle] += 25
                    self.enemy2.place(x=Enemies2Xpos[cycle],y=Enemies2Ypos[cycle])
                    if Xpos == Enemies2Xpos[cycle] and Ypos == Enemies2Ypos[cycle]:
                        GameOver()
                    cycle += 1

    def Enemy3Move():
        global Xpos
        global Ypos
        global gameover
        global created3
        if gameover != 1:
            self.after(350,Enemy3Move)
            if created3 == 1:
                cycle = 0
                for self.enemy3 in Enemies3:
                        rndDir = random.choice(["X","Y"])
                        if Enemies3Dmg[cycle] == 0:
                            Enemy3Color = "navy"
                        elif Enemies3Dmg[cycle] == 1:
                            Enemy3Color = "blue"
                        elif Enemies3Dmg[cycle] == 2:
                            Enemy3Color = "dodgerblue"
                        elif Enemies3Dmg[cycle] == 3:
                            Enemy3Color = "deepskyblue"
                        else:
                            Enemy3Color = "lightskyblue"
                        if Xpos < Enemies3Xpos[cycle] and Ypos < Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            if rndDir == "X":
                                Enemies3Xpos[cycle] -= 25
                                self.enemy3.polygon = self.enemy3.create_polygon(0,20,0,30,30,30,30,0,0,0,0,10,10,10,10,20,fill=Enemy3Color)
                            else:
                                Enemies3Ypos[cycle] -= 25
                                self.enemy3.polygon = self.enemy3.create_polygon(10,0,0,0,0,30,30,30,30,0,20,0,20,10,10,10,fill=Enemy3Color)
                        elif Xpos < Enemies3Xpos[cycle] and Ypos > Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            if rndDir == "X":
                                Enemies3Xpos[cycle] -= 25
                                self.enemy3.polygon = self.enemy3.create_polygon(0,20,0,30,30,30,30,0,0,0,0,10,10,10,10,20,fill=Enemy3Color)
                            else:
                                Enemies3Ypos[cycle] += 25
                                self.enemy3.polygon = self.enemy3.create_polygon(20,30,30,30,30,0,0,0,0,30,10,30,10,20,20,20,fill=Enemy3Color)
                        elif Xpos > Enemies3Xpos[cycle] and Ypos < Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            if rndDir == "X":
                                Enemies3Xpos[cycle] += 25
                                self.enemy3.polygon = self.enemy3.create_polygon(30,10,30,0,0,0,0,30,30,30,30,20,20,20,20,10,fill=Enemy3Color)
                            else:
                                Enemies3Ypos[cycle] -= 25
                                self.enemy3.polygon = self.enemy3.create_polygon(10,0,0,0,0,30,30,30,30,0,20,0,20,10,10,10,fill=Enemy3Color)
                        elif Xpos > Enemies3Xpos[cycle] and Ypos > Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            if rndDir == "X":
                                Enemies3Xpos[cycle] += 25
                                self.enemy3.polygon = self.enemy3.create_polygon(30,10,30,0,0,0,0,30,30,30,30,20,20,20,20,10,fill=Enemy3Color)
                            else:
                                Enemies3Ypos[cycle] += 25
                                self.enemy3.polygon = self.enemy3.create_polygon(20,30,30,30,30,0,0,0,0,30,10,30,10,20,20,20,fill=Enemy3Color)
                        elif Xpos < Enemies3Xpos[cycle] and Ypos == Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            self.enemy3.polygon = self.enemy3.create_polygon(0,20,0,30,30,30,30,0,0,0,0,10,10,10,10,20,fill=Enemy3Color)
                            Enemies3Xpos[cycle] -= 25
                        elif Xpos > Enemies3Xpos[cycle] and Ypos == Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            self.enemy3.polygon = self.enemy3.create_polygon(30,10,30,0,0,0,0,30,30,30,30,20,20,20,20,10,fill=Enemy3Color)
                            Enemies3Xpos[cycle] += 25
                        elif Xpos == Enemies3Xpos[cycle] and Ypos < Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            self.enemy3.polygon = self.enemy3.create_polygon(10,0,0,0,0,30,30,30,30,0,20,0,20,10,10,10,fill=Enemy3Color)
                            Enemies3Ypos[cycle] -= 25
                        elif Xpos == Enemies3Xpos[cycle] and Ypos > Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            self.enemy3.polygon = self.enemy3.create_polygon(20,30,30,30,30,0,0,0,0,30,10,30,10,20,20,20,fill=Enemy3Color)
                            Enemies3Ypos[cycle] += 25
                        self.enemy3.place(x=Enemies3Xpos[cycle],y=Enemies3Ypos[cycle])
                        if Xpos == Enemies3Xpos[cycle] and Ypos == Enemies3Ypos[cycle]:
                            GameOver()
                        cycle += 1

    def Enemy4Move():
        global Xpos
        global Ypos
        global gameover
        global created4
        if gameover != 1:
            self.after(100,Enemy4Move)
            if created4 == 1:
                cycle = 0
                for self.enemy4 in Enemies4:
                    rndDir = random.choice(["X","Y"])
                    Enemy4Color = "darkgreen"
                    if Xpos < Enemies4Xpos[cycle] and Ypos < Enemies4Ypos[cycle]:
                        self.enemy4.delete("all")
                        if rndDir == "X":
                            Enemies4Xpos[cycle] -= 25
                            self.enemy4.polygon = self.enemy4.create_polygon(0,15,15,25,15,17,30,25,30,5,15,13,15,5,fill=Enemy4Color)
                        else:
                            Enemies4Ypos[cycle] -= 25
                            self.enemy4.polygon = self.enemy4.create_polygon(15,0,5,15,12,15,5,30,25,30,17,15,25,15,fill=Enemy4Color)
                    elif Xpos < Enemies4Xpos[cycle] and Ypos > Enemies4Ypos[cycle]:
                        self.enemy4.delete("all")
                        if rndDir == "X":
                            Enemies4Xpos[cycle] -= 25
                            self.enemy4.polygon = self.enemy4.create_polygon(0,15,15,25,15,17,30,25,30,5,15,13,15,5,fill=Enemy4Color)
                        else:
                            Enemies4Ypos[cycle] += 25
                            self.enemy4.polygon = self.enemy4.create_polygon(15,30,25,15,17,15,25,0,5,0,13,15,5,15,fill=Enemy4Color)
                    elif Xpos > Enemies4Xpos[cycle] and Ypos < Enemies4Ypos[cycle]:
                        self.enemy4.delete("all")
                        if rndDir == "X":
                            Enemies4Xpos[cycle] += 25
                            self.enemy4.polygon = self.enemy4.create_polygon(30,15,15,5,15,13,0,5,0,25,15,17,15,25,fill=Enemy4Color)
                        else:
                            Enemies4Ypos[cycle] -= 25
                            self.enemy4.polygon = self.enemy4.create_polygon(15,0,5,15,12,15,5,30,25,30,17,15,25,15,fill=Enemy4Color)
                    elif Xpos > Enemies4Xpos[cycle] and Ypos > Enemies4Ypos[cycle]:
                        self.enemy4.delete("all")
                        if rndDir == "X":
                            Enemies4Xpos[cycle] += 25
                            self.enemy4.polygon = self.enemy4.create_polygon(30,15,15,5,15,13,0,5,0,25,15,17,15,25,fill=Enemy4Color)
                        else:
                            Enemies4Ypos[cycle] += 25
                            self.enemy4.polygon = self.enemy4.create_polygon(15,30,25,15,17,15,25,0,5,0,13,15,5,15,fill=Enemy4Color)
                    elif Xpos < Enemies4Xpos[cycle] and Ypos == Enemies4Ypos[cycle]:
                        self.enemy4.delete("all")
                        self.enemy4.polygon = self.enemy4.create_polygon(0,15,15,25,15,17,30,25,30,5,15,13,15,5,fill=Enemy4Color)
                        Enemies4Xpos[cycle] -= 25
                    elif Xpos > Enemies4Xpos[cycle] and Ypos == Enemies4Ypos[cycle]:
                        self.enemy4.delete("all")
                        self.enemy4.polygon = self.enemy4.create_polygon(30,15,15,5,15,13,0,5,0,25,15,17,15,25,fill=Enemy4Color)
                        Enemies4Xpos[cycle] += 25
                    elif Xpos == Enemies4Xpos[cycle] and Ypos < Enemies4Ypos[cycle]:
                        self.enemy4.delete("all")
                        self.enemy4.polygon = self.enemy4.create_polygon(15,0,5,15,12,15,5,30,25,30,17,15,25,15,fill=Enemy4Color)
                        Enemies4Ypos[cycle] -= 25
                    elif Xpos == Enemies4Xpos[cycle] and Ypos > Enemies4Ypos[cycle]:
                        self.enemy4.delete("all")
                        self.enemy4.polygon = self.enemy4.create_polygon(15,30,25,15,17,15,25,0,5,0,13,15,5,15,fill=Enemy4Color)
                        Enemies4Ypos[cycle] += 25
                    self.enemy4.place(x=Enemies4Xpos[cycle],y=Enemies4Ypos[cycle])
                    if Xpos == Enemies4Xpos[cycle] and Ypos == Enemies4Ypos[cycle]:
                        GameOver()
                    cycle += 1

    def Enemy5Move():
        global Xpos
        global Ypos
        global gameover
        global created5
        if gameover != 1:
            self.after(500,Enemy5Move)
            if created5 == 1:
                cycle = 0
                for self.enemy5 in Enemies5:
                    if (Enemies5Wall[cycle] == "E" or Enemies5Wall[cycle] == "W") and Ypos < Enemies5Ypos[cycle]:
                        Enemies5Ypos[cycle] -= 25
                    elif (Enemies5Wall[cycle] == "E" or Enemies5Wall[cycle] == "W") and Ypos > Enemies5Ypos[cycle]:
                        Enemies5Ypos[cycle] += 25
                    elif Xpos < Enemies5Xpos[cycle] and (Enemies5Wall[cycle] == "N" or Enemies5Wall[cycle] == "S"):
                        Enemies5Xpos[cycle] -= 25
                    elif Xpos > Enemies5Xpos[cycle] and (Enemies5Wall[cycle] == "N" or Enemies5Wall[cycle] == "S"):
                        Enemies5Xpos[cycle] += 25
                    self.enemy5.place(x=Enemies5Xpos[cycle],y=Enemies5Ypos[cycle])
                    if Xpos == Enemies5Xpos[cycle] and Ypos == Enemies5Ypos[cycle]:
                        GameOver()
                    if Enemies5Wall[cycle] == "E" or Enemies5Wall[cycle] == "W":
                        if Enemies5Ypos[cycle] == Ypos:
                            enShoot()
                    else:
                        if Enemies5Xpos[cycle] == Xpos:
                            enShoot()
                    cycle += 1

    def Generate():
        global generated1
        global generated2
        global generated3
        global generated4
        if gameover != 1:
            self.after(10,Generate)
            if generated1 == 0:
                GenerateEnemy1()
                generated1 = 1000
            if generated2 == 0:
                GenerateEnemy2()
                generated2 = 1250
            if generated3 == 0:
                GenerateEnemy3()
                generated3 = 1500
            if generated4 == 0:
                GenerateEnemy4()
                generated4 = 1750
            generated1 -= 10
            generated2 -= 10
            generated3 -= 10
            generated4 -= 10

    def GenerateEnemy1():
        global enXpos
        global enYpos
        global Damage
        global created
        cycle = 0
        for self.enemy6 in Enemies6:
            if Enemies6Type[cycle] == 1:
                enXpos = Enemies6Xpos[cycle]
                enYpos = Enemies6Ypos[cycle]
                self.enemy = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
                self.enemy.place(x=enXpos,y=enYpos)
                self.enemy.polygon = self.enemy.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="darkviolet")
                Enemies.append(self.enemy)
                EnemiesDmg.append(Damage)
                EnemiesXpos.append(enXpos)
                EnemiesYpos.append(enYpos)
                created = 1
            cycle += 1

    def GenerateEnemy2():
        global en2Xpos
        global en2Ypos
        global created2
        cycle = 0
        for self.enemy6 in Enemies6:
            if Enemies6Type[cycle] == 2:
                en2Xpos = Enemies6Xpos[cycle]
                en2Ypos = Enemies6Ypos[cycle]
                self.enemy2 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
                self.enemy2.place(x=en2Xpos,y=en2Ypos)
                self.enemy2.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="red")
                Enemies2.append(self.enemy2)
                Enemies2Xpos.append(en2Xpos)
                Enemies2Ypos.append(en2Ypos)
                created2 = 1
            cycle += 1

    def GenerateEnemy3():
        global en3Xpos
        global en3Ypos
        global Damage3
        global created3
        cycle = 0
        for self.enemy6 in Enemies6:
            if Enemies6Type[cycle] == 3:
                en3Xpos = Enemies6Xpos[cycle]
                en3Ypos = Enemies6Ypos[cycle]
                self.enemy3 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
                self.enemy3.place(x=en3Xpos,y=en3Ypos)
                self.enemy3.polygon = self.enemy3.create_polygon(10,0,0,0,0,30,30,30,30,0,20,0,20,10,10,10,fill="navy")
                Enemies3.append(self.enemy3)
                Enemies3Dmg.append(Damage3)
                Enemies3Xpos.append(en3Xpos)
                Enemies3Ypos.append(en3Ypos)
                created3 = 1
            cycle += 1

    def GenerateEnemy4():
        global en4Xpos
        global en4Ypos
        global created4
        cycle = 0
        for self.enemy6 in Enemies6:
            if Enemies6Type[cycle] == 4:
                en4Xpos = Enemies6Xpos[cycle]
                en4Ypos = Enemies6Ypos[cycle]
                self.enemy4 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
                self.enemy4.place(x=en4Xpos,y=en4Ypos)
                self.enemy4.create_polygon(15,0,5,15,12,15,5,30,25,30,17,15,25,15,fill="darkgreen")
                Enemies4.append(self.enemy4)
                Enemies4Xpos.append(en4Xpos)
                Enemies4Ypos.append(en4Ypos)
                created4 = 1
            cycle += 1

    def Shoot(event):
        global Xpos
        global Ypos
        global direction
        global start
        if direction == "N":
            shotXpos = Xpos + 10
            shotYpos = Ypos - 10
        elif direction == "E":
            shotXpos = Xpos + 30
            shotYpos = Ypos + 10
        elif direction == "S":
            shotXpos = Xpos + 10
            shotYpos = Ypos + 30
        elif direction == "W":
            shotXpos = Xpos - 10
            shotYpos = Ypos + 10
        self.shot = Canvas(bg="black",highlightthickness=0,width=10,height=10)
        self.shot.place(x=shotXpos,y=shotYpos)
        self.shot.create_oval(0,0,10,10,fill="white")
        Shots.append(self.shot)
        ShotsXpos.append(shotXpos)
        ShotsYpos.append(shotYpos)
        ShotDir.append(direction)
        if start == 0:
            NextWave()
        start = 1

    def enShoot():
        cycle = 0
        for self.enemy5 in Enemies5:
            if Enemies5Wall[cycle] == "N":
                enDir = "S"
                enShotXpos = Enemies5Xpos[cycle] + 10
                enShotYpos = Enemies5Ypos[cycle] + 30
            elif Enemies5Wall[cycle] == "E":
                enDir = "W"
                enShotXpos = Enemies5Xpos[cycle] - 10
                enShotYpos = Enemies5Ypos[cycle] + 10
            elif Enemies5Wall[cycle] == "S":
                enDir = "N"
                enShotXpos = Enemies5Xpos[cycle] + 10
                enShotYpos = Enemies5Ypos[cycle] - 10
            elif Enemies5Wall[cycle] == "W":
                enDir = "E"
                enShotXpos = Enemies5Xpos[cycle] + 30
                enShotYpos = Enemies5Ypos[cycle] + 10
            if Enemies5Wall[cycle] == "E" or Enemies5Wall[cycle] == "W":
                if Enemies5Ypos[cycle] == Ypos:
                    self.enShot = Canvas(bg="black",highlightthickness=0,width=10,height=10)
                    self.enShot.place(x=enShotXpos,y=enShotYpos)
                    self.enShot.create_oval(0,0,10,10,fill="yellow")
                    enShots.append(self.enShot)
                    enShotsXpos.append(enShotXpos)
                    enShotsYpos.append(enShotYpos)
                    enShotDir.append(enDir)
            else:
                if Enemies5Xpos[cycle] == Xpos:
                    self.enShot = Canvas(bg="black",highlightthickness=0,width=10,height=10)
                    self.enShot.place(x=enShotXpos,y=enShotYpos)
                    self.enShot.create_oval(0,0,10,10,fill="yellow")
                    enShots.append(self.enShot)
                    enShotsXpos.append(enShotXpos)
                    enShotsYpos.append(enShotYpos)
                    enShotDir.append(enDir)
            cycle += 1
            
    def ShotMove():
        global direction
        global en2Xpos
        global en2Ypos
        global destroy
        global gameover
        if gameover != 1:
            self.after(10,ShotMove)
            #Move Shots
            cycle = 0
            for self.shot in Shots:
                destroy = -1
                if ShotDir[cycle] == "N":
                    ShotsYpos[cycle] -= 10
                elif ShotDir[cycle] == "E":
                    ShotsXpos[cycle] += 10
                elif ShotDir[cycle] == "S":
                    ShotsYpos[cycle] += 10
                elif ShotDir[cycle] == "W":
                    ShotsXpos[cycle] -= 10
                self.shot.place(x=ShotsXpos[cycle],y=ShotsYpos[cycle])
                #Damage Enemy1
                enCycle = 0
                for self.enemy in Enemies:
                    if destroy == -1:
                        if EnemiesXpos[enCycle] + 30 >= ShotsXpos[cycle] >= EnemiesXpos[enCycle] - 10 and EnemiesYpos[enCycle] + 30 >= ShotsYpos[cycle] >= EnemiesYpos[enCycle] - 10:
                            destroy = 0
                            if EnemiesDmg[enCycle] == 1:
                                self.explode = Canvas(bg="black",highlightthickness=0,width=30,height=30)
                                self.explode.place(x=EnemiesXpos[enCycle],y=EnemiesYpos[enCycle])
                                self.explode.create_polygon(0,15,13,13,15,0,17,13,30,15,17,17,15,30,13,17,fill="orange")
                                Explosions.append(self.explode)
                                self.enemy.destroy()
                                del Enemies[enCycle]
                                del EnemiesDmg[enCycle]
                                del EnemiesXpos[enCycle]
                                del EnemiesYpos[enCycle]
                                self.after(10,destroyEnemy)
                                self.shot.destroy()
                                del Shots[cycle]
                                del ShotsXpos[cycle]
                                del ShotsYpos[cycle]
                                del ShotDir[cycle]
                            else:
                                self.shot.destroy()
                                del Shots[cycle]
                                del ShotsXpos[cycle]
                                del ShotsYpos[cycle]
                                del ShotDir[cycle]
                                EnemiesDmg[enCycle] += 1
                                if EnemiesDmg[enCycle] == 0:
                                    EnemyColor = "darkviolet"
                                else:
                                    EnemyColor = "violet"
                                self.enemy.itemconfig(self.enemy.polygon,fill=EnemyColor)
                        enCycle += 1
                #Damage Enemy2
                enCycle = 0
                for self.enemy2 in Enemies2:
                    if destroy == -1:
                        if Enemies2Xpos[enCycle] + 30 >= ShotsXpos[cycle] >= Enemies2Xpos[enCycle] - 10 and Enemies2Ypos[enCycle] + 30 >= ShotsYpos[cycle] >= Enemies2Ypos[enCycle] - 10:
                            destroy = 0
                            self.explode = Canvas(bg="black",highlightthickness=0,width=30,height=30)
                            self.explode.place(x=Enemies2Xpos[enCycle],y=Enemies2Ypos[enCycle])
                            self.explode.create_polygon(0,15,13,13,15,0,17,13,30,15,17,17,15,30,13,17,fill="orange")
                            Explosions.append(self.explode)
                            self.enemy2.destroy()
                            del Enemies2[enCycle]
                            del Enemies2Xpos[enCycle]
                            del Enemies2Ypos[enCycle]
                            self.shot.destroy()
                            del Shots[cycle]
                            del ShotsXpos[cycle]
                            del ShotsYpos[cycle]
                            del ShotDir[cycle]
                            self.after(10,destroyEnemy)
                        enCycle += 1
                #Damage Enemy3
                enCycle = 0
                for self.enemy3 in Enemies3:
                    if destroy == -1:
                        if Enemies3Xpos[enCycle] + 30 >= ShotsXpos[cycle] >= Enemies3Xpos[enCycle] - 10 and Enemies3Ypos[enCycle] + 30 >= ShotsYpos[cycle] >= Enemies3Ypos[enCycle] - 10:
                            destroy = 0
                            if Enemies3Dmg[enCycle] == 4:
                                self.explode = Canvas(bg="black",highlightthickness=0,width=30,height=30)
                                self.explode.place(x=Enemies3Xpos[enCycle],y=Enemies3Ypos[enCycle])
                                self.explode.create_polygon(0,15,13,13,15,0,17,13,30,15,17,17,15,30,13,17,fill="orange")
                                Explosions.append(self.explode)
                                self.enemy3.destroy()
                                del Enemies3[enCycle]
                                del Enemies3Dmg[enCycle]
                                del Enemies3Xpos[enCycle]
                                del Enemies3Ypos[enCycle]
                                self.after(10,destroyEnemy)
                                self.shot.destroy()
                                del Shots[cycle]
                                del ShotsXpos[cycle]
                                del ShotsYpos[cycle]
                                del ShotDir[cycle]
                            else:
                                self.shot.destroy()
                                del Shots[cycle]
                                del ShotsXpos[cycle]
                                del ShotsYpos[cycle]
                                del ShotDir[cycle]
                                Enemies3Dmg[enCycle] += 1
                                if Enemies3Dmg[enCycle] == 0:
                                    Enemy3Color = "navy"
                                elif Enemies3Dmg[enCycle] == 1:
                                    Enemy3Color = "darkblue"
                                elif Enemies3Dmg[enCycle] == 2:
                                    Enemy3Color = "dodgerblue"
                                elif Enemies3Dmg[enCycle] == 3:
                                    Enemy3Color = "deepskyblue"
                                else:
                                    Enemy3Color = "lightskyblue"
                                self.enemy3.itemconfig(self.enemy3.polygon,fill=Enemy3Color)
                        enCycle += 1
                #Damage Enemy4
                enCycle = 0
                for self.enemy4 in Enemies4:
                    if destroy == -1:
                        if Enemies4Xpos[enCycle] + 30 >= ShotsXpos[cycle] >= Enemies4Xpos[enCycle] - 10 and Enemies4Ypos[enCycle] + 30 >= ShotsYpos[cycle] >= Enemies4Ypos[enCycle] - 10:
                            destroy = 0
                            self.explode = Canvas(bg="black",highlightthickness=0,width=30,height=30)
                            self.explode.place(x=Enemies4Xpos[enCycle],y=Enemies4Ypos[enCycle])
                            self.explode.create_polygon(0,15,13,13,15,0,17,13,30,15,17,17,15,30,13,17,fill="orange")
                            Explosions.append(self.explode)
                            self.enemy4.destroy()
                            del Enemies4[enCycle]
                            del Enemies4Xpos[enCycle]
                            del Enemies4Ypos[enCycle]
                            self.shot.destroy()
                            del Shots[cycle]
                            del ShotsXpos[cycle]
                            del ShotsYpos[cycle]
                            del ShotDir[cycle]
                            self.after(10,destroyEnemy)
                        enCycle += 1
                #Damage Enemy5
                enCycle = 0
                for self.enemy5 in Enemies5:
                    if destroy == -1:
                        if Enemies5Xpos[enCycle] + 30 >= ShotsXpos[cycle] >= Enemies5Xpos[enCycle] - 10 and Enemies5Ypos[enCycle] + 30 >= ShotsYpos[cycle] >= Enemies5Ypos[enCycle] - 10:
                            destroy = 0
                            if Enemies5Dmg[enCycle] == 1:
                                self.explode = Canvas(bg="black",highlightthickness=0,width=30,height=30)
                                self.explode.place(x=Enemies5Xpos[enCycle],y=Enemies5Ypos[enCycle])
                                self.explode.create_polygon(0,15,13,13,15,0,17,13,30,15,17,17,15,30,13,17,fill="orange")
                                Explosions.append(self.explode)
                                self.enemy5.destroy()
                                del Enemies5[enCycle]
                                del Enemies5Dmg[enCycle]
                                del Enemies5Xpos[enCycle]
                                del Enemies5Ypos[enCycle]
                                del Enemies5Wall[enCycle]
                                self.after(10,destroyEnemy)
                                self.shot.destroy()
                                del Shots[cycle]
                                del ShotsXpos[cycle]
                                del ShotsYpos[cycle]
                                del ShotDir[cycle]
                            else:
                                self.shot.destroy()
                                del Shots[cycle]
                                del ShotsXpos[cycle]
                                del ShotsYpos[cycle]
                                del ShotDir[cycle]
                                Enemies5Dmg[enCycle] += 1
                                if Enemies5Dmg[enCycle] == 0:
                                    Enemy5Color = "darkorange2"
                                else:
                                    Enemy5Color = "orange"
                                self.enemy5.itemconfig(self.enemy5.polygon,fill=Enemy5Color)
                        enCycle += 1
                #Damage Enemy6
                enCycle = 0
                for self.enemy6 in Enemies6:
                    if destroy == -1:
                        if Enemies6Xpos[enCycle] + 30 >= ShotsXpos[cycle] >= Enemies6Xpos[enCycle] - 10 and Enemies6Ypos[enCycle] + 30 >= ShotsYpos[cycle] >= Enemies6Ypos[enCycle] - 10:
                            destroy = 0
                            if Enemies6Dmg[enCycle] == 5:
                                self.explode = Canvas(bg="black",highlightthickness=0,width=30,height=30)
                                self.explode.place(x=Enemies6Xpos[enCycle],y=Enemies6Ypos[enCycle])
                                self.explode.create_polygon(0,15,13,13,15,0,17,13,30,15,17,17,15,30,13,17,fill="orange")
                                Explosions.append(self.explode)
                                self.enemy6.destroy()
                                del Enemies6[enCycle]
                                del Enemies6Dmg[enCycle]
                                del Enemies6Xpos[enCycle]
                                del Enemies6Ypos[enCycle]
                                del Enemies6Type[enCycle]
                                self.after(10,destroyEnemy)
                                self.shot.destroy()
                                del Shots[cycle]
                                del ShotsXpos[cycle]
                                del ShotsYpos[cycle]
                                del ShotDir[cycle]
                            else:
                                self.shot.destroy()
                                del Shots[cycle]
                                del ShotsXpos[cycle]
                                del ShotsYpos[cycle]
                                del ShotDir[cycle]
                                Enemies6Dmg[enCycle] += 1
                                if Enemies6Dmg[enCycle] == 0:
                                    Enemy6Color = "gray20"
                                elif Enemies6Dmg[enCycle] == 1:
                                    Enemy6Color = "gray30"
                                elif Enemies6Dmg[enCycle] == 2:
                                    Enemy6Color = "gray40"
                                elif Enemies6Dmg[enCycle] == 3:
                                    Enemy6Color = "gray50"
                                elif Enemies6Dmg[enCycle] == 4:
                                    Enemy6Color = "gray60"
                                elif Enemies6Dmg[enCycle] == 5:
                                    Enemy6Color = "gray70"
                                self.enemy6.itemconfig(self.enemy6.oval,fill=Enemy6Color)
                        enCycle += 1
                #Destroy Shot at Boundary
                if destroy == -1:
                    if ShotsXpos[cycle] < 0 or ShotsXpos[cycle] > 830 or ShotsYpos[cycle] < 0 or ShotsYpos[cycle] > 680:
                        self.shot.destroy()
                        del Shots[cycle]
                        del ShotsXpos[cycle]
                        del ShotsYpos[cycle]
                        del ShotDir[cycle]
                cycle += 1

    def enShotMove():
        global gameover
        if gameover != 1:
            self.after(10,enShotMove)
            cycle = 0
            for self.enShot in enShots:
                enDestroy = -1
                if enShotDir[cycle] == "N":
                    enShotsYpos[cycle] -= 10
                elif enShotDir[cycle] == "E":
                    enShotsXpos[cycle] += 10
                elif enShotDir[cycle] == "S":
                    enShotsYpos[cycle] += 10
                elif enShotDir[cycle] == "W":
                    enShotsXpos[cycle] -= 10
                self.enShot.place(x=enShotsXpos[cycle],y=enShotsYpos[cycle])
                #Game Over
                if Xpos + 30 >= enShotsXpos[cycle] >= Xpos - 10 and Ypos + 30 >= enShotsYpos[cycle] >= Ypos - 10:
                    enDestroy = 0
                    self.enShot.destroy()
                    del enShots[cycle]
                    del enShotsXpos[cycle]
                    del enShotsYpos[cycle]
                    del enShotDir[cycle]
                    GameOver()
                #Destroy Shot at Boundary
                if enDestroy == -1:
                    if enShotsXpos[cycle] < 0 or enShotsXpos[cycle] > 830 or enShotsYpos[cycle] < 0 or enShotsYpos[cycle] > 680:
                        self.enShot.destroy()
                        del enShots[cycle]
                        del enShotsXpos[cycle]
                        del enShotsYpos[cycle]
                        del enShotDir[cycle] 
                cycle += 1

    def destroyEnemy():
        destroyed = 0
        for self.explode in Explosions:
            self.explode.destroy()
            del Explosions[destroyed]
            destroyed += 1            

    def Summon():
        global wave
        global summoned
        time = 0
        wave += 1
        #Wave 1
        if wave == 1:
            E = 0
            while E < 3:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
        #Wave 2
        elif wave == 2:
            E = 0
            while E < 3:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
        #Wave 3
        elif wave == 3:
            E = 0
            while E < 2:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < 2:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
        #Wave 4
        elif wave == 4:
            E = 0
            while E < 4:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < 2:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
        #Wave 5
        elif wave == 5:
            E = 0
            while E < 3:
                self.after(time,CreateEnemy3)
                E += 1
                time += 250
        #Wave 6
        elif wave == 6:
            E = 0
            while E < 2:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < 1:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < 3:
                self.after(time,CreateEnemy3)
                E += 1
                time += 250
        #Wave 7
        elif wave == 7:
            E = 0
            while E < 3:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < 2:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
            E = 0
            while E < 2:
                self.after(time,CreateEnemy3)
                E += 1
                time += 250
        #Wave 8
        elif wave == 8:
            E = 0
            while E < 2:
                self.after(time,CreateEnemy4)
                E += 1
                time += 250
        #Wave 9
        elif wave == 9:
            E = 0
            while E < 3:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < 2:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
            E = 0
            while E < 2:
                self.after(time,CreateEnemy4)
                E += 1
                time += 250
        #Wave 10
        elif wave == 10:
            E = 0
            while E < 3:
                self.after(time,CreateEnemy3)
                E += 1
                time += 250
            E = 0
            while E < 2:
                self.after(time,CreateEnemy4)
                E += 1
                time += 250
        #Wave 11
        elif wave == 11:
            E = 0
            while E < 2:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < 2:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
            E = 0
            while E < 1:
                self.after(time,CreateEnemy3)
                E += 1
                time += 250
            E = 0
            while E < 1:
                self.after(time,CreateEnemy4)
                E += 1
                time += 250
        #Wave 12
        elif wave == 12:
            E = 0
            while E < 2:
                self.after(time,CreateEnemy5)
                E += 1
                time += 250
        #Wave 13
        elif wave == 13:
            E = 0
            while E < 3:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < 2:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
            E = 0
            while E < 1:
                self.after(time,CreateEnemy3)
                E += 1
                time += 250
            E = 0
            while E < 1:
                self.after(time,CreateEnemy5)
                E += 1
                time += 250
        #Wave 14
        elif wave == 14:
            E = 0
            while E < 4:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < 1:
                self.after(time,CreateEnemy4)
                E += 1
                time += 250
            E = 0
            while E < 2:
                self.after(time,CreateEnemy5)
                E += 1
                time += 250
        #Wave 15
        elif wave == 15:
            E = 0
            while E < 2:
                self.after(time,CreateEnemy6)
                E += 1
                time += 250
        #Wave 16
        elif wave == 16:
            E = 0
            while E < 3:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < 2:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
            E = 0
            while E < 1:
                self.after(time,CreateEnemy6)
                E += 1
                time += 250
        #Wave 17
        elif wave == 17:
            E = 0
            while E < 1:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < 1:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
            E = 0
            while E < 1:
                self.after(time,CreateEnemy3)
                E += 1
                time += 250
            E = 0
            while E < 1:
                self.after(time,CreateEnemy4)
                E += 1
                time += 250
            E = 0
            while E < 1:
                self.after(time,CreateEnemy5)
                E += 1
                time += 250
            E = 0
            while E < 1:
                self.after(time,CreateEnemy6)
                E += 1
                time += 250
        #Wave 18+
        elif wave >= 18:
            E = 0
            while E < wave - 12:
                rndEnemy = random.choice([1,2,3,4,5,6])
                if rndEnemy == 1:
                    self.after(time,CreateEnemy)
                elif rndEnemy == 2:
                    self.after(time,CreateEnemy2)
                elif rndEnemy == 3:
                    self.after(time,CreateEnemy3)
                elif rndEnemy == 4:
                    self.after(time,CreateEnemy4)
                elif rndEnemy == 5:
                    self.after(time,CreateEnemy5)
                elif rndEnemy == 6:
                    self.after(time,CreateEnemy6)
                E += 1
                time += 250
        summoned = 0

    def NextWave():
        global wave
        global summoned
        global waveTime
        global pace
        global gameover
        if gameover == 0:
            self.after(10,NextWave)
            if summoned == 0:
                summoned = 1
                waveTime = pace
            if waveTime <= 0:
                Summon()
            if not Enemies and not Enemies2 and not Enemies3 and not Enemies4 and not Enemies5 and not Enemies6:
                Summon()
            waveTime -= 10
            self.lbScore.config(text="Wave: "+str(wave)+"  Next Wave: "+str(waveTime/1000)+"sec  Press 'p' to pause")

    def GameOver():
        global gameover
        global wave
        if gameover == 0:
            gameover = 1
            self.unbind('<Left>')
            self.unbind('<Right>')
            self.unbind('<Up>')
            self.unbind('<Down>')
            self.unbind('<space>')
            self.after_cancel(EnemyMove)
            self.after_cancel(Enemy2Move)
            self.after_cancel(Enemy3Move)
            self.after_cancel(Enemy4Move)
            self.after_cancel(Enemy5Move)
            self.after_cancel(CreateEnemy)
            self.after_cancel(CreateEnemy2)
            self.after_cancel(CreateEnemy3)
            self.after_cancel(CreateEnemy4)
            self.after_cancel(CreateEnemy5)
            self.after_cancel(CreateEnemy6)
            self.after_cancel(Generate)
            self.after_cancel(NextWave)
            self.after_cancel(ShotMove)
            self.after_cancel(enShotMove)
            for self.shot in Shots:
                self.shot.destroy()
            self.lbScore.destroy()
            self.lbGameOver = Label(text="Game Over" + "\n" "You survived to wave " + str(wave) + "\n" + "Click here to restart",bg="black",fg="white")
            self.lbGameOver.pack(fill=BOTH,expand=1)
            self.lbGameOver.bind('<Button>',Restart)
            self.btnMainMenu = Button(text="Main Menu")
            self.btnMainMenu.pack(side=LEFT)
            self.btnMainMenu.bind('<Button>',StartMainMenu)

    def Restart(event):
        self.destroy()
        SinglePlayer()

    def Pause(event):
        global pause
        global gameover
        global waveTime
        if pause == 0:
            gameover = 1
            pause = 1
            self.unbind('<Left>')
            self.unbind('<Right>')
            self.unbind('<Up>')
            self.unbind('<Down>')
            self.unbind('<space>')
            self.after_cancel(EnemyMove)
            self.after_cancel(Enemy2Move)
            self.after_cancel(Enemy3Move)
            self.after_cancel(Enemy4Move)
            self.after_cancel(Enemy5Move)
            self.after_cancel(CreateEnemy)
            self.after_cancel(CreateEnemy2)
            self.after_cancel(CreateEnemy3)
            self.after_cancel(CreateEnemy4)
            self.after_cancel(CreateEnemy5)
            self.after_cancel(CreateEnemy6)
            self.after_cancel(Generate)
            self.after_cancel(NextWave)
            self.after_cancel(ShotMove)
            self.after_cancel(enShotMove)
            for self.shot in Shots:
                self.shot.destroy()
            self.lbScore.destroy()
            self.lbPause = Label(text="Paused"+"\n"+"Press 'p' to Unpause",bg="black",fg="white")
            self.lbPause.pack(fill=BOTH,expand=1)
            self.btnMainMenu = Button(text="Main Menu")
            self.btnMainMenu.pack(side=LEFT)
            self.btnMainMenu.bind('<Button>',StartMainMenu)
        elif pause == 1:
            gameover = 0
            pause = 0
            self.bind('<Left>',LeftKey)
            self.bind('<Right>',RightKey)
            self.bind('<Up>',UpKey)
            self.bind('<Down>',DownKey)
            self.bind('<space>',Shoot)
            EnemyMove()
            Enemy2Move()
            Enemy3Move()
            Enemy4Move()
            Enemy5Move()
            Generate()
            ShotMove()
            enShotMove()
            self.lbScore = Label(text="Wave: "+str(wave)+"  Next Wave: "+str(waveTime/1000)+"sec  Press 'p' to pause",bg="black",fg="white")
            self.lbScore.place(x=165,y=680,width=500,height=20)
            NextWave()
            self.lbPause.destroy()
            self.btnMainMenu.unbind('<Button>')
            self.btnMainMenu.destroy()

    def Exit(event):
        self.destroy()

    def StartMainMenu(event):
        self.destroy()
        MainMenu()

    #Bindings
    self.bind('<Left>',LeftKey)
    self.bind('<Right>',RightKey)
    self.bind('<Up>',UpKey)
    self.bind('<Down>',DownKey)
    self.bind('<Escape>',Exit)
    self.bind('<space>',Shoot)
    self.bind('<p>',Pause)

    EnemyMove()
    Enemy2Move()
    Enemy3Move()
    Enemy4Move()
    Enemy5Move()
    Generate()
    ShotMove()
    enShotMove()
        
    #Frame settings
    self.geometry("830x700")
    self.title("Space Assault")
    self.configure(bg="black")

def MultiPlayer():
    self = Tk()

    #Variables
    global wave
    global Damage
    global Damage3
    global Damage5
    global Damage6
    global Xpos
    global Ypos
    global X2pos
    global Y2pos
    global enXpos
    global enYpos
    global en2Xpos
    global en2Ypos
    global en3Xpos
    global en3Ypos
    global en4Xpos
    global en4Ypos
    global en5Xpos
    global en5Ypos
    global en6Xpos
    global en6Ypos
    global gameover
    global direction
    global direction2
    global start
    global created
    global created2
    global created3
    global created4
    global created5
    global destroy
    global summoned
    global waveTime
    global generated1
    global generated2
    global generated3
    global generated4
    global pause
    global pace
    wave = 0
    Damage = 0
    Damage3 = 0
    Damage5 = 0
    Damage6 = 0
    Xpos = 425
    Ypos = 350
    X2pos = 400
    Y2pos = 325
    enXpos = 0
    enYpos = 0
    en2Xpos = 0
    en2Ypos = 0
    en3Xpos = 0
    en3Ypos = 0
    en4Xpos = 0
    en4Ypos = 0
    en5Xpos = 0
    en5Ypos = 0
    en6Xpos = 0
    en6Ypos = 0
    gameover = 0
    direction = "N"
    direction2 = "N"
    start = 0
    created = 0
    created2 = 0
    created3 = 0
    created4 = 0
    created5 = 0
    destroy = 0
    summoned = 0
    waveTime = 0
    generated1 = 1000
    generated2 = 1250
    generated3 = 1500
    generated4 = 1750
    pause = 0

    #Lists
    Players = []
    PlayersXpos = []
    PlayersYpos = []
    PlayersDir = []
    Shots = []
    ShotsXpos = []
    ShotsYpos = []
    ShotDir = []
    enShots = []
    enShotsXpos = []
    enShotsYpos = []
    enShotDir = []
    Enemies = []
    EnemiesDmg = []
    EnemiesXpos = []
    EnemiesYpos = []
    Enemies2 = []
    Enemies2Xpos = []
    Enemies2Ypos = []
    Enemies3 = []
    Enemies3Dmg = []
    Enemies3Xpos = []
    Enemies3Ypos = []
    Enemies4 = []
    Enemies4Xpos = []
    Enemies4Ypos = []
    Enemies5 = []
    Enemies5Dmg = []
    Enemies5Xpos = []
    Enemies5Ypos = []
    Enemies5Wall = []
    Enemies6 = []
    Enemies6Xpos = []
    Enemies6Ypos = []
    Enemies6Type = []
    Enemies6Dmg = []
    Explosions = []
    
    #Score
    self.lbScore = Label(text="Wave: "+str(wave)+"  Next Wave: "+str(pace/1000)+"sec  Press 'p' to pause",bg="black",fg="white")
    self.lbScore.place(x=165,y=680,width=500,height=20)

    #Player
    self.player = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
    self.player.place(x=Xpos,y=Ypos)
    self.player.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="green")
    Players.append(self.player)
    PlayersXpos.append(Xpos)
    PlayersYpos.append(Ypos)
    PlayersDir.append(direction)
    #Player2
    self.player2 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
    self.player2.place(x=X2pos,y=Y2pos)
    self.player2.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="white")
    Players.append(self.player2)
    PlayersXpos.append(X2pos)
    PlayersYpos.append(Y2pos)
    PlayersDir.append(direction2)
    
    #Functions
    def LeftKey(event):
        global Xpos
        global Ypos
        global direction
        global start
        self.player.delete("all")
        self.player.create_polygon(0,15,30,30,15,15,30,0,0,15,fill="green")
        if PlayersXpos[0] > 0:
            PlayersXpos[0] -= 25
        self.player.place(x=PlayersXpos[0],y=PlayersYpos[0])
        PlayersDir[0] = "W"
        cycle = 0
        for enemy in Enemies:
            if PlayersXpos[0] == EnemiesXpos[cycle] and PlayersYpos[0] == EnemiesYpos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy2 in Enemies2:
            if PlayersXpos[0] == Enemies2Xpos[cycle] and PlayersYpos[0] == Enemies2Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy3 in Enemies3:
            if PlayersXpos[0] == Enemies3Xpos[cycle] and PlayersYpos[0] == Enemies3Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy4 in Enemies4:
            if PlayersXpos[0] == Enemies4Xpos[cycle] and PlayersYpos[0] == Enemies4Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy5 in Enemies5:
            if PlayersXpos[0] == Enemies5Xpos[cycle] and PlayersYpos[0] == Enemies5Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy6 in Enemies6:
            if PlayersXpos[0] == Enemies6Xpos[cycle] and PlayersYpos[0] == Enemies6Ypos[cycle]:
                GameOver()
            cycle += 1
        if start == 0:
            NextWave()
        start = 1

    def RightKey(event):
        global Xpos
        global Ypos
        global direction
        global start
        self.player.delete("all")
        self.player.create_polygon(30,15,0,30,15,15,0,0,30,15,fill="green")
        if PlayersXpos[0] < 800:
            PlayersXpos[0] += 25
        self.player.place(x=PlayersXpos[0],y=PlayersYpos[0])
        PlayersDir[0] = "E"
        cycle = 0
        for enemy in Enemies:
            if PlayersXpos[0] == EnemiesXpos[cycle] and PlayersYpos[0] == EnemiesYpos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy2 in Enemies2:
            if PlayersXpos[0] == Enemies2Xpos[cycle] and PlayersYpos[0] == Enemies2Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy3 in Enemies3:
            if PlayersXpos[0] == Enemies3Xpos[cycle] and PlayersYpos[0] == Enemies3Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy4 in Enemies4:
            if PlayersXpos[0] == Enemies4Xpos[cycle] and PlayersYpos[0] == Enemies4Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy5 in Enemies5:
            if PlayersXpos[0] == Enemies5Xpos[cycle] and PlayersYpos[0] == Enemies5Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy6 in Enemies6:
            if PlayersXpos[0] == Enemies6Xpos[cycle] and PlayersYpos[0] == Enemies6Ypos[cycle]:
                GameOver()
            cycle += 1
        if start == 0:
            NextWave()
        start = 1

    def UpKey(event):
        global Xpos
        global Ypos
        global direction
        global start
        self.player.delete("all")
        self.player.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="green")
        if PlayersYpos[0] > 0:
            PlayersYpos[0] -= 25
        self.player.place(x=PlayersXpos[0],y=PlayersYpos[0])
        PlayersDir[0] = "N"
        cycle = 0
        for enemy in Enemies:
            if PlayersXpos[0] == EnemiesXpos[cycle] and PlayersYpos[0] == EnemiesYpos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy2 in Enemies2:
            if PlayersXpos[0] == Enemies2Xpos[cycle] and PlayersYpos[0] == Enemies2Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy3 in Enemies3:
            if PlayersXpos[0] == Enemies3Xpos[cycle] and PlayersYpos[0] == Enemies3Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy4 in Enemies4:
            if PlayersXpos[0] == Enemies4Xpos[cycle] and PlayersYpos[0] == Enemies4Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy5 in Enemies5:
            if PlayersXpos[0] == Enemies5Xpos[cycle] and PlayersYpos[0] == Enemies5Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy6 in Enemies6:
            if PlayersXpos[0] == Enemies6Xpos[cycle] and PlayersYpos[0] == Enemies6Ypos[cycle]:
                GameOver()
            cycle += 1
        if start == 0:
            NextWave()
        start = 1

    def DownKey(event):
        global Xpos
        global Ypos
        global direction
        global start
        self.player.delete("all")
        self.player.create_polygon(15,30,30,0,15,15,0,0,15,30,fill="green")
        if PlayersYpos[0] < 650:
            PlayersYpos[0] += 25
        self.player.place(x=PlayersXpos[0],y=PlayersYpos[0])
        PlayersDir[0] = "S"
        cycle = 0
        for enemy in Enemies:
            if PlayersXpos[0] == EnemiesXpos[cycle] and PlayersYpos[0] == EnemiesYpos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy2 in Enemies2:
            if PlayersXpos[0] == Enemies2Xpos[cycle] and PlayersYpos[0] == Enemies2Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy3 in Enemies3:
            if PlayersXpos[0] == Enemies3Xpos[cycle] and PlayersYpos[0] == Enemies3Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy4 in Enemies4:
            if PlayersXpos[0] == Enemies4Xpos[cycle] and PlayersYpos[0] == Enemies4Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy5 in Enemies5:
            if PlayersXpos[0] == Enemies5Xpos[cycle] and PlayersYpos[0] == Enemies5Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy6 in Enemies6:
            if PlayersXpos[0] == Enemies6Xpos[cycle] and PlayersYpos[0] == Enemies6Ypos[cycle]:
                GameOver()
            cycle += 1
        if start == 0:
            NextWave()
        start = 1

    def AKey(event):
        global start
        self.player2.delete("all")
        self.player2.create_polygon(0,15,30,30,15,15,30,0,0,15,fill="white")
        if PlayersXpos[1] > 0:
            PlayersXpos[1] -= 25
        self.player2.place(x=PlayersXpos[1],y=PlayersYpos[1])
        PlayersDir[1] = "W"
        cycle = 0
        for enemy in Enemies:
            if PlayersXpos[1] == EnemiesXpos[cycle] and PlayersYpos[1] == EnemiesYpos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy2 in Enemies2:
            if PlayersXpos[1] == Enemies2Xpos[cycle] and PlayersYpos[1] == Enemies2Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy3 in Enemies3:
            if PlayersXpos[1] == Enemies3Xpos[cycle] and PlayersYpos[1] == Enemies3Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy4 in Enemies4:
            if PlayersXpos[1] == Enemies4Xpos[cycle] and PlayersYpos[1] == Enemies4Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy5 in Enemies5:
            if PlayersXpos[1] == Enemies5Xpos[cycle] and PlayersYpos[1] == Enemies5Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy6 in Enemies6:
            if PlayersXpos[1] == Enemies6Xpos[cycle] and PlayersYpos[1] == Enemies6Ypos[cycle]:
                GameOver()
            cycle += 1
        if start == 0:
            NextWave()
        start = 1

    def DKey(event):
        global start
        self.player2.delete("all")
        self.player2.create_polygon(30,15,0,30,15,15,0,0,30,15,fill="white")
        if PlayersXpos[1]  < 800:
            PlayersXpos[1]  += 25
        self.player2.place(x=PlayersXpos[1] ,y=PlayersYpos[1] )
        PlayersDir[1] = "E"
        cycle = 0
        for enemy in Enemies:
            if PlayersXpos[1]  == EnemiesXpos[cycle] and PlayersYpos[1]  == EnemiesYpos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy2 in Enemies2:
            if PlayersXpos[1]  == Enemies2Xpos[cycle] and PlayersYpos[1]  == Enemies2Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy3 in Enemies3:
            if PlayersXpos[1]  == Enemies3Xpos[cycle] and PlayersYpos[1]  == Enemies3Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy4 in Enemies4:
            if PlayersXpos[1]  == Enemies4Xpos[cycle] and PlayersYpos[1]  == Enemies4Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy5 in Enemies5:
            if PlayersXpos[1]  == Enemies5Xpos[cycle] and PlayersYpos[1]  == Enemies5Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy6 in Enemies6:
            if PlayersXpos[1]  == Enemies6Xpos[cycle] and PlayersYpos[1]  == Enemies6Ypos[cycle]:
                GameOver()
            cycle += 1
        if start == 0:
            NextWave()
        start = 1

    def WKey(event):
        global start
        self.player2.delete("all")
        self.player2.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="white")
        if PlayersYpos[1] > 0:
            PlayersYpos[1] -= 25
        self.player2.place(x=PlayersXpos[1],y=PlayersYpos[1])
        PlayersDir[1] = "N"
        cycle = 0
        for enemy in Enemies:
            if PlayersXpos[1] == EnemiesXpos[cycle] and PlayersYpos[1] == EnemiesYpos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy2 in Enemies2:
            if PlayersXpos[1] == Enemies2Xpos[cycle] and PlayersYpos[1] == Enemies2Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy3 in Enemies3:
            if PlayersXpos[1] == Enemies3Xpos[cycle] and PlayersYpos[1] == Enemies3Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy4 in Enemies4:
            if PlayersXpos[1] == Enemies4Xpos[cycle] and PlayersYpos[1] == Enemies4Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy5 in Enemies5:
            if PlayersXpos[1] == Enemies5Xpos[cycle] and PlayersYpos[1] == Enemies5Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy6 in Enemies6:
            if PlayersXpos[1] == Enemies6Xpos[cycle] and PlayersYpos[1] == Enemies6Ypos[cycle]:
                GameOver()
            cycle += 1
        if start == 0:
            NextWave()
        start = 1

    def SKey(event):
        global start
        self.player2.delete("all")
        self.player2.create_polygon(15,30,30,0,15,15,0,0,15,30,fill="white")
        if PlayersYpos[1] < 650:
            PlayersYpos[1] += 25
        self.player2.place(x=PlayersXpos[1],y=PlayersYpos[1])
        PlayersDir[1] = "S"
        cycle = 0
        for enemy in Enemies:
            if PlayersXpos[1] == EnemiesXpos[cycle] and PlayersYpos[1] == EnemiesYpos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy2 in Enemies2:
            if PlayersXpos[1] == Enemies2Xpos[cycle] and PlayersYpos[1] == Enemies2Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy3 in Enemies3:
            if PlayersXpos[1] == Enemies3Xpos[cycle] and PlayersYpos[1] == Enemies3Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy4 in Enemies4:
            if PlayersXpos[1] == Enemies4Xpos[cycle] and PlayersYpos[1] == Enemies4Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy5 in Enemies5:
            if PlayersXpos[1] == Enemies5Xpos[cycle] and PlayersYpos[1] == Enemies5Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy6 in Enemies6:
            if PlayersXpos[1] == Enemies6Xpos[cycle] and PlayersYpos[1] == Enemies6Ypos[cycle]:
                GameOver()
            cycle += 1
        if start == 0:
            NextWave()
        start = 1

    def CreateEnemy():
        global Xpos
        global Ypos
        global enXpos
        global enYpos
        global Damage
        global created
        enXpos = random.randrange(0,33)*25
        enYpos = random.randrange(0,27)*25
        while (abs(PlayersXpos[0] - enXpos) <= 75 and abs(PlayersYpos[0] - enYpos) <= 75) or (abs(PlayersXpos[1] - enXpos) <= 75 and abs(PlayersYpos[1] - enYpos) <= 75):
            enXpos = random.randrange(0,33)*25
            enYpos = random.randrange(0,27)*25
        self.enemy = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
        self.enemy.place(x=enXpos,y=enYpos)
        self.enemy.polygon = self.enemy.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="darkviolet")
        Enemies.append(self.enemy)
        EnemiesDmg.append(Damage)
        EnemiesXpos.append(enXpos)
        EnemiesYpos.append(enYpos)
        created = 1

    def CreateEnemy2():
        global Xpos
        global Ypos
        global en2Xpos
        global en2Ypos
        global created2
        en2Xpos = random.randrange(0,33)*25
        en2Ypos = random.randrange(0,27)*25
        while (abs(PlayersXpos[0] - en2Xpos) <= 75 and abs(PlayersYpos[0] - en2Ypos) <= 75) or (abs(PlayersXpos[1] - en2Xpos) <= 75 and abs(PlayersYpos[1] - en2Ypos) <= 75):
            en2Xpos = random.randrange(0,33)*25
            en2Ypos = random.randrange(0,27)*25
        self.enemy2 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
        self.enemy2.place(x=en2Xpos,y=en2Ypos)
        self.enemy2.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="red")
        Enemies2.append(self.enemy2)
        Enemies2Xpos.append(en2Xpos)
        Enemies2Ypos.append(en2Ypos)
        created2 = 1

    def CreateEnemy3():
        global Xpos
        global Ypos
        global en3Xpos
        global en3Ypos
        global Damage3
        global created3
        en3Xpos = random.randrange(0,33)*25
        en3Ypos = random.randrange(0,27)*25
        while (abs(PlayersXpos[0] - en3Xpos) <= 75 and abs(PlayersYpos[0] - en3Ypos) <= 75) or (abs(PlayersXpos[1] - en3Xpos) <= 75 and abs(PlayersYpos[1] - en3Ypos) <= 75):
            en3Xpos = random.randrange(0,33)*25
            en3Ypos = random.randrange(0,27)*25
        self.enemy3 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
        self.enemy3.place(x=en3Xpos,y=en3Ypos)
        self.enemy3.polygon = self.enemy3.create_polygon(10,0,0,0,0,30,30,30,30,0,20,0,20,10,10,10,fill="navy")
        Enemies3.append(self.enemy3)
        Enemies3Dmg.append(Damage3)
        Enemies3Xpos.append(en3Xpos)
        Enemies3Ypos.append(en3Ypos)
        created3 = 1

    def CreateEnemy4():
        global Xpos
        global Ypos
        global en4Xpos
        global en4Ypos
        global created4
        en4Xpos = random.randrange(0,33)*25
        en4Ypos = random.randrange(0,27)*25
        while (abs(PlayersXpos[0] - en4Xpos) <= 150 and abs(PlayersYpos[0] - en4Ypos) <= 150) or (abs(PlayersXpos[1] - en4Xpos) <= 150 and abs(PlayersYpos[1] - en4Ypos) <= 150):
            en4Xpos = random.randrange(0,33)*25
            en4Ypos = random.randrange(0,27)*25
        self.enemy4 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
        self.enemy4.place(x=en4Xpos,y=en4Ypos)
        self.enemy4.create_polygon(15,0,5,15,12,15,5,30,25,30,17,15,25,15,fill="darkgreen")
        Enemies4.append(self.enemy4)
        Enemies4Xpos.append(en4Xpos)
        Enemies4Ypos.append(en4Ypos)
        created4 = 1

    def CreateEnemy5():
        global Xpos
        global Ypos
        global en5Xpos
        global en5Ypos
        global Damage5
        global created5
        wall = random.choice(["N","E","S","W"])
        if wall == "N":
            en5Xpos = random.randrange(0,33)*25
            en5Ypos = 0
            self.enemy5 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
            self.enemy5.place(x=en5Xpos,y=en5Ypos)
            self.enemy5.polygon = self.enemy5.create_polygon(0,0,10,15,10,30,20,30,20,15,30,0,fill="darkorange2")
        elif wall == "E":
            en5Xpos = 800
            en5Ypos = random.randrange(0,27)*25
            self.enemy5 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
            self.enemy5.place(x=en5Xpos,y=en5Ypos)
            self.enemy5.polygon = self.enemy5.create_polygon(30,0,15,10,0,10,0,20,15,20,30,30,fill="darkorange2")
        elif wall == "S":
            en5Xpos = random.randrange(0,33)*25
            en5Ypos = 650
            self.enemy5 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
            self.enemy5.place(x=en5Xpos,y=en5Ypos)
            self.enemy5.polygon = self.enemy5.create_polygon(30,30,20,15,20,0,10,0,10,15,0,30,fill="darkorange2")
        elif wall == "W":
            en5Xpos = 0
            en5Ypos = random.randrange(0,27)*25
            self.enemy5 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
            self.enemy5.place(x=en5Xpos,y=en5Ypos)
            self.enemy5.polygon = self.enemy5.create_polygon(0,30,15,20,30,20,30,10,15,10,0,0,fill="darkorange2")
        while (abs(PlayersXpos[0] - en5Xpos) <= 75 and abs(PlayersYpos[0] - en5Ypos) <= 75) or (abs(PlayersXpos[1] - en5Xpos) <= 75 and abs(PlayersYpos[1] - en5Ypos) <= 75):
            wall = random.choice(["N","E","S","W"])
            if wall == "N":
                en5Xpos = random.randrange(0,33)*25
                en5Ypos = 0
                self.enemy5 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
                self.enemy5.place(x=en5Xpos,y=en5Ypos)
                self.enemy5.polygon = self.enemy5.create_polygon(0,0,10,15,10,30,20,30,20,15,30,0,fill="darkorange2")
            elif wall == "E":
                en5Xpos = 800
                en5Ypos = random.randrange(0,27)*25
                self.enemy5 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
                self.enemy5.place(x=en5Xpos,y=en5Ypos)
                self.enemy5.polygon = self.enemy5.create_polygon(30,0,15,10,0,10,0,20,15,20,30,30,fill="darkorange2")
            elif wall == "S":
                en5Xpos = random.randrange(0,33)*25
                en5Ypos = 650
                self.enemy5 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
                self.enemy5.place(x=en5Xpos,y=en5Ypos)
                self.enemy5.polygon = self.enemy5.create_polygon(30,30,20,15,20,0,10,0,10,15,0,30,fill="darkorange2")
            elif wall == "W":
                en5Xpos = 0
                en5Ypos = random.randrange(0,27)*25
                self.enemy5 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
                self.enemy5.place(x=en5Xpos,y=en5Ypos)
                self.enemy5.polygon = self.enemy5.create_polygon(0,30,15,20,30,20,30,10,15,10,0,0,fill="darkorange2")
        Enemies5.append(self.enemy5)
        Enemies5Dmg.append(Damage5)
        Enemies5Xpos.append(en5Xpos)
        Enemies5Ypos.append(en5Ypos)
        Enemies5Wall.append(wall)
        created5 = 1

    def CreateEnemy6():
        global Xpos
        global Ypos
        global en6Xpos
        global en6Ypos
        en6Type = random.choice([1,2,3,4])
        en6Xpos = random.randrange(0,33)*25
        en6Ypos = random.randrange(0,27)*25
        while (abs(PlayersXpos[0] - en6Xpos) <= 75 and abs(PlayersYpos[0] - en6Ypos) <= 75) or (abs(PlayersXpos[1] - en6Xpos) <= 75 and abs(PlayersYpos[1] - en6Ypos) <= 75):
            en6Xpos = random.randrange(0,33)*25
            en6Ypos = random.randrange(0,27)*25
        self.enemy6 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
        self.enemy6.place(x=en6Xpos,y=en6Ypos)
        self.enemy6.oval = self.enemy6.create_oval(0,0,30,30,fill="gray20")
        Enemies6.append(self.enemy6)
        Enemies6Xpos.append(en6Xpos)
        Enemies6Ypos.append(en6Ypos)
        Enemies6Type.append(en6Type)
        Enemies6Dmg.append(Damage6)

    def EnemyMove():
        global Xpos
        global Ypos
        global gameover
        global created
        if gameover != 1:
            self.after(300,EnemyMove)
            if created == 1:
                cycle = 0
                for self.enemy in Enemies:
                    rndDir = random.choice(["X","Y"])
                    if EnemiesDmg[cycle] == 0:
                        EnemyColor = "darkviolet"
                    else:
                        EnemyColor = "violet"
                    if ((PlayersXpos[0] - EnemiesXpos[cycle])**2 + (PlayersYpos[0] - EnemiesYpos[cycle])**2)**0.5 <= ((PlayersXpos[1] - EnemiesXpos[cycle])**2 + (PlayersYpos[1] - EnemiesYpos[cycle])**2)**0.5:
                        #Target Player 1
                        if PlayersXpos[0] < EnemiesXpos[cycle] and PlayersYpos[0] < EnemiesYpos[cycle]:
                            self.enemy.delete("all")
                            if rndDir == "X":
                                EnemiesXpos[cycle] -= 25
                                self.enemy.polygon = self.enemy.create_polygon(0,15,30,30,15,15,30,0,0,15,fill=EnemyColor)
                            else:
                                EnemiesYpos[cycle] -= 25
                                self.enemy.polygon = self.enemy.create_polygon(15,0,30,30,15,15,0,30,15,0,fill=EnemyColor)
                        elif PlayersXpos[0] < EnemiesXpos[cycle] and PlayersYpos[0] > EnemiesYpos[cycle]:
                            self.enemy.delete("all")
                            if rndDir == "X":
                                EnemiesXpos[cycle] -= 25
                                self.enemy.polygon = self.enemy.create_polygon(0,15,30,30,15,15,30,0,0,15,fill=EnemyColor)
                            else:
                                EnemiesYpos[cycle] += 25
                                self.enemy.polygon = self.enemy.create_polygon(15,30,30,0,15,15,0,0,15,30,fill=EnemyColor)
                        elif PlayersXpos[0] > EnemiesXpos[cycle] and PlayersYpos[0] < EnemiesYpos[cycle]:
                            self.enemy.delete("all")
                            if rndDir == "X":
                                EnemiesXpos[cycle] += 25
                                self.enemy.polygon = self.enemy.create_polygon(30,15,0,30,15,15,0,0,30,15,fill=EnemyColor)
                            else:
                                EnemiesYpos[cycle] -= 25
                                self.enemy.polygon = self.enemy.create_polygon(15,0,30,30,15,15,0,30,15,0,fill=EnemyColor)
                        elif PlayersXpos[0] > EnemiesXpos[cycle] and PlayersYpos[0] > EnemiesYpos[cycle]:
                            self.enemy.delete("all")
                            if rndDir == "X":
                                EnemiesXpos[cycle] += 25
                                self.enemy.polygon = self.enemy.create_polygon(30,15,0,30,15,15,0,0,30,15,fill=EnemyColor)
                            else:
                                EnemiesYpos[cycle] += 25
                                self.enemy.polygon = self.enemy.create_polygon(15,30,30,0,15,15,0,0,15,30,fill=EnemyColor)
                        elif PlayersXpos[0] < EnemiesXpos[cycle] and PlayersYpos[0] == EnemiesYpos[cycle]:
                            self.enemy.delete("all")
                            self.enemy.polygon = self.enemy.create_polygon(0,15,30,30,15,15,30,0,0,15,fill=EnemyColor)
                            EnemiesXpos[cycle] -= 25
                        elif PlayersXpos[0] > EnemiesXpos[cycle] and PlayersYpos[0] == EnemiesYpos[cycle]:
                            self.enemy.delete("all")
                            self.enemy.polygon = self.enemy.create_polygon(30,15,0,30,15,15,0,0,30,15,fill=EnemyColor)
                            EnemiesXpos[cycle] += 25
                        elif PlayersXpos[0] == EnemiesXpos[cycle] and PlayersYpos[0] < EnemiesYpos[cycle]:
                            self.enemy.delete("all")
                            self.enemy.polygon = self.enemy.create_polygon(15,0,30,30,15,15,0,30,15,0,fill=EnemyColor)
                            EnemiesYpos[cycle] -= 25
                        elif PlayersXpos[0] == EnemiesXpos[cycle] and PlayersYpos[0] > EnemiesYpos[cycle]:
                            self.enemy.delete("all")
                            self.enemy.polygon = self.enemy.create_polygon(15,30,30,0,15,15,0,0,15,30,fill=EnemyColor)
                            EnemiesYpos[cycle] += 25
                    else:
                        #Target Player 2
                        if PlayersXpos[1] < EnemiesXpos[cycle] and PlayersYpos[1] < EnemiesYpos[cycle]:
                            self.enemy.delete("all")
                            if rndDir == "X":
                                EnemiesXpos[cycle] -= 25
                                self.enemy.polygon = self.enemy.create_polygon(0,15,30,30,15,15,30,0,0,15,fill=EnemyColor)
                            else:
                                EnemiesYpos[cycle] -= 25
                                self.enemy.polygon = self.enemy.create_polygon(15,0,30,30,15,15,0,30,15,0,fill=EnemyColor)
                        elif PlayersXpos[1] < EnemiesXpos[cycle] and PlayersYpos[1] > EnemiesYpos[cycle]:
                            self.enemy.delete("all")
                            if rndDir == "X":
                                EnemiesXpos[cycle] -= 25
                                self.enemy.polygon = self.enemy.create_polygon(0,15,30,30,15,15,30,0,0,15,fill=EnemyColor)
                            else:
                                EnemiesYpos[cycle] += 25
                                self.enemy.polygon = self.enemy.create_polygon(15,30,30,0,15,15,0,0,15,30,fill=EnemyColor)
                        elif PlayersXpos[1] > EnemiesXpos[cycle] and PlayersYpos[1] < EnemiesYpos[cycle]:
                            self.enemy.delete("all")
                            if rndDir == "X":
                                EnemiesXpos[cycle] += 25
                                self.enemy.polygon = self.enemy.create_polygon(30,15,0,30,15,15,0,0,30,15,fill=EnemyColor)
                            else:
                                EnemiesYpos[cycle] -= 25
                                self.enemy.polygon = self.enemy.create_polygon(15,0,30,30,15,15,0,30,15,0,fill=EnemyColor)
                        elif PlayersXpos[1] > EnemiesXpos[cycle] and PlayersYpos[1] > EnemiesYpos[cycle]:
                            self.enemy.delete("all")
                            if rndDir == "X":
                                EnemiesXpos[cycle] += 25
                                self.enemy.polygon = self.enemy.create_polygon(30,15,0,30,15,15,0,0,30,15,fill=EnemyColor)
                            else:
                                EnemiesYpos[cycle] += 25
                                self.enemy.polygon = self.enemy.create_polygon(15,30,30,0,15,15,0,0,15,30,fill=EnemyColor)
                        elif PlayersXpos[1] < EnemiesXpos[cycle] and PlayersYpos[1] == EnemiesYpos[cycle]:
                            self.enemy.delete("all")
                            self.enemy.polygon = self.enemy.create_polygon(0,15,30,30,15,15,30,0,0,15,fill=EnemyColor)
                            EnemiesXpos[cycle] -= 25
                        elif PlayersXpos[1] > EnemiesXpos[cycle] and PlayersYpos[1] == EnemiesYpos[cycle]:
                            self.enemy.delete("all")
                            self.enemy.polygon = self.enemy.create_polygon(30,15,0,30,15,15,0,0,30,15,fill=EnemyColor)
                            EnemiesXpos[cycle] += 25
                        elif PlayersXpos[1] == EnemiesXpos[cycle] and PlayersYpos[1] < EnemiesYpos[cycle]:
                            self.enemy.delete("all")
                            self.enemy.polygon = self.enemy.create_polygon(15,0,30,30,15,15,0,30,15,0,fill=EnemyColor)
                            EnemiesYpos[cycle] -= 25
                        elif PlayersXpos[1] == EnemiesXpos[cycle] and PlayersYpos[1] > EnemiesYpos[cycle]:
                            self.enemy.delete("all")
                            self.enemy.polygon = self.enemy.create_polygon(15,30,30,0,15,15,0,0,15,30,fill=EnemyColor)
                            EnemiesYpos[cycle] += 25
                    self.enemy.place(x=EnemiesXpos[cycle],y=EnemiesYpos[cycle])
                    for Pcycle in range(0,2):
                        if PlayersXpos[Pcycle] == EnemiesXpos[cycle] and PlayersYpos[Pcycle] == EnemiesYpos[cycle]:
                            GameOver()
                    cycle += 1

    def Enemy2Move():
        global Xpos
        global Ypos
        global gameover
        global created2
        if gameover != 1:
            self.after(300,Enemy2Move)
            if created2 == 1:
                cycle = 0
                for self.enemy2 in Enemies2:
                    if ((PlayersXpos[0] - Enemies2Xpos[cycle])**2 + (PlayersYpos[0] - Enemies2Ypos[cycle])**2)**0.5 <= ((PlayersXpos[1] - Enemies2Xpos[cycle])**2 + (PlayersYpos[1] - Enemies2Ypos[cycle])**2)**0.5:
                        #Target Player 1
                        if PlayersXpos[0] < Enemies2Xpos[cycle] and PlayersYpos[0] < Enemies2Ypos[cycle]:
                            self.enemy2.delete("all")
                            self.enemy2.create_polygon(0,0,30,15,15,15,15,30,0,0,fill="red")
                            Enemies2Xpos[cycle] -= 25
                            Enemies2Ypos[cycle] -= 25
                        elif PlayersXpos[0] < Enemies2Xpos[cycle] and PlayersYpos[0] > Enemies2Ypos[cycle]:
                            self.enemy2.delete("all")
                            self.enemy2.create_polygon(0,30,15,0,15,15,30,15,0,30,fill="red")
                            Enemies2Xpos[cycle] -= 25
                            Enemies2Ypos[cycle] += 25
                        elif PlayersXpos[0] > Enemies2Xpos[cycle] and PlayersYpos[0] < Enemies2Ypos[cycle]:
                            self.enemy2.delete("all")
                            self.enemy2.create_polygon(30,0,0,15,15,15,15,30,30,0,fill="red")
                            Enemies2Xpos[cycle] += 25
                            Enemies2Ypos[cycle] -= 25
                        elif PlayersXpos[0] > Enemies2Xpos[cycle] and PlayersYpos[0] > Enemies2Ypos[cycle]:
                            self.enemy2.delete("all")
                            self.enemy2.create_polygon(30,30,15,0,15,15,0,15,30,30,fill="red")
                            Enemies2Xpos[cycle] += 25
                            Enemies2Ypos[cycle] += 25
                        elif PlayersXpos[0] < Enemies2Xpos[cycle] and PlayersYpos[0] == Enemies2Ypos[cycle]:
                            self.enemy2.delete("all")
                            self.enemy2.create_polygon(0,15,30,30,15,15,30,0,0,15,fill="red")
                            Enemies2Xpos[cycle] -= 25
                        elif PlayersXpos[0] > Enemies2Xpos[cycle] and PlayersYpos[0] == Enemies2Ypos[cycle]:
                            self.enemy2.delete("all")
                            self.enemy2.create_polygon(30,15,0,30,15,15,0,0,30,15,fill="red")
                            Enemies2Xpos[cycle] += 25
                        elif PlayersXpos[0] == Enemies2Xpos[cycle] and PlayersYpos[0] < Enemies2Ypos[cycle]:
                            self.enemy2.delete("all")
                            self.enemy2.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="red")
                            Enemies2Ypos[cycle] -= 25
                        elif PlayersXpos[0] == Enemies2Xpos[cycle] and PlayersYpos[0] > Enemies2Ypos[cycle]:
                            self.enemy2.delete("all")
                            self.enemy2.create_polygon(15,30,30,0,15,15,0,0,15,30,fill="red")
                            Enemies2Ypos[cycle] += 25
                    else:
                        #Target Player 2
                        if PlayersXpos[1] < Enemies2Xpos[cycle] and PlayersYpos[1] < Enemies2Ypos[cycle]:
                            self.enemy2.delete("all")
                            self.enemy2.create_polygon(0,0,30,15,15,15,15,30,0,0,fill="red")
                            Enemies2Xpos[cycle] -= 25
                            Enemies2Ypos[cycle] -= 25
                        elif PlayersXpos[1] < Enemies2Xpos[cycle] and PlayersYpos[1] > Enemies2Ypos[cycle]:
                            self.enemy2.delete("all")
                            self.enemy2.create_polygon(0,30,15,0,15,15,30,15,0,30,fill="red")
                            Enemies2Xpos[cycle] -= 25
                            Enemies2Ypos[cycle] += 25
                        elif PlayersXpos[1] > Enemies2Xpos[cycle] and PlayersYpos[1] < Enemies2Ypos[cycle]:
                            self.enemy2.delete("all")
                            self.enemy2.create_polygon(30,0,0,15,15,15,15,30,30,0,fill="red")
                            Enemies2Xpos[cycle] += 25
                            Enemies2Ypos[cycle] -= 25
                        elif PlayersXpos[1] > Enemies2Xpos[cycle] and PlayersYpos[1] > Enemies2Ypos[cycle]:
                            self.enemy2.delete("all")
                            self.enemy2.create_polygon(30,30,15,0,15,15,0,15,30,30,fill="red")
                            Enemies2Xpos[cycle] += 25
                            Enemies2Ypos[cycle] += 25
                        elif PlayersXpos[1] < Enemies2Xpos[cycle] and PlayersYpos[1] == Enemies2Ypos[cycle]:
                            self.enemy2.delete("all")
                            self.enemy2.create_polygon(0,15,30,30,15,15,30,0,0,15,fill="red")
                            Enemies2Xpos[cycle] -= 25
                        elif PlayersXpos[1] > Enemies2Xpos[cycle] and PlayersYpos[1] == Enemies2Ypos[cycle]:
                            self.enemy2.delete("all")
                            self.enemy2.create_polygon(30,15,0,30,15,15,0,0,30,15,fill="red")
                            Enemies2Xpos[cycle] += 25
                        elif PlayersXpos[1] == Enemies2Xpos[cycle] and PlayersYpos[1] < Enemies2Ypos[cycle]:
                            self.enemy2.delete("all")
                            self.enemy2.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="red")
                            Enemies2Ypos[cycle] -= 25
                        elif PlayersXpos[1] == Enemies2Xpos[cycle] and PlayersYpos[1] > Enemies2Ypos[cycle]:
                            self.enemy2.delete("all")
                            self.enemy2.create_polygon(15,30,30,0,15,15,0,0,15,30,fill="red")
                            Enemies2Ypos[cycle] += 25
                    self.enemy2.place(x=Enemies2Xpos[cycle],y=Enemies2Ypos[cycle])
                    for Pcycle in range(0,2):
                            if PlayersXpos[Pcycle] == Enemies2Xpos[cycle] and PlayersYpos[Pcycle] == Enemies2Ypos[cycle]:
                                GameOver()
                    cycle += 1

    def Enemy3Move():
        global Xpos
        global Ypos
        global gameover
        global created3
        if gameover != 1:
            self.after(350,Enemy3Move)
            if created3 == 1:
                cycle = 0
                for self.enemy3 in Enemies3:
                    rndDir = random.choice(["X","Y"])
                    if Enemies3Dmg[cycle] == 0:
                        Enemy3Color = "navy"
                    elif Enemies3Dmg[cycle] == 1:
                        Enemy3Color = "blue"
                    elif Enemies3Dmg[cycle] == 2:
                        Enemy3Color = "dodgerblue"
                    elif Enemies3Dmg[cycle] == 3:
                        Enemy3Color = "deepskyblue"
                    else:
                        Enemy3Color = "lightskyblue"
                    if ((PlayersXpos[0] - Enemies3Xpos[cycle])**2 + (PlayersYpos[0] - Enemies3Ypos[cycle])**2)**0.5 <= ((PlayersXpos[1] - Enemies3Xpos[cycle])**2 + (PlayersYpos[1] - Enemies3Ypos[cycle])**2)**0.5:
                        #Target Player 1
                        if PlayersXpos[0] < Enemies3Xpos[cycle] and PlayersYpos[0] < Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            if rndDir == "X":
                                Enemies3Xpos[cycle] -= 25
                                self.enemy3.polygon = self.enemy3.create_polygon(0,20,0,30,30,30,30,0,0,0,0,10,10,10,10,20,fill=Enemy3Color)
                            else:
                                Enemies3Ypos[cycle] -= 25
                                self.enemy3.polygon = self.enemy3.create_polygon(10,0,0,0,0,30,30,30,30,0,20,0,20,10,10,10,fill=Enemy3Color)
                        elif PlayersXpos[0] < Enemies3Xpos[cycle] and PlayersYpos[0] > Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            if rndDir == "X":
                                Enemies3Xpos[cycle] -= 25
                                self.enemy3.polygon = self.enemy3.create_polygon(0,20,0,30,30,30,30,0,0,0,0,10,10,10,10,20,fill=Enemy3Color)
                            else:
                                Enemies3Ypos[cycle] += 25
                                self.enemy3.polygon = self.enemy3.create_polygon(20,30,30,30,30,0,0,0,0,30,10,30,10,20,20,20,fill=Enemy3Color)
                        elif PlayersXpos[0] > Enemies3Xpos[cycle] and PlayersYpos[0] < Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            if rndDir == "X":
                                Enemies3Xpos[cycle] += 25
                                self.enemy3.polygon = self.enemy3.create_polygon(30,10,30,0,0,0,0,30,30,30,30,20,20,20,20,10,fill=Enemy3Color)
                            else:
                                Enemies3Ypos[cycle] -= 25
                                self.enemy3.polygon = self.enemy3.create_polygon(10,0,0,0,0,30,30,30,30,0,20,0,20,10,10,10,fill=Enemy3Color)
                        elif PlayersXpos[0] > Enemies3Xpos[cycle] and PlayersYpos[0] > Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            if rndDir == "X":
                                Enemies3Xpos[cycle] += 25
                                self.enemy3.polygon = self.enemy3.create_polygon(30,10,30,0,0,0,0,30,30,30,30,20,20,20,20,10,fill=Enemy3Color)
                            else:
                                Enemies3Ypos[cycle] += 25
                                self.enemy3.polygon = self.enemy3.create_polygon(20,30,30,30,30,0,0,0,0,30,10,30,10,20,20,20,fill=Enemy3Color)
                        elif PlayersXpos[0] < Enemies3Xpos[cycle] and PlayersYpos[0] == Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            self.enemy3.polygon = self.enemy3.create_polygon(0,20,0,30,30,30,30,0,0,0,0,10,10,10,10,20,fill=Enemy3Color)
                            Enemies3Xpos[cycle] -= 25
                        elif PlayersXpos[0] > Enemies3Xpos[cycle] and PlayersYpos[0] == Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            self.enemy3.polygon = self.enemy3.create_polygon(30,10,30,0,0,0,0,30,30,30,30,20,20,20,20,10,fill=Enemy3Color)
                            Enemies3Xpos[cycle] += 25
                        elif PlayersXpos[0] == Enemies3Xpos[cycle] and PlayersYpos[0] < Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            self.enemy3.polygon = self.enemy3.create_polygon(10,0,0,0,0,30,30,30,30,0,20,0,20,10,10,10,fill=Enemy3Color)
                            Enemies3Ypos[cycle] -= 25
                        elif PlayersXpos[0] == Enemies3Xpos[cycle] and PlayersYpos[0] > Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            self.enemy3.polygon = self.enemy3.create_polygon(20,30,30,30,30,0,0,0,0,30,10,30,10,20,20,20,fill=Enemy3Color)
                            Enemies3Ypos[cycle] += 25
                    else:
                    #Target Player 2
                        if PlayersXpos[1] < Enemies3Xpos[cycle] and PlayersYpos[1] < Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            if rndDir == "X":
                                Enemies3Xpos[cycle] -= 25
                                self.enemy3.polygon = self.enemy3.create_polygon(0,20,0,30,30,30,30,0,0,0,0,10,10,10,10,20,fill=Enemy3Color)
                            else:
                                Enemies3Ypos[cycle] -= 25
                                self.enemy3.polygon = self.enemy3.create_polygon(10,0,0,0,0,30,30,30,30,0,20,0,20,10,10,10,fill=Enemy3Color)
                        elif PlayersXpos[1] < Enemies3Xpos[cycle] and PlayersYpos[1] > Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            if rndDir == "X":
                                Enemies3Xpos[cycle] -= 25
                                self.enemy3.polygon = self.enemy3.create_polygon(0,20,0,30,30,30,30,0,0,0,0,10,10,10,10,20,fill=Enemy3Color)
                            else:
                                Enemies3Ypos[cycle] += 25
                                self.enemy3.polygon = self.enemy3.create_polygon(20,30,30,30,30,0,0,0,0,30,10,30,10,20,20,20,fill=Enemy3Color)
                        elif PlayersXpos[1] > Enemies3Xpos[cycle] and PlayersYpos[1] < Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            if rndDir == "X":
                                Enemies3Xpos[cycle] += 25
                                self.enemy3.polygon = self.enemy3.create_polygon(30,10,30,0,0,0,0,30,30,30,30,20,20,20,20,10,fill=Enemy3Color)
                            else:
                                Enemies3Ypos[cycle] -= 25
                                self.enemy3.polygon = self.enemy3.create_polygon(10,0,0,0,0,30,30,30,30,0,20,0,20,10,10,10,fill=Enemy3Color)
                        elif PlayersXpos[1] > Enemies3Xpos[cycle] and PlayersYpos[1] > Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            if rndDir == "X":
                                Enemies3Xpos[cycle] += 25
                                self.enemy3.polygon = self.enemy3.create_polygon(30,10,30,0,0,0,0,30,30,30,30,20,20,20,20,10,fill=Enemy3Color)
                            else:
                                Enemies3Ypos[cycle] += 25
                                self.enemy3.polygon = self.enemy3.create_polygon(20,30,30,30,30,0,0,0,0,30,10,30,10,20,20,20,fill=Enemy3Color)
                        elif PlayersXpos[1] < Enemies3Xpos[cycle] and PlayersYpos[1] == Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            self.enemy3.polygon = self.enemy3.create_polygon(0,20,0,30,30,30,30,0,0,0,0,10,10,10,10,20,fill=Enemy3Color)
                            Enemies3Xpos[cycle] -= 25
                        elif PlayersXpos[1] > Enemies3Xpos[cycle] and PlayersYpos[1] == Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            self.enemy3.polygon = self.enemy3.create_polygon(30,10,30,0,0,0,0,30,30,30,30,20,20,20,20,10,fill=Enemy3Color)
                            Enemies3Xpos[cycle] += 25
                        elif PlayersXpos[1] == Enemies3Xpos[cycle] and PlayersYpos[1] < Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            self.enemy3.polygon = self.enemy3.create_polygon(10,0,0,0,0,30,30,30,30,0,20,0,20,10,10,10,fill=Enemy3Color)
                            Enemies3Ypos[cycle] -= 25
                        elif PlayersXpos[1] == Enemies3Xpos[cycle] and PlayersYpos[1] > Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            self.enemy3.polygon = self.enemy3.create_polygon(20,30,30,30,30,0,0,0,0,30,10,30,10,20,20,20,fill=Enemy3Color)
                            Enemies3Ypos[cycle] += 25
                    self.enemy3.place(x=Enemies3Xpos[cycle],y=Enemies3Ypos[cycle])
                    for Pcycle in range(0,2):
                        if PlayersXpos[Pcycle] == Enemies3Xpos[cycle] and PlayersYpos[Pcycle] == Enemies3Ypos[cycle]:
                            GameOver()
                    cycle += 1

    def Enemy4Move():
        global Xpos
        global Ypos
        global gameover
        global created4
        if gameover != 1:
            self.after(100,Enemy4Move)
            if created4 == 1:
                cycle = 0
                for self.enemy4 in Enemies4:
                    rndDir = random.choice(["X","Y"])
                    Enemy4Color = "darkgreen"
                    if ((PlayersXpos[0] - Enemies4Xpos[cycle])**2 + (PlayersYpos[0] - Enemies4Ypos[cycle])**2)**0.5 <= ((PlayersXpos[1] - Enemies4Xpos[cycle])**2 + (PlayersYpos[1] - Enemies4Ypos[cycle])**2)**0.5:
                        #Target Player 1
                        if PlayersXpos[0] < Enemies4Xpos[cycle] and PlayersYpos[0] < Enemies4Ypos[cycle]:
                            self.enemy4.delete("all")
                            if rndDir == "X":
                                Enemies4Xpos[cycle] -= 25
                                self.enemy4.polygon = self.enemy4.create_polygon(0,15,15,25,15,17,30,25,30,5,15,13,15,5,fill=Enemy4Color)
                            else:
                                Enemies4Ypos[cycle] -= 25
                                self.enemy4.polygon = self.enemy4.create_polygon(15,0,5,15,12,15,5,30,25,30,17,15,25,15,fill=Enemy4Color)
                        elif PlayersXpos[0] < Enemies4Xpos[cycle] and PlayersYpos[0] > Enemies4Ypos[cycle]:
                            self.enemy4.delete("all")
                            if rndDir == "X":
                                Enemies4Xpos[cycle] -= 25
                                self.enemy4.polygon = self.enemy4.create_polygon(0,15,15,25,15,17,30,25,30,5,15,13,15,5,fill=Enemy4Color)
                            else:
                                Enemies4Ypos[cycle] += 25
                                self.enemy4.polygon = self.enemy4.create_polygon(15,30,25,15,17,15,25,0,5,0,13,15,5,15,fill=Enemy4Color)
                        elif PlayersXpos[0] > Enemies4Xpos[cycle] and PlayersYpos[0] < Enemies4Ypos[cycle]:
                            self.enemy4.delete("all")
                            if rndDir == "X":
                                Enemies4Xpos[cycle] += 25
                                self.enemy4.polygon = self.enemy4.create_polygon(30,15,15,5,15,13,0,5,0,25,15,17,15,25,fill=Enemy4Color)
                            else:
                                Enemies4Ypos[cycle] -= 25
                                self.enemy4.polygon = self.enemy4.create_polygon(15,0,5,15,12,15,5,30,25,30,17,15,25,15,fill=Enemy4Color)
                        elif PlayersXpos[0] > Enemies4Xpos[cycle] and PlayersYpos[0] > Enemies4Ypos[cycle]:
                            self.enemy4.delete("all")
                            if rndDir == "X":
                                Enemies4Xpos[cycle] += 25
                                self.enemy4.polygon = self.enemy4.create_polygon(30,15,15,5,15,13,0,5,0,25,15,17,15,25,fill=Enemy4Color)
                            else:
                                Enemies4Ypos[cycle] += 25
                                self.enemy4.polygon = self.enemy4.create_polygon(15,30,25,15,17,15,25,0,5,0,13,15,5,15,fill=Enemy4Color)
                        elif PlayersXpos[0] < Enemies4Xpos[cycle] and PlayersYpos[0] == Enemies4Ypos[cycle]:
                            self.enemy4.delete("all")
                            self.enemy4.polygon = self.enemy4.create_polygon(0,15,15,25,15,17,30,25,30,5,15,13,15,5,fill=Enemy4Color)
                            Enemies4Xpos[cycle] -= 25
                        elif PlayersXpos[0] > Enemies4Xpos[cycle] and PlayersYpos[0] == Enemies4Ypos[cycle]:
                            self.enemy4.delete("all")
                            self.enemy4.polygon = self.enemy4.create_polygon(30,15,15,5,15,13,0,5,0,25,15,17,15,25,fill=Enemy4Color)
                            Enemies4Xpos[cycle] += 25
                        elif PlayersXpos[0] == Enemies4Xpos[cycle] and PlayersYpos[0] < Enemies4Ypos[cycle]:
                            self.enemy4.delete("all")
                            self.enemy4.polygon = self.enemy4.create_polygon(15,0,5,15,12,15,5,30,25,30,17,15,25,15,fill=Enemy4Color)
                            Enemies4Ypos[cycle] -= 25
                        elif PlayersXpos[0] == Enemies4Xpos[cycle] and PlayersYpos[0] > Enemies4Ypos[cycle]:
                            self.enemy4.delete("all")
                            self.enemy4.polygon = self.enemy4.create_polygon(15,30,25,15,17,15,25,0,5,0,13,15,5,15,fill=Enemy4Color)
                            Enemies4Ypos[cycle] += 25
                    else:
                        #Target Player 2
                        if PlayersXpos[1] < Enemies4Xpos[cycle] and PlayersYpos[1] < Enemies4Ypos[cycle]:
                            self.enemy4.delete("all")
                            if rndDir == "X":
                                Enemies4Xpos[cycle] -= 25
                                self.enemy4.polygon = self.enemy4.create_polygon(0,15,15,25,15,17,30,25,30,5,15,13,15,5,fill=Enemy4Color)
                            else:
                                Enemies4Ypos[cycle] -= 25
                                self.enemy4.polygon = self.enemy4.create_polygon(15,0,5,15,12,15,5,30,25,30,17,15,25,15,fill=Enemy4Color)
                        elif PlayersXpos[1] < Enemies4Xpos[cycle] and PlayersYpos[1] > Enemies4Ypos[cycle]:
                            self.enemy4.delete("all")
                            if rndDir == "X":
                                Enemies4Xpos[cycle] -= 25
                                self.enemy4.polygon = self.enemy4.create_polygon(0,15,15,25,15,17,30,25,30,5,15,13,15,5,fill=Enemy4Color)
                            else:
                                Enemies4Ypos[cycle] += 25
                                self.enemy4.polygon = self.enemy4.create_polygon(15,30,25,15,17,15,25,0,5,0,13,15,5,15,fill=Enemy4Color)
                        elif PlayersXpos[1] > Enemies4Xpos[cycle] and PlayersYpos[1] < Enemies4Ypos[cycle]:
                            self.enemy4.delete("all")
                            if rndDir == "X":
                                Enemies4Xpos[cycle] += 25
                                self.enemy4.polygon = self.enemy4.create_polygon(30,15,15,5,15,13,0,5,0,25,15,17,15,25,fill=Enemy4Color)
                            else:
                                Enemies4Ypos[cycle] -= 25
                                self.enemy4.polygon = self.enemy4.create_polygon(15,0,5,15,12,15,5,30,25,30,17,15,25,15,fill=Enemy4Color)
                        elif PlayersXpos[1] > Enemies4Xpos[cycle] and PlayersYpos[1] > Enemies4Ypos[cycle]:
                            self.enemy4.delete("all")
                            if rndDir == "X":
                                Enemies4Xpos[cycle] += 25
                                self.enemy4.polygon = self.enemy4.create_polygon(30,15,15,5,15,13,0,5,0,25,15,17,15,25,fill=Enemy4Color)
                            else:
                                Enemies4Ypos[cycle] += 25
                                self.enemy4.polygon = self.enemy4.create_polygon(15,30,25,15,17,15,25,0,5,0,13,15,5,15,fill=Enemy4Color)
                        elif PlayersXpos[1] < Enemies4Xpos[cycle] and PlayersYpos[1] == Enemies4Ypos[cycle]:
                            self.enemy4.delete("all")
                            self.enemy4.polygon = self.enemy4.create_polygon(0,15,15,25,15,17,30,25,30,5,15,13,15,5,fill=Enemy4Color)
                            Enemies4Xpos[cycle] -= 25
                        elif PlayersXpos[1] > Enemies4Xpos[cycle] and PlayersYpos[1] == Enemies4Ypos[cycle]:
                            self.enemy4.delete("all")
                            self.enemy4.polygon = self.enemy4.create_polygon(30,15,15,5,15,13,0,5,0,25,15,17,15,25,fill=Enemy4Color)
                            Enemies4Xpos[cycle] += 25
                        elif PlayersXpos[1] == Enemies4Xpos[cycle] and PlayersYpos[1] < Enemies4Ypos[cycle]:
                            self.enemy4.delete("all")
                            self.enemy4.polygon = self.enemy4.create_polygon(15,0,5,15,12,15,5,30,25,30,17,15,25,15,fill=Enemy4Color)
                            Enemies4Ypos[cycle] -= 25
                        elif PlayersXpos[1] == Enemies4Xpos[cycle] and PlayersYpos[1] > Enemies4Ypos[cycle]:
                            self.enemy4.delete("all")
                            self.enemy4.polygon = self.enemy4.create_polygon(15,30,25,15,17,15,25,0,5,0,13,15,5,15,fill=Enemy4Color)
                            Enemies4Ypos[cycle] += 25
                    self.enemy4.place(x=Enemies4Xpos[cycle],y=Enemies4Ypos[cycle])
                    for Pcycle in range(0,2):
                        if PlayersXpos[Pcycle] == Enemies4Xpos[cycle] and PlayersYpos[Pcycle] == Enemies4Ypos[cycle]:
                            GameOver()
                    cycle += 1

    def Enemy5Move():
        global Xpos
        global Ypos
        global gameover
        global created5
        if gameover != 1:
            self.after(500,Enemy5Move)
            if created5 == 1:
                cycle = 0
                for self.enemy5 in Enemies5:
                    if ((PlayersXpos[0] - Enemies5Xpos[cycle])**2 + (PlayersYpos[0] - Enemies5Ypos[cycle])**2)**0.5 <= ((PlayersXpos[1] - Enemies5Xpos[cycle])**2 + (PlayersYpos[1] - Enemies5Ypos[cycle])**2)**0.5:
                        #Target Player 1
                        if (Enemies5Wall[cycle] == "E" or Enemies5Wall[cycle] == "W") and PlayersYpos[0] < Enemies5Ypos[cycle]:
                            Enemies5Ypos[cycle] -= 25
                        elif (Enemies5Wall[cycle] == "E" or Enemies5Wall[cycle] == "W") and PlayersYpos[0] > Enemies5Ypos[cycle]:
                            Enemies5Ypos[cycle] += 25
                        elif PlayersXpos[0] < Enemies5Xpos[cycle] and (Enemies5Wall[cycle] == "N" or Enemies5Wall[cycle] == "S"):
                            Enemies5Xpos[cycle] -= 25
                        elif PlayersXpos[0] > Enemies5Xpos[cycle] and (Enemies5Wall[cycle] == "N" or Enemies5Wall[cycle] == "S"):
                            Enemies5Xpos[cycle] += 25
                    else:
                        #Target Player 2
                        if (Enemies5Wall[cycle] == "E" or Enemies5Wall[cycle] == "W") and PlayersYpos[1] < Enemies5Ypos[cycle]:
                            Enemies5Ypos[cycle] -= 25
                        elif (Enemies5Wall[cycle] == "E" or Enemies5Wall[cycle] == "W") and PlayersYpos[1] > Enemies5Ypos[cycle]:
                            Enemies5Ypos[cycle] += 25
                        elif PlayersXpos[1] < Enemies5Xpos[cycle] and (Enemies5Wall[cycle] == "N" or Enemies5Wall[cycle] == "S"):
                            Enemies5Xpos[cycle] -= 25
                        elif PlayersXpos[1] > Enemies5Xpos[cycle] and (Enemies5Wall[cycle] == "N" or Enemies5Wall[cycle] == "S"):
                            Enemies5Xpos[cycle] += 25
                    self.enemy5.place(x=Enemies5Xpos[cycle],y=Enemies5Ypos[cycle])
                    for Pcycle in range(0,2):
                        if PlayersXpos[Pcycle] == Enemies5Xpos[cycle] and PlayersYpos[Pcycle] == Enemies5Ypos[cycle]:
                            GameOver()
                    for Pcycle in range(0,2):
                        if Enemies5Wall[cycle] == "E" or Enemies5Wall[cycle] == "W":
                            if Enemies5Ypos[cycle] == PlayersYpos[Pcycle]:
                                enShoot()
                        else:
                            if Enemies5Xpos[cycle] == PlayersXpos[Pcycle]:
                                enShoot()
                    cycle += 1

    def Generate():
        global generated1
        global generated2
        global generated3
        global generated4
        if gameover != 1:
            self.after(10,Generate)
            if generated1 == 0:
                GenerateEnemy1()
                generated1 = 1000
            if generated2 == 0:
                GenerateEnemy2()
                generated2 = 1250
            if generated3 == 0:
                GenerateEnemy3()
                generated3 = 1500
            if generated4 == 0:
                GenerateEnemy4()
                generated4 = 1750
            generated1 -= 10
            generated2 -= 10
            generated3 -= 10
            generated4 -= 10

    def GenerateEnemy1():
        global enXpos
        global enYpos
        global Damage
        global created
        cycle = 0
        for self.enemy6 in Enemies6:
            if Enemies6Type[cycle] == 1:
                enXpos = Enemies6Xpos[cycle]
                enYpos = Enemies6Ypos[cycle]
                self.enemy = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
                self.enemy.place(x=enXpos,y=enYpos)
                self.enemy.polygon = self.enemy.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="darkviolet")
                Enemies.append(self.enemy)
                EnemiesDmg.append(Damage)
                EnemiesXpos.append(enXpos)
                EnemiesYpos.append(enYpos)
                created = 1
            cycle += 1

    def GenerateEnemy2():
        global en2Xpos
        global en2Ypos
        global created2
        cycle = 0
        for self.enemy6 in Enemies6:
            if Enemies6Type[cycle] == 2:
                en2Xpos = Enemies6Xpos[cycle]
                en2Ypos = Enemies6Ypos[cycle]
                self.enemy2 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
                self.enemy2.place(x=en2Xpos,y=en2Ypos)
                self.enemy2.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="red")
                Enemies2.append(self.enemy2)
                Enemies2Xpos.append(en2Xpos)
                Enemies2Ypos.append(en2Ypos)
                created2 = 1
            cycle += 1

    def GenerateEnemy3():
        global en3Xpos
        global en3Ypos
        global Damage3
        global created3
        cycle = 0
        for self.enemy6 in Enemies6:
            if Enemies6Type[cycle] == 3:
                en3Xpos = Enemies6Xpos[cycle]
                en3Ypos = Enemies6Ypos[cycle]
                self.enemy3 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
                self.enemy3.place(x=en3Xpos,y=en3Ypos)
                self.enemy3.polygon = self.enemy3.create_polygon(10,0,0,0,0,30,30,30,30,0,20,0,20,10,10,10,fill="navy")
                Enemies3.append(self.enemy3)
                Enemies3Dmg.append(Damage3)
                Enemies3Xpos.append(en3Xpos)
                Enemies3Ypos.append(en3Ypos)
                created3 = 1
            cycle += 1

    def GenerateEnemy4():
        global en4Xpos
        global en4Ypos
        global created4
        cycle = 0
        for self.enemy6 in Enemies6:
            if Enemies6Type[cycle] == 4:
                en4Xpos = Enemies6Xpos[cycle]
                en4Ypos = Enemies6Ypos[cycle]
                self.enemy4 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
                self.enemy4.place(x=en4Xpos,y=en4Ypos)
                self.enemy4.create_polygon(15,0,5,15,12,15,5,30,25,30,17,15,25,15,fill="darkgreen")
                Enemies4.append(self.enemy4)
                Enemies4Xpos.append(en4Xpos)
                Enemies4Ypos.append(en4Ypos)
                created4 = 1
            cycle += 1

    def Shoot(event):
        global Xpos
        global Ypos
        global direction
        global start
        if PlayersDir[0] == "N":
            shotXpos = PlayersXpos[0] + 10
            shotYpos = PlayersYpos[0] - 10
        elif PlayersDir[0] == "E":
            shotXpos = PlayersXpos[0] + 30
            shotYpos = PlayersYpos[0] + 10
        elif PlayersDir[0] == "S":
            shotXpos = PlayersXpos[0] + 10
            shotYpos = PlayersYpos[0] + 30
        elif PlayersDir[0] == "W":
            shotXpos = PlayersXpos[0] - 10
            shotYpos = PlayersYpos[0] + 10
        self.shot = Canvas(bg="black",highlightthickness=0,width=10,height=10)
        self.shot.place(x=shotXpos,y=shotYpos)
        self.shot.create_oval(0,0,10,10,fill="white")
        Shots.append(self.shot)
        ShotsXpos.append(shotXpos)
        ShotsYpos.append(shotYpos)
        ShotDir.append(PlayersDir[0])
        if start == 0:
            NextWave()
        start = 1

    def Shoot2(event):
        global start
        if PlayersDir[1] == "N":
            shotXpos = PlayersXpos[1] + 10
            shotYpos = PlayersYpos[1] - 10
        elif PlayersDir[1] == "E":
            shotXpos = PlayersXpos[1] + 30
            shotYpos = PlayersYpos[1] + 10
        elif PlayersDir[1] == "S":
            shotXpos = PlayersXpos[1] + 10
            shotYpos = PlayersYpos[1] + 30
        elif PlayersDir[1] == "W":
            shotXpos = PlayersXpos[1] - 10
            shotYpos = PlayersYpos[1] + 10
        self.shot = Canvas(bg="black",highlightthickness=0,width=10,height=10)
        self.shot.place(x=shotXpos,y=shotYpos)
        self.shot.create_oval(0,0,10,10,fill="white")
        Shots.append(self.shot)
        ShotsXpos.append(shotXpos)
        ShotsYpos.append(shotYpos)
        ShotDir.append(PlayersDir[1])
        if start == 0:
            NextWave()
        start = 1

    def enShoot():
        cycle = 0
        for self.enemy5 in Enemies5:
            if Enemies5Wall[cycle] == "N":
                enDir = "S"
                enShotXpos = Enemies5Xpos[cycle] + 10
                enShotYpos = Enemies5Ypos[cycle] + 30
            elif Enemies5Wall[cycle] == "E":
                enDir = "W"
                enShotXpos = Enemies5Xpos[cycle] - 10
                enShotYpos = Enemies5Ypos[cycle] + 10
            elif Enemies5Wall[cycle] == "S":
                enDir = "N"
                enShotXpos = Enemies5Xpos[cycle] + 10
                enShotYpos = Enemies5Ypos[cycle] - 10
            elif Enemies5Wall[cycle] == "W":
                enDir = "E"
                enShotXpos = Enemies5Xpos[cycle] + 30
                enShotYpos = Enemies5Ypos[cycle] + 10
            if Enemies5Wall[cycle] == "E" or Enemies5Wall[cycle] == "W":
                for Pcycle in range(0,2):
                    if Enemies5Ypos[cycle] == Ypos:
                        self.enShot = Canvas(bg="black",highlightthickness=0,width=10,height=10)
                        self.enShot.place(x=enShotXpos,y=enShotYpos)
                        self.enShot.create_oval(0,0,10,10,fill="yellow")
                        enShots.append(self.enShot)
                        enShotsXpos.append(enShotXpos)
                        enShotsYpos.append(enShotYpos)
                        enShotDir.append(enDir)
            else:
                for Pcycle in range(0,2):
                    if Enemies5Xpos[cycle] == Xpos:
                        self.enShot = Canvas(bg="black",highlightthickness=0,width=10,height=10)
                        self.enShot.place(x=enShotXpos,y=enShotYpos)
                        self.enShot.create_oval(0,0,10,10,fill="yellow")
                        enShots.append(self.enShot)
                        enShotsXpos.append(enShotXpos)
                        enShotsYpos.append(enShotYpos)
                        enShotDir.append(enDir)
            cycle += 1
            
    def ShotMove():
        global direction
        global en2Xpos
        global en2Ypos
        global destroy
        global gameover
        if gameover != 1:
            self.after(10,ShotMove)
            #Move Shots
            cycle = 0
            for self.shot in Shots:
                destroy = -1
                if ShotDir[cycle] == "N":
                    ShotsYpos[cycle] -= 10
                elif ShotDir[cycle] == "E":
                    ShotsXpos[cycle] += 10
                elif ShotDir[cycle] == "S":
                    ShotsYpos[cycle] += 10
                elif ShotDir[cycle] == "W":
                    ShotsXpos[cycle] -= 10
                self.shot.place(x=ShotsXpos[cycle],y=ShotsYpos[cycle])
                #Damage Enemy1
                enCycle = 0
                for self.enemy in Enemies:
                    if destroy == -1:
                        if EnemiesXpos[enCycle] + 30 >= ShotsXpos[cycle] >= EnemiesXpos[enCycle] - 10 and EnemiesYpos[enCycle] + 30 >= ShotsYpos[cycle] >= EnemiesYpos[enCycle] - 10:
                            destroy = 0
                            if EnemiesDmg[enCycle] == 1:
                                self.explode = Canvas(bg="black",highlightthickness=0,width=30,height=30)
                                self.explode.place(x=EnemiesXpos[enCycle],y=EnemiesYpos[enCycle])
                                self.explode.create_polygon(0,15,13,13,15,0,17,13,30,15,17,17,15,30,13,17,fill="orange")
                                Explosions.append(self.explode)
                                self.enemy.destroy()
                                del Enemies[enCycle]
                                del EnemiesDmg[enCycle]
                                del EnemiesXpos[enCycle]
                                del EnemiesYpos[enCycle]
                                self.after(10,destroyEnemy)
                                self.shot.destroy()
                                del Shots[cycle]
                                del ShotsXpos[cycle]
                                del ShotsYpos[cycle]
                                del ShotDir[cycle]
                            else:
                                self.shot.destroy()
                                del Shots[cycle]
                                del ShotsXpos[cycle]
                                del ShotsYpos[cycle]
                                del ShotDir[cycle]
                                EnemiesDmg[enCycle] += 1
                                if EnemiesDmg[enCycle] == 0:
                                    EnemyColor = "darkviolet"
                                else:
                                    EnemyColor = "violet"
                                self.enemy.itemconfig(self.enemy.polygon,fill=EnemyColor)
                        enCycle += 1
                #Damage Enemy2
                enCycle = 0
                for self.enemy2 in Enemies2:
                    if destroy == -1:
                        if Enemies2Xpos[enCycle] + 30 >= ShotsXpos[cycle] >= Enemies2Xpos[enCycle] - 10 and Enemies2Ypos[enCycle] + 30 >= ShotsYpos[cycle] >= Enemies2Ypos[enCycle] - 10:
                            destroy = 0
                            self.explode = Canvas(bg="black",highlightthickness=0,width=30,height=30)
                            self.explode.place(x=Enemies2Xpos[enCycle],y=Enemies2Ypos[enCycle])
                            self.explode.create_polygon(0,15,13,13,15,0,17,13,30,15,17,17,15,30,13,17,fill="orange")
                            Explosions.append(self.explode)
                            self.enemy2.destroy()
                            del Enemies2[enCycle]
                            del Enemies2Xpos[enCycle]
                            del Enemies2Ypos[enCycle]
                            self.shot.destroy()
                            del Shots[cycle]
                            del ShotsXpos[cycle]
                            del ShotsYpos[cycle]
                            del ShotDir[cycle]
                            self.after(10,destroyEnemy)
                        enCycle += 1
                #Damage Enemy3
                enCycle = 0
                for self.enemy3 in Enemies3:
                    if destroy == -1:
                        if Enemies3Xpos[enCycle] + 30 >= ShotsXpos[cycle] >= Enemies3Xpos[enCycle] - 10 and Enemies3Ypos[enCycle] + 30 >= ShotsYpos[cycle] >= Enemies3Ypos[enCycle] - 10:
                            destroy = 0
                            if Enemies3Dmg[enCycle] == 4:
                                self.explode = Canvas(bg="black",highlightthickness=0,width=30,height=30)
                                self.explode.place(x=Enemies3Xpos[enCycle],y=Enemies3Ypos[enCycle])
                                self.explode.create_polygon(0,15,13,13,15,0,17,13,30,15,17,17,15,30,13,17,fill="orange")
                                Explosions.append(self.explode)
                                self.enemy3.destroy()
                                del Enemies3[enCycle]
                                del Enemies3Dmg[enCycle]
                                del Enemies3Xpos[enCycle]
                                del Enemies3Ypos[enCycle]
                                self.after(10,destroyEnemy)
                                self.shot.destroy()
                                del Shots[cycle]
                                del ShotsXpos[cycle]
                                del ShotsYpos[cycle]
                                del ShotDir[cycle]
                            else:
                                self.shot.destroy()
                                del Shots[cycle]
                                del ShotsXpos[cycle]
                                del ShotsYpos[cycle]
                                del ShotDir[cycle]
                                Enemies3Dmg[enCycle] += 1
                                if Enemies3Dmg[enCycle] == 0:
                                    Enemy3Color = "navy"
                                elif Enemies3Dmg[enCycle] == 1:
                                    Enemy3Color = "darkblue"
                                elif Enemies3Dmg[enCycle] == 2:
                                    Enemy3Color = "dodgerblue"
                                elif Enemies3Dmg[enCycle] == 3:
                                    Enemy3Color = "deepskyblue"
                                else:
                                    Enemy3Color = "lightskyblue"
                                self.enemy3.itemconfig(self.enemy3.polygon,fill=Enemy3Color)
                        enCycle += 1
                #Damage Enemy4
                enCycle = 0
                for self.enemy4 in Enemies4:
                    if destroy == -1:
                        if Enemies4Xpos[enCycle] + 30 >= ShotsXpos[cycle] >= Enemies4Xpos[enCycle] - 10 and Enemies4Ypos[enCycle] + 30 >= ShotsYpos[cycle] >= Enemies4Ypos[enCycle] - 10:
                            destroy = 0
                            self.explode = Canvas(bg="black",highlightthickness=0,width=30,height=30)
                            self.explode.place(x=Enemies4Xpos[enCycle],y=Enemies4Ypos[enCycle])
                            self.explode.create_polygon(0,15,13,13,15,0,17,13,30,15,17,17,15,30,13,17,fill="orange")
                            Explosions.append(self.explode)
                            self.enemy4.destroy()
                            del Enemies4[enCycle]
                            del Enemies4Xpos[enCycle]
                            del Enemies4Ypos[enCycle]
                            self.shot.destroy()
                            del Shots[cycle]
                            del ShotsXpos[cycle]
                            del ShotsYpos[cycle]
                            del ShotDir[cycle]
                            self.after(10,destroyEnemy)
                        enCycle += 1
                #Damage Enemy5
                enCycle = 0
                for self.enemy5 in Enemies5:
                    if destroy == -1:
                        if Enemies5Xpos[enCycle] + 30 >= ShotsXpos[cycle] >= Enemies5Xpos[enCycle] - 10 and Enemies5Ypos[enCycle] + 30 >= ShotsYpos[cycle] >= Enemies5Ypos[enCycle] - 10:
                            destroy = 0
                            if Enemies5Dmg[enCycle] == 1:
                                self.explode = Canvas(bg="black",highlightthickness=0,width=30,height=30)
                                self.explode.place(x=Enemies5Xpos[enCycle],y=Enemies5Ypos[enCycle])
                                self.explode.create_polygon(0,15,13,13,15,0,17,13,30,15,17,17,15,30,13,17,fill="orange")
                                Explosions.append(self.explode)
                                self.enemy5.destroy()
                                del Enemies5[enCycle]
                                del Enemies5Dmg[enCycle]
                                del Enemies5Xpos[enCycle]
                                del Enemies5Ypos[enCycle]
                                del Enemies5Wall[enCycle]
                                self.after(10,destroyEnemy)
                                self.shot.destroy()
                                del Shots[cycle]
                                del ShotsXpos[cycle]
                                del ShotsYpos[cycle]
                                del ShotDir[cycle]
                            else:
                                self.shot.destroy()
                                del Shots[cycle]
                                del ShotsXpos[cycle]
                                del ShotsYpos[cycle]
                                del ShotDir[cycle]
                                Enemies5Dmg[enCycle] += 1
                                if Enemies5Dmg[enCycle] == 0:
                                    Enemy5Color = "darkorange2"
                                else:
                                    Enemy5Color = "orange"
                                self.enemy5.itemconfig(self.enemy5.polygon,fill=Enemy5Color)
                        enCycle += 1
                #Damage Enemy6
                enCycle = 0
                for self.enemy6 in Enemies6:
                    if destroy == -1:
                        if Enemies6Xpos[enCycle] + 30 >= ShotsXpos[cycle] >= Enemies6Xpos[enCycle] - 10 and Enemies6Ypos[enCycle] + 30 >= ShotsYpos[cycle] >= Enemies6Ypos[enCycle] - 10:
                            destroy = 0
                            if Enemies6Dmg[enCycle] == 5:
                                self.explode = Canvas(bg="black",highlightthickness=0,width=30,height=30)
                                self.explode.place(x=Enemies6Xpos[enCycle],y=Enemies6Ypos[enCycle])
                                self.explode.create_polygon(0,15,13,13,15,0,17,13,30,15,17,17,15,30,13,17,fill="orange")
                                Explosions.append(self.explode)
                                self.enemy6.destroy()
                                del Enemies6[enCycle]
                                del Enemies6Dmg[enCycle]
                                del Enemies6Xpos[enCycle]
                                del Enemies6Ypos[enCycle]
                                del Enemies6Type[enCycle]
                                self.after(10,destroyEnemy)
                                self.shot.destroy()
                                del Shots[cycle]
                                del ShotsXpos[cycle]
                                del ShotsYpos[cycle]
                                del ShotDir[cycle]
                            else:
                                self.shot.destroy()
                                del Shots[cycle]
                                del ShotsXpos[cycle]
                                del ShotsYpos[cycle]
                                del ShotDir[cycle]
                                Enemies6Dmg[enCycle] += 1
                                if Enemies6Dmg[enCycle] == 0:
                                    Enemy6Color = "gray20"
                                elif Enemies6Dmg[enCycle] == 1:
                                    Enemy6Color = "gray30"
                                elif Enemies6Dmg[enCycle] == 2:
                                    Enemy6Color = "gray40"
                                elif Enemies6Dmg[enCycle] == 3:
                                    Enemy6Color = "gray50"
                                elif Enemies6Dmg[enCycle] == 4:
                                    Enemy6Color = "gray60"
                                elif Enemies6Dmg[enCycle] == 5:
                                    Enemy6Color = "gray70"
                                self.enemy6.itemconfig(self.enemy6.oval,fill=Enemy6Color)
                        enCycle += 1
                #Destroy Shot at Boundary
                if destroy == -1:
                    if ShotsXpos[cycle] < 0 or ShotsXpos[cycle] > 830 or ShotsYpos[cycle] < 0 or ShotsYpos[cycle] > 680:
                        self.shot.destroy()
                        del Shots[cycle]
                        del ShotsXpos[cycle]
                        del ShotsYpos[cycle]
                        del ShotDir[cycle]
                cycle += 1

    def enShotMove():
        global gameover
        if gameover != 1:
            self.after(10,enShotMove)
            cycle = 0
            for self.enShot in enShots:
                enDestroy = -1
                if enShotDir[cycle] == "N":
                    enShotsYpos[cycle] -= 10
                elif enShotDir[cycle] == "E":
                    enShotsXpos[cycle] += 10
                elif enShotDir[cycle] == "S":
                    enShotsYpos[cycle] += 10
                elif enShotDir[cycle] == "W":
                    enShotsXpos[cycle] -= 10
                self.enShot.place(x=enShotsXpos[cycle],y=enShotsYpos[cycle])
                #Game Over
                for Pcycle in range(0,2):
                    if gameover != 1:
                        if PlayersXpos[Pcycle] + 30 >= enShotsXpos[cycle] >= PlayersXpos[Pcycle] - 10 and PlayersYpos[Pcycle] + 30 >= enShotsYpos[cycle] >= PlayersYpos[Pcycle] - 10:
                            enDestroy = 0
                            self.enShot.destroy()
                            del enShots[cycle]
                            del enShotsXpos[cycle]
                            del enShotsYpos[cycle]
                            del enShotDir[cycle]
                            GameOver()
                #Destroy Shot at Boundary
                if enDestroy == -1:
                    if enShotsXpos[cycle] < 0 or enShotsXpos[cycle] > 830 or enShotsYpos[cycle] < 0 or enShotsYpos[cycle] > 680:
                        self.enShot.destroy()
                        del enShots[cycle]
                        del enShotsXpos[cycle]
                        del enShotsYpos[cycle]
                        del enShotDir[cycle] 
                cycle += 1

    def destroyEnemy():
        destroyed = 0
        for self.explode in Explosions:
            self.explode.destroy()
            del Explosions[destroyed]
            destroyed += 1            

    def Summon():
        global wave
        global summoned
        time = 0
        wave += 1
        #Wave 1
        if wave == 1:
            E = 0
            while E < 3:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
        #Wave 2
        elif wave == 2:
            E = 0
            while E < 3:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
        #Wave 3
        elif wave == 3:
            E = 0
            while E < 2:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < 2:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
        #Wave 4
        elif wave == 4:
            E = 0
            while E < 4:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < 2:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
        #Wave 5
        elif wave == 5:
            E = 0
            while E < 3:
                self.after(time,CreateEnemy3)
                E += 1
                time += 250
        #Wave 6
        elif wave == 6:
            E = 0
            while E < 2:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < 1:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < 3:
                self.after(time,CreateEnemy3)
                E += 1
                time += 250
        #Wave 7
        elif wave == 7:
            E = 0
            while E < 3:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < 2:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
            E = 0
            while E < 2:
                self.after(time,CreateEnemy3)
                E += 1
                time += 250
        #Wave 8
        elif wave == 8:
            E = 0
            while E < 2:
                self.after(time,CreateEnemy4)
                E += 1
                time += 250
        #Wave 9
        elif wave == 9:
            E = 0
            while E < 3:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < 2:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
            E = 0
            while E < 2:
                self.after(time,CreateEnemy4)
                E += 1
                time += 250
        #Wave 10
        elif wave == 10:
            E = 0
            while E < 3:
                self.after(time,CreateEnemy3)
                E += 1
                time += 250
            E = 0
            while E < 2:
                self.after(time,CreateEnemy4)
                E += 1
                time += 250
        #Wave 11
        elif wave == 11:
            E = 0
            while E < 2:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < 2:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
            E = 0
            while E < 1:
                self.after(time,CreateEnemy3)
                E += 1
                time += 250
            E = 0
            while E < 1:
                self.after(time,CreateEnemy4)
                E += 1
                time += 250
        #Wave 12
        elif wave == 12:
            E = 0
            while E < 2:
                self.after(time,CreateEnemy5)
                E += 1
                time += 250
        #Wave 13
        elif wave == 13:
            E = 0
            while E < 3:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < 2:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
            E = 0
            while E < 1:
                self.after(time,CreateEnemy3)
                E += 1
                time += 250
            E = 0
            while E < 1:
                self.after(time,CreateEnemy5)
                E += 1
                time += 250
        #Wave 14
        elif wave == 14:
            E = 0
            while E < 4:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < 1:
                self.after(time,CreateEnemy4)
                E += 1
                time += 250
            E = 0
            while E < 2:
                self.after(time,CreateEnemy5)
                E += 1
                time += 250
        #Wave 15
        elif wave == 15:
            E = 0
            while E < 2:
                self.after(time,CreateEnemy6)
                E += 1
                time += 250
        #Wave 16
        elif wave == 16:
            E = 0
            while E < 3:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < 2:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
            E = 0
            while E < 1:
                self.after(time,CreateEnemy6)
                E += 1
                time += 250
        #Wave 17
        elif wave == 17:
            E = 0
            while E < 1:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < 1:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
            E = 0
            while E < 1:
                self.after(time,CreateEnemy3)
                E += 1
                time += 250
            E = 0
            while E < 1:
                self.after(time,CreateEnemy4)
                E += 1
                time += 250
            E = 0
            while E < 1:
                self.after(time,CreateEnemy5)
                E += 1
                time += 250
            E = 0
            while E < 1:
                self.after(time,CreateEnemy6)
                E += 1
                time += 250
        #Wave 18+
        elif wave >= 18:
            E = 0
            while E < wave - 12:
                rndEnemy = random.choice([1,2,3,4,5,6])
                if rndEnemy == 1:
                    self.after(time,CreateEnemy)
                elif rndEnemy == 2:
                    self.after(time,CreateEnemy2)
                elif rndEnemy == 3:
                    self.after(time,CreateEnemy3)
                elif rndEnemy == 4:
                    self.after(time,CreateEnemy4)
                elif rndEnemy == 5:
                    self.after(time,CreateEnemy5)
                elif rndEnemy == 6:
                    self.after(time,CreateEnemy6)
                E += 1
                time += 250
        summoned = 0

    def NextWave():
        global wave
        global summoned
        global waveTime
        global pace
        global gameover
        if gameover == 0:
            self.after(10,NextWave)
            if summoned == 0:
                summoned = 1
                waveTime = pace
            if waveTime <= 0:
                Summon()
            if not Enemies and not Enemies2 and not Enemies3 and not Enemies4 and not Enemies5 and not Enemies6:
                Summon()
            waveTime -= 10
            self.lbScore.config(text="Wave: "+str(wave)+"  Next Wave: "+str(waveTime/1000)+"sec  Press 'p' to pause")

    def GameOver():
        global gameover
        global wave
        if gameover == 0:
            gameover = 1
            self.unbind('<Left>')
            self.unbind('<Right>')
            self.unbind('<Up>')
            self.unbind('<Down>')
            self.unbind('<space>')
            self.after_cancel(EnemyMove)
            self.after_cancel(Enemy2Move)
            self.after_cancel(Enemy3Move)
            self.after_cancel(Enemy4Move)
            self.after_cancel(Enemy5Move)
            self.after_cancel(CreateEnemy)
            self.after_cancel(CreateEnemy2)
            self.after_cancel(CreateEnemy3)
            self.after_cancel(CreateEnemy4)
            self.after_cancel(CreateEnemy5)
            self.after_cancel(CreateEnemy6)
            self.after_cancel(Generate)
            self.after_cancel(NextWave)
            self.after_cancel(ShotMove)
            self.after_cancel(enShotMove)
            for self.shot in Shots:
                self.shot.destroy()
            self.lbScore.destroy()
            self.lbGameOver = Label(text="Game Over" + "\n" "You survived to wave " + str(wave) + "\n" + "Click here to restart",bg="black",fg="white")
            self.lbGameOver.pack(fill=BOTH,expand=1)
            self.lbGameOver.bind('<Button>',Restart)
            self.btnMainMenu = Button(text="Main Menu")
            self.btnMainMenu.pack(side=LEFT)
            self.btnMainMenu.bind('<Button>',StartMainMenu)

    def Restart(event):
        self.destroy()
        MultiPlayer()

    def Pause(event):
        global pause
        global gameover
        global waveTime
        if pause == 0:
            gameover = 1
            pause = 1
            self.unbind('<Left>')
            self.unbind('<Right>')
            self.unbind('<Up>')
            self.unbind('<Down>')
            self.unbind('<space>')
            self.after_cancel(EnemyMove)
            self.after_cancel(Enemy2Move)
            self.after_cancel(Enemy3Move)
            self.after_cancel(Enemy4Move)
            self.after_cancel(Enemy5Move)
            self.after_cancel(CreateEnemy)
            self.after_cancel(CreateEnemy2)
            self.after_cancel(CreateEnemy3)
            self.after_cancel(CreateEnemy4)
            self.after_cancel(CreateEnemy5)
            self.after_cancel(CreateEnemy6)
            self.after_cancel(Generate)
            self.after_cancel(NextWave)
            self.after_cancel(ShotMove)
            self.after_cancel(enShotMove)
            for self.shot in Shots:
                self.shot.destroy()
            self.lbScore.destroy()
            self.lbPause = Label(text="Paused"+"\n"+"Press 'p' to Unpause",bg="black",fg="white")
            self.lbPause.pack(fill=BOTH,expand=1)
            self.btnMainMenu = Button(text="Main Menu")
            self.btnMainMenu.pack(side=LEFT)
            self.btnMainMenu.bind('<Button>',StartMainMenu)
        elif pause == 1:
            gameover = 0
            pause = 0
            self.bind('<Left>',LeftKey)
            self.bind('<Right>',RightKey)
            self.bind('<Up>',UpKey)
            self.bind('<Down>',DownKey)
            self.bind('<space>',Shoot)
            EnemyMove()
            Enemy2Move()
            Enemy3Move()
            Enemy4Move()
            Enemy5Move()
            Generate()
            ShotMove()
            enShotMove()
            self.lbScore = Label(text="Wave: "+str(wave)+"  Next Wave: "+str(waveTime/1000)+"sec  Press 'p' to pause",bg="black",fg="white")
            self.lbScore.place(x=165,y=680,width=500,height=20)
            NextWave()
            self.lbPause.destroy()
            self.btnMainMenu.unbind('<Button>')
            self.btnMainMenu.destroy()

    def Exit(event):
        self.destroy()

    def StartMainMenu(event):
        self.destroy()
        MainMenu()

    #Bindings
    self.bind('<Left>',LeftKey)
    self.bind('<Right>',RightKey)
    self.bind('<Up>',UpKey)
    self.bind('<Down>',DownKey)
    self.bind('<a>',AKey)
    self.bind('<d>',DKey)
    self.bind('<w>',WKey)
    self.bind('<s>',SKey)
    self.bind('<Escape>',Exit)
    self.bind('<space>',Shoot)
    self.bind('<Tab>',Shoot2)
    self.bind('<p>',Pause)

    EnemyMove()
    Enemy2Move()
    Enemy3Move()
    Enemy4Move()
    Enemy5Move()
    Generate()
    ShotMove()
    enShotMove()
        
    #Frame settings
    self.geometry("830x700")
    self.title("Space Assault")
    self.configure(bg="black")

def TenWaveChallengeSinglePlayerChooseEnemies():
    self = Tk()

    #Variables
    global W1E1
    global W1E2
    global W1E3
    global W1E4
    global W1E5
    global W1E6
    global W2E1
    global W2E2
    global W2E3
    global W2E4
    global W2E5
    global W2E6
    global W3E1
    global W3E2
    global W3E3
    global W3E4
    global W3E5
    global W3E6
    global W4E1
    global W4E2
    global W4E3
    global W4E4
    global W4E5
    global W4E6
    global W5E1
    global W5E2
    global W5E3
    global W5E4
    global W5E5
    global W5E6
    global W6E1
    global W6E2
    global W6E3
    global W6E4
    global W6E5
    global W6E6
    global W7E1
    global W7E2
    global W7E3
    global W7E4
    global W7E5
    global W7E6
    global W8E1
    global W8E2
    global W8E3
    global W8E4
    global W8E5
    global W8E6
    global W9E1
    global W9E2
    global W9E3
    global W9E4
    global W9E5
    global W9E6
    global W10E1
    global W10E2
    global W10E3
    global W10E4
    global W10E5
    global W10E6
    W1E1 = 0
    W1E2 = 0
    W1E3 = 0
    W1E4 = 0
    W1E5 = 0
    W1E6 = 0
    W2E1 = 0
    W2E2 = 0
    W2E3 = 0
    W2E4 = 0
    W2E5 = 0
    W2E6 = 0
    W3E1 = 0
    W3E2 = 0
    W3E3 = 0
    W3E4 = 0
    W3E5 = 0
    W3E6 = 0
    W4E1 = 0
    W4E2 = 0
    W4E3 = 0
    W4E4 = 0
    W4E5 = 0
    W4E6 = 0
    W5E1 = 0
    W5E2 = 0
    W5E3 = 0
    W5E4 = 0
    W5E5 = 0
    W5E6 = 0
    W6E1 = 0
    W6E2 = 0
    W6E3 = 0
    W6E4 = 0
    W6E5 = 0
    W6E6 = 0
    W7E1 = 0
    W7E2 = 0
    W7E3 = 0
    W7E4 = 0
    W7E5 = 0
    W7E6 = 0
    W8E1 = 0
    W8E2 = 0
    W8E3 = 0
    W8E4 = 0
    W8E5 = 0
    W8E6 = 0
    W9E1 = 0
    W9E2 = 0
    W9E3 = 0
    W9E4 = 0
    W9E5 = 0
    W9E6 = 0
    W10E1 = 0
    W10E2 = 0
    W10E3 = 0
    W10E4 = 0
    W10E5 = 0
    W10E6 = 0

    #Objects
    self.lbDirections = Label(text="Choose what enemies are in each wave",bg="black",fg="white")
    self.lbDirections.pack()
    self.btnMainMenu = Button(text="Main Menu")
    self.btnMainMenu.place(x=0,y=680,width=100,height=20)
    self.lbWave1 = Label(text="Wave 1",bg="black",fg="white")
    self.lbWave1.place(x=115,y=680,width=60,height=20)
    self.lbWave2 = Label(text="Wave 2",bg="black",fg="white")
    self.lbWave2.place(x=175,y=680,width=60,height=20)
    self.lbWave3 = Label(text="Wave 3",bg="black",fg="white")
    self.lbWave3.place(x=235,y=680,width=60,height=20)
    self.lbWave4 = Label(text="Wave 4",bg="black",fg="white")
    self.lbWave4.place(x=295,y=680,width=60,height=20)
    self.lbWave5 = Label(text="Wave 5",bg="black",fg="white")
    self.lbWave5.place(x=355,y=680,width=60,height=20)
    self.lbWave6 = Label(text="Wave 6",bg="black",fg="white")
    self.lbWave6.place(x=415,y=680,width=60,height=20)
    self.lbWave7 = Label(text="Wave 7",bg="black",fg="white")
    self.lbWave7.place(x=475,y=680,width=60,height=20)
    self.lbWave8 = Label(text="Wave 8",bg="black",fg="white")
    self.lbWave8.place(x=535,y=680,width=60,height=20)
    self.lbWave9 = Label(text="Wave 9",bg="black",fg="white")
    self.lbWave9.place(x=595,y=680,width=60,height=20)
    self.lbWave10 = Label(text="Wave 10",bg="black",fg="white")
    self.lbWave10.place(x=655,y=680,width=60,height=20)
    self.btnPlaySinglePlayer = Button(text="Play")
    self.btnPlaySinglePlayer.place(x=730,y=680,width=100,height=20)
    self.enemy1Up = Canvas(bg="black",highlightthickness=0)
    self.enemy1Up.place(x=90,y=300,width=30,height=30)
    self.enemy1Up.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="darkviolet")
    self.enemy1num = Label(text="0",bg="black",fg="white")
    self.enemy1num.place(x=90,y=330,width=30,height=20)
    self.enemy1Down = Canvas(bg="black",highlightthickness=0)
    self.enemy1Down.place(x=90,y=350,width=30,height=30)
    self.enemy1Down.create_polygon(15,30,30,0,15,15,0,0,15,30,fill="darkviolet")
    self.enemy2Up = Canvas(bg="black",highlightthickness=0)
    self.enemy2Up.place(x=210,y=300,width=30,height=30)
    self.enemy2Up.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="red")
    self.enemy2num = Label(text="0",bg="black",fg="white")
    self.enemy2num.place(x=210,y=330,width=30,height=20)
    self.enemy2Down = Canvas(bg="black",highlightthickness=0)
    self.enemy2Down.place(x=210,y=350,width=30,height=30)
    self.enemy2Down.create_polygon(15,30,30,0,15,15,0,0,15,30,fill="red")
    self.enemy3Up = Canvas(bg="black",highlightthickness=0)
    self.enemy3Up.place(x=330,y=300,width=30,height=30)
    self.enemy3Up.create_polygon(10,0,0,0,0,30,30,30,30,0,20,0,20,10,10,10,fill="navy")
    self.enemy3num = Label(text="0",bg="black",fg="white")
    self.enemy3num.place(x=330,y=330,width=30,height=20)
    self.enemy3Down = Canvas(bg="black",highlightthickness=0)
    self.enemy3Down.place(x=330,y=350,width=30,height=30)
    self.enemy3Down.create_polygon(20,30,30,30,30,0,0,0,0,30,10,30,10,20,20,20,fill="navy")
    self.enemy4Up = Canvas(bg="black",highlightthickness=0)
    self.enemy4Up.place(x=450,y=300,width=30,height=30)
    self.enemy4Up.create_polygon(15,0,5,15,12,15,5,30,25,30,17,15,25,15,fill="darkgreen")
    self.enemy4num = Label(text="0",bg="black",fg="white")
    self.enemy4num.place(x=450,y=330,width=30,height=20)
    self.enemy4Down = Canvas(bg="black",highlightthickness=0)
    self.enemy4Down.place(x=450,y=350,width=30,height=30)
    self.enemy4Down.create_polygon(15,30,25,15,17,15,25,0,5,0,13,15,5,15,fill="darkgreen")
    self.enemy5Up = Canvas(bg="black",highlightthickness=0)
    self.enemy5Up.place(x=570,y=300,width=30,height=30)
    self.enemy5Up.create_polygon(30,30,20,15,20,0,10,0,10,15,0,30,fill="darkorange2")
    self.enemy5num = Label(text="0",bg="black",fg="white")
    self.enemy5num.place(x=570,y=330,width=30,height=20)
    self.enemy5Down = Canvas(bg="black",highlightthickness=0)
    self.enemy5Down.place(x=570,y=350,width=30,height=30)
    self.enemy5Down.create_polygon(0,0,10,15,10,30,20,30,20,15,30,0,fill="darkorange2")
    self.enemy6Up = Canvas(bg="black",highlightthickness=0)
    self.enemy6Up.place(x=690,y=300,width=30,height=30)
    self.enemy6Up.create_oval(0,0,30,30,fill="gray20")
    self.enemy6num = Label(text="0",bg="black",fg="white")
    self.enemy6num.place(x=690,y=330,width=30,height=20)
    self.enemy6Down = Canvas(bg="black",highlightthickness=0)
    self.enemy6Down.place(x=690,y=350,width=30,height=30)
    self.enemy6Down.create_oval(0,0,30,30,fill="gray20")
    
    #Functions
    def StartMainMenu(event):
        self.destroy()
        MainMenu()

    def Wave1(*args):
        global W1E1
        global W1E2
        global W1E3
        global W1E4
        global W1E5
        global W1E6
        self.lbWave1.config(bg="darkblue")
        self.lbWave2.config(bg="black")
        self.lbWave3.config(bg="black")
        self.lbWave4.config(bg="black")
        self.lbWave5.config(bg="black")
        self.lbWave6.config(bg="black")
        self.lbWave7.config(bg="black")
        self.lbWave8.config(bg="black")
        self.lbWave9.config(bg="black")
        self.lbWave10.config(bg="black")
        self.enemy1Up.unbind('<Button>')
        self.enemy2Up.unbind('<Button>')
        self.enemy3Up.unbind('<Button>')
        self.enemy4Up.unbind('<Button>')
        self.enemy5Up.unbind('<Button>')
        self.enemy6Up.unbind('<Button>')
        self.enemy1Down.unbind('<Button>')
        self.enemy2Down.unbind('<Button>')
        self.enemy3Down.unbind('<Button>')
        self.enemy4Down.unbind('<Button>')
        self.enemy5Down.unbind('<Button>')
        self.enemy6Down.unbind('<Button>')
        self.enemy1Up.bind('<Button>',W1E1Up)
        self.enemy2Up.bind('<Button>',W1E2Up)
        self.enemy3Up.bind('<Button>',W1E3Up)
        self.enemy4Up.bind('<Button>',W1E4Up)
        self.enemy5Up.bind('<Button>',W1E5Up)
        self.enemy6Up.bind('<Button>',W1E6Up)
        self.enemy1Down.bind('<Button>',W1E1Down)
        self.enemy2Down.bind('<Button>',W1E2Down)
        self.enemy3Down.bind('<Button>',W1E3Down)
        self.enemy4Down.bind('<Button>',W1E4Down)
        self.enemy5Down.bind('<Button>',W1E5Down)
        self.enemy6Down.bind('<Button>',W1E6Down)
        self.enemy1num.config(text=str(W1E1))
        self.enemy2num.config(text=str(W1E2))
        self.enemy3num.config(text=str(W1E3))
        self.enemy4num.config(text=str(W1E4))
        self.enemy5num.config(text=str(W1E5))
        self.enemy6num.config(text=str(W1E6))
        
    def Wave2(event):
        global W2E1
        global W2E2
        global W2E3
        global W2E4
        global W2E5
        global W2E6
        self.lbWave1.config(bg="black")
        self.lbWave2.config(bg="darkblue")
        self.lbWave3.config(bg="black")
        self.lbWave4.config(bg="black")
        self.lbWave5.config(bg="black")
        self.lbWave6.config(bg="black")
        self.lbWave7.config(bg="black")
        self.lbWave8.config(bg="black")
        self.lbWave9.config(bg="black")
        self.lbWave10.config(bg="black")
        self.enemy1Up.unbind('<Button>')
        self.enemy2Up.unbind('<Button>')
        self.enemy3Up.unbind('<Button>')
        self.enemy4Up.unbind('<Button>')
        self.enemy5Up.unbind('<Button>')
        self.enemy6Up.unbind('<Button>')
        self.enemy1Down.unbind('<Button>')
        self.enemy2Down.unbind('<Button>')
        self.enemy3Down.unbind('<Button>')
        self.enemy4Down.unbind('<Button>')
        self.enemy5Down.unbind('<Button>')
        self.enemy6Down.unbind('<Button>')
        self.enemy1Up.bind('<Button>',W2E1Up)
        self.enemy2Up.bind('<Button>',W2E2Up)
        self.enemy3Up.bind('<Button>',W2E3Up)
        self.enemy4Up.bind('<Button>',W2E4Up)
        self.enemy5Up.bind('<Button>',W2E5Up)
        self.enemy6Up.bind('<Button>',W2E6Up)
        self.enemy1Down.bind('<Button>',W2E1Down)
        self.enemy2Down.bind('<Button>',W2E2Down)
        self.enemy3Down.bind('<Button>',W2E3Down)
        self.enemy4Down.bind('<Button>',W2E4Down)
        self.enemy5Down.bind('<Button>',W2E5Down)
        self.enemy6Down.bind('<Button>',W2E6Down)
        self.enemy1num.config(text=str(W2E1))
        self.enemy2num.config(text=str(W2E2))
        self.enemy3num.config(text=str(W2E3))
        self.enemy4num.config(text=str(W2E4))
        self.enemy5num.config(text=str(W2E5))
        self.enemy6num.config(text=str(W2E6))

    def Wave3(event):
        global W3E1
        global W3E2
        global W3E3
        global W3E4
        global W3E5
        global W3E6
        self.lbWave1.config(bg="black")
        self.lbWave2.config(bg="black")
        self.lbWave3.config(bg="darkblue")
        self.lbWave4.config(bg="black")
        self.lbWave5.config(bg="black")
        self.lbWave6.config(bg="black")
        self.lbWave7.config(bg="black")
        self.lbWave8.config(bg="black")
        self.lbWave9.config(bg="black")
        self.lbWave10.config(bg="black")
        self.enemy1Up.unbind('<Button>')
        self.enemy2Up.unbind('<Button>')
        self.enemy3Up.unbind('<Button>')
        self.enemy4Up.unbind('<Button>')
        self.enemy5Up.unbind('<Button>')
        self.enemy6Up.unbind('<Button>')
        self.enemy1Down.unbind('<Button>')
        self.enemy2Down.unbind('<Button>')
        self.enemy3Down.unbind('<Button>')
        self.enemy4Down.unbind('<Button>')
        self.enemy5Down.unbind('<Button>')
        self.enemy6Down.unbind('<Button>')
        self.enemy1Up.bind('<Button>',W3E1Up)
        self.enemy2Up.bind('<Button>',W3E2Up)
        self.enemy3Up.bind('<Button>',W3E3Up)
        self.enemy4Up.bind('<Button>',W3E4Up)
        self.enemy5Up.bind('<Button>',W3E5Up)
        self.enemy6Up.bind('<Button>',W3E6Up)
        self.enemy1Down.bind('<Button>',W3E1Down)
        self.enemy2Down.bind('<Button>',W3E2Down)
        self.enemy3Down.bind('<Button>',W3E3Down)
        self.enemy4Down.bind('<Button>',W3E4Down)
        self.enemy5Down.bind('<Button>',W3E5Down)
        self.enemy6Down.bind('<Button>',W3E6Down)
        self.enemy1num.config(text=str(W3E1))
        self.enemy2num.config(text=str(W3E2))
        self.enemy3num.config(text=str(W3E3))
        self.enemy4num.config(text=str(W3E4))
        self.enemy5num.config(text=str(W3E5))
        self.enemy6num.config(text=str(W3E6))
    
    def Wave4(event):
        global W4E1
        global W4E2
        global W4E3
        global W4E4
        global W4E5
        global W4E6
        self.lbWave1.config(bg="black")
        self.lbWave2.config(bg="black")
        self.lbWave3.config(bg="black")
        self.lbWave4.config(bg="darkblue")
        self.lbWave5.config(bg="black")
        self.lbWave6.config(bg="black")
        self.lbWave7.config(bg="black")
        self.lbWave8.config(bg="black")
        self.lbWave9.config(bg="black")
        self.lbWave10.config(bg="black")
        self.enemy1Up.unbind('<Button>')
        self.enemy2Up.unbind('<Button>')
        self.enemy3Up.unbind('<Button>')
        self.enemy4Up.unbind('<Button>')
        self.enemy5Up.unbind('<Button>')
        self.enemy6Up.unbind('<Button>')
        self.enemy1Down.unbind('<Button>')
        self.enemy2Down.unbind('<Button>')
        self.enemy3Down.unbind('<Button>')
        self.enemy4Down.unbind('<Button>')
        self.enemy5Down.unbind('<Button>')
        self.enemy6Down.unbind('<Button>')
        self.enemy1Up.bind('<Button>',W4E1Up)
        self.enemy2Up.bind('<Button>',W4E2Up)
        self.enemy3Up.bind('<Button>',W4E3Up)
        self.enemy4Up.bind('<Button>',W4E4Up)
        self.enemy5Up.bind('<Button>',W4E5Up)
        self.enemy6Up.bind('<Button>',W4E6Up)
        self.enemy1Down.bind('<Button>',W4E1Down)
        self.enemy2Down.bind('<Button>',W4E2Down)
        self.enemy3Down.bind('<Button>',W4E3Down)
        self.enemy4Down.bind('<Button>',W4E4Down)
        self.enemy5Down.bind('<Button>',W4E5Down)
        self.enemy6Down.bind('<Button>',W4E6Down)
        self.enemy1num.config(text=str(W4E1))
        self.enemy2num.config(text=str(W4E2))
        self.enemy3num.config(text=str(W4E3))
        self.enemy4num.config(text=str(W4E4))
        self.enemy5num.config(text=str(W4E5))
        self.enemy6num.config(text=str(W4E6))

    def Wave5(event):
        global W5E1
        global W5E2
        global W5E3
        global W5E4
        global W5E5
        global W5E6
        self.lbWave1.config(bg="black")
        self.lbWave2.config(bg="black")
        self.lbWave3.config(bg="black")
        self.lbWave4.config(bg="black")
        self.lbWave5.config(bg="darkblue")
        self.lbWave6.config(bg="black")
        self.lbWave7.config(bg="black")
        self.lbWave8.config(bg="black")
        self.lbWave9.config(bg="black")
        self.lbWave10.config(bg="black")
        self.enemy1Up.unbind('<Button>')
        self.enemy2Up.unbind('<Button>')
        self.enemy3Up.unbind('<Button>')
        self.enemy4Up.unbind('<Button>')
        self.enemy5Up.unbind('<Button>')
        self.enemy6Up.unbind('<Button>')
        self.enemy1Down.unbind('<Button>')
        self.enemy2Down.unbind('<Button>')
        self.enemy3Down.unbind('<Button>')
        self.enemy4Down.unbind('<Button>')
        self.enemy5Down.unbind('<Button>')
        self.enemy6Down.unbind('<Button>')
        self.enemy1Up.bind('<Button>',W5E1Up)
        self.enemy2Up.bind('<Button>',W5E2Up)
        self.enemy3Up.bind('<Button>',W5E3Up)
        self.enemy4Up.bind('<Button>',W5E4Up)
        self.enemy5Up.bind('<Button>',W5E5Up)
        self.enemy6Up.bind('<Button>',W5E6Up)
        self.enemy1Down.bind('<Button>',W5E1Down)
        self.enemy2Down.bind('<Button>',W5E2Down)
        self.enemy3Down.bind('<Button>',W5E3Down)
        self.enemy4Down.bind('<Button>',W5E4Down)
        self.enemy5Down.bind('<Button>',W5E5Down)
        self.enemy6Down.bind('<Button>',W5E6Down)
        self.enemy1num.config(text=str(W5E1))
        self.enemy2num.config(text=str(W5E2))
        self.enemy3num.config(text=str(W5E3))
        self.enemy4num.config(text=str(W5E4))
        self.enemy5num.config(text=str(W5E5))
        self.enemy6num.config(text=str(W5E6))
    
    def Wave6(event):
        global W6E1
        global W6E2
        global W6E3
        global W6E4
        global W6E5
        global W6E6
        self.lbWave1.config(bg="black")
        self.lbWave2.config(bg="black")
        self.lbWave3.config(bg="black")
        self.lbWave4.config(bg="black")
        self.lbWave5.config(bg="black")
        self.lbWave6.config(bg="darkblue")
        self.lbWave7.config(bg="black")
        self.lbWave8.config(bg="black")
        self.lbWave9.config(bg="black")
        self.lbWave10.config(bg="black")
        self.enemy1Up.unbind('<Button>')
        self.enemy2Up.unbind('<Button>')
        self.enemy3Up.unbind('<Button>')
        self.enemy4Up.unbind('<Button>')
        self.enemy5Up.unbind('<Button>')
        self.enemy6Up.unbind('<Button>')
        self.enemy1Down.unbind('<Button>')
        self.enemy2Down.unbind('<Button>')
        self.enemy3Down.unbind('<Button>')
        self.enemy4Down.unbind('<Button>')
        self.enemy5Down.unbind('<Button>')
        self.enemy6Down.unbind('<Button>')
        self.enemy1Up.bind('<Button>',W6E1Up)
        self.enemy2Up.bind('<Button>',W6E2Up)
        self.enemy3Up.bind('<Button>',W6E3Up)
        self.enemy4Up.bind('<Button>',W6E4Up)
        self.enemy5Up.bind('<Button>',W6E5Up)
        self.enemy6Up.bind('<Button>',W6E6Up)
        self.enemy1Down.bind('<Button>',W6E1Down)
        self.enemy2Down.bind('<Button>',W6E2Down)
        self.enemy3Down.bind('<Button>',W6E3Down)
        self.enemy4Down.bind('<Button>',W6E4Down)
        self.enemy5Down.bind('<Button>',W6E5Down)
        self.enemy6Down.bind('<Button>',W6E6Down)
        self.enemy1num.config(text=str(W6E1))
        self.enemy2num.config(text=str(W6E2))
        self.enemy3num.config(text=str(W6E3))
        self.enemy4num.config(text=str(W6E4))
        self.enemy5num.config(text=str(W6E5))
        self.enemy6num.config(text=str(W6E6))

    def Wave7(event):
        global W7E1
        global W7E2
        global W7E3
        global W7E4
        global W7E5
        global W7E6
        self.lbWave1.config(bg="black")
        self.lbWave2.config(bg="black")
        self.lbWave3.config(bg="black")
        self.lbWave4.config(bg="black")
        self.lbWave5.config(bg="black")
        self.lbWave6.config(bg="black")
        self.lbWave7.config(bg="darkblue")
        self.lbWave8.config(bg="black")
        self.lbWave9.config(bg="black")
        self.lbWave10.config(bg="black")
        self.enemy1Up.unbind('<Button>')
        self.enemy2Up.unbind('<Button>')
        self.enemy3Up.unbind('<Button>')
        self.enemy4Up.unbind('<Button>')
        self.enemy5Up.unbind('<Button>')
        self.enemy6Up.unbind('<Button>')
        self.enemy1Down.unbind('<Button>')
        self.enemy2Down.unbind('<Button>')
        self.enemy3Down.unbind('<Button>')
        self.enemy4Down.unbind('<Button>')
        self.enemy5Down.unbind('<Button>')
        self.enemy6Down.unbind('<Button>')
        self.enemy1Up.bind('<Button>',W7E1Up)
        self.enemy2Up.bind('<Button>',W7E2Up)
        self.enemy3Up.bind('<Button>',W7E3Up)
        self.enemy4Up.bind('<Button>',W7E4Up)
        self.enemy5Up.bind('<Button>',W7E5Up)
        self.enemy6Up.bind('<Button>',W7E6Up)
        self.enemy1Down.bind('<Button>',W7E1Down)
        self.enemy2Down.bind('<Button>',W7E2Down)
        self.enemy3Down.bind('<Button>',W7E3Down)
        self.enemy4Down.bind('<Button>',W7E4Down)
        self.enemy5Down.bind('<Button>',W7E5Down)
        self.enemy6Down.bind('<Button>',W7E6Down)
        self.enemy1num.config(text=str(W7E1))
        self.enemy2num.config(text=str(W7E2))
        self.enemy3num.config(text=str(W7E3))
        self.enemy4num.config(text=str(W7E4))
        self.enemy5num.config(text=str(W7E5))
        self.enemy6num.config(text=str(W7E6))

    def Wave8(event):
        global W8E1
        global W8E2
        global W8E3
        global W8E4
        global W8E5
        global W8E6
        self.lbWave1.config(bg="black")
        self.lbWave2.config(bg="black")
        self.lbWave3.config(bg="black")
        self.lbWave4.config(bg="black")
        self.lbWave5.config(bg="black")
        self.lbWave6.config(bg="black")
        self.lbWave7.config(bg="black")
        self.lbWave8.config(bg="darkblue")
        self.lbWave9.config(bg="black")
        self.lbWave10.config(bg="black")
        self.enemy1Up.unbind('<Button>')
        self.enemy2Up.unbind('<Button>')
        self.enemy3Up.unbind('<Button>')
        self.enemy4Up.unbind('<Button>')
        self.enemy5Up.unbind('<Button>')
        self.enemy6Up.unbind('<Button>')
        self.enemy1Down.unbind('<Button>')
        self.enemy2Down.unbind('<Button>')
        self.enemy3Down.unbind('<Button>')
        self.enemy4Down.unbind('<Button>')
        self.enemy5Down.unbind('<Button>')
        self.enemy6Down.unbind('<Button>')
        self.enemy1Up.bind('<Button>',W8E1Up)
        self.enemy2Up.bind('<Button>',W8E2Up)
        self.enemy3Up.bind('<Button>',W8E3Up)
        self.enemy4Up.bind('<Button>',W8E4Up)
        self.enemy5Up.bind('<Button>',W8E5Up)
        self.enemy6Up.bind('<Button>',W8E6Up)
        self.enemy1Down.bind('<Button>',W8E1Down)
        self.enemy2Down.bind('<Button>',W8E2Down)
        self.enemy3Down.bind('<Button>',W8E3Down)
        self.enemy4Down.bind('<Button>',W8E4Down)
        self.enemy5Down.bind('<Button>',W8E5Down)
        self.enemy6Down.bind('<Button>',W8E6Down)
        self.enemy1num.config(text=str(W8E1))
        self.enemy2num.config(text=str(W8E2))
        self.enemy3num.config(text=str(W8E3))
        self.enemy4num.config(text=str(W8E4))
        self.enemy5num.config(text=str(W8E5))
        self.enemy6num.config(text=str(W8E6))
    
    def Wave9(event):
        global W9E1
        global W9E2
        global W9E3
        global W9E4
        global W9E5
        global W9E6
        self.lbWave1.config(bg="black")
        self.lbWave2.config(bg="black")
        self.lbWave3.config(bg="black")
        self.lbWave4.config(bg="black")
        self.lbWave5.config(bg="black")
        self.lbWave6.config(bg="black")
        self.lbWave7.config(bg="black")
        self.lbWave8.config(bg="black")
        self.lbWave9.config(bg="darkblue")
        self.lbWave10.config(bg="black")
        self.enemy1Up.unbind('<Button>')
        self.enemy2Up.unbind('<Button>')
        self.enemy3Up.unbind('<Button>')
        self.enemy4Up.unbind('<Button>')
        self.enemy5Up.unbind('<Button>')
        self.enemy6Up.unbind('<Button>')
        self.enemy1Down.unbind('<Button>')
        self.enemy2Down.unbind('<Button>')
        self.enemy3Down.unbind('<Button>')
        self.enemy4Down.unbind('<Button>')
        self.enemy5Down.unbind('<Button>')
        self.enemy6Down.unbind('<Button>')
        self.enemy1Up.bind('<Button>',W9E1Up)
        self.enemy2Up.bind('<Button>',W9E2Up)
        self.enemy3Up.bind('<Button>',W9E3Up)
        self.enemy4Up.bind('<Button>',W9E4Up)
        self.enemy5Up.bind('<Button>',W9E5Up)
        self.enemy6Up.bind('<Button>',W9E6Up)
        self.enemy1Down.bind('<Button>',W9E1Down)
        self.enemy2Down.bind('<Button>',W9E2Down)
        self.enemy3Down.bind('<Button>',W9E3Down)
        self.enemy4Down.bind('<Button>',W9E4Down)
        self.enemy5Down.bind('<Button>',W9E5Down)
        self.enemy6Down.bind('<Button>',W9E6Down)
        self.enemy1num.config(text=str(W9E1))
        self.enemy2num.config(text=str(W9E2))
        self.enemy3num.config(text=str(W9E3))
        self.enemy4num.config(text=str(W9E4))
        self.enemy5num.config(text=str(W9E5))
        self.enemy6num.config(text=str(W9E6))
    
    def Wave10(event):
        global W10E1
        global W10E2
        global W10E3
        global W10E4
        global W10E5
        global W10E6
        self.lbWave1.config(bg="black")
        self.lbWave2.config(bg="black")
        self.lbWave3.config(bg="black")
        self.lbWave4.config(bg="black")
        self.lbWave5.config(bg="black")
        self.lbWave6.config(bg="black")
        self.lbWave7.config(bg="black")
        self.lbWave8.config(bg="black")
        self.lbWave9.config(bg="black")
        self.lbWave10.config(bg="darkblue")
        self.enemy1Up.unbind('<Button>')
        self.enemy2Up.unbind('<Button>')
        self.enemy3Up.unbind('<Button>')
        self.enemy4Up.unbind('<Button>')
        self.enemy5Up.unbind('<Button>')
        self.enemy6Up.unbind('<Button>')
        self.enemy1Down.unbind('<Button>')
        self.enemy2Down.unbind('<Button>')
        self.enemy3Down.unbind('<Button>')
        self.enemy4Down.unbind('<Button>')
        self.enemy5Down.unbind('<Button>')
        self.enemy6Down.unbind('<Button>')
        self.enemy1Up.bind('<Button>',W10E1Up)
        self.enemy2Up.bind('<Button>',W10E2Up)
        self.enemy3Up.bind('<Button>',W10E3Up)
        self.enemy4Up.bind('<Button>',W10E4Up)
        self.enemy5Up.bind('<Button>',W10E5Up)
        self.enemy6Up.bind('<Button>',W10E6Up)
        self.enemy1Down.bind('<Button>',W10E1Down)
        self.enemy2Down.bind('<Button>',W10E2Down)
        self.enemy3Down.bind('<Button>',W10E3Down)
        self.enemy4Down.bind('<Button>',W10E4Down)
        self.enemy5Down.bind('<Button>',W10E5Down)
        self.enemy6Down.bind('<Button>',W10E6Down)
        self.enemy1num.config(text=str(W10E1))
        self.enemy2num.config(text=str(W10E2))
        self.enemy3num.config(text=str(W10E3))
        self.enemy4num.config(text=str(W10E4))
        self.enemy5num.config(text=str(W10E5))
        self.enemy6num.config(text=str(W10E6))

    def StartTenWaveChallengeSinglePlayer(event):
        self.destroy()
        TenWaveChallengeSinglePlayer()

    def W1E1Up(event):
        global W1E1
        W1E1 += 1
        self.enemy1num.config(text=str(W1E1))

    def W1E2Up(event):
        global W1E2
        W1E2 += 1
        self.enemy2num.config(text=str(W1E2))
        
    def W1E3Up(event):
        global W1E3
        W1E3 += 1
        self.enemy3num.config(text=str(W1E3))

    def W1E4Up(event):
        global W1E4
        W1E4 += 1
        self.enemy4num.config(text=str(W1E4))

    def W1E5Up(event):
        global W1E5
        W1E5 += 1
        self.enemy5num.config(text=str(W1E5))

    def W1E6Up(event):
        global W1E6
        W1E6 += 1
        self.enemy6num.config(text=str(W1E6))

    def W1E1Down(event):
        global W1E1
        if W1E1 > 0:
            W1E1 -= 1
        self.enemy1num.config(text=str(W1E1))

    def W1E2Down(event):
        global W1E2
        if W1E2 > 0:
            W1E2 -= 1
        self.enemy2num.config(text=str(W1E2))
        
    def W1E3Down(event):
        global W1E3
        if W1E3 > 0:
            W1E3 -= 1
        self.enemy3num.config(text=str(W1E3))

    def W1E4Down(event):
        global W1E4
        if W1E4 > 0:
            W1E4 -= 1
        self.enemy4num.config(text=str(W1E4))

    def W1E5Down(event):
        global W1E5
        if W1E5 > 0:
            W1E5 -= 1
        self.enemy5num.config(text=str(W1E5))

    def W1E6Down(event):
        global W1E6
        if W1E6 > 0:
            W1E6 -= 1
        self.enemy6num.config(text=str(W1E6))

    def W2E1Up(event):
        global W2E1
        W2E1 += 1
        self.enemy1num.config(text=str(W2E1))

    def W2E2Up(event):
        global W2E2
        W2E2 += 1
        self.enemy2num.config(text=str(W2E2))
        
    def W2E3Up(event):
        global W2E3
        W2E3 += 1
        self.enemy3num.config(text=str(W2E3))

    def W2E4Up(event):
        global W2E4
        W2E4 += 1
        self.enemy4num.config(text=str(W2E4))

    def W2E5Up(event):
        global W2E5
        W2E5 += 1
        self.enemy5num.config(text=str(W2E5))

    def W2E6Up(event):
        global W2E6
        W2E6 += 1
        self.enemy6num.config(text=str(W2E6))

    def W2E1Down(event):
        global W2E1
        if W2E1 > 0:
            W2E1 -= 1
        self.enemy1num.config(text=str(W2E1))

    def W2E2Down(event):
        global W2E2
        if W2E2 > 0:
            W2E2 -= 1
        self.enemy2num.config(text=str(W2E2))
        
    def W2E3Down(event):
        global W2E3
        if W2E3 > 0:
            W2E3 -= 1
        self.enemy3num.config(text=str(W2E3))

    def W2E4Down(event):
        global W2E4
        if W2E4 > 0:
            W2E4 -= 1
        self.enemy4num.config(text=str(W2E4))

    def W2E5Down(event):
        global W2E5
        if W2E5 > 0:
            W2E5 -= 1
        self.enemy5num.config(text=str(W2E5))

    def W2E6Down(event):
        global W2E6
        if W2E6 > 0:
            W2E6 -= 1
        self.enemy6num.config(text=str(W2E6))

    def W3E1Up(event):
        global W3E1
        W3E1 += 1
        self.enemy1num.config(text=str(W3E1))

    def W3E2Up(event):
        global W3E2
        W3E2 += 1
        self.enemy2num.config(text=str(W3E2))
        
    def W3E3Up(event):
        global W3E3
        W3E3 += 1
        self.enemy3num.config(text=str(W3E3))

    def W3E4Up(event):
        global W3E4
        W3E4 += 1
        self.enemy4num.config(text=str(W3E4))

    def W3E5Up(event):
        global W3E5
        W3E5 += 1
        self.enemy5num.config(text=str(W3E5))

    def W3E6Up(event):
        global W3E6
        W3E6 += 1
        self.enemy6num.config(text=str(W3E6))

    def W3E1Down(event):
        global W3E1
        if W3E1 > 0:
            W3E1 -= 1
        self.enemy1num.config(text=str(W3E1))

    def W3E2Down(event):
        global W3E2
        if W3E2 > 0:
            W3E2 -= 1
        self.enemy2num.config(text=str(W3E2))
        
    def W3E3Down(event):
        global W3E3
        if W3E3 > 0:
            W3E3 -= 1
        self.enemy3num.config(text=str(W3E3))

    def W3E4Down(event):
        global W3E4
        if W3E4 > 0:
            W3E4 -= 1
        self.enemy4num.config(text=str(W3E4))

    def W3E5Down(event):
        global W3E5
        if W3E5 > 0:
            W3E5 -= 1
        self.enemy5num.config(text=str(W3E5))

    def W3E6Down(event):
        global W3E6
        if W3E6 > 0:
            W3E6 -= 1
        self.enemy6num.config(text=str(W3E6))

    def W4E1Up(event):
        global W4E1
        W4E1 += 1
        self.enemy1num.config(text=str(W4E1))

    def W4E2Up(event):
        global W4E2
        W4E2 += 1
        self.enemy2num.config(text=str(W4E2))
        
    def W4E3Up(event):
        global W4E3
        W4E3 += 1
        self.enemy3num.config(text=str(W4E3))

    def W4E4Up(event):
        global W4E4
        W4E4 += 1
        self.enemy4num.config(text=str(W4E4))

    def W4E5Up(event):
        global W4E5
        W4E5 += 1
        self.enemy5num.config(text=str(W4E5))

    def W4E6Up(event):
        global W4E6
        W4E6 += 1
        self.enemy6num.config(text=str(W4E6))

    def W4E1Down(event):
        global W4E1
        if W4E1 > 0:
            W4E1 -= 1
        self.enemy1num.config(text=str(W4E1))

    def W4E2Down(event):
        global W4E2
        if W4E2 > 0:
            W4E2 -= 1
        self.enemy2num.config(text=str(W4E2))
        
    def W4E3Down(event):
        global W4E3
        if W4E3 > 0:
            W4E3 -= 1
        self.enemy3num.config(text=str(W4E3))

    def W4E4Down(event):
        global W4E4
        if W4E4 > 0:
            W4E4 -= 1
        self.enemy4num.config(text=str(W4E4))

    def W4E5Down(event):
        global W4E5
        if W4E5 > 0:
            W4E5 -= 1
        self.enemy5num.config(text=str(W4E5))

    def W4E6Down(event):
        global W4E6
        if W4E6 > 0:
            W4E6 -= 1
        self.enemy6num.config(text=str(W4E6))

    def W5E1Up(event):
        global W5E1
        W5E1 += 1
        self.enemy1num.config(text=str(W5E1))

    def W5E2Up(event):
        global W5E2
        W5E2 += 1
        self.enemy2num.config(text=str(W5E2))
        
    def W5E3Up(event):
        global W5E3
        W5E3 += 1
        self.enemy3num.config(text=str(W5E3))

    def W5E4Up(event):
        global W5E4
        W5E4 += 1
        self.enemy4num.config(text=str(W5E4))

    def W5E5Up(event):
        global W5E5
        W5E5 += 1
        self.enemy5num.config(text=str(W5E5))

    def W5E6Up(event):
        global W5E6
        W5E6 += 1
        self.enemy6num.config(text=str(W5E6))

    def W5E1Down(event):
        global W5E1
        if W5E1 > 0:
            W5E1 -= 1
        self.enemy1num.config(text=str(W5E1))

    def W5E2Down(event):
        global W5E2
        if W5E2 > 0:
            W5E2 -= 1
        self.enemy2num.config(text=str(W5E2))
        
    def W5E3Down(event):
        global W5E3
        if W5E3 > 0:
            W5E3 -= 1
        self.enemy3num.config(text=str(W5E3))

    def W5E4Down(event):
        global W5E4
        if W5E4 > 0:
            W5E4 -= 1
        self.enemy4num.config(text=str(W5E4))

    def W5E5Down(event):
        global W5E5
        if W5E5 > 0:
            W5E5 -= 1
        self.enemy5num.config(text=str(W5E5))

    def W5E6Down(event):
        global W5E6
        if W5E6 > 0:
            W5E6 -= 1
        self.enemy6num.config(text=str(W5E6))

    def W6E1Up(event):
        global W6E1
        W6E1 += 1
        self.enemy1num.config(text=str(W6E1))

    def W6E2Up(event):
        global W6E2
        W6E2 += 1
        self.enemy2num.config(text=str(W6E2))
        
    def W6E3Up(event):
        global W6E3
        W6E3 += 1
        self.enemy3num.config(text=str(W6E3))

    def W6E4Up(event):
        global W6E4
        W6E4 += 1
        self.enemy4num.config(text=str(W6E4))

    def W6E5Up(event):
        global W6E5
        W6E5 += 1
        self.enemy5num.config(text=str(W6E5))

    def W6E6Up(event):
        global W6E6
        W6E6 += 1
        self.enemy6num.config(text=str(W6E6))

    def W6E1Down(event):
        global W6E1
        if W6E1 > 0:
            W6E1 -= 1
        self.enemy1num.config(text=str(W6E1))

    def W6E2Down(event):
        global W6E2
        if W6E2 > 0:
            W6E2 -= 1
        self.enemy2num.config(text=str(W6E2))
        
    def W6E3Down(event):
        global W6E3
        if W6E3 > 0:
            W6E3 -= 1
        self.enemy3num.config(text=str(W6E3))

    def W6E4Down(event):
        global W6E4
        if W6E4 > 0:
            W6E4 -= 1
        self.enemy4num.config(text=str(W6E4))

    def W6E5Down(event):
        global W6E5
        if W6E5 > 0:
            W6E5 -= 1
        self.enemy5num.config(text=str(W6E5))

    def W6E6Down(event):
        global W6E6
        if W6E6 > 0:
            W6E6 -= 1
        self.enemy6num.config(text=str(W6E6))

    def W7E1Up(event):
        global W7E1
        W7E1 += 1
        self.enemy1num.config(text=str(W7E1))

    def W7E2Up(event):
        global W7E2
        W7E2 += 1
        self.enemy2num.config(text=str(W7E2))
        
    def W7E3Up(event):
        global W7E3
        W7E3 += 1
        self.enemy3num.config(text=str(W7E3))

    def W7E4Up(event):
        global W7E4
        W7E4 += 1
        self.enemy4num.config(text=str(W7E4))

    def W7E5Up(event):
        global W7E5
        W7E5 += 1
        self.enemy5num.config(text=str(W7E5))

    def W7E6Up(event):
        global W7E6
        W7E6 += 1
        self.enemy6num.config(text=str(W7E6))

    def W7E1Down(event):
        global W7E1
        if W7E1 > 0:
            W7E1 -= 1
        self.enemy1num.config(text=str(W7E1))

    def W7E2Down(event):
        global W7E2
        if W7E2 > 0:
            W7E2 -= 1
        self.enemy2num.config(text=str(W7E2))
        
    def W7E3Down(event):
        global W7E3
        if W7E3 > 0:
            W7E3 -= 1
        self.enemy3num.config(text=str(W7E3))

    def W7E4Down(event):
        global W7E4
        if W7E4 > 0:
            W7E4 -= 1
        self.enemy4num.config(text=str(W7E4))

    def W7E5Down(event):
        global W7E5
        if W7E5 > 0:
            W7E5 -= 1
        self.enemy5num.config(text=str(W7E5))

    def W7E6Down(event):
        global W7E6
        if W7E6 > 0:
            W7E6 -= 1
        self.enemy6num.config(text=str(W7E6))

    def W8E1Up(event):
        global W8E1
        W8E1 += 1
        self.enemy1num.config(text=str(W8E1))

    def W8E2Up(event):
        global W8E2
        W8E2 += 1
        self.enemy2num.config(text=str(W8E2))
        
    def W8E3Up(event):
        global W8E3
        W8E3 += 1
        self.enemy3num.config(text=str(W8E3))

    def W8E4Up(event):
        global W8E4
        W8E4 += 1
        self.enemy4num.config(text=str(W8E4))

    def W8E5Up(event):
        global W8E5
        W8E5 += 1
        self.enemy5num.config(text=str(W8E5))

    def W8E6Up(event):
        global W8E6
        W8E6 += 1
        self.enemy6num.config(text=str(W8E6))

    def W8E1Down(event):
        global W8E1
        if W8E1 > 0:
            W8E1 -= 1
        self.enemy1num.config(text=str(W8E1))

    def W8E2Down(event):
        global W8E2
        if W8E2 > 0:
            W8E2 -= 1
        self.enemy2num.config(text=str(W8E2))
        
    def W8E3Down(event):
        global W8E3
        if W8E3 > 0:
            W8E3 -= 1
        self.enemy3num.config(text=str(W8E3))

    def W8E4Down(event):
        global W8E4
        if W8E4 > 0:
            W8E4 -= 1
        self.enemy4num.config(text=str(W8E4))

    def W8E5Down(event):
        global W8E5
        if W8E5 > 0:
            W8E5 -= 1
        self.enemy5num.config(text=str(W8E5))

    def W8E6Down(event):
        global W8E6
        if W8E6 > 0:
            W8E6 -= 1
        self.enemy6num.config(text=str(W8E6))

    def W9E1Up(event):
        global W9E1
        W9E1 += 1
        self.enemy1num.config(text=str(W9E1))

    def W9E2Up(event):
        global W9E2
        W9E2 += 1
        self.enemy2num.config(text=str(W9E2))
        
    def W9E3Up(event):
        global W9E3
        W9E3 += 1
        self.enemy3num.config(text=str(W9E3))

    def W9E4Up(event):
        global W9E4
        W9E4 += 1
        self.enemy4num.config(text=str(W9E4))

    def W9E5Up(event):
        global W9E5
        W9E5 += 1
        self.enemy5num.config(text=str(W9E5))

    def W9E6Up(event):
        global W9E6
        W9E6 += 1
        self.enemy6num.config(text=str(W9E6))

    def W9E1Down(event):
        global W9E1
        if W9E1 > 0:
            W9E1 -= 1
        self.enemy1num.config(text=str(W9E1))

    def W9E2Down(event):
        global W9E2
        if W9E2 > 0:
            W9E2 -= 1
        self.enemy2num.config(text=str(W9E2))
        
    def W9E3Down(event):
        global W9E3
        if W9E3 > 0:
            W9E3 -= 1
        self.enemy3num.config(text=str(W9E3))

    def W9E4Down(event):
        global W9E4
        if W9E4 > 0:
            W9E4 -= 1
        self.enemy4num.config(text=str(W9E4))

    def W9E5Down(event):
        global W9E5
        if W9E5 > 0:
            W9E5 -= 1
        self.enemy5num.config(text=str(W9E5))

    def W9E6Down(event):
        global W9E6
        if W9E6 > 0:
            W9E6 -= 1
        self.enemy6num.config(text=str(W9E6))

    def W10E1Up(event):
        global W10E1
        W10E1 += 1
        self.enemy1num.config(text=str(W10E1))

    def W10E2Up(event):
        global W10E2
        W10E2 += 1
        self.enemy2num.config(text=str(W10E2))
        
    def W10E3Up(event):
        global W10E3
        W10E3 += 1
        self.enemy3num.config(text=str(W10E3))

    def W10E4Up(event):
        global W10E4
        W10E4 += 1
        self.enemy4num.config(text=str(W10E4))

    def W10E5Up(event):
        global W10E5
        W10E5 += 1
        self.enemy5num.config(text=str(W10E5))

    def W10E6Up(event):
        global W10E6
        W10E6 += 1
        self.enemy6num.config(text=str(W10E6))

    def W10E1Down(event):
        global W10E1
        if W10E1 > 0:
            W10E1 -= 1
        self.enemy1num.config(text=str(W10E1))

    def W10E2Down(event):
        global W10E2
        if W10E2 > 0:
            W10E2 -= 1
        self.enemy2num.config(text=str(W10E2))
        
    def W10E3Down(event):
        global W10E3
        if W10E3 > 0:
            W10E3 -= 1
        self.enemy3num.config(text=str(W10E3))

    def W10E4Down(event):
        global W10E4
        if W10E4 > 0:
            W10E4 -= 1
        self.enemy4num.config(text=str(W10E4))

    def W10E5Down(event):
        global W10E5
        if W10E5 > 0:
            W10E5 -= 1
        self.enemy5num.config(text=str(W10E5))

    def W10E6Down(event):
        global W10E6
        if W10E6 > 0:
            W10E6 -= 1
        self.enemy6num.config(text=str(W10E6))

    def Exit(event):
        self.destroy()

    #Bind
    self.btnMainMenu.bind('<Button>',StartMainMenu)
    self.lbWave1.bind('<Button>',Wave1)
    self.lbWave2.bind('<Button>',Wave2)
    self.lbWave3.bind('<Button>',Wave3)
    self.lbWave4.bind('<Button>',Wave4)
    self.lbWave5.bind('<Button>',Wave5)
    self.lbWave6.bind('<Button>',Wave6)
    self.lbWave7.bind('<Button>',Wave7)
    self.lbWave8.bind('<Button>',Wave8)
    self.lbWave9.bind('<Button>',Wave9)
    self.lbWave10.bind('<Button>',Wave10)
    self.btnPlaySinglePlayer.bind('<Button>',StartTenWaveChallengeSinglePlayer)
    self.bind('<Escape>',Exit)
        
    #Frame settings
    self.geometry("830x700")
    self.title("Space Assault")
    self.configure(bg="black")

    Wave1()

def TenWaveChallengeSinglePlayer():
    self = Tk()

    #Variables
    global wave
    global Damage
    global Damage3
    global Damage5
    global Damage6
    global Xpos
    global Ypos
    global enXpos
    global enYpos
    global en2Xpos
    global en2Ypos
    global en3Xpos
    global en3Ypos
    global en4Xpos
    global en4Ypos
    global en5Xpos
    global en5Ypos
    global en6Xpos
    global en6Ypos
    global gameover
    global direction
    global start
    global created
    global created2
    global created3
    global created4
    global created5
    global destroy
    global generated1
    global generated2
    global generated3
    global generated4
    global pause
    wave = 0
    Damage = 0
    Damage3 = 0
    Damage5 = 0
    Damage6 = 0
    Xpos = 425
    Ypos = 350
    enXpos = 0
    enYpos = 0
    en2Xpos = 0
    en2Ypos = 0
    en3Xpos = 0
    en3Ypos = 0
    en4Xpos = 0
    en4Ypos = 0
    en5Xpos = 0
    en5Ypos = 0
    en6Xpos = 0
    en6Ypos = 0
    gameover = 0
    direction = "N"
    start = 0
    created = 0
    created2 = 0
    created3 = 0
    created4 = 0
    created5 = 0
    destroy = 0
    generated1 = 1000
    generated2 = 1250
    generated3 = 1500
    generated4 = 1750
    pause = 0
    global W1E1
    global W1E2
    global W1E3
    global W1E4
    global W1E5
    global W1E6
    global W2E1
    global W2E2
    global W2E3
    global W2E4
    global W2E5
    global W2E6
    global W3E1
    global W3E2
    global W3E3
    global W3E4
    global W3E5
    global W3E6
    global W4E1
    global W4E2
    global W4E3
    global W4E4
    global W4E5
    global W4E6
    global W5E1
    global W5E2
    global W5E3
    global W5E4
    global W5E5
    global W5E6
    global W6E1
    global W6E2
    global W6E3
    global W6E4
    global W6E5
    global W6E6
    global W7E1
    global W7E2
    global W7E3
    global W7E4
    global W7E5
    global W7E6
    global W8E1
    global W8E2
    global W8E3
    global W8E4
    global W8E5
    global W8E6
    global W9E1
    global W9E2
    global W9E3
    global W9E4
    global W9E5
    global W9E6
    global W10E1
    global W10E2
    global W10E3
    global W10E4
    global W10E5
    global W10E6
    
    #Lists
    Shots = []
    ShotsXpos = []
    ShotsYpos = []
    ShotDir = []
    enShots = []
    enShotsXpos = []
    enShotsYpos = []
    enShotDir = []
    Enemies = []
    EnemiesDmg = []
    EnemiesXpos = []
    EnemiesYpos = []
    Enemies2 = []
    Enemies2Xpos = []
    Enemies2Ypos = []
    Enemies3 = []
    Enemies3Dmg = []
    Enemies3Xpos = []
    Enemies3Ypos = []
    Enemies4 = []
    Enemies4Xpos = []
    Enemies4Ypos = []
    Enemies5 = []
    Enemies5Dmg = []
    Enemies5Xpos = []
    Enemies5Ypos = []
    Enemies5Wall = []
    Enemies6 = []
    Enemies6Xpos = []
    Enemies6Ypos = []
    Enemies6Type = []
    Enemies6Dmg = []
    Explosions = []
    
    #Score
    self.lbScore = Label(text="Wave: "+str(wave)+"  Press 'p' to pause",bg="black",fg="white")
    self.lbScore.place(x=165,y=680,width=500,height=20)

    #Player
    self.player = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
    self.player.place(x=Xpos,y=Ypos)
    self.player.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="green")

    #Functions
    def LeftKey(event):
        global Xpos
        global Ypos
        global direction
        global start
        self.player.delete("all")
        self.player.create_polygon(0,15,30,30,15,15,30,0,0,15,fill="green")
        if Xpos > 0:
            Xpos -= 25
        self.player.place(x=Xpos,y=Ypos)
        direction = "W"
        cycle = 0
        for enemy in Enemies:
            if Xpos == EnemiesXpos[cycle] and Ypos == EnemiesYpos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy2 in Enemies2:
            if Xpos == Enemies2Xpos[cycle] and Ypos == Enemies2Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy3 in Enemies3:
            if Xpos == Enemies3Xpos[cycle] and Ypos == Enemies3Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy4 in Enemies4:
            if Xpos == Enemies4Xpos[cycle] and Ypos == Enemies4Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy5 in Enemies5:
            if Xpos == Enemies5Xpos[cycle] and Ypos == Enemies5Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy6 in Enemies6:
            if Xpos == Enemies6Xpos[cycle] and Ypos == Enemies6Ypos[cycle]:
                GameOver()
            cycle += 1
        if start == 0:
            NextWave()
        start = 1

    def RightKey(event):
        global Xpos
        global Ypos
        global direction
        global start
        self.player.delete("all")
        self.player.create_polygon(30,15,0,30,15,15,0,0,30,15,fill="green")
        if Xpos < 800:
            Xpos += 25
        self.player.place(x=Xpos,y=Ypos)
        direction = "E"
        cycle = 0
        for enemy in Enemies:
            if Xpos == EnemiesXpos[cycle] and Ypos == EnemiesYpos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy2 in Enemies2:
            if Xpos == Enemies2Xpos[cycle] and Ypos == Enemies2Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy3 in Enemies3:
            if Xpos == Enemies3Xpos[cycle] and Ypos == Enemies3Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy4 in Enemies4:
            if Xpos == Enemies4Xpos[cycle] and Ypos == Enemies4Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy5 in Enemies5:
            if Xpos == Enemies5Xpos[cycle] and Ypos == Enemies5Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy6 in Enemies6:
            if Xpos == Enemies6Xpos[cycle] and Ypos == Enemies6Ypos[cycle]:
                GameOver()
            cycle += 1
        if start == 0:
            NextWave()
        start = 1

    def UpKey(event):
        global Xpos
        global Ypos
        global direction
        global start
        self.player.delete("all")
        self.player.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="green")
        if Ypos > 0:
            Ypos -= 25
        self.player.place(x=Xpos,y=Ypos)
        direction = "N"
        cycle = 0
        for enemy in Enemies:
            if Xpos == EnemiesXpos[cycle] and Ypos == EnemiesYpos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy2 in Enemies2:
            if Xpos == Enemies2Xpos[cycle] and Ypos == Enemies2Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy3 in Enemies3:
            if Xpos == Enemies3Xpos[cycle] and Ypos == Enemies3Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy4 in Enemies4:
            if Xpos == Enemies4Xpos[cycle] and Ypos == Enemies4Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy5 in Enemies5:
            if Xpos == Enemies5Xpos[cycle] and Ypos == Enemies5Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy6 in Enemies6:
            if Xpos == Enemies6Xpos[cycle] and Ypos == Enemies6Ypos[cycle]:
                GameOver()
            cycle += 1
        if start == 0:
            NextWave()
        start = 1

    def DownKey(event):
        global Xpos
        global Ypos
        global direction
        global start
        self.player.delete("all")
        self.player.create_polygon(15,30,30,0,15,15,0,0,15,30,fill="green")
        if Ypos < 650:
            Ypos += 25
        self.player.place(x=Xpos,y=Ypos)
        direction = "S"
        cycle = 0
        for enemy in Enemies:
            if Xpos == EnemiesXpos[cycle] and Ypos == EnemiesYpos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy2 in Enemies2:
            if Xpos == Enemies2Xpos[cycle] and Ypos == Enemies2Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy3 in Enemies3:
            if Xpos == Enemies3Xpos[cycle] and Ypos == Enemies3Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy4 in Enemies4:
            if Xpos == Enemies4Xpos[cycle] and Ypos == Enemies4Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy5 in Enemies5:
            if Xpos == Enemies5Xpos[cycle] and Ypos == Enemies5Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy6 in Enemies6:
            if Xpos == Enemies6Xpos[cycle] and Ypos == Enemies6Ypos[cycle]:
                GameOver()
            cycle += 1
        if start == 0:
            NextWave()
        start = 1

    def CreateEnemy():
        global Xpos
        global Ypos
        global enXpos
        global enYpos
        global Damage
        global created
        enXpos = random.randrange(0,33)*25
        enYpos = random.randrange(0,27)*25
        while abs(Xpos - enXpos) <= 75 and abs(Ypos - enYpos) <= 75:
            enXpos = random.randrange(0,33)*25
            enYpos = random.randrange(0,27)*25
        self.enemy = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
        self.enemy.place(x=enXpos,y=enYpos)
        self.enemy.polygon = self.enemy.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="darkviolet")
        Enemies.append(self.enemy)
        EnemiesDmg.append(Damage)
        EnemiesXpos.append(enXpos)
        EnemiesYpos.append(enYpos)
        created = 1

    def CreateEnemy2():
        global Xpos
        global Ypos
        global en2Xpos
        global en2Ypos
        global created2
        en2Xpos = random.randrange(0,33)*25
        en2Ypos = random.randrange(0,27)*25
        while abs(Xpos - en2Xpos) <= 75 and abs(Ypos - en2Ypos) <= 75:
            en2Xpos = random.randrange(0,33)*25
            en2Ypos = random.randrange(0,27)*25
        self.enemy2 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
        self.enemy2.place(x=en2Xpos,y=en2Ypos)
        self.enemy2.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="red")
        Enemies2.append(self.enemy2)
        Enemies2Xpos.append(en2Xpos)
        Enemies2Ypos.append(en2Ypos)
        created2 = 1

    def CreateEnemy3():
        global Xpos
        global Ypos
        global en3Xpos
        global en3Ypos
        global Damage3
        global created3
        en3Xpos = random.randrange(0,33)*25
        en3Ypos = random.randrange(0,27)*25
        while abs(Xpos - en3Xpos) <= 75 and abs(Ypos - en3Ypos) <= 75:
            en3Xpos = random.randrange(0,33)*25
            en3Ypos = random.randrange(0,27)*25
        self.enemy3 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
        self.enemy3.place(x=en3Xpos,y=en3Ypos)
        self.enemy3.polygon = self.enemy3.create_polygon(10,0,0,0,0,30,30,30,30,0,20,0,20,10,10,10,fill="navy")
        Enemies3.append(self.enemy3)
        Enemies3Dmg.append(Damage3)
        Enemies3Xpos.append(en3Xpos)
        Enemies3Ypos.append(en3Ypos)
        created3 = 1

    def CreateEnemy4():
        global Xpos
        global Ypos
        global en4Xpos
        global en4Ypos
        global created4
        en4Xpos = random.randrange(0,33)*25
        en4Ypos = random.randrange(0,27)*25
        while abs(Xpos - en4Xpos) <= 150 and abs(Ypos - en4Ypos) <= 150:
            en4Xpos = random.randrange(0,33)*25
            en4Ypos = random.randrange(0,27)*25
        self.enemy4 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
        self.enemy4.place(x=en4Xpos,y=en4Ypos)
        self.enemy4.create_polygon(15,0,5,15,12,15,5,30,25,30,17,15,25,15,fill="darkgreen")
        Enemies4.append(self.enemy4)
        Enemies4Xpos.append(en4Xpos)
        Enemies4Ypos.append(en4Ypos)
        created4 = 1

    def CreateEnemy5():
        global Xpos
        global Ypos
        global en5Xpos
        global en5Ypos
        global Damage5
        global created5
        wall = random.choice(["N","E","S","W"])
        if wall == "N":
            en5Xpos = random.randrange(0,33)*25
            en5Ypos = 0
            self.enemy5 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
            self.enemy5.place(x=en5Xpos,y=en5Ypos)
            self.enemy5.polygon = self.enemy5.create_polygon(0,0,10,15,10,30,20,30,20,15,30,0,fill="darkorange2")
        elif wall == "E":
            en5Xpos = 800
            en5Ypos = random.randrange(0,27)*25
            self.enemy5 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
            self.enemy5.place(x=en5Xpos,y=en5Ypos)
            self.enemy5.polygon = self.enemy5.create_polygon(30,0,15,10,0,10,0,20,15,20,30,30,fill="darkorange2")
        elif wall == "S":
            en5Xpos = random.randrange(0,33)*25
            en5Ypos = 650
            self.enemy5 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
            self.enemy5.place(x=en5Xpos,y=en5Ypos)
            self.enemy5.polygon = self.enemy5.create_polygon(30,30,20,15,20,0,10,0,10,15,0,30,fill="darkorange2")
        elif wall == "W":
            en5Xpos = 0
            en5Ypos = random.randrange(0,27)*25
            self.enemy5 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
            self.enemy5.place(x=en5Xpos,y=en5Ypos)
            self.enemy5.polygon = self.enemy5.create_polygon(0,30,15,20,30,20,30,10,15,10,0,0,fill="darkorange2")
        while abs(Xpos - en5Xpos) <= 75 and abs(Ypos - en5Ypos) <= 75:
            wall = random.choice(["N","E","S","W"])
            if wall == "N":
                en5Xpos = random.randrange(0,33)*25
                en5Ypos = 0
                self.enemy5 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
                self.enemy5.place(x=en5Xpos,y=en5Ypos)
                self.enemy5.polygon = self.enemy5.create_polygon(0,0,10,15,10,30,20,30,20,15,30,0,fill="darkorange2")
            elif wall == "E":
                en5Xpos = 800
                en5Ypos = random.randrange(0,27)*25
                self.enemy5 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
                self.enemy5.place(x=en5Xpos,y=en5Ypos)
                self.enemy5.polygon = self.enemy5.create_polygon(30,0,15,10,0,10,0,20,15,20,30,30,fill="darkorange2")
            elif wall == "S":
                en5Xpos = random.randrange(0,33)*25
                en5Ypos = 650
                self.enemy5 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
                self.enemy5.place(x=en5Xpos,y=en5Ypos)
                self.enemy5.polygon = self.enemy5.create_polygon(30,30,20,15,20,0,10,0,10,15,0,30,fill="darkorange2")
            elif wall == "W":
                en5Xpos = 0
                en5Ypos = random.randrange(0,27)*25
                self.enemy5 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
                self.enemy5.place(x=en5Xpos,y=en5Ypos)
                self.enemy5.polygon = self.enemy5.create_polygon(0,30,15,20,30,20,30,10,15,10,0,0,fill="darkorange2")
        Enemies5.append(self.enemy5)
        Enemies5Dmg.append(Damage5)
        Enemies5Xpos.append(en5Xpos)
        Enemies5Ypos.append(en5Ypos)
        Enemies5Wall.append(wall)
        created5 = 1

    def CreateEnemy6():
        global Xpos
        global Ypos
        global en6Xpos
        global en6Ypos
        en6Type = random.choice([1,2,3,4])
        en6Xpos = random.randrange(0,33)*25
        en6Ypos = random.randrange(0,27)*25
        while abs(Xpos - en6Xpos) <= 75 and abs(Ypos - en6Ypos) <= 75:
            en6Xpos = random.randrange(0,33)*25
            en6Ypos = random.randrange(0,27)*25
        self.enemy6 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
        self.enemy6.place(x=en6Xpos,y=en6Ypos)
        self.enemy6.oval = self.enemy6.create_oval(0,0,30,30,fill="gray20")
        Enemies6.append(self.enemy6)
        Enemies6Xpos.append(en6Xpos)
        Enemies6Ypos.append(en6Ypos)
        Enemies6Type.append(en6Type)
        Enemies6Dmg.append(Damage6)

    def EnemyMove():
        global Xpos
        global Ypos
        global gameover
        global created
        if gameover != 1:
            self.after(300,EnemyMove)
            if created == 1:
                cycle = 0
                for self.enemy in Enemies:
                    rndDir = random.choice(["X","Y"])
                    if EnemiesDmg[cycle] == 0:
                        EnemyColor = "darkviolet"
                    else:
                        EnemyColor = "violet"
                    if Xpos < EnemiesXpos[cycle] and Ypos < EnemiesYpos[cycle]:
                        self.enemy.delete("all")
                        if rndDir == "X":
                            EnemiesXpos[cycle] -= 25
                            self.enemy.polygon = self.enemy.create_polygon(0,15,30,30,15,15,30,0,0,15,fill=EnemyColor)
                        else:
                            EnemiesYpos[cycle] -= 25
                            self.enemy.polygon = self.enemy.create_polygon(15,0,30,30,15,15,0,30,15,0,fill=EnemyColor)
                    elif Xpos < EnemiesXpos[cycle] and Ypos > EnemiesYpos[cycle]:
                        self.enemy.delete("all")
                        if rndDir == "X":
                            EnemiesXpos[cycle] -= 25
                            self.enemy.polygon = self.enemy.create_polygon(0,15,30,30,15,15,30,0,0,15,fill=EnemyColor)
                        else:
                            EnemiesYpos[cycle] += 25
                            self.enemy.polygon = self.enemy.create_polygon(15,30,30,0,15,15,0,0,15,30,fill=EnemyColor)
                    elif Xpos > EnemiesXpos[cycle] and Ypos < EnemiesYpos[cycle]:
                        self.enemy.delete("all")
                        if rndDir == "X":
                            EnemiesXpos[cycle] += 25
                            self.enemy.polygon = self.enemy.create_polygon(30,15,0,30,15,15,0,0,30,15,fill=EnemyColor)
                        else:
                            EnemiesYpos[cycle] -= 25
                            self.enemy.polygon = self.enemy.create_polygon(15,0,30,30,15,15,0,30,15,0,fill=EnemyColor)
                    elif Xpos > EnemiesXpos[cycle] and Ypos > EnemiesYpos[cycle]:
                        self.enemy.delete("all")
                        if rndDir == "X":
                            EnemiesXpos[cycle] += 25
                            self.enemy.polygon = self.enemy.create_polygon(30,15,0,30,15,15,0,0,30,15,fill=EnemyColor)
                        else:
                            EnemiesYpos[cycle] += 25
                            self.enemy.polygon = self.enemy.create_polygon(15,30,30,0,15,15,0,0,15,30,fill=EnemyColor)
                    elif Xpos < EnemiesXpos[cycle] and Ypos == EnemiesYpos[cycle]:
                        self.enemy.delete("all")
                        self.enemy.polygon = self.enemy.create_polygon(0,15,30,30,15,15,30,0,0,15,fill=EnemyColor)
                        EnemiesXpos[cycle] -= 25
                    elif Xpos > EnemiesXpos[cycle] and Ypos == EnemiesYpos[cycle]:
                        self.enemy.delete("all")
                        self.enemy.polygon = self.enemy.create_polygon(30,15,0,30,15,15,0,0,30,15,fill=EnemyColor)
                        EnemiesXpos[cycle] += 25
                    elif Xpos == EnemiesXpos[cycle] and Ypos < EnemiesYpos[cycle]:
                        self.enemy.delete("all")
                        self.enemy.polygon = self.enemy.create_polygon(15,0,30,30,15,15,0,30,15,0,fill=EnemyColor)
                        EnemiesYpos[cycle] -= 25
                    elif Xpos == EnemiesXpos[cycle] and Ypos > EnemiesYpos[cycle]:
                        self.enemy.delete("all")
                        self.enemy.polygon = self.enemy.create_polygon(15,30,30,0,15,15,0,0,15,30,fill=EnemyColor)
                        EnemiesYpos[cycle] += 25
                    self.enemy.place(x=EnemiesXpos[cycle],y=EnemiesYpos[cycle])
                    if Xpos == EnemiesXpos[cycle] and Ypos == EnemiesYpos[cycle]:
                        GameOver()
                    cycle += 1

    def Enemy2Move():
        global Xpos
        global Ypos
        global gameover
        global created2
        if gameover != 1:
            self.after(300,Enemy2Move)
            if created2 == 1:
                cycle = 0
                for self.enemy2 in Enemies2:
                    if Xpos < Enemies2Xpos[cycle] and Ypos < Enemies2Ypos[cycle]:
                        self.enemy2.delete("all")
                        self.enemy2.create_polygon(0,0,30,15,15,15,15,30,0,0,fill="red")
                        Enemies2Xpos[cycle] -= 25
                        Enemies2Ypos[cycle] -= 25
                    elif Xpos < Enemies2Xpos[cycle] and Ypos > Enemies2Ypos[cycle]:
                        self.enemy2.delete("all")
                        self.enemy2.create_polygon(0,30,15,0,15,15,30,15,0,30,fill="red")
                        Enemies2Xpos[cycle] -= 25
                        Enemies2Ypos[cycle] += 25
                    elif Xpos > Enemies2Xpos[cycle] and Ypos < Enemies2Ypos[cycle]:
                        self.enemy2.delete("all")
                        self.enemy2.create_polygon(30,0,0,15,15,15,15,30,30,0,fill="red")
                        Enemies2Xpos[cycle] += 25
                        Enemies2Ypos[cycle] -= 25
                    elif Xpos > Enemies2Xpos[cycle] and Ypos > Enemies2Ypos[cycle]:
                        self.enemy2.delete("all")
                        self.enemy2.create_polygon(30,30,15,0,15,15,0,15,30,30,fill="red")
                        Enemies2Xpos[cycle] += 25
                        Enemies2Ypos[cycle] += 25
                    elif Xpos < Enemies2Xpos[cycle] and Ypos == Enemies2Ypos[cycle]:
                        self.enemy2.delete("all")
                        self.enemy2.create_polygon(0,15,30,30,15,15,30,0,0,15,fill="red")
                        Enemies2Xpos[cycle] -= 25
                    elif Xpos > Enemies2Xpos[cycle] and Ypos == Enemies2Ypos[cycle]:
                        self.enemy2.delete("all")
                        self.enemy2.create_polygon(30,15,0,30,15,15,0,0,30,15,fill="red")
                        Enemies2Xpos[cycle] += 25
                    elif Xpos == Enemies2Xpos[cycle] and Ypos < Enemies2Ypos[cycle]:
                        self.enemy2.delete("all")
                        self.enemy2.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="red")
                        Enemies2Ypos[cycle] -= 25
                    elif Xpos == Enemies2Xpos[cycle] and Ypos > Enemies2Ypos[cycle]:
                        self.enemy2.delete("all")
                        self.enemy2.create_polygon(15,30,30,0,15,15,0,0,15,30,fill="red")
                        Enemies2Ypos[cycle] += 25
                    self.enemy2.place(x=Enemies2Xpos[cycle],y=Enemies2Ypos[cycle])
                    if Xpos == Enemies2Xpos[cycle] and Ypos == Enemies2Ypos[cycle]:
                        GameOver()
                    cycle += 1

    def Enemy3Move():
        global Xpos
        global Ypos
        global gameover
        global created3
        if gameover != 1:
            self.after(350,Enemy3Move)
            if created3 == 1:
                cycle = 0
                for self.enemy3 in Enemies3:
                        rndDir = random.choice(["X","Y"])
                        if Enemies3Dmg[cycle] == 0:
                            Enemy3Color = "navy"
                        elif Enemies3Dmg[cycle] == 1:
                            Enemy3Color = "blue"
                        elif Enemies3Dmg[cycle] == 2:
                            Enemy3Color = "dodgerblue"
                        elif Enemies3Dmg[cycle] == 3:
                            Enemy3Color = "deepskyblue"
                        else:
                            Enemy3Color = "lightskyblue"
                        if Xpos < Enemies3Xpos[cycle] and Ypos < Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            if rndDir == "X":
                                Enemies3Xpos[cycle] -= 25
                                self.enemy3.polygon = self.enemy3.create_polygon(0,20,0,30,30,30,30,0,0,0,0,10,10,10,10,20,fill=Enemy3Color)
                            else:
                                Enemies3Ypos[cycle] -= 25
                                self.enemy3.polygon = self.enemy3.create_polygon(10,0,0,0,0,30,30,30,30,0,20,0,20,10,10,10,fill=Enemy3Color)
                        elif Xpos < Enemies3Xpos[cycle] and Ypos > Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            if rndDir == "X":
                                Enemies3Xpos[cycle] -= 25
                                self.enemy3.polygon = self.enemy3.create_polygon(0,20,0,30,30,30,30,0,0,0,0,10,10,10,10,20,fill=Enemy3Color)
                            else:
                                Enemies3Ypos[cycle] += 25
                                self.enemy3.polygon = self.enemy3.create_polygon(20,30,30,30,30,0,0,0,0,30,10,30,10,20,20,20,fill=Enemy3Color)
                        elif Xpos > Enemies3Xpos[cycle] and Ypos < Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            if rndDir == "X":
                                Enemies3Xpos[cycle] += 25
                                self.enemy3.polygon = self.enemy3.create_polygon(30,10,30,0,0,0,0,30,30,30,30,20,20,20,20,10,fill=Enemy3Color)
                            else:
                                Enemies3Ypos[cycle] -= 25
                                self.enemy3.polygon = self.enemy3.create_polygon(10,0,0,0,0,30,30,30,30,0,20,0,20,10,10,10,fill=Enemy3Color)
                        elif Xpos > Enemies3Xpos[cycle] and Ypos > Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            if rndDir == "X":
                                Enemies3Xpos[cycle] += 25
                                self.enemy3.polygon = self.enemy3.create_polygon(30,10,30,0,0,0,0,30,30,30,30,20,20,20,20,10,fill=Enemy3Color)
                            else:
                                Enemies3Ypos[cycle] += 25
                                self.enemy3.polygon = self.enemy3.create_polygon(20,30,30,30,30,0,0,0,0,30,10,30,10,20,20,20,fill=Enemy3Color)
                        elif Xpos < Enemies3Xpos[cycle] and Ypos == Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            self.enemy3.polygon = self.enemy3.create_polygon(0,20,0,30,30,30,30,0,0,0,0,10,10,10,10,20,fill=Enemy3Color)
                            Enemies3Xpos[cycle] -= 25
                        elif Xpos > Enemies3Xpos[cycle] and Ypos == Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            self.enemy3.polygon = self.enemy3.create_polygon(30,10,30,0,0,0,0,30,30,30,30,20,20,20,20,10,fill=Enemy3Color)
                            Enemies3Xpos[cycle] += 25
                        elif Xpos == Enemies3Xpos[cycle] and Ypos < Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            self.enemy3.polygon = self.enemy3.create_polygon(10,0,0,0,0,30,30,30,30,0,20,0,20,10,10,10,fill=Enemy3Color)
                            Enemies3Ypos[cycle] -= 25
                        elif Xpos == Enemies3Xpos[cycle] and Ypos > Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            self.enemy3.polygon = self.enemy3.create_polygon(20,30,30,30,30,0,0,0,0,30,10,30,10,20,20,20,fill=Enemy3Color)
                            Enemies3Ypos[cycle] += 25
                        self.enemy3.place(x=Enemies3Xpos[cycle],y=Enemies3Ypos[cycle])
                        if Xpos == Enemies3Xpos[cycle] and Ypos == Enemies3Ypos[cycle]:
                            GameOver()
                        cycle += 1

    def Enemy4Move():
        global Xpos
        global Ypos
        global gameover
        global created4
        if gameover != 1:
            self.after(100,Enemy4Move)
            if created4 == 1:
                cycle = 0
                for self.enemy4 in Enemies4:
                    rndDir = random.choice(["X","Y"])
                    Enemy4Color = "darkgreen"
                    if Xpos < Enemies4Xpos[cycle] and Ypos < Enemies4Ypos[cycle]:
                        self.enemy4.delete("all")
                        if rndDir == "X":
                            Enemies4Xpos[cycle] -= 25
                            self.enemy4.polygon = self.enemy4.create_polygon(0,15,15,25,15,17,30,25,30,5,15,13,15,5,fill=Enemy4Color)
                        else:
                            Enemies4Ypos[cycle] -= 25
                            self.enemy4.polygon = self.enemy4.create_polygon(15,0,5,15,12,15,5,30,25,30,17,15,25,15,fill=Enemy4Color)
                    elif Xpos < Enemies4Xpos[cycle] and Ypos > Enemies4Ypos[cycle]:
                        self.enemy4.delete("all")
                        if rndDir == "X":
                            Enemies4Xpos[cycle] -= 25
                            self.enemy4.polygon = self.enemy4.create_polygon(0,15,15,25,15,17,30,25,30,5,15,13,15,5,fill=Enemy4Color)
                        else:
                            Enemies4Ypos[cycle] += 25
                            self.enemy4.polygon = self.enemy4.create_polygon(15,30,25,15,17,15,25,0,5,0,13,15,5,15,fill=Enemy4Color)
                    elif Xpos > Enemies4Xpos[cycle] and Ypos < Enemies4Ypos[cycle]:
                        self.enemy4.delete("all")
                        if rndDir == "X":
                            Enemies4Xpos[cycle] += 25
                            self.enemy4.polygon = self.enemy4.create_polygon(30,15,15,5,15,13,0,5,0,25,15,17,15,25,fill=Enemy4Color)
                        else:
                            Enemies4Ypos[cycle] -= 25
                            self.enemy4.polygon = self.enemy4.create_polygon(15,0,5,15,12,15,5,30,25,30,17,15,25,15,fill=Enemy4Color)
                    elif Xpos > Enemies4Xpos[cycle] and Ypos > Enemies4Ypos[cycle]:
                        self.enemy4.delete("all")
                        if rndDir == "X":
                            Enemies4Xpos[cycle] += 25
                            self.enemy4.polygon = self.enemy4.create_polygon(30,15,15,5,15,13,0,5,0,25,15,17,15,25,fill=Enemy4Color)
                        else:
                            Enemies4Ypos[cycle] += 25
                            self.enemy4.polygon = self.enemy4.create_polygon(15,30,25,15,17,15,25,0,5,0,13,15,5,15,fill=Enemy4Color)
                    elif Xpos < Enemies4Xpos[cycle] and Ypos == Enemies4Ypos[cycle]:
                        self.enemy4.delete("all")
                        self.enemy4.polygon = self.enemy4.create_polygon(0,15,15,25,15,17,30,25,30,5,15,13,15,5,fill=Enemy4Color)
                        Enemies4Xpos[cycle] -= 25
                    elif Xpos > Enemies4Xpos[cycle] and Ypos == Enemies4Ypos[cycle]:
                        self.enemy4.delete("all")
                        self.enemy4.polygon = self.enemy4.create_polygon(30,15,15,5,15,13,0,5,0,25,15,17,15,25,fill=Enemy4Color)
                        Enemies4Xpos[cycle] += 25
                    elif Xpos == Enemies4Xpos[cycle] and Ypos < Enemies4Ypos[cycle]:
                        self.enemy4.delete("all")
                        self.enemy4.polygon = self.enemy4.create_polygon(15,0,5,15,12,15,5,30,25,30,17,15,25,15,fill=Enemy4Color)
                        Enemies4Ypos[cycle] -= 25
                    elif Xpos == Enemies4Xpos[cycle] and Ypos > Enemies4Ypos[cycle]:
                        self.enemy4.delete("all")
                        self.enemy4.polygon = self.enemy4.create_polygon(15,30,25,15,17,15,25,0,5,0,13,15,5,15,fill=Enemy4Color)
                        Enemies4Ypos[cycle] += 25
                    self.enemy4.place(x=Enemies4Xpos[cycle],y=Enemies4Ypos[cycle])
                    if Xpos == Enemies4Xpos[cycle] and Ypos == Enemies4Ypos[cycle]:
                        GameOver()
                    cycle += 1

    def Enemy5Move():
        global Xpos
        global Ypos
        global gameover
        global created5
        if gameover != 1:
            self.after(500,Enemy5Move)
            if created5 == 1:
                cycle = 0
                for self.enemy5 in Enemies5:
                    if (Enemies5Wall[cycle] == "E" or Enemies5Wall[cycle] == "W") and Ypos < Enemies5Ypos[cycle]:
                        Enemies5Ypos[cycle] -= 25
                    elif (Enemies5Wall[cycle] == "E" or Enemies5Wall[cycle] == "W") and Ypos > Enemies5Ypos[cycle]:
                        Enemies5Ypos[cycle] += 25
                    elif Xpos < Enemies5Xpos[cycle] and (Enemies5Wall[cycle] == "N" or Enemies5Wall[cycle] == "S"):
                        Enemies5Xpos[cycle] -= 25
                    elif Xpos > Enemies5Xpos[cycle] and (Enemies5Wall[cycle] == "N" or Enemies5Wall[cycle] == "S"):
                        Enemies5Xpos[cycle] += 25
                    self.enemy5.place(x=Enemies5Xpos[cycle],y=Enemies5Ypos[cycle])
                    if Xpos == Enemies5Xpos[cycle] and Ypos == Enemies5Ypos[cycle]:
                        GameOver()
                    if Enemies5Wall[cycle] == "E" or Enemies5Wall[cycle] == "W":
                        if Enemies5Ypos[cycle] == Ypos:
                            enShoot()
                    else:
                        if Enemies5Xpos[cycle] == Xpos:
                            enShoot()
                    cycle += 1

    def Generate():
        global generated1
        global generated2
        global generated3
        global generated4
        if gameover != 1:
            self.after(10,Generate)
            if generated1 == 0:
                GenerateEnemy1()
                generated1 = 1000
            if generated2 == 0:
                GenerateEnemy2()
                generated2 = 1250
            if generated3 == 0:
                GenerateEnemy3()
                generated3 = 1500
            if generated4 == 0:
                GenerateEnemy4()
                generated4 = 1750
            generated1 -= 10
            generated2 -= 10
            generated3 -= 10
            generated4 -= 10

    def GenerateEnemy1():
        global enXpos
        global enYpos
        global Damage
        global created
        cycle = 0
        for self.enemy6 in Enemies6:
            if Enemies6Type[cycle] == 1:
                enXpos = Enemies6Xpos[cycle]
                enYpos = Enemies6Ypos[cycle]
                self.enemy = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
                self.enemy.place(x=enXpos,y=enYpos)
                self.enemy.polygon = self.enemy.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="darkviolet")
                Enemies.append(self.enemy)
                EnemiesDmg.append(Damage)
                EnemiesXpos.append(enXpos)
                EnemiesYpos.append(enYpos)
                created = 1
            cycle += 1

    def GenerateEnemy2():
        global en2Xpos
        global en2Ypos
        global created2
        cycle = 0
        for self.enemy6 in Enemies6:
            if Enemies6Type[cycle] == 2:
                en2Xpos = Enemies6Xpos[cycle]
                en2Ypos = Enemies6Ypos[cycle]
                self.enemy2 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
                self.enemy2.place(x=en2Xpos,y=en2Ypos)
                self.enemy2.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="red")
                Enemies2.append(self.enemy2)
                Enemies2Xpos.append(en2Xpos)
                Enemies2Ypos.append(en2Ypos)
                created2 = 1
            cycle += 1

    def GenerateEnemy3():
        global en3Xpos
        global en3Ypos
        global Damage3
        global created3
        cycle = 0
        for self.enemy6 in Enemies6:
            if Enemies6Type[cycle] == 3:
                en3Xpos = Enemies6Xpos[cycle]
                en3Ypos = Enemies6Ypos[cycle]
                self.enemy3 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
                self.enemy3.place(x=en3Xpos,y=en3Ypos)
                self.enemy3.polygon = self.enemy3.create_polygon(10,0,0,0,0,30,30,30,30,0,20,0,20,10,10,10,fill="navy")
                Enemies3.append(self.enemy3)
                Enemies3Dmg.append(Damage3)
                Enemies3Xpos.append(en3Xpos)
                Enemies3Ypos.append(en3Ypos)
                created3 = 1
            cycle += 1

    def GenerateEnemy4():
        global en4Xpos
        global en4Ypos
        global created4
        cycle = 0
        for self.enemy6 in Enemies6:
            if Enemies6Type[cycle] == 4:
                en4Xpos = Enemies6Xpos[cycle]
                en4Ypos = Enemies6Ypos[cycle]
                self.enemy4 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
                self.enemy4.place(x=en4Xpos,y=en4Ypos)
                self.enemy4.create_polygon(15,0,5,15,12,15,5,30,25,30,17,15,25,15,fill="darkgreen")
                Enemies4.append(self.enemy4)
                Enemies4Xpos.append(en4Xpos)
                Enemies4Ypos.append(en4Ypos)
                created4 = 1
            cycle += 1

    def Shoot(event):
        global Xpos
        global Ypos
        global direction
        global start
        if direction == "N":
            shotXpos = Xpos + 10
            shotYpos = Ypos - 10
        elif direction == "E":
            shotXpos = Xpos + 30
            shotYpos = Ypos + 10
        elif direction == "S":
            shotXpos = Xpos + 10
            shotYpos = Ypos + 30
        elif direction == "W":
            shotXpos = Xpos - 10
            shotYpos = Ypos + 10
        self.shot = Canvas(bg="black",highlightthickness=0,width=10,height=10)
        self.shot.place(x=shotXpos,y=shotYpos)
        self.shot.create_oval(0,0,10,10,fill="white")
        Shots.append(self.shot)
        ShotsXpos.append(shotXpos)
        ShotsYpos.append(shotYpos)
        ShotDir.append(direction)
        if start == 0:
            NextWave()
        start = 1

    def enShoot():
        cycle = 0
        for self.enemy5 in Enemies5:
            if Enemies5Wall[cycle] == "N":
                enDir = "S"
                enShotXpos = Enemies5Xpos[cycle] + 10
                enShotYpos = Enemies5Ypos[cycle] + 30
            elif Enemies5Wall[cycle] == "E":
                enDir = "W"
                enShotXpos = Enemies5Xpos[cycle] - 10
                enShotYpos = Enemies5Ypos[cycle] + 10
            elif Enemies5Wall[cycle] == "S":
                enDir = "N"
                enShotXpos = Enemies5Xpos[cycle] + 10
                enShotYpos = Enemies5Ypos[cycle] - 10
            elif Enemies5Wall[cycle] == "W":
                enDir = "E"
                enShotXpos = Enemies5Xpos[cycle] + 30
                enShotYpos = Enemies5Ypos[cycle] + 10
            if Enemies5Wall[cycle] == "E" or Enemies5Wall[cycle] == "W":
                if Enemies5Ypos[cycle] == Ypos:
                    self.enShot = Canvas(bg="black",highlightthickness=0,width=10,height=10)
                    self.enShot.place(x=enShotXpos,y=enShotYpos)
                    self.enShot.create_oval(0,0,10,10,fill="yellow")
                    enShots.append(self.enShot)
                    enShotsXpos.append(enShotXpos)
                    enShotsYpos.append(enShotYpos)
                    enShotDir.append(enDir)
            else:
                if Enemies5Xpos[cycle] == Xpos:
                    self.enShot = Canvas(bg="black",highlightthickness=0,width=10,height=10)
                    self.enShot.place(x=enShotXpos,y=enShotYpos)
                    self.enShot.create_oval(0,0,10,10,fill="yellow")
                    enShots.append(self.enShot)
                    enShotsXpos.append(enShotXpos)
                    enShotsYpos.append(enShotYpos)
                    enShotDir.append(enDir)
            cycle += 1
            
    def ShotMove():
        global direction
        global en2Xpos
        global en2Ypos
        global destroy
        global gameover
        if gameover != 1:
            self.after(10,ShotMove)
            #Move Shots
            cycle = 0
            for self.shot in Shots:
                destroy = -1
                if ShotDir[cycle] == "N":
                    ShotsYpos[cycle] -= 10
                elif ShotDir[cycle] == "E":
                    ShotsXpos[cycle] += 10
                elif ShotDir[cycle] == "S":
                    ShotsYpos[cycle] += 10
                elif ShotDir[cycle] == "W":
                    ShotsXpos[cycle] -= 10
                self.shot.place(x=ShotsXpos[cycle],y=ShotsYpos[cycle])
                #Damage Enemy1
                enCycle = 0
                for self.enemy in Enemies:
                    if destroy == -1:
                        if EnemiesXpos[enCycle] + 30 >= ShotsXpos[cycle] >= EnemiesXpos[enCycle] - 10 and EnemiesYpos[enCycle] + 30 >= ShotsYpos[cycle] >= EnemiesYpos[enCycle] - 10:
                            destroy = 0
                            if EnemiesDmg[enCycle] == 1:
                                self.explode = Canvas(bg="black",highlightthickness=0,width=30,height=30)
                                self.explode.place(x=EnemiesXpos[enCycle],y=EnemiesYpos[enCycle])
                                self.explode.create_polygon(0,15,13,13,15,0,17,13,30,15,17,17,15,30,13,17,fill="orange")
                                Explosions.append(self.explode)
                                self.enemy.destroy()
                                del Enemies[enCycle]
                                del EnemiesDmg[enCycle]
                                del EnemiesXpos[enCycle]
                                del EnemiesYpos[enCycle]
                                self.after(10,destroyEnemy)
                                self.shot.destroy()
                                del Shots[cycle]
                                del ShotsXpos[cycle]
                                del ShotsYpos[cycle]
                                del ShotDir[cycle]
                            else:
                                self.shot.destroy()
                                del Shots[cycle]
                                del ShotsXpos[cycle]
                                del ShotsYpos[cycle]
                                del ShotDir[cycle]
                                EnemiesDmg[enCycle] += 1
                                if EnemiesDmg[enCycle] == 0:
                                    EnemyColor = "darkviolet"
                                else:
                                    EnemyColor = "violet"
                                self.enemy.itemconfig(self.enemy.polygon,fill=EnemyColor)
                        enCycle += 1
                #Damage Enemy2
                enCycle = 0
                for self.enemy2 in Enemies2:
                    if destroy == -1:
                        if Enemies2Xpos[enCycle] + 30 >= ShotsXpos[cycle] >= Enemies2Xpos[enCycle] - 10 and Enemies2Ypos[enCycle] + 30 >= ShotsYpos[cycle] >= Enemies2Ypos[enCycle] - 10:
                            destroy = 0
                            self.explode = Canvas(bg="black",highlightthickness=0,width=30,height=30)
                            self.explode.place(x=Enemies2Xpos[enCycle],y=Enemies2Ypos[enCycle])
                            self.explode.create_polygon(0,15,13,13,15,0,17,13,30,15,17,17,15,30,13,17,fill="orange")
                            Explosions.append(self.explode)
                            self.enemy2.destroy()
                            del Enemies2[enCycle]
                            del Enemies2Xpos[enCycle]
                            del Enemies2Ypos[enCycle]
                            self.shot.destroy()
                            del Shots[cycle]
                            del ShotsXpos[cycle]
                            del ShotsYpos[cycle]
                            del ShotDir[cycle]
                            self.after(10,destroyEnemy)
                        enCycle += 1
                #Damage Enemy3
                enCycle = 0
                for self.enemy3 in Enemies3:
                    if destroy == -1:
                        if Enemies3Xpos[enCycle] + 30 >= ShotsXpos[cycle] >= Enemies3Xpos[enCycle] - 10 and Enemies3Ypos[enCycle] + 30 >= ShotsYpos[cycle] >= Enemies3Ypos[enCycle] - 10:
                            destroy = 0
                            if Enemies3Dmg[enCycle] == 4:
                                self.explode = Canvas(bg="black",highlightthickness=0,width=30,height=30)
                                self.explode.place(x=Enemies3Xpos[enCycle],y=Enemies3Ypos[enCycle])
                                self.explode.create_polygon(0,15,13,13,15,0,17,13,30,15,17,17,15,30,13,17,fill="orange")
                                Explosions.append(self.explode)
                                self.enemy3.destroy()
                                del Enemies3[enCycle]
                                del Enemies3Dmg[enCycle]
                                del Enemies3Xpos[enCycle]
                                del Enemies3Ypos[enCycle]
                                self.after(10,destroyEnemy)
                                self.shot.destroy()
                                del Shots[cycle]
                                del ShotsXpos[cycle]
                                del ShotsYpos[cycle]
                                del ShotDir[cycle]
                            else:
                                self.shot.destroy()
                                del Shots[cycle]
                                del ShotsXpos[cycle]
                                del ShotsYpos[cycle]
                                del ShotDir[cycle]
                                Enemies3Dmg[enCycle] += 1
                                if Enemies3Dmg[enCycle] == 0:
                                    Enemy3Color = "navy"
                                elif Enemies3Dmg[enCycle] == 1:
                                    Enemy3Color = "darkblue"
                                elif Enemies3Dmg[enCycle] == 2:
                                    Enemy3Color = "dodgerblue"
                                elif Enemies3Dmg[enCycle] == 3:
                                    Enemy3Color = "deepskyblue"
                                else:
                                    Enemy3Color = "lightskyblue"
                                self.enemy3.itemconfig(self.enemy3.polygon,fill=Enemy3Color)
                        enCycle += 1
                #Damage Enemy4
                enCycle = 0
                for self.enemy4 in Enemies4:
                    if destroy == -1:
                        if Enemies4Xpos[enCycle] + 30 >= ShotsXpos[cycle] >= Enemies4Xpos[enCycle] - 10 and Enemies4Ypos[enCycle] + 30 >= ShotsYpos[cycle] >= Enemies4Ypos[enCycle] - 10:
                            destroy = 0
                            self.explode = Canvas(bg="black",highlightthickness=0,width=30,height=30)
                            self.explode.place(x=Enemies4Xpos[enCycle],y=Enemies4Ypos[enCycle])
                            self.explode.create_polygon(0,15,13,13,15,0,17,13,30,15,17,17,15,30,13,17,fill="orange")
                            Explosions.append(self.explode)
                            self.enemy4.destroy()
                            del Enemies4[enCycle]
                            del Enemies4Xpos[enCycle]
                            del Enemies4Ypos[enCycle]
                            self.shot.destroy()
                            del Shots[cycle]
                            del ShotsXpos[cycle]
                            del ShotsYpos[cycle]
                            del ShotDir[cycle]
                            self.after(10,destroyEnemy)
                        enCycle += 1
                #Damage Enemy5
                enCycle = 0
                for self.enemy5 in Enemies5:
                    if destroy == -1:
                        if Enemies5Xpos[enCycle] + 30 >= ShotsXpos[cycle] >= Enemies5Xpos[enCycle] - 10 and Enemies5Ypos[enCycle] + 30 >= ShotsYpos[cycle] >= Enemies5Ypos[enCycle] - 10:
                            destroy = 0
                            if Enemies5Dmg[enCycle] == 1:
                                self.explode = Canvas(bg="black",highlightthickness=0,width=30,height=30)
                                self.explode.place(x=Enemies5Xpos[enCycle],y=Enemies5Ypos[enCycle])
                                self.explode.create_polygon(0,15,13,13,15,0,17,13,30,15,17,17,15,30,13,17,fill="orange")
                                Explosions.append(self.explode)
                                self.enemy5.destroy()
                                del Enemies5[enCycle]
                                del Enemies5Dmg[enCycle]
                                del Enemies5Xpos[enCycle]
                                del Enemies5Ypos[enCycle]
                                del Enemies5Wall[enCycle]
                                self.after(10,destroyEnemy)
                                self.shot.destroy()
                                del Shots[cycle]
                                del ShotsXpos[cycle]
                                del ShotsYpos[cycle]
                                del ShotDir[cycle]
                            else:
                                self.shot.destroy()
                                del Shots[cycle]
                                del ShotsXpos[cycle]
                                del ShotsYpos[cycle]
                                del ShotDir[cycle]
                                Enemies5Dmg[enCycle] += 1
                                if Enemies5Dmg[enCycle] == 0:
                                    Enemy5Color = "darkorange2"
                                else:
                                    Enemy5Color = "orange"
                                self.enemy5.itemconfig(self.enemy5.polygon,fill=Enemy5Color)
                        enCycle += 1
                #Damage Enemy6
                enCycle = 0
                for self.enemy6 in Enemies6:
                    if destroy == -1:
                        if Enemies6Xpos[enCycle] + 30 >= ShotsXpos[cycle] >= Enemies6Xpos[enCycle] - 10 and Enemies6Ypos[enCycle] + 30 >= ShotsYpos[cycle] >= Enemies6Ypos[enCycle] - 10:
                            destroy = 0
                            if Enemies6Dmg[enCycle] == 5:
                                self.explode = Canvas(bg="black",highlightthickness=0,width=30,height=30)
                                self.explode.place(x=Enemies6Xpos[enCycle],y=Enemies6Ypos[enCycle])
                                self.explode.create_polygon(0,15,13,13,15,0,17,13,30,15,17,17,15,30,13,17,fill="orange")
                                Explosions.append(self.explode)
                                self.enemy6.destroy()
                                del Enemies6[enCycle]
                                del Enemies6Dmg[enCycle]
                                del Enemies6Xpos[enCycle]
                                del Enemies6Ypos[enCycle]
                                del Enemies6Type[enCycle]
                                self.after(10,destroyEnemy)
                                self.shot.destroy()
                                del Shots[cycle]
                                del ShotsXpos[cycle]
                                del ShotsYpos[cycle]
                                del ShotDir[cycle]
                            else:
                                self.shot.destroy()
                                del Shots[cycle]
                                del ShotsXpos[cycle]
                                del ShotsYpos[cycle]
                                del ShotDir[cycle]
                                Enemies6Dmg[enCycle] += 1
                                if Enemies6Dmg[enCycle] == 0:
                                    Enemy6Color = "gray20"
                                elif Enemies6Dmg[enCycle] == 1:
                                    Enemy6Color = "gray30"
                                elif Enemies6Dmg[enCycle] == 2:
                                    Enemy6Color = "gray40"
                                elif Enemies6Dmg[enCycle] == 3:
                                    Enemy6Color = "gray50"
                                elif Enemies6Dmg[enCycle] == 4:
                                    Enemy6Color = "gray60"
                                elif Enemies6Dmg[enCycle] == 5:
                                    Enemy6Color = "gray70"
                                self.enemy6.itemconfig(self.enemy6.oval,fill=Enemy6Color)
                        enCycle += 1
                #Destroy Shot at Boundary
                if destroy == -1:
                    if ShotsXpos[cycle] < 0 or ShotsXpos[cycle] > 830 or ShotsYpos[cycle] < 0 or ShotsYpos[cycle] > 680:
                        self.shot.destroy()
                        del Shots[cycle]
                        del ShotsXpos[cycle]
                        del ShotsYpos[cycle]
                        del ShotDir[cycle]
                cycle += 1

    def enShotMove():
        global gameover
        if gameover != 1:
            self.after(10,enShotMove)
            cycle = 0
            for self.enShot in enShots:
                enDestroy = -1
                if enShotDir[cycle] == "N":
                    enShotsYpos[cycle] -= 10
                elif enShotDir[cycle] == "E":
                    enShotsXpos[cycle] += 10
                elif enShotDir[cycle] == "S":
                    enShotsYpos[cycle] += 10
                elif enShotDir[cycle] == "W":
                    enShotsXpos[cycle] -= 10
                self.enShot.place(x=enShotsXpos[cycle],y=enShotsYpos[cycle])
                #Game Over
                if Xpos + 30 >= enShotsXpos[cycle] >= Xpos - 10 and Ypos + 30 >= enShotsYpos[cycle] >= Ypos - 10:
                    enDestroy = 0
                    self.enShot.destroy()
                    del enShots[cycle]
                    del enShotsXpos[cycle]
                    del enShotsYpos[cycle]
                    del enShotDir[cycle]
                    GameOver()
                #Destroy Shot at Boundary
                if enDestroy == -1:
                    if enShotsXpos[cycle] < 0 or enShotsXpos[cycle] > 830 or enShotsYpos[cycle] < 0 or enShotsYpos[cycle] > 680:
                        self.enShot.destroy()
                        del enShots[cycle]
                        del enShotsXpos[cycle]
                        del enShotsYpos[cycle]
                        del enShotDir[cycle] 
                cycle += 1

    def destroyEnemy():
        destroyed = 0
        for self.explode in Explosions:
            self.explode.destroy()
            del Explosions[destroyed]
            destroyed += 1            

    def Summon():
        global wave
        time = 0
        wave += 1
        #Wave 1
        if wave == 1:
            E = 0
            while E < W1E1:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < W1E2:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
            E = 0
            while E < W1E3:
                self.after(time,CreateEnemy3)
                E += 1
                time += 250
            E = 0
            while E < W1E4:
                self.after(time,CreateEnemy4)
                E += 1
                time += 250
            E = 0
            while E < W1E5:
                self.after(time,CreateEnemy5)
                E += 1
                time += 250
            E = 0
            while E < W1E6:
                self.after(time,CreateEnemy6)
                E += 1
                time += 250
        #Wave 2
        if wave == 2:
            E = 0
            while E < W2E1:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < W2E2:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
            E = 0
            while E < W2E3:
                self.after(time,CreateEnemy3)
                E += 1
                time += 250
            E = 0
            while E < W2E4:
                self.after(time,CreateEnemy4)
                E += 1
                time += 250
            E = 0
            while E < W2E5:
                self.after(time,CreateEnemy5)
                E += 1
                time += 250
            E = 0
            while E < W2E6:
                self.after(time,CreateEnemy6)
                E += 1
                time += 250
        #Wave 3
        if wave == 3:
            E = 0
            while E < W3E1:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < W3E2:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
            E = 0
            while E < W3E3:
                self.after(time,CreateEnemy3)
                E += 1
                time += 250
            E = 0
            while E < W3E4:
                self.after(time,CreateEnemy4)
                E += 1
                time += 250
            E = 0
            while E < W3E5:
                self.after(time,CreateEnemy5)
                E += 1
                time += 250
            E = 0
            while E < W3E6:
                self.after(time,CreateEnemy6)
                E += 1
                time += 250
        #Wave 4
        if wave == 4:
            E = 0
            while E < W4E1:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < W4E2:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
            E = 0
            while E < W4E3:
                self.after(time,CreateEnemy3)
                E += 1
                time += 250
            E = 0
            while E < W4E4:
                self.after(time,CreateEnemy4)
                E += 1
                time += 250
            E = 0
            while E < W4E5:
                self.after(time,CreateEnemy5)
                E += 1
                time += 250
            E = 0
            while E < W4E6:
                self.after(time,CreateEnemy6)
                E += 1
                time += 250
        #Wave 5
        if wave == 5:
            E = 0
            while E < W5E1:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < W5E2:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
            E = 0
            while E < W5E3:
                self.after(time,CreateEnemy3)
                E += 1
                time += 250
            E = 0
            while E < W5E4:
                self.after(time,CreateEnemy4)
                E += 1
                time += 250
            E = 0
            while E < W5E5:
                self.after(time,CreateEnemy5)
                E += 1
                time += 250
            E = 0
            while E < W5E6:
                self.after(time,CreateEnemy6)
                E += 1
                time += 250
        #Wave 6
        if wave == 6:
            E = 0
            while E < W6E1:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < W6E2:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
            E = 0
            while E < W6E3:
                self.after(time,CreateEnemy3)
                E += 1
                time += 250
            E = 0
            while E < W6E4:
                self.after(time,CreateEnemy4)
                E += 1
                time += 250
            E = 0
            while E < W6E5:
                self.after(time,CreateEnemy5)
                E += 1
                time += 250
            E = 0
            while E < W6E6:
                self.after(time,CreateEnemy6)
                E += 1
                time += 250
        #Wave 7
        if wave == 7:
            E = 0
            while E < W7E1:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < W7E2:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
            E = 0
            while E < W7E3:
                self.after(time,CreateEnemy3)
                E += 1
                time += 250
            E = 0
            while E < W7E4:
                self.after(time,CreateEnemy4)
                E += 1
                time += 250
            E = 0
            while E < W7E5:
                self.after(time,CreateEnemy5)
                E += 1
                time += 250
            E = 0
            while E < W7E6:
                self.after(time,CreateEnemy6)
                E += 1
                time += 250
        #Wave 8
        if wave == 8:
            E = 0
            while E < W8E1:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < W8E2:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
            E = 0
            while E < W8E3:
                self.after(time,CreateEnemy3)
                E += 1
                time += 250
            E = 0
            while E < W8E4:
                self.after(time,CreateEnemy4)
                E += 1
                time += 250
            E = 0
            while E < W8E5:
                self.after(time,CreateEnemy5)
                E += 1
                time += 250
            E = 0
            while E < W8E6:
                self.after(time,CreateEnemy6)
                E += 1
                time += 250
        #Wave 9
        if wave == 9:
            E = 0
            while E < W9E1:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < W9E2:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
            E = 0
            while E < W9E3:
                self.after(time,CreateEnemy3)
                E += 1
                time += 250
            E = 0
            while E < W9E4:
                self.after(time,CreateEnemy4)
                E += 1
                time += 250
            E = 0
            while E < W9E5:
                self.after(time,CreateEnemy5)
                E += 1
                time += 250
            E = 0
            while E < W9E6:
                self.after(time,CreateEnemy6)
                E += 1
                time += 250
        #Wave 10
        if wave == 10:
            E = 0
            while E < W10E1:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < W10E2:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
            E = 0
            while E < W10E3:
                self.after(time,CreateEnemy3)
                E += 1
                time += 250
            E = 0
            while E < W10E4:
                self.after(time,CreateEnemy4)
                E += 1
                time += 250
            E = 0
            while E < W10E5:
                self.after(time,CreateEnemy5)
                E += 1
                time += 250
            E = 0
            while E < W10E6:
                self.after(time,CreateEnemy6)
                E += 1
                time += 250
        #Win
        if wave == 11:
            Winner()

    def NextWave():
        global wave
        global gameover
        if gameover == 0:
            self.after(10,NextWave)
            if not Enemies and not Enemies2 and not Enemies3 and not Enemies4 and not Enemies5 and not Enemies6:
                Summon()
                if wave != 11:
                    self.lbScore.config(text="Wave: "+str(wave)+"  Press 'p' to pause")

    def Winner():
        global gameover
        if gameover == 0:
            gameover = 1
            self.unbind('<Left>')
            self.unbind('<Right>')
            self.unbind('<Up>')
            self.unbind('<Down>')
            self.unbind('<space>')
            self.after_cancel(EnemyMove)
            self.after_cancel(Enemy2Move)
            self.after_cancel(Enemy3Move)
            self.after_cancel(Enemy4Move)
            self.after_cancel(Enemy5Move)
            self.after_cancel(CreateEnemy)
            self.after_cancel(CreateEnemy2)
            self.after_cancel(CreateEnemy3)
            self.after_cancel(CreateEnemy4)
            self.after_cancel(CreateEnemy5)
            self.after_cancel(CreateEnemy6)
            self.after_cancel(Generate)
            self.after_cancel(NextWave)
            self.after_cancel(ShotMove)
            self.after_cancel(enShotMove)
            for self.shot in Shots:
                self.shot.destroy()
            self.lbScore.destroy()
            self.lbWinner = Label(text="You Win!!!",bg="black",fg="white")
            self.lbWinner.pack(fill=BOTH,expand=1)
            self.btnMainMenu = Button(text="Main Menu")
            self.btnMainMenu.pack(side=LEFT)
            self.btnMainMenu.bind('<Button>',StartMainMenu)

    def GameOver():
        global gameover
        global wave
        if gameover == 0:
            gameover = 1
            self.unbind('<Left>')
            self.unbind('<Right>')
            self.unbind('<Up>')
            self.unbind('<Down>')
            self.unbind('<space>')
            self.after_cancel(EnemyMove)
            self.after_cancel(Enemy2Move)
            self.after_cancel(Enemy3Move)
            self.after_cancel(Enemy4Move)
            self.after_cancel(Enemy5Move)
            self.after_cancel(CreateEnemy)
            self.after_cancel(CreateEnemy2)
            self.after_cancel(CreateEnemy3)
            self.after_cancel(CreateEnemy4)
            self.after_cancel(CreateEnemy5)
            self.after_cancel(CreateEnemy6)
            self.after_cancel(Generate)
            self.after_cancel(NextWave)
            self.after_cancel(ShotMove)
            self.after_cancel(enShotMove)
            for self.shot in Shots:
                self.shot.destroy()
            self.lbScore.destroy()
            self.lbGameOver = Label(text="Game Over" + "\n" "You survived to wave " + str(wave) + "\n" + "Click here to restart",bg="black",fg="white")
            self.lbGameOver.pack(fill=BOTH,expand=1)
            self.lbGameOver.bind('<Button>',Restart)
            self.btnMainMenu = Button(text="Main Menu")
            self.btnMainMenu.pack(side=LEFT)
            self.btnMainMenu.bind('<Button>',StartMainMenu)

    def Restart(event):
        self.destroy()
        TenWaveChallengeSinglePlayer()

    def Pause(event):
        global pause
        global gameover
        if pause == 0:
            gameover = 1
            pause = 1
            self.unbind('<Left>')
            self.unbind('<Right>')
            self.unbind('<Up>')
            self.unbind('<Down>')
            self.unbind('<space>')
            self.after_cancel(EnemyMove)
            self.after_cancel(Enemy2Move)
            self.after_cancel(Enemy3Move)
            self.after_cancel(Enemy4Move)
            self.after_cancel(Enemy5Move)
            self.after_cancel(CreateEnemy)
            self.after_cancel(CreateEnemy2)
            self.after_cancel(CreateEnemy3)
            self.after_cancel(CreateEnemy4)
            self.after_cancel(CreateEnemy5)
            self.after_cancel(CreateEnemy6)
            self.after_cancel(Generate)
            self.after_cancel(NextWave)
            self.after_cancel(ShotMove)
            self.after_cancel(enShotMove)
            for self.shot in Shots:
                self.shot.destroy()
            self.lbScore.destroy()
            self.lbPause = Label(text="Paused"+"\n"+"Press 'p' to Unpause",bg="black",fg="white")
            self.lbPause.pack(fill=BOTH,expand=1)
            self.btnMainMenu = Button(text="Main Menu")
            self.btnMainMenu.pack(side=LEFT)
            self.btnMainMenu.bind('<Button>',StartMainMenu)
        elif pause == 1:
            gameover = 0
            pause = 0
            self.bind('<Left>',LeftKey)
            self.bind('<Right>',RightKey)
            self.bind('<Up>',UpKey)
            self.bind('<Down>',DownKey)
            self.bind('<space>',Shoot)
            EnemyMove()
            Enemy2Move()
            Enemy3Move()
            Enemy4Move()
            Enemy5Move()
            Generate()
            ShotMove()
            enShotMove()
            self.lbScore = Label(text="Wave: "+str(wave)+"  Press 'p' to pause",bg="black",fg="white")
            self.lbScore.place(x=165,y=680,width=500,height=20)
            NextWave()
            self.lbPause.destroy()
            self.btnMainMenu.unbind('<Button>')
            self.btnMainMenu.destroy()

    def Exit(event):
        self.destroy()

    def StartMainMenu(event):
        self.destroy()
        MainMenu()

    #Bindings
    self.bind('<Left>',LeftKey)
    self.bind('<Right>',RightKey)
    self.bind('<Up>',UpKey)
    self.bind('<Down>',DownKey)
    self.bind('<Escape>',Exit)
    self.bind('<space>',Shoot)
    self.bind('<p>',Pause)

    EnemyMove()
    Enemy2Move()
    Enemy3Move()
    Enemy4Move()
    Enemy5Move()
    Generate()
    ShotMove()
    enShotMove()
        
    #Frame settings
    self.geometry("830x700")
    self.title("Space Assault")
    self.configure(bg="black")

def TenWaveChallengeMultiPlayerChooseEnemies():
    self = Tk()

    #Variables
    global W1E1
    global W1E2
    global W1E3
    global W1E4
    global W1E5
    global W1E6
    global W2E1
    global W2E2
    global W2E3
    global W2E4
    global W2E5
    global W2E6
    global W3E1
    global W3E2
    global W3E3
    global W3E4
    global W3E5
    global W3E6
    global W4E1
    global W4E2
    global W4E3
    global W4E4
    global W4E5
    global W4E6
    global W5E1
    global W5E2
    global W5E3
    global W5E4
    global W5E5
    global W5E6
    global W6E1
    global W6E2
    global W6E3
    global W6E4
    global W6E5
    global W6E6
    global W7E1
    global W7E2
    global W7E3
    global W7E4
    global W7E5
    global W7E6
    global W8E1
    global W8E2
    global W8E3
    global W8E4
    global W8E5
    global W8E6
    global W9E1
    global W9E2
    global W9E3
    global W9E4
    global W9E5
    global W9E6
    global W10E1
    global W10E2
    global W10E3
    global W10E4
    global W10E5
    global W10E6
    W1E1 = 0
    W1E2 = 0
    W1E3 = 0
    W1E4 = 0
    W1E5 = 0
    W1E6 = 0
    W2E1 = 0
    W2E2 = 0
    W2E3 = 0
    W2E4 = 0
    W2E5 = 0
    W2E6 = 0
    W3E1 = 0
    W3E2 = 0
    W3E3 = 0
    W3E4 = 0
    W3E5 = 0
    W3E6 = 0
    W4E1 = 0
    W4E2 = 0
    W4E3 = 0
    W4E4 = 0
    W4E5 = 0
    W4E6 = 0
    W5E1 = 0
    W5E2 = 0
    W5E3 = 0
    W5E4 = 0
    W5E5 = 0
    W5E6 = 0
    W6E1 = 0
    W6E2 = 0
    W6E3 = 0
    W6E4 = 0
    W6E5 = 0
    W6E6 = 0
    W7E1 = 0
    W7E2 = 0
    W7E3 = 0
    W7E4 = 0
    W7E5 = 0
    W7E6 = 0
    W8E1 = 0
    W8E2 = 0
    W8E3 = 0
    W8E4 = 0
    W8E5 = 0
    W8E6 = 0
    W9E1 = 0
    W9E2 = 0
    W9E3 = 0
    W9E4 = 0
    W9E5 = 0
    W9E6 = 0
    W10E1 = 0
    W10E2 = 0
    W10E3 = 0
    W10E4 = 0
    W10E5 = 0
    W10E6 = 0

    #Objects
    self.lbDirections = Label(text="Choose what enemies are in each wave",bg="black",fg="white")
    self.lbDirections.pack()
    self.btnMainMenu = Button(text="Main Menu")
    self.btnMainMenu.place(x=0,y=680,width=100,height=20)
    self.lbWave1 = Label(text="Wave 1",bg="black",fg="white")
    self.lbWave1.place(x=115,y=680,width=60,height=20)
    self.lbWave2 = Label(text="Wave 2",bg="black",fg="white")
    self.lbWave2.place(x=175,y=680,width=60,height=20)
    self.lbWave3 = Label(text="Wave 3",bg="black",fg="white")
    self.lbWave3.place(x=235,y=680,width=60,height=20)
    self.lbWave4 = Label(text="Wave 4",bg="black",fg="white")
    self.lbWave4.place(x=295,y=680,width=60,height=20)
    self.lbWave5 = Label(text="Wave 5",bg="black",fg="white")
    self.lbWave5.place(x=355,y=680,width=60,height=20)
    self.lbWave6 = Label(text="Wave 6",bg="black",fg="white")
    self.lbWave6.place(x=415,y=680,width=60,height=20)
    self.lbWave7 = Label(text="Wave 7",bg="black",fg="white")
    self.lbWave7.place(x=475,y=680,width=60,height=20)
    self.lbWave8 = Label(text="Wave 8",bg="black",fg="white")
    self.lbWave8.place(x=535,y=680,width=60,height=20)
    self.lbWave9 = Label(text="Wave 9",bg="black",fg="white")
    self.lbWave9.place(x=595,y=680,width=60,height=20)
    self.lbWave10 = Label(text="Wave 10",bg="black",fg="white")
    self.lbWave10.place(x=655,y=680,width=60,height=20)
    self.btnPlayMultiPlayer = Button(text="Play")
    self.btnPlayMultiPlayer.place(x=730,y=680,width=100,height=20)
    self.enemy1Up = Canvas(bg="black",highlightthickness=0)
    self.enemy1Up.place(x=90,y=300,width=30,height=30)
    self.enemy1Up.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="darkviolet")
    self.enemy1num = Label(text="0",bg="black",fg="white")
    self.enemy1num.place(x=90,y=330,width=30,height=20)
    self.enemy1Down = Canvas(bg="black",highlightthickness=0)
    self.enemy1Down.place(x=90,y=350,width=30,height=30)
    self.enemy1Down.create_polygon(15,30,30,0,15,15,0,0,15,30,fill="darkviolet")
    self.enemy2Up = Canvas(bg="black",highlightthickness=0)
    self.enemy2Up.place(x=210,y=300,width=30,height=30)
    self.enemy2Up.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="red")
    self.enemy2num = Label(text="0",bg="black",fg="white")
    self.enemy2num.place(x=210,y=330,width=30,height=20)
    self.enemy2Down = Canvas(bg="black",highlightthickness=0)
    self.enemy2Down.place(x=210,y=350,width=30,height=30)
    self.enemy2Down.create_polygon(15,30,30,0,15,15,0,0,15,30,fill="red")
    self.enemy3Up = Canvas(bg="black",highlightthickness=0)
    self.enemy3Up.place(x=330,y=300,width=30,height=30)
    self.enemy3Up.create_polygon(10,0,0,0,0,30,30,30,30,0,20,0,20,10,10,10,fill="navy")
    self.enemy3num = Label(text="0",bg="black",fg="white")
    self.enemy3num.place(x=330,y=330,width=30,height=20)
    self.enemy3Down = Canvas(bg="black",highlightthickness=0)
    self.enemy3Down.place(x=330,y=350,width=30,height=30)
    self.enemy3Down.create_polygon(20,30,30,30,30,0,0,0,0,30,10,30,10,20,20,20,fill="navy")
    self.enemy4Up = Canvas(bg="black",highlightthickness=0)
    self.enemy4Up.place(x=450,y=300,width=30,height=30)
    self.enemy4Up.create_polygon(15,0,5,15,12,15,5,30,25,30,17,15,25,15,fill="darkgreen")
    self.enemy4num = Label(text="0",bg="black",fg="white")
    self.enemy4num.place(x=450,y=330,width=30,height=20)
    self.enemy4Down = Canvas(bg="black",highlightthickness=0)
    self.enemy4Down.place(x=450,y=350,width=30,height=30)
    self.enemy4Down.create_polygon(15,30,25,15,17,15,25,0,5,0,13,15,5,15,fill="darkgreen")
    self.enemy5Up = Canvas(bg="black",highlightthickness=0)
    self.enemy5Up.place(x=570,y=300,width=30,height=30)
    self.enemy5Up.create_polygon(30,30,20,15,20,0,10,0,10,15,0,30,fill="darkorange2")
    self.enemy5num = Label(text="0",bg="black",fg="white")
    self.enemy5num.place(x=570,y=330,width=30,height=20)
    self.enemy5Down = Canvas(bg="black",highlightthickness=0)
    self.enemy5Down.place(x=570,y=350,width=30,height=30)
    self.enemy5Down.create_polygon(0,0,10,15,10,30,20,30,20,15,30,0,fill="darkorange2")
    self.enemy6Up = Canvas(bg="black",highlightthickness=0)
    self.enemy6Up.place(x=690,y=300,width=30,height=30)
    self.enemy6Up.create_oval(0,0,30,30,fill="gray20")
    self.enemy6num = Label(text="0",bg="black",fg="white")
    self.enemy6num.place(x=690,y=330,width=30,height=20)
    self.enemy6Down = Canvas(bg="black",highlightthickness=0)
    self.enemy6Down.place(x=690,y=350,width=30,height=30)
    self.enemy6Down.create_oval(0,0,30,30,fill="gray20")
    
    #Functions
    def StartMainMenu(event):
        self.destroy()
        MainMenu()
    
    def Wave1(*args):
        global W1E1
        global W1E2
        global W1E3
        global W1E4
        global W1E5
        global W1E6
        self.lbWave1.config(bg="darkblue")
        self.lbWave2.config(bg="black")
        self.lbWave3.config(bg="black")
        self.lbWave4.config(bg="black")
        self.lbWave5.config(bg="black")
        self.lbWave6.config(bg="black")
        self.lbWave7.config(bg="black")
        self.lbWave8.config(bg="black")
        self.lbWave9.config(bg="black")
        self.lbWave10.config(bg="black")
        self.enemy1Up.unbind('<Button>')
        self.enemy2Up.unbind('<Button>')
        self.enemy3Up.unbind('<Button>')
        self.enemy4Up.unbind('<Button>')
        self.enemy5Up.unbind('<Button>')
        self.enemy6Up.unbind('<Button>')
        self.enemy1Down.unbind('<Button>')
        self.enemy2Down.unbind('<Button>')
        self.enemy3Down.unbind('<Button>')
        self.enemy4Down.unbind('<Button>')
        self.enemy5Down.unbind('<Button>')
        self.enemy6Down.unbind('<Button>')
        self.enemy1Up.bind('<Button>',W1E1Up)
        self.enemy2Up.bind('<Button>',W1E2Up)
        self.enemy3Up.bind('<Button>',W1E3Up)
        self.enemy4Up.bind('<Button>',W1E4Up)
        self.enemy5Up.bind('<Button>',W1E5Up)
        self.enemy6Up.bind('<Button>',W1E6Up)
        self.enemy1Down.bind('<Button>',W1E1Down)
        self.enemy2Down.bind('<Button>',W1E2Down)
        self.enemy3Down.bind('<Button>',W1E3Down)
        self.enemy4Down.bind('<Button>',W1E4Down)
        self.enemy5Down.bind('<Button>',W1E5Down)
        self.enemy6Down.bind('<Button>',W1E6Down)
        self.enemy1num.config(text=str(W1E1))
        self.enemy2num.config(text=str(W1E2))
        self.enemy3num.config(text=str(W1E3))
        self.enemy4num.config(text=str(W1E4))
        self.enemy5num.config(text=str(W1E5))
        self.enemy6num.config(text=str(W1E6))
        
    def Wave2(event):
        global W2E1
        global W2E2
        global W2E3
        global W2E4
        global W2E5
        global W2E6
        self.lbWave1.config(bg="black")
        self.lbWave2.config(bg="darkblue")
        self.lbWave3.config(bg="black")
        self.lbWave4.config(bg="black")
        self.lbWave5.config(bg="black")
        self.lbWave6.config(bg="black")
        self.lbWave7.config(bg="black")
        self.lbWave8.config(bg="black")
        self.lbWave9.config(bg="black")
        self.lbWave10.config(bg="black")
        self.enemy1Up.unbind('<Button>')
        self.enemy2Up.unbind('<Button>')
        self.enemy3Up.unbind('<Button>')
        self.enemy4Up.unbind('<Button>')
        self.enemy5Up.unbind('<Button>')
        self.enemy6Up.unbind('<Button>')
        self.enemy1Down.unbind('<Button>')
        self.enemy2Down.unbind('<Button>')
        self.enemy3Down.unbind('<Button>')
        self.enemy4Down.unbind('<Button>')
        self.enemy5Down.unbind('<Button>')
        self.enemy6Down.unbind('<Button>')
        self.enemy1Up.bind('<Button>',W2E1Up)
        self.enemy2Up.bind('<Button>',W2E2Up)
        self.enemy3Up.bind('<Button>',W2E3Up)
        self.enemy4Up.bind('<Button>',W2E4Up)
        self.enemy5Up.bind('<Button>',W2E5Up)
        self.enemy6Up.bind('<Button>',W2E6Up)
        self.enemy1Down.bind('<Button>',W2E1Down)
        self.enemy2Down.bind('<Button>',W2E2Down)
        self.enemy3Down.bind('<Button>',W2E3Down)
        self.enemy4Down.bind('<Button>',W2E4Down)
        self.enemy5Down.bind('<Button>',W2E5Down)
        self.enemy6Down.bind('<Button>',W2E6Down)
        self.enemy1num.config(text=str(W2E1))
        self.enemy2num.config(text=str(W2E2))
        self.enemy3num.config(text=str(W2E3))
        self.enemy4num.config(text=str(W2E4))
        self.enemy5num.config(text=str(W2E5))
        self.enemy6num.config(text=str(W2E6))

    def Wave3(event):
        global W3E1
        global W3E2
        global W3E3
        global W3E4
        global W3E5
        global W3E6
        self.lbWave1.config(bg="black")
        self.lbWave2.config(bg="black")
        self.lbWave3.config(bg="darkblue")
        self.lbWave4.config(bg="black")
        self.lbWave5.config(bg="black")
        self.lbWave6.config(bg="black")
        self.lbWave7.config(bg="black")
        self.lbWave8.config(bg="black")
        self.lbWave9.config(bg="black")
        self.lbWave10.config(bg="black")
        self.enemy1Up.unbind('<Button>')
        self.enemy2Up.unbind('<Button>')
        self.enemy3Up.unbind('<Button>')
        self.enemy4Up.unbind('<Button>')
        self.enemy5Up.unbind('<Button>')
        self.enemy6Up.unbind('<Button>')
        self.enemy1Down.unbind('<Button>')
        self.enemy2Down.unbind('<Button>')
        self.enemy3Down.unbind('<Button>')
        self.enemy4Down.unbind('<Button>')
        self.enemy5Down.unbind('<Button>')
        self.enemy6Down.unbind('<Button>')
        self.enemy1Up.bind('<Button>',W3E1Up)
        self.enemy2Up.bind('<Button>',W3E2Up)
        self.enemy3Up.bind('<Button>',W3E3Up)
        self.enemy4Up.bind('<Button>',W3E4Up)
        self.enemy5Up.bind('<Button>',W3E5Up)
        self.enemy6Up.bind('<Button>',W3E6Up)
        self.enemy1Down.bind('<Button>',W3E1Down)
        self.enemy2Down.bind('<Button>',W3E2Down)
        self.enemy3Down.bind('<Button>',W3E3Down)
        self.enemy4Down.bind('<Button>',W3E4Down)
        self.enemy5Down.bind('<Button>',W3E5Down)
        self.enemy6Down.bind('<Button>',W3E6Down)
        self.enemy1num.config(text=str(W3E1))
        self.enemy2num.config(text=str(W3E2))
        self.enemy3num.config(text=str(W3E3))
        self.enemy4num.config(text=str(W3E4))
        self.enemy5num.config(text=str(W3E5))
        self.enemy6num.config(text=str(W3E6))
    
    def Wave4(event):
        global W4E1
        global W4E2
        global W4E3
        global W4E4
        global W4E5
        global W4E6
        self.lbWave1.config(bg="black")
        self.lbWave2.config(bg="black")
        self.lbWave3.config(bg="black")
        self.lbWave4.config(bg="darkblue")
        self.lbWave5.config(bg="black")
        self.lbWave6.config(bg="black")
        self.lbWave7.config(bg="black")
        self.lbWave8.config(bg="black")
        self.lbWave9.config(bg="black")
        self.lbWave10.config(bg="black")
        self.enemy1Up.unbind('<Button>')
        self.enemy2Up.unbind('<Button>')
        self.enemy3Up.unbind('<Button>')
        self.enemy4Up.unbind('<Button>')
        self.enemy5Up.unbind('<Button>')
        self.enemy6Up.unbind('<Button>')
        self.enemy1Down.unbind('<Button>')
        self.enemy2Down.unbind('<Button>')
        self.enemy3Down.unbind('<Button>')
        self.enemy4Down.unbind('<Button>')
        self.enemy5Down.unbind('<Button>')
        self.enemy6Down.unbind('<Button>')
        self.enemy1Up.bind('<Button>',W4E1Up)
        self.enemy2Up.bind('<Button>',W4E2Up)
        self.enemy3Up.bind('<Button>',W4E3Up)
        self.enemy4Up.bind('<Button>',W4E4Up)
        self.enemy5Up.bind('<Button>',W4E5Up)
        self.enemy6Up.bind('<Button>',W4E6Up)
        self.enemy1Down.bind('<Button>',W4E1Down)
        self.enemy2Down.bind('<Button>',W4E2Down)
        self.enemy3Down.bind('<Button>',W4E3Down)
        self.enemy4Down.bind('<Button>',W4E4Down)
        self.enemy5Down.bind('<Button>',W4E5Down)
        self.enemy6Down.bind('<Button>',W4E6Down)
        self.enemy1num.config(text=str(W4E1))
        self.enemy2num.config(text=str(W4E2))
        self.enemy3num.config(text=str(W4E3))
        self.enemy4num.config(text=str(W4E4))
        self.enemy5num.config(text=str(W4E5))
        self.enemy6num.config(text=str(W4E6))

    def Wave5(event):
        global W5E1
        global W5E2
        global W5E3
        global W5E4
        global W5E5
        global W5E6
        self.lbWave1.config(bg="black")
        self.lbWave2.config(bg="black")
        self.lbWave3.config(bg="black")
        self.lbWave4.config(bg="black")
        self.lbWave5.config(bg="darkblue")
        self.lbWave6.config(bg="black")
        self.lbWave7.config(bg="black")
        self.lbWave8.config(bg="black")
        self.lbWave9.config(bg="black")
        self.lbWave10.config(bg="black")
        self.enemy1Up.unbind('<Button>')
        self.enemy2Up.unbind('<Button>')
        self.enemy3Up.unbind('<Button>')
        self.enemy4Up.unbind('<Button>')
        self.enemy5Up.unbind('<Button>')
        self.enemy6Up.unbind('<Button>')
        self.enemy1Down.unbind('<Button>')
        self.enemy2Down.unbind('<Button>')
        self.enemy3Down.unbind('<Button>')
        self.enemy4Down.unbind('<Button>')
        self.enemy5Down.unbind('<Button>')
        self.enemy6Down.unbind('<Button>')
        self.enemy1Up.bind('<Button>',W5E1Up)
        self.enemy2Up.bind('<Button>',W5E2Up)
        self.enemy3Up.bind('<Button>',W5E3Up)
        self.enemy4Up.bind('<Button>',W5E4Up)
        self.enemy5Up.bind('<Button>',W5E5Up)
        self.enemy6Up.bind('<Button>',W5E6Up)
        self.enemy1Down.bind('<Button>',W5E1Down)
        self.enemy2Down.bind('<Button>',W5E2Down)
        self.enemy3Down.bind('<Button>',W5E3Down)
        self.enemy4Down.bind('<Button>',W5E4Down)
        self.enemy5Down.bind('<Button>',W5E5Down)
        self.enemy6Down.bind('<Button>',W5E6Down)
        self.enemy1num.config(text=str(W5E1))
        self.enemy2num.config(text=str(W5E2))
        self.enemy3num.config(text=str(W5E3))
        self.enemy4num.config(text=str(W5E4))
        self.enemy5num.config(text=str(W5E5))
        self.enemy6num.config(text=str(W5E6))
    
    def Wave6(event):
        global W6E1
        global W6E2
        global W6E3
        global W6E4
        global W6E5
        global W6E6
        self.lbWave1.config(bg="black")
        self.lbWave2.config(bg="black")
        self.lbWave3.config(bg="black")
        self.lbWave4.config(bg="black")
        self.lbWave5.config(bg="black")
        self.lbWave6.config(bg="darkblue")
        self.lbWave7.config(bg="black")
        self.lbWave8.config(bg="black")
        self.lbWave9.config(bg="black")
        self.lbWave10.config(bg="black")
        self.enemy1Up.unbind('<Button>')
        self.enemy2Up.unbind('<Button>')
        self.enemy3Up.unbind('<Button>')
        self.enemy4Up.unbind('<Button>')
        self.enemy5Up.unbind('<Button>')
        self.enemy6Up.unbind('<Button>')
        self.enemy1Down.unbind('<Button>')
        self.enemy2Down.unbind('<Button>')
        self.enemy3Down.unbind('<Button>')
        self.enemy4Down.unbind('<Button>')
        self.enemy5Down.unbind('<Button>')
        self.enemy6Down.unbind('<Button>')
        self.enemy1Up.bind('<Button>',W6E1Up)
        self.enemy2Up.bind('<Button>',W6E2Up)
        self.enemy3Up.bind('<Button>',W6E3Up)
        self.enemy4Up.bind('<Button>',W6E4Up)
        self.enemy5Up.bind('<Button>',W6E5Up)
        self.enemy6Up.bind('<Button>',W6E6Up)
        self.enemy1Down.bind('<Button>',W6E1Down)
        self.enemy2Down.bind('<Button>',W6E2Down)
        self.enemy3Down.bind('<Button>',W6E3Down)
        self.enemy4Down.bind('<Button>',W6E4Down)
        self.enemy5Down.bind('<Button>',W6E5Down)
        self.enemy6Down.bind('<Button>',W6E6Down)
        self.enemy1num.config(text=str(W6E1))
        self.enemy2num.config(text=str(W6E2))
        self.enemy3num.config(text=str(W6E3))
        self.enemy4num.config(text=str(W6E4))
        self.enemy5num.config(text=str(W6E5))
        self.enemy6num.config(text=str(W6E6))

    def Wave7(event):
        global W7E1
        global W7E2
        global W7E3
        global W7E4
        global W7E5
        global W7E6
        self.lbWave1.config(bg="black")
        self.lbWave2.config(bg="black")
        self.lbWave3.config(bg="black")
        self.lbWave4.config(bg="black")
        self.lbWave5.config(bg="black")
        self.lbWave6.config(bg="black")
        self.lbWave7.config(bg="darkblue")
        self.lbWave8.config(bg="black")
        self.lbWave9.config(bg="black")
        self.lbWave10.config(bg="black")
        self.enemy1Up.unbind('<Button>')
        self.enemy2Up.unbind('<Button>')
        self.enemy3Up.unbind('<Button>')
        self.enemy4Up.unbind('<Button>')
        self.enemy5Up.unbind('<Button>')
        self.enemy6Up.unbind('<Button>')
        self.enemy1Down.unbind('<Button>')
        self.enemy2Down.unbind('<Button>')
        self.enemy3Down.unbind('<Button>')
        self.enemy4Down.unbind('<Button>')
        self.enemy5Down.unbind('<Button>')
        self.enemy6Down.unbind('<Button>')
        self.enemy1Up.bind('<Button>',W7E1Up)
        self.enemy2Up.bind('<Button>',W7E2Up)
        self.enemy3Up.bind('<Button>',W7E3Up)
        self.enemy4Up.bind('<Button>',W7E4Up)
        self.enemy5Up.bind('<Button>',W7E5Up)
        self.enemy6Up.bind('<Button>',W7E6Up)
        self.enemy1Down.bind('<Button>',W7E1Down)
        self.enemy2Down.bind('<Button>',W7E2Down)
        self.enemy3Down.bind('<Button>',W7E3Down)
        self.enemy4Down.bind('<Button>',W7E4Down)
        self.enemy5Down.bind('<Button>',W7E5Down)
        self.enemy6Down.bind('<Button>',W7E6Down)
        self.enemy1num.config(text=str(W7E1))
        self.enemy2num.config(text=str(W7E2))
        self.enemy3num.config(text=str(W7E3))
        self.enemy4num.config(text=str(W7E4))
        self.enemy5num.config(text=str(W7E5))
        self.enemy6num.config(text=str(W7E6))

    def Wave8(event):
        global W8E1
        global W8E2
        global W8E3
        global W8E4
        global W8E5
        global W8E6
        self.lbWave1.config(bg="black")
        self.lbWave2.config(bg="black")
        self.lbWave3.config(bg="black")
        self.lbWave4.config(bg="black")
        self.lbWave5.config(bg="black")
        self.lbWave6.config(bg="black")
        self.lbWave7.config(bg="black")
        self.lbWave8.config(bg="darkblue")
        self.lbWave9.config(bg="black")
        self.lbWave10.config(bg="black")
        self.enemy1Up.unbind('<Button>')
        self.enemy2Up.unbind('<Button>')
        self.enemy3Up.unbind('<Button>')
        self.enemy4Up.unbind('<Button>')
        self.enemy5Up.unbind('<Button>')
        self.enemy6Up.unbind('<Button>')
        self.enemy1Down.unbind('<Button>')
        self.enemy2Down.unbind('<Button>')
        self.enemy3Down.unbind('<Button>')
        self.enemy4Down.unbind('<Button>')
        self.enemy5Down.unbind('<Button>')
        self.enemy6Down.unbind('<Button>')
        self.enemy1Up.bind('<Button>',W8E1Up)
        self.enemy2Up.bind('<Button>',W8E2Up)
        self.enemy3Up.bind('<Button>',W8E3Up)
        self.enemy4Up.bind('<Button>',W8E4Up)
        self.enemy5Up.bind('<Button>',W8E5Up)
        self.enemy6Up.bind('<Button>',W8E6Up)
        self.enemy1Down.bind('<Button>',W8E1Down)
        self.enemy2Down.bind('<Button>',W8E2Down)
        self.enemy3Down.bind('<Button>',W8E3Down)
        self.enemy4Down.bind('<Button>',W8E4Down)
        self.enemy5Down.bind('<Button>',W8E5Down)
        self.enemy6Down.bind('<Button>',W8E6Down)
        self.enemy1num.config(text=str(W8E1))
        self.enemy2num.config(text=str(W8E2))
        self.enemy3num.config(text=str(W8E3))
        self.enemy4num.config(text=str(W8E4))
        self.enemy5num.config(text=str(W8E5))
        self.enemy6num.config(text=str(W8E6))
    
    def Wave9(event):
        global W9E1
        global W9E2
        global W9E3
        global W9E4
        global W9E5
        global W9E6
        self.lbWave1.config(bg="black")
        self.lbWave2.config(bg="black")
        self.lbWave3.config(bg="black")
        self.lbWave4.config(bg="black")
        self.lbWave5.config(bg="black")
        self.lbWave6.config(bg="black")
        self.lbWave7.config(bg="black")
        self.lbWave8.config(bg="black")
        self.lbWave9.config(bg="darkblue")
        self.lbWave10.config(bg="black")
        self.enemy1Up.unbind('<Button>')
        self.enemy2Up.unbind('<Button>')
        self.enemy3Up.unbind('<Button>')
        self.enemy4Up.unbind('<Button>')
        self.enemy5Up.unbind('<Button>')
        self.enemy6Up.unbind('<Button>')
        self.enemy1Down.unbind('<Button>')
        self.enemy2Down.unbind('<Button>')
        self.enemy3Down.unbind('<Button>')
        self.enemy4Down.unbind('<Button>')
        self.enemy5Down.unbind('<Button>')
        self.enemy6Down.unbind('<Button>')
        self.enemy1Up.bind('<Button>',W9E1Up)
        self.enemy2Up.bind('<Button>',W9E2Up)
        self.enemy3Up.bind('<Button>',W9E3Up)
        self.enemy4Up.bind('<Button>',W9E4Up)
        self.enemy5Up.bind('<Button>',W9E5Up)
        self.enemy6Up.bind('<Button>',W9E6Up)
        self.enemy1Down.bind('<Button>',W9E1Down)
        self.enemy2Down.bind('<Button>',W9E2Down)
        self.enemy3Down.bind('<Button>',W9E3Down)
        self.enemy4Down.bind('<Button>',W9E4Down)
        self.enemy5Down.bind('<Button>',W9E5Down)
        self.enemy6Down.bind('<Button>',W9E6Down)
        self.enemy1num.config(text=str(W9E1))
        self.enemy2num.config(text=str(W9E2))
        self.enemy3num.config(text=str(W9E3))
        self.enemy4num.config(text=str(W9E4))
        self.enemy5num.config(text=str(W9E5))
        self.enemy6num.config(text=str(W9E6))
    
    def Wave10(event):
        global W10E1
        global W10E2
        global W10E3
        global W10E4
        global W10E5
        global W10E6
        self.lbWave1.config(bg="black")
        self.lbWave2.config(bg="black")
        self.lbWave3.config(bg="black")
        self.lbWave4.config(bg="black")
        self.lbWave5.config(bg="black")
        self.lbWave6.config(bg="black")
        self.lbWave7.config(bg="black")
        self.lbWave8.config(bg="black")
        self.lbWave9.config(bg="black")
        self.lbWave10.config(bg="darkblue")
        self.enemy1Up.unbind('<Button>')
        self.enemy2Up.unbind('<Button>')
        self.enemy3Up.unbind('<Button>')
        self.enemy4Up.unbind('<Button>')
        self.enemy5Up.unbind('<Button>')
        self.enemy6Up.unbind('<Button>')
        self.enemy1Down.unbind('<Button>')
        self.enemy2Down.unbind('<Button>')
        self.enemy3Down.unbind('<Button>')
        self.enemy4Down.unbind('<Button>')
        self.enemy5Down.unbind('<Button>')
        self.enemy6Down.unbind('<Button>')
        self.enemy1Up.bind('<Button>',W10E1Up)
        self.enemy2Up.bind('<Button>',W10E2Up)
        self.enemy3Up.bind('<Button>',W10E3Up)
        self.enemy4Up.bind('<Button>',W10E4Up)
        self.enemy5Up.bind('<Button>',W10E5Up)
        self.enemy6Up.bind('<Button>',W10E6Up)
        self.enemy1Down.bind('<Button>',W10E1Down)
        self.enemy2Down.bind('<Button>',W10E2Down)
        self.enemy3Down.bind('<Button>',W10E3Down)
        self.enemy4Down.bind('<Button>',W10E4Down)
        self.enemy5Down.bind('<Button>',W10E5Down)
        self.enemy6Down.bind('<Button>',W10E6Down)
        self.enemy1num.config(text=str(W10E1))
        self.enemy2num.config(text=str(W10E2))
        self.enemy3num.config(text=str(W10E3))
        self.enemy4num.config(text=str(W10E4))
        self.enemy5num.config(text=str(W10E5))
        self.enemy6num.config(text=str(W10E6))

    def StartTenWaveChallengeMultiPlayer(event):
        self.destroy()
        TenWaveChallengeMultiPlayer()

    def W1E1Up(event):
        global W1E1
        W1E1 += 1
        self.enemy1num.config(text=str(W1E1))

    def W1E2Up(event):
        global W1E2
        W1E2 += 1
        self.enemy2num.config(text=str(W1E2))
        
    def W1E3Up(event):
        global W1E3
        W1E3 += 1
        self.enemy3num.config(text=str(W1E3))

    def W1E4Up(event):
        global W1E4
        W1E4 += 1
        self.enemy4num.config(text=str(W1E4))

    def W1E5Up(event):
        global W1E5
        W1E5 += 1
        self.enemy5num.config(text=str(W1E5))

    def W1E6Up(event):
        global W1E6
        W1E6 += 1
        self.enemy6num.config(text=str(W1E6))

    def W1E1Down(event):
        global W1E1
        if W1E1 > 0:
            W1E1 -= 1
        self.enemy1num.config(text=str(W1E1))

    def W1E2Down(event):
        global W1E2
        if W1E2 > 0:
            W1E2 -= 1
        self.enemy2num.config(text=str(W1E2))
        
    def W1E3Down(event):
        global W1E3
        if W1E3 > 0:
            W1E3 -= 1
        self.enemy3num.config(text=str(W1E3))

    def W1E4Down(event):
        global W1E4
        if W1E4 > 0:
            W1E4 -= 1
        self.enemy4num.config(text=str(W1E4))

    def W1E5Down(event):
        global W1E5
        if W1E5 > 0:
            W1E5 -= 1
        self.enemy5num.config(text=str(W1E5))

    def W1E6Down(event):
        global W1E6
        if W1E6 > 0:
            W1E6 -= 1
        self.enemy6num.config(text=str(W1E6))

    def W2E1Up(event):
        global W2E1
        W2E1 += 1
        self.enemy1num.config(text=str(W2E1))

    def W2E2Up(event):
        global W2E2
        W2E2 += 1
        self.enemy2num.config(text=str(W2E2))
        
    def W2E3Up(event):
        global W2E3
        W2E3 += 1
        self.enemy3num.config(text=str(W2E3))

    def W2E4Up(event):
        global W2E4
        W2E4 += 1
        self.enemy4num.config(text=str(W2E4))

    def W2E5Up(event):
        global W2E5
        W2E5 += 1
        self.enemy5num.config(text=str(W2E5))

    def W2E6Up(event):
        global W2E6
        W2E6 += 1
        self.enemy6num.config(text=str(W2E6))

    def W2E1Down(event):
        global W2E1
        if W2E1 > 0:
            W2E1 -= 1
        self.enemy1num.config(text=str(W2E1))

    def W2E2Down(event):
        global W2E2
        if W2E2 > 0:
            W2E2 -= 1
        self.enemy2num.config(text=str(W2E2))
        
    def W2E3Down(event):
        global W2E3
        if W2E3 > 0:
            W2E3 -= 1
        self.enemy3num.config(text=str(W2E3))

    def W2E4Down(event):
        global W2E4
        if W2E4 > 0:
            W2E4 -= 1
        self.enemy4num.config(text=str(W2E4))

    def W2E5Down(event):
        global W2E5
        if W2E5 > 0:
            W2E5 -= 1
        self.enemy5num.config(text=str(W2E5))

    def W2E6Down(event):
        global W2E6
        if W2E6 > 0:
            W2E6 -= 1
        self.enemy6num.config(text=str(W2E6))

    def W3E1Up(event):
        global W3E1
        W3E1 += 1
        self.enemy1num.config(text=str(W3E1))

    def W3E2Up(event):
        global W3E2
        W3E2 += 1
        self.enemy2num.config(text=str(W3E2))
        
    def W3E3Up(event):
        global W3E3
        W3E3 += 1
        self.enemy3num.config(text=str(W3E3))

    def W3E4Up(event):
        global W3E4
        W3E4 += 1
        self.enemy4num.config(text=str(W3E4))

    def W3E5Up(event):
        global W3E5
        W3E5 += 1
        self.enemy5num.config(text=str(W3E5))

    def W3E6Up(event):
        global W3E6
        W3E6 += 1
        self.enemy6num.config(text=str(W3E6))

    def W3E1Down(event):
        global W3E1
        if W3E1 > 0:
            W3E1 -= 1
        self.enemy1num.config(text=str(W3E1))

    def W3E2Down(event):
        global W3E2
        if W3E2 > 0:
            W3E2 -= 1
        self.enemy2num.config(text=str(W3E2))
        
    def W3E3Down(event):
        global W3E3
        if W3E3 > 0:
            W3E3 -= 1
        self.enemy3num.config(text=str(W3E3))

    def W3E4Down(event):
        global W3E4
        if W3E4 > 0:
            W3E4 -= 1
        self.enemy4num.config(text=str(W3E4))

    def W3E5Down(event):
        global W3E5
        if W3E5 > 0:
            W3E5 -= 1
        self.enemy5num.config(text=str(W3E5))

    def W3E6Down(event):
        global W3E6
        if W3E6 > 0:
            W3E6 -= 1
        self.enemy6num.config(text=str(W3E6))

    def W4E1Up(event):
        global W4E1
        W4E1 += 1
        self.enemy1num.config(text=str(W4E1))

    def W4E2Up(event):
        global W4E2
        W4E2 += 1
        self.enemy2num.config(text=str(W4E2))
        
    def W4E3Up(event):
        global W4E3
        W4E3 += 1
        self.enemy3num.config(text=str(W4E3))

    def W4E4Up(event):
        global W4E4
        W4E4 += 1
        self.enemy4num.config(text=str(W4E4))

    def W4E5Up(event):
        global W4E5
        W4E5 += 1
        self.enemy5num.config(text=str(W4E5))

    def W4E6Up(event):
        global W4E6
        W4E6 += 1
        self.enemy6num.config(text=str(W4E6))

    def W4E1Down(event):
        global W4E1
        if W4E1 > 0:
            W4E1 -= 1
        self.enemy1num.config(text=str(W4E1))

    def W4E2Down(event):
        global W4E2
        if W4E2 > 0:
            W4E2 -= 1
        self.enemy2num.config(text=str(W4E2))
        
    def W4E3Down(event):
        global W4E3
        if W4E3 > 0:
            W4E3 -= 1
        self.enemy3num.config(text=str(W4E3))

    def W4E4Down(event):
        global W4E4
        if W4E4 > 0:
            W4E4 -= 1
        self.enemy4num.config(text=str(W4E4))

    def W4E5Down(event):
        global W4E5
        if W4E5 > 0:
            W4E5 -= 1
        self.enemy5num.config(text=str(W4E5))

    def W4E6Down(event):
        global W4E6
        if W4E6 > 0:
            W4E6 -= 1
        self.enemy6num.config(text=str(W4E6))

    def W5E1Up(event):
        global W5E1
        W5E1 += 1
        self.enemy1num.config(text=str(W5E1))

    def W5E2Up(event):
        global W5E2
        W5E2 += 1
        self.enemy2num.config(text=str(W5E2))
        
    def W5E3Up(event):
        global W5E3
        W5E3 += 1
        self.enemy3num.config(text=str(W5E3))

    def W5E4Up(event):
        global W5E4
        W5E4 += 1
        self.enemy4num.config(text=str(W5E4))

    def W5E5Up(event):
        global W5E5
        W5E5 += 1
        self.enemy5num.config(text=str(W5E5))

    def W5E6Up(event):
        global W5E6
        W5E6 += 1
        self.enemy6num.config(text=str(W5E6))

    def W5E1Down(event):
        global W5E1
        if W5E1 > 0:
            W5E1 -= 1
        self.enemy1num.config(text=str(W5E1))

    def W5E2Down(event):
        global W5E2
        if W5E2 > 0:
            W5E2 -= 1
        self.enemy2num.config(text=str(W5E2))
        
    def W5E3Down(event):
        global W5E3
        if W5E3 > 0:
            W5E3 -= 1
        self.enemy3num.config(text=str(W5E3))

    def W5E4Down(event):
        global W5E4
        if W5E4 > 0:
            W5E4 -= 1
        self.enemy4num.config(text=str(W5E4))

    def W5E5Down(event):
        global W5E5
        if W5E5 > 0:
            W5E5 -= 1
        self.enemy5num.config(text=str(W5E5))

    def W5E6Down(event):
        global W5E6
        if W5E6 > 0:
            W5E6 -= 1
        self.enemy6num.config(text=str(W5E6))

    def W6E1Up(event):
        global W6E1
        W6E1 += 1
        self.enemy1num.config(text=str(W6E1))

    def W6E2Up(event):
        global W6E2
        W6E2 += 1
        self.enemy2num.config(text=str(W6E2))
        
    def W6E3Up(event):
        global W6E3
        W6E3 += 1
        self.enemy3num.config(text=str(W6E3))

    def W6E4Up(event):
        global W6E4
        W6E4 += 1
        self.enemy4num.config(text=str(W6E4))

    def W6E5Up(event):
        global W6E5
        W6E5 += 1
        self.enemy5num.config(text=str(W6E5))

    def W6E6Up(event):
        global W6E6
        W6E6 += 1
        self.enemy6num.config(text=str(W6E6))

    def W6E1Down(event):
        global W6E1
        if W6E1 > 0:
            W6E1 -= 1
        self.enemy1num.config(text=str(W6E1))

    def W6E2Down(event):
        global W6E2
        if W6E2 > 0:
            W6E2 -= 1
        self.enemy2num.config(text=str(W6E2))
        
    def W6E3Down(event):
        global W6E3
        if W6E3 > 0:
            W6E3 -= 1
        self.enemy3num.config(text=str(W6E3))

    def W6E4Down(event):
        global W6E4
        if W6E4 > 0:
            W6E4 -= 1
        self.enemy4num.config(text=str(W6E4))

    def W6E5Down(event):
        global W6E5
        if W6E5 > 0:
            W6E5 -= 1
        self.enemy5num.config(text=str(W6E5))

    def W6E6Down(event):
        global W6E6
        if W6E6 > 0:
            W6E6 -= 1
        self.enemy6num.config(text=str(W6E6))

    def W7E1Up(event):
        global W7E1
        W7E1 += 1
        self.enemy1num.config(text=str(W7E1))

    def W7E2Up(event):
        global W7E2
        W7E2 += 1
        self.enemy2num.config(text=str(W7E2))
        
    def W7E3Up(event):
        global W7E3
        W7E3 += 1
        self.enemy3num.config(text=str(W7E3))

    def W7E4Up(event):
        global W7E4
        W7E4 += 1
        self.enemy4num.config(text=str(W7E4))

    def W7E5Up(event):
        global W7E5
        W7E5 += 1
        self.enemy5num.config(text=str(W7E5))

    def W7E6Up(event):
        global W7E6
        W7E6 += 1
        self.enemy6num.config(text=str(W7E6))

    def W7E1Down(event):
        global W7E1
        if W7E1 > 0:
            W7E1 -= 1
        self.enemy1num.config(text=str(W7E1))

    def W7E2Down(event):
        global W7E2
        if W7E2 > 0:
            W7E2 -= 1
        self.enemy2num.config(text=str(W7E2))
        
    def W7E3Down(event):
        global W7E3
        if W7E3 > 0:
            W7E3 -= 1
        self.enemy3num.config(text=str(W7E3))

    def W7E4Down(event):
        global W7E4
        if W7E4 > 0:
            W7E4 -= 1
        self.enemy4num.config(text=str(W7E4))

    def W7E5Down(event):
        global W7E5
        if W7E5 > 0:
            W7E5 -= 1
        self.enemy5num.config(text=str(W7E5))

    def W7E6Down(event):
        global W7E6
        if W7E6 > 0:
            W7E6 -= 1
        self.enemy6num.config(text=str(W7E6))

    def W8E1Up(event):
        global W8E1
        W8E1 += 1
        self.enemy1num.config(text=str(W8E1))

    def W8E2Up(event):
        global W8E2
        W8E2 += 1
        self.enemy2num.config(text=str(W8E2))
        
    def W8E3Up(event):
        global W8E3
        W8E3 += 1
        self.enemy3num.config(text=str(W8E3))

    def W8E4Up(event):
        global W8E4
        W8E4 += 1
        self.enemy4num.config(text=str(W8E4))

    def W8E5Up(event):
        global W8E5
        W8E5 += 1
        self.enemy5num.config(text=str(W8E5))

    def W8E6Up(event):
        global W8E6
        W8E6 += 1
        self.enemy6num.config(text=str(W8E6))

    def W8E1Down(event):
        global W8E1
        if W8E1 > 0:
            W8E1 -= 1
        self.enemy1num.config(text=str(W8E1))

    def W8E2Down(event):
        global W8E2
        if W8E2 > 0:
            W8E2 -= 1
        self.enemy2num.config(text=str(W8E2))
        
    def W8E3Down(event):
        global W8E3
        if W8E3 > 0:
            W8E3 -= 1
        self.enemy3num.config(text=str(W8E3))

    def W8E4Down(event):
        global W8E4
        if W8E4 > 0:
            W8E4 -= 1
        self.enemy4num.config(text=str(W8E4))

    def W8E5Down(event):
        global W8E5
        if W8E5 > 0:
            W8E5 -= 1
        self.enemy5num.config(text=str(W8E5))

    def W8E6Down(event):
        global W8E6
        if W8E6 > 0:
            W8E6 -= 1
        self.enemy6num.config(text=str(W8E6))

    def W9E1Up(event):
        global W9E1
        W9E1 += 1
        self.enemy1num.config(text=str(W9E1))

    def W9E2Up(event):
        global W9E2
        W9E2 += 1
        self.enemy2num.config(text=str(W9E2))
        
    def W9E3Up(event):
        global W9E3
        W9E3 += 1
        self.enemy3num.config(text=str(W9E3))

    def W9E4Up(event):
        global W9E4
        W9E4 += 1
        self.enemy4num.config(text=str(W9E4))

    def W9E5Up(event):
        global W9E5
        W9E5 += 1
        self.enemy5num.config(text=str(W9E5))

    def W9E6Up(event):
        global W9E6
        W9E6 += 1
        self.enemy6num.config(text=str(W9E6))

    def W9E1Down(event):
        global W9E1
        if W9E1 > 0:
            W9E1 -= 1
        self.enemy1num.config(text=str(W9E1))

    def W9E2Down(event):
        global W9E2
        if W9E2 > 0:
            W9E2 -= 1
        self.enemy2num.config(text=str(W9E2))
        
    def W9E3Down(event):
        global W9E3
        if W9E3 > 0:
            W9E3 -= 1
        self.enemy3num.config(text=str(W9E3))

    def W9E4Down(event):
        global W9E4
        if W9E4 > 0:
            W9E4 -= 1
        self.enemy4num.config(text=str(W9E4))

    def W9E5Down(event):
        global W9E5
        if W9E5 > 0:
            W9E5 -= 1
        self.enemy5num.config(text=str(W9E5))

    def W9E6Down(event):
        global W9E6
        if W9E6 > 0:
            W9E6 -= 1
        self.enemy6num.config(text=str(W9E6))

    def W10E1Up(event):
        global W10E1
        W10E1 += 1
        self.enemy1num.config(text=str(W10E1))

    def W10E2Up(event):
        global W10E2
        W10E2 += 1
        self.enemy2num.config(text=str(W10E2))
        
    def W10E3Up(event):
        global W10E3
        W10E3 += 1
        self.enemy3num.config(text=str(W10E3))

    def W10E4Up(event):
        global W10E4
        W10E4 += 1
        self.enemy4num.config(text=str(W10E4))

    def W10E5Up(event):
        global W10E5
        W10E5 += 1
        self.enemy5num.config(text=str(W10E5))

    def W10E6Up(event):
        global W10E6
        W10E6 += 1
        self.enemy6num.config(text=str(W10E6))

    def W10E1Down(event):
        global W10E1
        if W10E1 > 0:
            W10E1 -= 1
        self.enemy1num.config(text=str(W10E1))

    def W10E2Down(event):
        global W10E2
        if W10E2 > 0:
            W10E2 -= 1
        self.enemy2num.config(text=str(W10E2))
        
    def W10E3Down(event):
        global W10E3
        if W10E3 > 0:
            W10E3 -= 1
        self.enemy3num.config(text=str(W10E3))

    def W10E4Down(event):
        global W10E4
        if W10E4 > 0:
            W10E4 -= 1
        self.enemy4num.config(text=str(W10E4))

    def W10E5Down(event):
        global W10E5
        if W10E5 > 0:
            W10E5 -= 1
        self.enemy5num.config(text=str(W10E5))

    def W10E6Down(event):
        global W10E6
        if W10E6 > 0:
            W10E6 -= 1
        self.enemy6num.config(text=str(W10E6))

    def Exit(event):
        self.destroy()

    #Bind
    self.btnMainMenu.bind('<Button>',StartMainMenu)
    self.lbWave1.bind('<Button>',Wave1)
    self.lbWave2.bind('<Button>',Wave2)
    self.lbWave3.bind('<Button>',Wave3)
    self.lbWave4.bind('<Button>',Wave4)
    self.lbWave5.bind('<Button>',Wave5)
    self.lbWave6.bind('<Button>',Wave6)
    self.lbWave7.bind('<Button>',Wave7)
    self.lbWave8.bind('<Button>',Wave8)
    self.lbWave9.bind('<Button>',Wave9)
    self.lbWave10.bind('<Button>',Wave10)
    self.btnPlayMultiPlayer.bind('<Button>',StartTenWaveChallengeMultiPlayer)
    self.bind('<Escape>',Exit)
        
    #Frame settings
    self.geometry("830x700")
    self.title("Space Assault")
    self.configure(bg="black")

    Wave1()

def TenWaveChallengeMultiPlayer():
    self = Tk()

    #Variables
    global wave
    global Damage
    global Damage3
    global Damage5
    global Damage6
    global Xpos
    global Ypos
    global X2pos
    global Y2pos
    global enXpos
    global enYpos
    global en2Xpos
    global en2Ypos
    global en3Xpos
    global en3Ypos
    global en4Xpos
    global en4Ypos
    global en5Xpos
    global en5Ypos
    global en6Xpos
    global en6Ypos
    global gameover
    global direction
    global direction2
    global start
    global created
    global created2
    global created3
    global created4
    global created5
    global destroy
    global generated1
    global generated2
    global generated3
    global generated4
    global pause
    wave = 0
    Damage = 0
    Damage3 = 0
    Damage5 = 0
    Damage6 = 0
    Xpos = 425
    Ypos = 350
    X2pos = 400
    Y2pos = 325
    enXpos = 0
    enYpos = 0
    en2Xpos = 0
    en2Ypos = 0
    en3Xpos = 0
    en3Ypos = 0
    en4Xpos = 0
    en4Ypos = 0
    en5Xpos = 0
    en5Ypos = 0
    en6Xpos = 0
    en6Ypos = 0
    gameover = 0
    direction = "N"
    direction2 = "N"
    start = 0
    created = 0
    created2 = 0
    created3 = 0
    created4 = 0
    created5 = 0
    destroy = 0
    generated1 = 1000
    generated2 = 1250
    generated3 = 1500
    generated4 = 1750
    pause = 0
    global W1E1
    global W1E2
    global W1E3
    global W1E4
    global W1E5
    global W1E6
    global W2E1
    global W2E2
    global W2E3
    global W2E4
    global W2E5
    global W2E6
    global W3E1
    global W3E2
    global W3E3
    global W3E4
    global W3E5
    global W3E6
    global W4E1
    global W4E2
    global W4E3
    global W4E4
    global W4E5
    global W4E6
    global W5E1
    global W5E2
    global W5E3
    global W5E4
    global W5E5
    global W5E6
    global W6E1
    global W6E2
    global W6E3
    global W6E4
    global W6E5
    global W6E6
    global W7E1
    global W7E2
    global W7E3
    global W7E4
    global W7E5
    global W7E6
    global W8E1
    global W8E2
    global W8E3
    global W8E4
    global W8E5
    global W8E6
    global W9E1
    global W9E2
    global W9E3
    global W9E4
    global W9E5
    global W9E6
    global W10E1
    global W10E2
    global W10E3
    global W10E4
    global W10E5
    global W10E6

    #Lists
    Players = []
    PlayersXpos = []
    PlayersYpos = []
    PlayersDir = []
    Shots = []
    ShotsXpos = []
    ShotsYpos = []
    ShotDir = []
    enShots = []
    enShotsXpos = []
    enShotsYpos = []
    enShotDir = []
    Enemies = []
    EnemiesDmg = []
    EnemiesXpos = []
    EnemiesYpos = []
    Enemies2 = []
    Enemies2Xpos = []
    Enemies2Ypos = []
    Enemies3 = []
    Enemies3Dmg = []
    Enemies3Xpos = []
    Enemies3Ypos = []
    Enemies4 = []
    Enemies4Xpos = []
    Enemies4Ypos = []
    Enemies5 = []
    Enemies5Dmg = []
    Enemies5Xpos = []
    Enemies5Ypos = []
    Enemies5Wall = []
    Enemies6 = []
    Enemies6Xpos = []
    Enemies6Ypos = []
    Enemies6Type = []
    Enemies6Dmg = []
    Explosions = []
    
    #Score
    self.lbScore = Label(text="Wave: "+str(wave)+"  Press 'p' to pause",bg="black",fg="white")
    self.lbScore.place(x=165,y=680,width=500,height=20)

    #Player
    self.player = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
    self.player.place(x=Xpos,y=Ypos)
    self.player.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="green")
    Players.append(self.player)
    PlayersXpos.append(Xpos)
    PlayersYpos.append(Ypos)
    PlayersDir.append(direction)
    #Player2
    self.player2 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
    self.player2.place(x=X2pos,y=Y2pos)
    self.player2.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="white")
    Players.append(self.player2)
    PlayersXpos.append(X2pos)
    PlayersYpos.append(Y2pos)
    PlayersDir.append(direction2)
    
    #Functions
    def LeftKey(event):
        global Xpos
        global Ypos
        global direction
        global start
        self.player.delete("all")
        self.player.create_polygon(0,15,30,30,15,15,30,0,0,15,fill="green")
        if PlayersXpos[0] > 0:
            PlayersXpos[0] -= 25
        self.player.place(x=PlayersXpos[0],y=PlayersYpos[0])
        PlayersDir[0] = "W"
        cycle = 0
        for enemy in Enemies:
            if PlayersXpos[0] == EnemiesXpos[cycle] and PlayersYpos[0] == EnemiesYpos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy2 in Enemies2:
            if PlayersXpos[0] == Enemies2Xpos[cycle] and PlayersYpos[0] == Enemies2Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy3 in Enemies3:
            if PlayersXpos[0] == Enemies3Xpos[cycle] and PlayersYpos[0] == Enemies3Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy4 in Enemies4:
            if PlayersXpos[0] == Enemies4Xpos[cycle] and PlayersYpos[0] == Enemies4Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy5 in Enemies5:
            if PlayersXpos[0] == Enemies5Xpos[cycle] and PlayersYpos[0] == Enemies5Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy6 in Enemies6:
            if PlayersXpos[0] == Enemies6Xpos[cycle] and PlayersYpos[0] == Enemies6Ypos[cycle]:
                GameOver()
            cycle += 1
        if start == 0:
            NextWave()
        start = 1

    def RightKey(event):
        global Xpos
        global Ypos
        global direction
        global start
        self.player.delete("all")
        self.player.create_polygon(30,15,0,30,15,15,0,0,30,15,fill="green")
        if PlayersXpos[0] < 800:
            PlayersXpos[0] += 25
        self.player.place(x=PlayersXpos[0],y=PlayersYpos[0])
        PlayersDir[0] = "E"
        cycle = 0
        for enemy in Enemies:
            if PlayersXpos[0] == EnemiesXpos[cycle] and PlayersYpos[0] == EnemiesYpos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy2 in Enemies2:
            if PlayersXpos[0] == Enemies2Xpos[cycle] and PlayersYpos[0] == Enemies2Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy3 in Enemies3:
            if PlayersXpos[0] == Enemies3Xpos[cycle] and PlayersYpos[0] == Enemies3Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy4 in Enemies4:
            if PlayersXpos[0] == Enemies4Xpos[cycle] and PlayersYpos[0] == Enemies4Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy5 in Enemies5:
            if PlayersXpos[0] == Enemies5Xpos[cycle] and PlayersYpos[0] == Enemies5Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy6 in Enemies6:
            if PlayersXpos[0] == Enemies6Xpos[cycle] and PlayersYpos[0] == Enemies6Ypos[cycle]:
                GameOver()
            cycle += 1
        if start == 0:
            NextWave()
        start = 1

    def UpKey(event):
        global Xpos
        global Ypos
        global direction
        global start
        self.player.delete("all")
        self.player.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="green")
        if PlayersYpos[0] > 0:
            PlayersYpos[0] -= 25
        self.player.place(x=PlayersXpos[0],y=PlayersYpos[0])
        PlayersDir[0] = "N"
        cycle = 0
        for enemy in Enemies:
            if PlayersXpos[0] == EnemiesXpos[cycle] and PlayersYpos[0] == EnemiesYpos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy2 in Enemies2:
            if PlayersXpos[0] == Enemies2Xpos[cycle] and PlayersYpos[0] == Enemies2Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy3 in Enemies3:
            if PlayersXpos[0] == Enemies3Xpos[cycle] and PlayersYpos[0] == Enemies3Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy4 in Enemies4:
            if PlayersXpos[0] == Enemies4Xpos[cycle] and PlayersYpos[0] == Enemies4Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy5 in Enemies5:
            if PlayersXpos[0] == Enemies5Xpos[cycle] and PlayersYpos[0] == Enemies5Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy6 in Enemies6:
            if PlayersXpos[0] == Enemies6Xpos[cycle] and PlayersYpos[0] == Enemies6Ypos[cycle]:
                GameOver()
            cycle += 1
        if start == 0:
            NextWave()
        start = 1

    def DownKey(event):
        global Xpos
        global Ypos
        global direction
        global start
        self.player.delete("all")
        self.player.create_polygon(15,30,30,0,15,15,0,0,15,30,fill="green")
        if PlayersYpos[0] < 650:
            PlayersYpos[0] += 25
        self.player.place(x=PlayersXpos[0],y=PlayersYpos[0])
        PlayersDir[0] = "S"
        cycle = 0
        for enemy in Enemies:
            if PlayersXpos[0] == EnemiesXpos[cycle] and PlayersYpos[0] == EnemiesYpos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy2 in Enemies2:
            if PlayersXpos[0] == Enemies2Xpos[cycle] and PlayersYpos[0] == Enemies2Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy3 in Enemies3:
            if PlayersXpos[0] == Enemies3Xpos[cycle] and PlayersYpos[0] == Enemies3Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy4 in Enemies4:
            if PlayersXpos[0] == Enemies4Xpos[cycle] and PlayersYpos[0] == Enemies4Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy5 in Enemies5:
            if PlayersXpos[0] == Enemies5Xpos[cycle] and PlayersYpos[0] == Enemies5Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy6 in Enemies6:
            if PlayersXpos[0] == Enemies6Xpos[cycle] and PlayersYpos[0] == Enemies6Ypos[cycle]:
                GameOver()
            cycle += 1
        if start == 0:
            NextWave()
        start = 1

    def AKey(event):
        global start
        self.player2.delete("all")
        self.player2.create_polygon(0,15,30,30,15,15,30,0,0,15,fill="white")
        if PlayersXpos[1] > 0:
            PlayersXpos[1] -= 25
        self.player2.place(x=PlayersXpos[1],y=PlayersYpos[1])
        PlayersDir[1] = "W"
        cycle = 0
        for enemy in Enemies:
            if PlayersXpos[1] == EnemiesXpos[cycle] and PlayersYpos[1] == EnemiesYpos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy2 in Enemies2:
            if PlayersXpos[1] == Enemies2Xpos[cycle] and PlayersYpos[1] == Enemies2Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy3 in Enemies3:
            if PlayersXpos[1] == Enemies3Xpos[cycle] and PlayersYpos[1] == Enemies3Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy4 in Enemies4:
            if PlayersXpos[1] == Enemies4Xpos[cycle] and PlayersYpos[1] == Enemies4Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy5 in Enemies5:
            if PlayersXpos[1] == Enemies5Xpos[cycle] and PlayersYpos[1] == Enemies5Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy6 in Enemies6:
            if PlayersXpos[1] == Enemies6Xpos[cycle] and PlayersYpos[1] == Enemies6Ypos[cycle]:
                GameOver()
            cycle += 1
        if start == 0:
            NextWave()
        start = 1

    def DKey(event):
        global start
        self.player2.delete("all")
        self.player2.create_polygon(30,15,0,30,15,15,0,0,30,15,fill="white")
        if PlayersXpos[1]  < 800:
            PlayersXpos[1]  += 25
        self.player2.place(x=PlayersXpos[1] ,y=PlayersYpos[1] )
        PlayersDir[1] = "E"
        cycle = 0
        for enemy in Enemies:
            if PlayersXpos[1]  == EnemiesXpos[cycle] and PlayersYpos[1]  == EnemiesYpos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy2 in Enemies2:
            if PlayersXpos[1]  == Enemies2Xpos[cycle] and PlayersYpos[1]  == Enemies2Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy3 in Enemies3:
            if PlayersXpos[1]  == Enemies3Xpos[cycle] and PlayersYpos[1]  == Enemies3Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy4 in Enemies4:
            if PlayersXpos[1]  == Enemies4Xpos[cycle] and PlayersYpos[1]  == Enemies4Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy5 in Enemies5:
            if PlayersXpos[1]  == Enemies5Xpos[cycle] and PlayersYpos[1]  == Enemies5Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy6 in Enemies6:
            if PlayersXpos[1]  == Enemies6Xpos[cycle] and PlayersYpos[1]  == Enemies6Ypos[cycle]:
                GameOver()
            cycle += 1
        if start == 0:
            NextWave()
        start = 1

    def WKey(event):
        global start
        self.player2.delete("all")
        self.player2.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="white")
        if PlayersYpos[1] > 0:
            PlayersYpos[1] -= 25
        self.player2.place(x=PlayersXpos[1],y=PlayersYpos[1])
        PlayersDir[1] = "N"
        cycle = 0
        for enemy in Enemies:
            if PlayersXpos[1] == EnemiesXpos[cycle] and PlayersYpos[1] == EnemiesYpos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy2 in Enemies2:
            if PlayersXpos[1] == Enemies2Xpos[cycle] and PlayersYpos[1] == Enemies2Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy3 in Enemies3:
            if PlayersXpos[1] == Enemies3Xpos[cycle] and PlayersYpos[1] == Enemies3Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy4 in Enemies4:
            if PlayersXpos[1] == Enemies4Xpos[cycle] and PlayersYpos[1] == Enemies4Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy5 in Enemies5:
            if PlayersXpos[1] == Enemies5Xpos[cycle] and PlayersYpos[1] == Enemies5Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy6 in Enemies6:
            if PlayersXpos[1] == Enemies6Xpos[cycle] and PlayersYpos[1] == Enemies6Ypos[cycle]:
                GameOver()
            cycle += 1
        if start == 0:
            NextWave()
        start = 1

    def SKey(event):
        global start
        self.player2.delete("all")
        self.player2.create_polygon(15,30,30,0,15,15,0,0,15,30,fill="white")
        if PlayersYpos[1] < 650:
            PlayersYpos[1] += 25
        self.player2.place(x=PlayersXpos[1],y=PlayersYpos[1])
        PlayersDir[1] = "S"
        cycle = 0
        for enemy in Enemies:
            if PlayersXpos[1] == EnemiesXpos[cycle] and PlayersYpos[1] == EnemiesYpos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy2 in Enemies2:
            if PlayersXpos[1] == Enemies2Xpos[cycle] and PlayersYpos[1] == Enemies2Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy3 in Enemies3:
            if PlayersXpos[1] == Enemies3Xpos[cycle] and PlayersYpos[1] == Enemies3Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy4 in Enemies4:
            if PlayersXpos[1] == Enemies4Xpos[cycle] and PlayersYpos[1] == Enemies4Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy5 in Enemies5:
            if PlayersXpos[1] == Enemies5Xpos[cycle] and PlayersYpos[1] == Enemies5Ypos[cycle]:
                GameOver()
            cycle += 1
        cycle = 0
        for enemy6 in Enemies6:
            if PlayersXpos[1] == Enemies6Xpos[cycle] and PlayersYpos[1] == Enemies6Ypos[cycle]:
                GameOver()
            cycle += 1
        if start == 0:
            NextWave()
        start = 1

    def CreateEnemy():
        global Xpos
        global Ypos
        global enXpos
        global enYpos
        global Damage
        global created
        enXpos = random.randrange(0,33)*25
        enYpos = random.randrange(0,27)*25
        while (abs(PlayersXpos[0] - enXpos) <= 75 and abs(PlayersYpos[0] - enYpos) <= 75) or (abs(PlayersXpos[1] - enXpos) <= 75 and abs(PlayersYpos[1] - enYpos) <= 75):
            enXpos = random.randrange(0,33)*25
            enYpos = random.randrange(0,27)*25
        self.enemy = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
        self.enemy.place(x=enXpos,y=enYpos)
        self.enemy.polygon = self.enemy.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="darkviolet")
        Enemies.append(self.enemy)
        EnemiesDmg.append(Damage)
        EnemiesXpos.append(enXpos)
        EnemiesYpos.append(enYpos)
        created = 1

    def CreateEnemy2():
        global Xpos
        global Ypos
        global en2Xpos
        global en2Ypos
        global created2
        en2Xpos = random.randrange(0,33)*25
        en2Ypos = random.randrange(0,27)*25
        while (abs(PlayersXpos[0] - en2Xpos) <= 75 and abs(PlayersYpos[0] - en2Ypos) <= 75) or (abs(PlayersXpos[1] - en2Xpos) <= 75 and abs(PlayersYpos[1] - en2Ypos) <= 75):
            en2Xpos = random.randrange(0,33)*25
            en2Ypos = random.randrange(0,27)*25
        self.enemy2 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
        self.enemy2.place(x=en2Xpos,y=en2Ypos)
        self.enemy2.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="red")
        Enemies2.append(self.enemy2)
        Enemies2Xpos.append(en2Xpos)
        Enemies2Ypos.append(en2Ypos)
        created2 = 1

    def CreateEnemy3():
        global Xpos
        global Ypos
        global en3Xpos
        global en3Ypos
        global Damage3
        global created3
        en3Xpos = random.randrange(0,33)*25
        en3Ypos = random.randrange(0,27)*25
        while (abs(PlayersXpos[0] - en3Xpos) <= 75 and abs(PlayersYpos[0] - en3Ypos) <= 75) or (abs(PlayersXpos[1] - en3Xpos) <= 75 and abs(PlayersYpos[1] - en3Ypos) <= 75):
            en3Xpos = random.randrange(0,33)*25
            en3Ypos = random.randrange(0,27)*25
        self.enemy3 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
        self.enemy3.place(x=en3Xpos,y=en3Ypos)
        self.enemy3.polygon = self.enemy3.create_polygon(10,0,0,0,0,30,30,30,30,0,20,0,20,10,10,10,fill="navy")
        Enemies3.append(self.enemy3)
        Enemies3Dmg.append(Damage3)
        Enemies3Xpos.append(en3Xpos)
        Enemies3Ypos.append(en3Ypos)
        created3 = 1

    def CreateEnemy4():
        global Xpos
        global Ypos
        global en4Xpos
        global en4Ypos
        global created4
        en4Xpos = random.randrange(0,33)*25
        en4Ypos = random.randrange(0,27)*25
        while (abs(PlayersXpos[0] - en4Xpos) <= 150 and abs(PlayersYpos[0] - en4Ypos) <= 150) or (abs(PlayersXpos[1] - en4Xpos) <= 150 and abs(PlayersYpos[1] - en4Ypos) <= 150):
            en4Xpos = random.randrange(0,33)*25
            en4Ypos = random.randrange(0,27)*25
        self.enemy4 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
        self.enemy4.place(x=en4Xpos,y=en4Ypos)
        self.enemy4.create_polygon(15,0,5,15,12,15,5,30,25,30,17,15,25,15,fill="darkgreen")
        Enemies4.append(self.enemy4)
        Enemies4Xpos.append(en4Xpos)
        Enemies4Ypos.append(en4Ypos)
        created4 = 1

    def CreateEnemy5():
        global Xpos
        global Ypos
        global en5Xpos
        global en5Ypos
        global Damage5
        global created5
        wall = random.choice(["N","E","S","W"])
        if wall == "N":
            en5Xpos = random.randrange(0,33)*25
            en5Ypos = 0
            self.enemy5 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
            self.enemy5.place(x=en5Xpos,y=en5Ypos)
            self.enemy5.polygon = self.enemy5.create_polygon(0,0,10,15,10,30,20,30,20,15,30,0,fill="darkorange2")
        elif wall == "E":
            en5Xpos = 800
            en5Ypos = random.randrange(0,27)*25
            self.enemy5 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
            self.enemy5.place(x=en5Xpos,y=en5Ypos)
            self.enemy5.polygon = self.enemy5.create_polygon(30,0,15,10,0,10,0,20,15,20,30,30,fill="darkorange2")
        elif wall == "S":
            en5Xpos = random.randrange(0,33)*25
            en5Ypos = 650
            self.enemy5 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
            self.enemy5.place(x=en5Xpos,y=en5Ypos)
            self.enemy5.polygon = self.enemy5.create_polygon(30,30,20,15,20,0,10,0,10,15,0,30,fill="darkorange2")
        elif wall == "W":
            en5Xpos = 0
            en5Ypos = random.randrange(0,27)*25
            self.enemy5 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
            self.enemy5.place(x=en5Xpos,y=en5Ypos)
            self.enemy5.polygon = self.enemy5.create_polygon(0,30,15,20,30,20,30,10,15,10,0,0,fill="darkorange2")
        while (abs(PlayersXpos[0] - en5Xpos) <= 75 and abs(PlayersYpos[0] - en5Ypos) <= 75) or (abs(PlayersXpos[1] - en5Xpos) <= 75 and abs(PlayersYpos[1] - en5Ypos) <= 75):
            wall = random.choice(["N","E","S","W"])
            if wall == "N":
                en5Xpos = random.randrange(0,33)*25
                en5Ypos = 0
                self.enemy5 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
                self.enemy5.place(x=en5Xpos,y=en5Ypos)
                self.enemy5.polygon = self.enemy5.create_polygon(0,0,10,15,10,30,20,30,20,15,30,0,fill="darkorange2")
            elif wall == "E":
                en5Xpos = 800
                en5Ypos = random.randrange(0,27)*25
                self.enemy5 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
                self.enemy5.place(x=en5Xpos,y=en5Ypos)
                self.enemy5.polygon = self.enemy5.create_polygon(30,0,15,10,0,10,0,20,15,20,30,30,fill="darkorange2")
            elif wall == "S":
                en5Xpos = random.randrange(0,33)*25
                en5Ypos = 650
                self.enemy5 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
                self.enemy5.place(x=en5Xpos,y=en5Ypos)
                self.enemy5.polygon = self.enemy5.create_polygon(30,30,20,15,20,0,10,0,10,15,0,30,fill="darkorange2")
            elif wall == "W":
                en5Xpos = 0
                en5Ypos = random.randrange(0,27)*25
                self.enemy5 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
                self.enemy5.place(x=en5Xpos,y=en5Ypos)
                self.enemy5.polygon = self.enemy5.create_polygon(0,30,15,20,30,20,30,10,15,10,0,0,fill="darkorange2")
        Enemies5.append(self.enemy5)
        Enemies5Dmg.append(Damage5)
        Enemies5Xpos.append(en5Xpos)
        Enemies5Ypos.append(en5Ypos)
        Enemies5Wall.append(wall)
        created5 = 1

    def CreateEnemy6():
        global Xpos
        global Ypos
        global en6Xpos
        global en6Ypos
        en6Type = random.choice([1,2,3,4])
        en6Xpos = random.randrange(0,33)*25
        en6Ypos = random.randrange(0,27)*25
        while (abs(PlayersXpos[0] - en6Xpos) <= 75 and abs(PlayersYpos[0] - en6Ypos) <= 75) or (abs(PlayersXpos[1] - en6Xpos) <= 75 and abs(PlayersYpos[1] - en6Ypos) <= 75):
            en6Xpos = random.randrange(0,33)*25
            en6Ypos = random.randrange(0,27)*25
        self.enemy6 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
        self.enemy6.place(x=en6Xpos,y=en6Ypos)
        self.enemy6.oval = self.enemy6.create_oval(0,0,30,30,fill="gray20")
        Enemies6.append(self.enemy6)
        Enemies6Xpos.append(en6Xpos)
        Enemies6Ypos.append(en6Ypos)
        Enemies6Type.append(en6Type)
        Enemies6Dmg.append(Damage6)

    def EnemyMove():
        global Xpos
        global Ypos
        global gameover
        global created
        if gameover != 1:
            self.after(300,EnemyMove)
            if created == 1:
                cycle = 0
                for self.enemy in Enemies:
                    rndDir = random.choice(["X","Y"])
                    if EnemiesDmg[cycle] == 0:
                        EnemyColor = "darkviolet"
                    else:
                        EnemyColor = "violet"
                    if ((PlayersXpos[0] - EnemiesXpos[cycle])**2 + (PlayersYpos[0] - EnemiesYpos[cycle])**2)**0.5 <= ((PlayersXpos[1] - EnemiesXpos[cycle])**2 + (PlayersYpos[1] - EnemiesYpos[cycle])**2)**0.5:
                        #Target Player 1
                        if PlayersXpos[0] < EnemiesXpos[cycle] and PlayersYpos[0] < EnemiesYpos[cycle]:
                            self.enemy.delete("all")
                            if rndDir == "X":
                                EnemiesXpos[cycle] -= 25
                                self.enemy.polygon = self.enemy.create_polygon(0,15,30,30,15,15,30,0,0,15,fill=EnemyColor)
                            else:
                                EnemiesYpos[cycle] -= 25
                                self.enemy.polygon = self.enemy.create_polygon(15,0,30,30,15,15,0,30,15,0,fill=EnemyColor)
                        elif PlayersXpos[0] < EnemiesXpos[cycle] and PlayersYpos[0] > EnemiesYpos[cycle]:
                            self.enemy.delete("all")
                            if rndDir == "X":
                                EnemiesXpos[cycle] -= 25
                                self.enemy.polygon = self.enemy.create_polygon(0,15,30,30,15,15,30,0,0,15,fill=EnemyColor)
                            else:
                                EnemiesYpos[cycle] += 25
                                self.enemy.polygon = self.enemy.create_polygon(15,30,30,0,15,15,0,0,15,30,fill=EnemyColor)
                        elif PlayersXpos[0] > EnemiesXpos[cycle] and PlayersYpos[0] < EnemiesYpos[cycle]:
                            self.enemy.delete("all")
                            if rndDir == "X":
                                EnemiesXpos[cycle] += 25
                                self.enemy.polygon = self.enemy.create_polygon(30,15,0,30,15,15,0,0,30,15,fill=EnemyColor)
                            else:
                                EnemiesYpos[cycle] -= 25
                                self.enemy.polygon = self.enemy.create_polygon(15,0,30,30,15,15,0,30,15,0,fill=EnemyColor)
                        elif PlayersXpos[0] > EnemiesXpos[cycle] and PlayersYpos[0] > EnemiesYpos[cycle]:
                            self.enemy.delete("all")
                            if rndDir == "X":
                                EnemiesXpos[cycle] += 25
                                self.enemy.polygon = self.enemy.create_polygon(30,15,0,30,15,15,0,0,30,15,fill=EnemyColor)
                            else:
                                EnemiesYpos[cycle] += 25
                                self.enemy.polygon = self.enemy.create_polygon(15,30,30,0,15,15,0,0,15,30,fill=EnemyColor)
                        elif PlayersXpos[0] < EnemiesXpos[cycle] and PlayersYpos[0] == EnemiesYpos[cycle]:
                            self.enemy.delete("all")
                            self.enemy.polygon = self.enemy.create_polygon(0,15,30,30,15,15,30,0,0,15,fill=EnemyColor)
                            EnemiesXpos[cycle] -= 25
                        elif PlayersXpos[0] > EnemiesXpos[cycle] and PlayersYpos[0] == EnemiesYpos[cycle]:
                            self.enemy.delete("all")
                            self.enemy.polygon = self.enemy.create_polygon(30,15,0,30,15,15,0,0,30,15,fill=EnemyColor)
                            EnemiesXpos[cycle] += 25
                        elif PlayersXpos[0] == EnemiesXpos[cycle] and PlayersYpos[0] < EnemiesYpos[cycle]:
                            self.enemy.delete("all")
                            self.enemy.polygon = self.enemy.create_polygon(15,0,30,30,15,15,0,30,15,0,fill=EnemyColor)
                            EnemiesYpos[cycle] -= 25
                        elif PlayersXpos[0] == EnemiesXpos[cycle] and PlayersYpos[0] > EnemiesYpos[cycle]:
                            self.enemy.delete("all")
                            self.enemy.polygon = self.enemy.create_polygon(15,30,30,0,15,15,0,0,15,30,fill=EnemyColor)
                            EnemiesYpos[cycle] += 25
                    else:
                        #Target Player 2
                        if PlayersXpos[1] < EnemiesXpos[cycle] and PlayersYpos[1] < EnemiesYpos[cycle]:
                            self.enemy.delete("all")
                            if rndDir == "X":
                                EnemiesXpos[cycle] -= 25
                                self.enemy.polygon = self.enemy.create_polygon(0,15,30,30,15,15,30,0,0,15,fill=EnemyColor)
                            else:
                                EnemiesYpos[cycle] -= 25
                                self.enemy.polygon = self.enemy.create_polygon(15,0,30,30,15,15,0,30,15,0,fill=EnemyColor)
                        elif PlayersXpos[1] < EnemiesXpos[cycle] and PlayersYpos[1] > EnemiesYpos[cycle]:
                            self.enemy.delete("all")
                            if rndDir == "X":
                                EnemiesXpos[cycle] -= 25
                                self.enemy.polygon = self.enemy.create_polygon(0,15,30,30,15,15,30,0,0,15,fill=EnemyColor)
                            else:
                                EnemiesYpos[cycle] += 25
                                self.enemy.polygon = self.enemy.create_polygon(15,30,30,0,15,15,0,0,15,30,fill=EnemyColor)
                        elif PlayersXpos[1] > EnemiesXpos[cycle] and PlayersYpos[1] < EnemiesYpos[cycle]:
                            self.enemy.delete("all")
                            if rndDir == "X":
                                EnemiesXpos[cycle] += 25
                                self.enemy.polygon = self.enemy.create_polygon(30,15,0,30,15,15,0,0,30,15,fill=EnemyColor)
                            else:
                                EnemiesYpos[cycle] -= 25
                                self.enemy.polygon = self.enemy.create_polygon(15,0,30,30,15,15,0,30,15,0,fill=EnemyColor)
                        elif PlayersXpos[1] > EnemiesXpos[cycle] and PlayersYpos[1] > EnemiesYpos[cycle]:
                            self.enemy.delete("all")
                            if rndDir == "X":
                                EnemiesXpos[cycle] += 25
                                self.enemy.polygon = self.enemy.create_polygon(30,15,0,30,15,15,0,0,30,15,fill=EnemyColor)
                            else:
                                EnemiesYpos[cycle] += 25
                                self.enemy.polygon = self.enemy.create_polygon(15,30,30,0,15,15,0,0,15,30,fill=EnemyColor)
                        elif PlayersXpos[1] < EnemiesXpos[cycle] and PlayersYpos[1] == EnemiesYpos[cycle]:
                            self.enemy.delete("all")
                            self.enemy.polygon = self.enemy.create_polygon(0,15,30,30,15,15,30,0,0,15,fill=EnemyColor)
                            EnemiesXpos[cycle] -= 25
                        elif PlayersXpos[1] > EnemiesXpos[cycle] and PlayersYpos[1] == EnemiesYpos[cycle]:
                            self.enemy.delete("all")
                            self.enemy.polygon = self.enemy.create_polygon(30,15,0,30,15,15,0,0,30,15,fill=EnemyColor)
                            EnemiesXpos[cycle] += 25
                        elif PlayersXpos[1] == EnemiesXpos[cycle] and PlayersYpos[1] < EnemiesYpos[cycle]:
                            self.enemy.delete("all")
                            self.enemy.polygon = self.enemy.create_polygon(15,0,30,30,15,15,0,30,15,0,fill=EnemyColor)
                            EnemiesYpos[cycle] -= 25
                        elif PlayersXpos[1] == EnemiesXpos[cycle] and PlayersYpos[1] > EnemiesYpos[cycle]:
                            self.enemy.delete("all")
                            self.enemy.polygon = self.enemy.create_polygon(15,30,30,0,15,15,0,0,15,30,fill=EnemyColor)
                            EnemiesYpos[cycle] += 25
                    self.enemy.place(x=EnemiesXpos[cycle],y=EnemiesYpos[cycle])
                    for Pcycle in range(0,2):
                        if PlayersXpos[Pcycle] == EnemiesXpos[cycle] and PlayersYpos[Pcycle] == EnemiesYpos[cycle]:
                            GameOver()
                    cycle += 1

    def Enemy2Move():
        global Xpos
        global Ypos
        global gameover
        global created2
        if gameover != 1:
            self.after(300,Enemy2Move)
            if created2 == 1:
                cycle = 0
                for self.enemy2 in Enemies2:
                    if ((PlayersXpos[0] - Enemies2Xpos[cycle])**2 + (PlayersYpos[0] - Enemies2Ypos[cycle])**2)**0.5 <= ((PlayersXpos[1] - Enemies2Xpos[cycle])**2 + (PlayersYpos[1] - Enemies2Ypos[cycle])**2)**0.5:
                        #Target Player 1
                        if PlayersXpos[0] < Enemies2Xpos[cycle] and PlayersYpos[0] < Enemies2Ypos[cycle]:
                            self.enemy2.delete("all")
                            self.enemy2.create_polygon(0,0,30,15,15,15,15,30,0,0,fill="red")
                            Enemies2Xpos[cycle] -= 25
                            Enemies2Ypos[cycle] -= 25
                        elif PlayersXpos[0] < Enemies2Xpos[cycle] and PlayersYpos[0] > Enemies2Ypos[cycle]:
                            self.enemy2.delete("all")
                            self.enemy2.create_polygon(0,30,15,0,15,15,30,15,0,30,fill="red")
                            Enemies2Xpos[cycle] -= 25
                            Enemies2Ypos[cycle] += 25
                        elif PlayersXpos[0] > Enemies2Xpos[cycle] and PlayersYpos[0] < Enemies2Ypos[cycle]:
                            self.enemy2.delete("all")
                            self.enemy2.create_polygon(30,0,0,15,15,15,15,30,30,0,fill="red")
                            Enemies2Xpos[cycle] += 25
                            Enemies2Ypos[cycle] -= 25
                        elif PlayersXpos[0] > Enemies2Xpos[cycle] and PlayersYpos[0] > Enemies2Ypos[cycle]:
                            self.enemy2.delete("all")
                            self.enemy2.create_polygon(30,30,15,0,15,15,0,15,30,30,fill="red")
                            Enemies2Xpos[cycle] += 25
                            Enemies2Ypos[cycle] += 25
                        elif PlayersXpos[0] < Enemies2Xpos[cycle] and PlayersYpos[0] == Enemies2Ypos[cycle]:
                            self.enemy2.delete("all")
                            self.enemy2.create_polygon(0,15,30,30,15,15,30,0,0,15,fill="red")
                            Enemies2Xpos[cycle] -= 25
                        elif PlayersXpos[0] > Enemies2Xpos[cycle] and PlayersYpos[0] == Enemies2Ypos[cycle]:
                            self.enemy2.delete("all")
                            self.enemy2.create_polygon(30,15,0,30,15,15,0,0,30,15,fill="red")
                            Enemies2Xpos[cycle] += 25
                        elif PlayersXpos[0] == Enemies2Xpos[cycle] and PlayersYpos[0] < Enemies2Ypos[cycle]:
                            self.enemy2.delete("all")
                            self.enemy2.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="red")
                            Enemies2Ypos[cycle] -= 25
                        elif PlayersXpos[0] == Enemies2Xpos[cycle] and PlayersYpos[0] > Enemies2Ypos[cycle]:
                            self.enemy2.delete("all")
                            self.enemy2.create_polygon(15,30,30,0,15,15,0,0,15,30,fill="red")
                            Enemies2Ypos[cycle] += 25
                    else:
                        #Target Player 2
                        if PlayersXpos[1] < Enemies2Xpos[cycle] and PlayersYpos[1] < Enemies2Ypos[cycle]:
                            self.enemy2.delete("all")
                            self.enemy2.create_polygon(0,0,30,15,15,15,15,30,0,0,fill="red")
                            Enemies2Xpos[cycle] -= 25
                            Enemies2Ypos[cycle] -= 25
                        elif PlayersXpos[1] < Enemies2Xpos[cycle] and PlayersYpos[1] > Enemies2Ypos[cycle]:
                            self.enemy2.delete("all")
                            self.enemy2.create_polygon(0,30,15,0,15,15,30,15,0,30,fill="red")
                            Enemies2Xpos[cycle] -= 25
                            Enemies2Ypos[cycle] += 25
                        elif PlayersXpos[1] > Enemies2Xpos[cycle] and PlayersYpos[1] < Enemies2Ypos[cycle]:
                            self.enemy2.delete("all")
                            self.enemy2.create_polygon(30,0,0,15,15,15,15,30,30,0,fill="red")
                            Enemies2Xpos[cycle] += 25
                            Enemies2Ypos[cycle] -= 25
                        elif PlayersXpos[1] > Enemies2Xpos[cycle] and PlayersYpos[1] > Enemies2Ypos[cycle]:
                            self.enemy2.delete("all")
                            self.enemy2.create_polygon(30,30,15,0,15,15,0,15,30,30,fill="red")
                            Enemies2Xpos[cycle] += 25
                            Enemies2Ypos[cycle] += 25
                        elif PlayersXpos[1] < Enemies2Xpos[cycle] and PlayersYpos[1] == Enemies2Ypos[cycle]:
                            self.enemy2.delete("all")
                            self.enemy2.create_polygon(0,15,30,30,15,15,30,0,0,15,fill="red")
                            Enemies2Xpos[cycle] -= 25
                        elif PlayersXpos[1] > Enemies2Xpos[cycle] and PlayersYpos[1] == Enemies2Ypos[cycle]:
                            self.enemy2.delete("all")
                            self.enemy2.create_polygon(30,15,0,30,15,15,0,0,30,15,fill="red")
                            Enemies2Xpos[cycle] += 25
                        elif PlayersXpos[1] == Enemies2Xpos[cycle] and PlayersYpos[1] < Enemies2Ypos[cycle]:
                            self.enemy2.delete("all")
                            self.enemy2.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="red")
                            Enemies2Ypos[cycle] -= 25
                        elif PlayersXpos[1] == Enemies2Xpos[cycle] and PlayersYpos[1] > Enemies2Ypos[cycle]:
                            self.enemy2.delete("all")
                            self.enemy2.create_polygon(15,30,30,0,15,15,0,0,15,30,fill="red")
                            Enemies2Ypos[cycle] += 25
                    self.enemy2.place(x=Enemies2Xpos[cycle],y=Enemies2Ypos[cycle])
                    for Pcycle in range(0,2):
                            if PlayersXpos[Pcycle] == Enemies2Xpos[cycle] and PlayersYpos[Pcycle] == Enemies2Ypos[cycle]:
                                GameOver()
                    cycle += 1

    def Enemy3Move():
        global Xpos
        global Ypos
        global gameover
        global created3
        if gameover != 1:
            self.after(350,Enemy3Move)
            if created3 == 1:
                cycle = 0
                for self.enemy3 in Enemies3:
                    rndDir = random.choice(["X","Y"])
                    if Enemies3Dmg[cycle] == 0:
                        Enemy3Color = "navy"
                    elif Enemies3Dmg[cycle] == 1:
                        Enemy3Color = "blue"
                    elif Enemies3Dmg[cycle] == 2:
                        Enemy3Color = "dodgerblue"
                    elif Enemies3Dmg[cycle] == 3:
                        Enemy3Color = "deepskyblue"
                    else:
                        Enemy3Color = "lightskyblue"
                    if ((PlayersXpos[0] - Enemies3Xpos[cycle])**2 + (PlayersYpos[0] - Enemies3Ypos[cycle])**2)**0.5 <= ((PlayersXpos[1] - Enemies3Xpos[cycle])**2 + (PlayersYpos[1] - Enemies3Ypos[cycle])**2)**0.5:
                        #Target Player 1
                        if PlayersXpos[0] < Enemies3Xpos[cycle] and PlayersYpos[0] < Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            if rndDir == "X":
                                Enemies3Xpos[cycle] -= 25
                                self.enemy3.polygon = self.enemy3.create_polygon(0,20,0,30,30,30,30,0,0,0,0,10,10,10,10,20,fill=Enemy3Color)
                            else:
                                Enemies3Ypos[cycle] -= 25
                                self.enemy3.polygon = self.enemy3.create_polygon(10,0,0,0,0,30,30,30,30,0,20,0,20,10,10,10,fill=Enemy3Color)
                        elif PlayersXpos[0] < Enemies3Xpos[cycle] and PlayersYpos[0] > Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            if rndDir == "X":
                                Enemies3Xpos[cycle] -= 25
                                self.enemy3.polygon = self.enemy3.create_polygon(0,20,0,30,30,30,30,0,0,0,0,10,10,10,10,20,fill=Enemy3Color)
                            else:
                                Enemies3Ypos[cycle] += 25
                                self.enemy3.polygon = self.enemy3.create_polygon(20,30,30,30,30,0,0,0,0,30,10,30,10,20,20,20,fill=Enemy3Color)
                        elif PlayersXpos[0] > Enemies3Xpos[cycle] and PlayersYpos[0] < Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            if rndDir == "X":
                                Enemies3Xpos[cycle] += 25
                                self.enemy3.polygon = self.enemy3.create_polygon(30,10,30,0,0,0,0,30,30,30,30,20,20,20,20,10,fill=Enemy3Color)
                            else:
                                Enemies3Ypos[cycle] -= 25
                                self.enemy3.polygon = self.enemy3.create_polygon(10,0,0,0,0,30,30,30,30,0,20,0,20,10,10,10,fill=Enemy3Color)
                        elif PlayersXpos[0] > Enemies3Xpos[cycle] and PlayersYpos[0] > Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            if rndDir == "X":
                                Enemies3Xpos[cycle] += 25
                                self.enemy3.polygon = self.enemy3.create_polygon(30,10,30,0,0,0,0,30,30,30,30,20,20,20,20,10,fill=Enemy3Color)
                            else:
                                Enemies3Ypos[cycle] += 25
                                self.enemy3.polygon = self.enemy3.create_polygon(20,30,30,30,30,0,0,0,0,30,10,30,10,20,20,20,fill=Enemy3Color)
                        elif PlayersXpos[0] < Enemies3Xpos[cycle] and PlayersYpos[0] == Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            self.enemy3.polygon = self.enemy3.create_polygon(0,20,0,30,30,30,30,0,0,0,0,10,10,10,10,20,fill=Enemy3Color)
                            Enemies3Xpos[cycle] -= 25
                        elif PlayersXpos[0] > Enemies3Xpos[cycle] and PlayersYpos[0] == Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            self.enemy3.polygon = self.enemy3.create_polygon(30,10,30,0,0,0,0,30,30,30,30,20,20,20,20,10,fill=Enemy3Color)
                            Enemies3Xpos[cycle] += 25
                        elif PlayersXpos[0] == Enemies3Xpos[cycle] and PlayersYpos[0] < Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            self.enemy3.polygon = self.enemy3.create_polygon(10,0,0,0,0,30,30,30,30,0,20,0,20,10,10,10,fill=Enemy3Color)
                            Enemies3Ypos[cycle] -= 25
                        elif PlayersXpos[0] == Enemies3Xpos[cycle] and PlayersYpos[0] > Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            self.enemy3.polygon = self.enemy3.create_polygon(20,30,30,30,30,0,0,0,0,30,10,30,10,20,20,20,fill=Enemy3Color)
                            Enemies3Ypos[cycle] += 25
                    else:
                    #Target Player 2
                        if PlayersXpos[1] < Enemies3Xpos[cycle] and PlayersYpos[1] < Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            if rndDir == "X":
                                Enemies3Xpos[cycle] -= 25
                                self.enemy3.polygon = self.enemy3.create_polygon(0,20,0,30,30,30,30,0,0,0,0,10,10,10,10,20,fill=Enemy3Color)
                            else:
                                Enemies3Ypos[cycle] -= 25
                                self.enemy3.polygon = self.enemy3.create_polygon(10,0,0,0,0,30,30,30,30,0,20,0,20,10,10,10,fill=Enemy3Color)
                        elif PlayersXpos[1] < Enemies3Xpos[cycle] and PlayersYpos[1] > Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            if rndDir == "X":
                                Enemies3Xpos[cycle] -= 25
                                self.enemy3.polygon = self.enemy3.create_polygon(0,20,0,30,30,30,30,0,0,0,0,10,10,10,10,20,fill=Enemy3Color)
                            else:
                                Enemies3Ypos[cycle] += 25
                                self.enemy3.polygon = self.enemy3.create_polygon(20,30,30,30,30,0,0,0,0,30,10,30,10,20,20,20,fill=Enemy3Color)
                        elif PlayersXpos[1] > Enemies3Xpos[cycle] and PlayersYpos[1] < Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            if rndDir == "X":
                                Enemies3Xpos[cycle] += 25
                                self.enemy3.polygon = self.enemy3.create_polygon(30,10,30,0,0,0,0,30,30,30,30,20,20,20,20,10,fill=Enemy3Color)
                            else:
                                Enemies3Ypos[cycle] -= 25
                                self.enemy3.polygon = self.enemy3.create_polygon(10,0,0,0,0,30,30,30,30,0,20,0,20,10,10,10,fill=Enemy3Color)
                        elif PlayersXpos[1] > Enemies3Xpos[cycle] and PlayersYpos[1] > Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            if rndDir == "X":
                                Enemies3Xpos[cycle] += 25
                                self.enemy3.polygon = self.enemy3.create_polygon(30,10,30,0,0,0,0,30,30,30,30,20,20,20,20,10,fill=Enemy3Color)
                            else:
                                Enemies3Ypos[cycle] += 25
                                self.enemy3.polygon = self.enemy3.create_polygon(20,30,30,30,30,0,0,0,0,30,10,30,10,20,20,20,fill=Enemy3Color)
                        elif PlayersXpos[1] < Enemies3Xpos[cycle] and PlayersYpos[1] == Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            self.enemy3.polygon = self.enemy3.create_polygon(0,20,0,30,30,30,30,0,0,0,0,10,10,10,10,20,fill=Enemy3Color)
                            Enemies3Xpos[cycle] -= 25
                        elif PlayersXpos[1] > Enemies3Xpos[cycle] and PlayersYpos[1] == Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            self.enemy3.polygon = self.enemy3.create_polygon(30,10,30,0,0,0,0,30,30,30,30,20,20,20,20,10,fill=Enemy3Color)
                            Enemies3Xpos[cycle] += 25
                        elif PlayersXpos[1] == Enemies3Xpos[cycle] and PlayersYpos[1] < Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            self.enemy3.polygon = self.enemy3.create_polygon(10,0,0,0,0,30,30,30,30,0,20,0,20,10,10,10,fill=Enemy3Color)
                            Enemies3Ypos[cycle] -= 25
                        elif PlayersXpos[1] == Enemies3Xpos[cycle] and PlayersYpos[1] > Enemies3Ypos[cycle]:
                            self.enemy3.delete("all")
                            self.enemy3.polygon = self.enemy3.create_polygon(20,30,30,30,30,0,0,0,0,30,10,30,10,20,20,20,fill=Enemy3Color)
                            Enemies3Ypos[cycle] += 25
                    self.enemy3.place(x=Enemies3Xpos[cycle],y=Enemies3Ypos[cycle])
                    for Pcycle in range(0,2):
                        if PlayersXpos[Pcycle] == Enemies3Xpos[cycle] and PlayersYpos[Pcycle] == Enemies3Ypos[cycle]:
                            GameOver()
                    cycle += 1

    def Enemy4Move():
        global Xpos
        global Ypos
        global gameover
        global created4
        if gameover != 1:
            self.after(100,Enemy4Move)
            if created4 == 1:
                cycle = 0
                for self.enemy4 in Enemies4:
                    rndDir = random.choice(["X","Y"])
                    Enemy4Color = "darkgreen"
                    if ((PlayersXpos[0] - Enemies4Xpos[cycle])**2 + (PlayersYpos[0] - Enemies4Ypos[cycle])**2)**0.5 <= ((PlayersXpos[1] - Enemies4Xpos[cycle])**2 + (PlayersYpos[1] - Enemies4Ypos[cycle])**2)**0.5:
                        #Target Player 1
                        if PlayersXpos[0] < Enemies4Xpos[cycle] and PlayersYpos[0] < Enemies4Ypos[cycle]:
                            self.enemy4.delete("all")
                            if rndDir == "X":
                                Enemies4Xpos[cycle] -= 25
                                self.enemy4.polygon = self.enemy4.create_polygon(0,15,15,25,15,17,30,25,30,5,15,13,15,5,fill=Enemy4Color)
                            else:
                                Enemies4Ypos[cycle] -= 25
                                self.enemy4.polygon = self.enemy4.create_polygon(15,0,5,15,12,15,5,30,25,30,17,15,25,15,fill=Enemy4Color)
                        elif PlayersXpos[0] < Enemies4Xpos[cycle] and PlayersYpos[0] > Enemies4Ypos[cycle]:
                            self.enemy4.delete("all")
                            if rndDir == "X":
                                Enemies4Xpos[cycle] -= 25
                                self.enemy4.polygon = self.enemy4.create_polygon(0,15,15,25,15,17,30,25,30,5,15,13,15,5,fill=Enemy4Color)
                            else:
                                Enemies4Ypos[cycle] += 25
                                self.enemy4.polygon = self.enemy4.create_polygon(15,30,25,15,17,15,25,0,5,0,13,15,5,15,fill=Enemy4Color)
                        elif PlayersXpos[0] > Enemies4Xpos[cycle] and PlayersYpos[0] < Enemies4Ypos[cycle]:
                            self.enemy4.delete("all")
                            if rndDir == "X":
                                Enemies4Xpos[cycle] += 25
                                self.enemy4.polygon = self.enemy4.create_polygon(30,15,15,5,15,13,0,5,0,25,15,17,15,25,fill=Enemy4Color)
                            else:
                                Enemies4Ypos[cycle] -= 25
                                self.enemy4.polygon = self.enemy4.create_polygon(15,0,5,15,12,15,5,30,25,30,17,15,25,15,fill=Enemy4Color)
                        elif PlayersXpos[0] > Enemies4Xpos[cycle] and PlayersYpos[0] > Enemies4Ypos[cycle]:
                            self.enemy4.delete("all")
                            if rndDir == "X":
                                Enemies4Xpos[cycle] += 25
                                self.enemy4.polygon = self.enemy4.create_polygon(30,15,15,5,15,13,0,5,0,25,15,17,15,25,fill=Enemy4Color)
                            else:
                                Enemies4Ypos[cycle] += 25
                                self.enemy4.polygon = self.enemy4.create_polygon(15,30,25,15,17,15,25,0,5,0,13,15,5,15,fill=Enemy4Color)
                        elif PlayersXpos[0] < Enemies4Xpos[cycle] and PlayersYpos[0] == Enemies4Ypos[cycle]:
                            self.enemy4.delete("all")
                            self.enemy4.polygon = self.enemy4.create_polygon(0,15,15,25,15,17,30,25,30,5,15,13,15,5,fill=Enemy4Color)
                            Enemies4Xpos[cycle] -= 25
                        elif PlayersXpos[0] > Enemies4Xpos[cycle] and PlayersYpos[0] == Enemies4Ypos[cycle]:
                            self.enemy4.delete("all")
                            self.enemy4.polygon = self.enemy4.create_polygon(30,15,15,5,15,13,0,5,0,25,15,17,15,25,fill=Enemy4Color)
                            Enemies4Xpos[cycle] += 25
                        elif PlayersXpos[0] == Enemies4Xpos[cycle] and PlayersYpos[0] < Enemies4Ypos[cycle]:
                            self.enemy4.delete("all")
                            self.enemy4.polygon = self.enemy4.create_polygon(15,0,5,15,12,15,5,30,25,30,17,15,25,15,fill=Enemy4Color)
                            Enemies4Ypos[cycle] -= 25
                        elif PlayersXpos[0] == Enemies4Xpos[cycle] and PlayersYpos[0] > Enemies4Ypos[cycle]:
                            self.enemy4.delete("all")
                            self.enemy4.polygon = self.enemy4.create_polygon(15,30,25,15,17,15,25,0,5,0,13,15,5,15,fill=Enemy4Color)
                            Enemies4Ypos[cycle] += 25
                    else:
                        #Target Player 2
                        if PlayersXpos[1] < Enemies4Xpos[cycle] and PlayersYpos[1] < Enemies4Ypos[cycle]:
                            self.enemy4.delete("all")
                            if rndDir == "X":
                                Enemies4Xpos[cycle] -= 25
                                self.enemy4.polygon = self.enemy4.create_polygon(0,15,15,25,15,17,30,25,30,5,15,13,15,5,fill=Enemy4Color)
                            else:
                                Enemies4Ypos[cycle] -= 25
                                self.enemy4.polygon = self.enemy4.create_polygon(15,0,5,15,12,15,5,30,25,30,17,15,25,15,fill=Enemy4Color)
                        elif PlayersXpos[1] < Enemies4Xpos[cycle] and PlayersYpos[1] > Enemies4Ypos[cycle]:
                            self.enemy4.delete("all")
                            if rndDir == "X":
                                Enemies4Xpos[cycle] -= 25
                                self.enemy4.polygon = self.enemy4.create_polygon(0,15,15,25,15,17,30,25,30,5,15,13,15,5,fill=Enemy4Color)
                            else:
                                Enemies4Ypos[cycle] += 25
                                self.enemy4.polygon = self.enemy4.create_polygon(15,30,25,15,17,15,25,0,5,0,13,15,5,15,fill=Enemy4Color)
                        elif PlayersXpos[1] > Enemies4Xpos[cycle] and PlayersYpos[1] < Enemies4Ypos[cycle]:
                            self.enemy4.delete("all")
                            if rndDir == "X":
                                Enemies4Xpos[cycle] += 25
                                self.enemy4.polygon = self.enemy4.create_polygon(30,15,15,5,15,13,0,5,0,25,15,17,15,25,fill=Enemy4Color)
                            else:
                                Enemies4Ypos[cycle] -= 25
                                self.enemy4.polygon = self.enemy4.create_polygon(15,0,5,15,12,15,5,30,25,30,17,15,25,15,fill=Enemy4Color)
                        elif PlayersXpos[1] > Enemies4Xpos[cycle] and PlayersYpos[1] > Enemies4Ypos[cycle]:
                            self.enemy4.delete("all")
                            if rndDir == "X":
                                Enemies4Xpos[cycle] += 25
                                self.enemy4.polygon = self.enemy4.create_polygon(30,15,15,5,15,13,0,5,0,25,15,17,15,25,fill=Enemy4Color)
                            else:
                                Enemies4Ypos[cycle] += 25
                                self.enemy4.polygon = self.enemy4.create_polygon(15,30,25,15,17,15,25,0,5,0,13,15,5,15,fill=Enemy4Color)
                        elif PlayersXpos[1] < Enemies4Xpos[cycle] and PlayersYpos[1] == Enemies4Ypos[cycle]:
                            self.enemy4.delete("all")
                            self.enemy4.polygon = self.enemy4.create_polygon(0,15,15,25,15,17,30,25,30,5,15,13,15,5,fill=Enemy4Color)
                            Enemies4Xpos[cycle] -= 25
                        elif PlayersXpos[1] > Enemies4Xpos[cycle] and PlayersYpos[1] == Enemies4Ypos[cycle]:
                            self.enemy4.delete("all")
                            self.enemy4.polygon = self.enemy4.create_polygon(30,15,15,5,15,13,0,5,0,25,15,17,15,25,fill=Enemy4Color)
                            Enemies4Xpos[cycle] += 25
                        elif PlayersXpos[1] == Enemies4Xpos[cycle] and PlayersYpos[1] < Enemies4Ypos[cycle]:
                            self.enemy4.delete("all")
                            self.enemy4.polygon = self.enemy4.create_polygon(15,0,5,15,12,15,5,30,25,30,17,15,25,15,fill=Enemy4Color)
                            Enemies4Ypos[cycle] -= 25
                        elif PlayersXpos[1] == Enemies4Xpos[cycle] and PlayersYpos[1] > Enemies4Ypos[cycle]:
                            self.enemy4.delete("all")
                            self.enemy4.polygon = self.enemy4.create_polygon(15,30,25,15,17,15,25,0,5,0,13,15,5,15,fill=Enemy4Color)
                            Enemies4Ypos[cycle] += 25
                    self.enemy4.place(x=Enemies4Xpos[cycle],y=Enemies4Ypos[cycle])
                    for Pcycle in range(0,2):
                        if PlayersXpos[Pcycle] == Enemies4Xpos[cycle] and PlayersYpos[Pcycle] == Enemies4Ypos[cycle]:
                            GameOver()
                    cycle += 1

    def Enemy5Move():
        global Xpos
        global Ypos
        global gameover
        global created5
        if gameover != 1:
            self.after(500,Enemy5Move)
            if created5 == 1:
                cycle = 0
                for self.enemy5 in Enemies5:
                    if ((PlayersXpos[0] - Enemies5Xpos[cycle])**2 + (PlayersYpos[0] - Enemies5Ypos[cycle])**2)**0.5 <= ((PlayersXpos[1] - Enemies5Xpos[cycle])**2 + (PlayersYpos[1] - Enemies5Ypos[cycle])**2)**0.5:
                        #Target Player 1
                        if (Enemies5Wall[cycle] == "E" or Enemies5Wall[cycle] == "W") and PlayersYpos[0] < Enemies5Ypos[cycle]:
                            Enemies5Ypos[cycle] -= 25
                        elif (Enemies5Wall[cycle] == "E" or Enemies5Wall[cycle] == "W") and PlayersYpos[0] > Enemies5Ypos[cycle]:
                            Enemies5Ypos[cycle] += 25
                        elif PlayersXpos[0] < Enemies5Xpos[cycle] and (Enemies5Wall[cycle] == "N" or Enemies5Wall[cycle] == "S"):
                            Enemies5Xpos[cycle] -= 25
                        elif PlayersXpos[0] > Enemies5Xpos[cycle] and (Enemies5Wall[cycle] == "N" or Enemies5Wall[cycle] == "S"):
                            Enemies5Xpos[cycle] += 25
                    else:
                        #Target Player 2
                        if (Enemies5Wall[cycle] == "E" or Enemies5Wall[cycle] == "W") and PlayersYpos[1] < Enemies5Ypos[cycle]:
                            Enemies5Ypos[cycle] -= 25
                        elif (Enemies5Wall[cycle] == "E" or Enemies5Wall[cycle] == "W") and PlayersYpos[1] > Enemies5Ypos[cycle]:
                            Enemies5Ypos[cycle] += 25
                        elif PlayersXpos[1] < Enemies5Xpos[cycle] and (Enemies5Wall[cycle] == "N" or Enemies5Wall[cycle] == "S"):
                            Enemies5Xpos[cycle] -= 25
                        elif PlayersXpos[1] > Enemies5Xpos[cycle] and (Enemies5Wall[cycle] == "N" or Enemies5Wall[cycle] == "S"):
                            Enemies5Xpos[cycle] += 25
                    self.enemy5.place(x=Enemies5Xpos[cycle],y=Enemies5Ypos[cycle])
                    for Pcycle in range(0,2):
                        if PlayersXpos[Pcycle] == Enemies5Xpos[cycle] and PlayersYpos[Pcycle] == Enemies5Ypos[cycle]:
                            GameOver()
                    for Pcycle in range(0,2):
                        if Enemies5Wall[cycle] == "E" or Enemies5Wall[cycle] == "W":
                            if Enemies5Ypos[cycle] == PlayersYpos[Pcycle]:
                                enShoot()
                        else:
                            if Enemies5Xpos[cycle] == PlayersXpos[Pcycle]:
                                enShoot()
                    cycle += 1

    def Generate():
        global generated1
        global generated2
        global generated3
        global generated4
        if gameover != 1:
            self.after(10,Generate)
            if generated1 == 0:
                GenerateEnemy1()
                generated1 = 1000
            if generated2 == 0:
                GenerateEnemy2()
                generated2 = 1250
            if generated3 == 0:
                GenerateEnemy3()
                generated3 = 1500
            if generated4 == 0:
                GenerateEnemy4()
                generated4 = 1750
            generated1 -= 10
            generated2 -= 10
            generated3 -= 10
            generated4 -= 10

    def GenerateEnemy1():
        global enXpos
        global enYpos
        global Damage
        global created
        cycle = 0
        for self.enemy6 in Enemies6:
            if Enemies6Type[cycle] == 1:
                enXpos = Enemies6Xpos[cycle]
                enYpos = Enemies6Ypos[cycle]
                self.enemy = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
                self.enemy.place(x=enXpos,y=enYpos)
                self.enemy.polygon = self.enemy.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="darkviolet")
                Enemies.append(self.enemy)
                EnemiesDmg.append(Damage)
                EnemiesXpos.append(enXpos)
                EnemiesYpos.append(enYpos)
                created = 1
            cycle += 1

    def GenerateEnemy2():
        global en2Xpos
        global en2Ypos
        global created2
        cycle = 0
        for self.enemy6 in Enemies6:
            if Enemies6Type[cycle] == 2:
                en2Xpos = Enemies6Xpos[cycle]
                en2Ypos = Enemies6Ypos[cycle]
                self.enemy2 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
                self.enemy2.place(x=en2Xpos,y=en2Ypos)
                self.enemy2.create_polygon(15,0,30,30,15,15,0,30,15,0,fill="red")
                Enemies2.append(self.enemy2)
                Enemies2Xpos.append(en2Xpos)
                Enemies2Ypos.append(en2Ypos)
                created2 = 1
            cycle += 1

    def GenerateEnemy3():
        global en3Xpos
        global en3Ypos
        global Damage3
        global created3
        cycle = 0
        for self.enemy6 in Enemies6:
            if Enemies6Type[cycle] == 3:
                en3Xpos = Enemies6Xpos[cycle]
                en3Ypos = Enemies6Ypos[cycle]
                self.enemy3 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
                self.enemy3.place(x=en3Xpos,y=en3Ypos)
                self.enemy3.polygon = self.enemy3.create_polygon(10,0,0,0,0,30,30,30,30,0,20,0,20,10,10,10,fill="navy")
                Enemies3.append(self.enemy3)
                Enemies3Dmg.append(Damage3)
                Enemies3Xpos.append(en3Xpos)
                Enemies3Ypos.append(en3Ypos)
                created3 = 1
            cycle += 1

    def GenerateEnemy4():
        global en4Xpos
        global en4Ypos
        global created4
        cycle = 0
        for self.enemy6 in Enemies6:
            if Enemies6Type[cycle] == 4:
                en4Xpos = Enemies6Xpos[cycle]
                en4Ypos = Enemies6Ypos[cycle]
                self.enemy4 = Canvas(self,bg="black",highlightthickness=0,width=30,height=30)
                self.enemy4.place(x=en4Xpos,y=en4Ypos)
                self.enemy4.create_polygon(15,0,5,15,12,15,5,30,25,30,17,15,25,15,fill="darkgreen")
                Enemies4.append(self.enemy4)
                Enemies4Xpos.append(en4Xpos)
                Enemies4Ypos.append(en4Ypos)
                created4 = 1
            cycle += 1

    def Shoot(event):
        global Xpos
        global Ypos
        global direction
        global start
        if PlayersDir[0] == "N":
            shotXpos = PlayersXpos[0] + 10
            shotYpos = PlayersYpos[0] - 10
        elif PlayersDir[0] == "E":
            shotXpos = PlayersXpos[0] + 30
            shotYpos = PlayersYpos[0] + 10
        elif PlayersDir[0] == "S":
            shotXpos = PlayersXpos[0] + 10
            shotYpos = PlayersYpos[0] + 30
        elif PlayersDir[0] == "W":
            shotXpos = PlayersXpos[0] - 10
            shotYpos = PlayersYpos[0] + 10
        self.shot = Canvas(bg="black",highlightthickness=0,width=10,height=10)
        self.shot.place(x=shotXpos,y=shotYpos)
        self.shot.create_oval(0,0,10,10,fill="white")
        Shots.append(self.shot)
        ShotsXpos.append(shotXpos)
        ShotsYpos.append(shotYpos)
        ShotDir.append(PlayersDir[0])
        if start == 0:
            NextWave()
        start = 1

    def Shoot2(event):
        global start
        if PlayersDir[1] == "N":
            shotXpos = PlayersXpos[1] + 10
            shotYpos = PlayersYpos[1] - 10
        elif PlayersDir[1] == "E":
            shotXpos = PlayersXpos[1] + 30
            shotYpos = PlayersYpos[1] + 10
        elif PlayersDir[1] == "S":
            shotXpos = PlayersXpos[1] + 10
            shotYpos = PlayersYpos[1] + 30
        elif PlayersDir[1] == "W":
            shotXpos = PlayersXpos[1] - 10
            shotYpos = PlayersYpos[1] + 10
        self.shot = Canvas(bg="black",highlightthickness=0,width=10,height=10)
        self.shot.place(x=shotXpos,y=shotYpos)
        self.shot.create_oval(0,0,10,10,fill="white")
        Shots.append(self.shot)
        ShotsXpos.append(shotXpos)
        ShotsYpos.append(shotYpos)
        ShotDir.append(PlayersDir[1])
        if start == 0:
            NextWave()
        start = 1

    def enShoot():
        cycle = 0
        for self.enemy5 in Enemies5:
            if Enemies5Wall[cycle] == "N":
                enDir = "S"
                enShotXpos = Enemies5Xpos[cycle] + 10
                enShotYpos = Enemies5Ypos[cycle] + 30
            elif Enemies5Wall[cycle] == "E":
                enDir = "W"
                enShotXpos = Enemies5Xpos[cycle] - 10
                enShotYpos = Enemies5Ypos[cycle] + 10
            elif Enemies5Wall[cycle] == "S":
                enDir = "N"
                enShotXpos = Enemies5Xpos[cycle] + 10
                enShotYpos = Enemies5Ypos[cycle] - 10
            elif Enemies5Wall[cycle] == "W":
                enDir = "E"
                enShotXpos = Enemies5Xpos[cycle] + 30
                enShotYpos = Enemies5Ypos[cycle] + 10
            if Enemies5Wall[cycle] == "E" or Enemies5Wall[cycle] == "W":
                for Pcycle in range(0,2):
                    if Enemies5Ypos[cycle] == PlayersYpos[Pcycle]:
                        self.enShot = Canvas(bg="black",highlightthickness=0,width=10,height=10)
                        self.enShot.place(x=enShotXpos,y=enShotYpos)
                        self.enShot.create_oval(0,0,10,10,fill="yellow")
                        enShots.append(self.enShot)
                        enShotsXpos.append(enShotXpos)
                        enShotsYpos.append(enShotYpos)
                        enShotDir.append(enDir)
            else:
                for Pcycle in range(0,2):
                    if Enemies5Xpos[cycle] == PlayersXpos[Pcycle]:
                        self.enShot = Canvas(bg="black",highlightthickness=0,width=10,height=10)
                        self.enShot.place(x=enShotXpos,y=enShotYpos)
                        self.enShot.create_oval(0,0,10,10,fill="yellow")
                        enShots.append(self.enShot)
                        enShotsXpos.append(enShotXpos)
                        enShotsYpos.append(enShotYpos)
                        enShotDir.append(enDir)
            cycle += 1
            
    def ShotMove():
        global direction
        global en2Xpos
        global en2Ypos
        global destroy
        global gameover
        if gameover != 1:
            self.after(10,ShotMove)
            #Move Shots
            cycle = 0
            for self.shot in Shots:
                destroy = -1
                if ShotDir[cycle] == "N":
                    ShotsYpos[cycle] -= 10
                elif ShotDir[cycle] == "E":
                    ShotsXpos[cycle] += 10
                elif ShotDir[cycle] == "S":
                    ShotsYpos[cycle] += 10
                elif ShotDir[cycle] == "W":
                    ShotsXpos[cycle] -= 10
                self.shot.place(x=ShotsXpos[cycle],y=ShotsYpos[cycle])
                #Damage Enemy1
                enCycle = 0
                for self.enemy in Enemies:
                    if destroy == -1:
                        if EnemiesXpos[enCycle] + 30 >= ShotsXpos[cycle] >= EnemiesXpos[enCycle] - 10 and EnemiesYpos[enCycle] + 30 >= ShotsYpos[cycle] >= EnemiesYpos[enCycle] - 10:
                            destroy = 0
                            if EnemiesDmg[enCycle] == 1:
                                self.explode = Canvas(bg="black",highlightthickness=0,width=30,height=30)
                                self.explode.place(x=EnemiesXpos[enCycle],y=EnemiesYpos[enCycle])
                                self.explode.create_polygon(0,15,13,13,15,0,17,13,30,15,17,17,15,30,13,17,fill="orange")
                                Explosions.append(self.explode)
                                self.enemy.destroy()
                                del Enemies[enCycle]
                                del EnemiesDmg[enCycle]
                                del EnemiesXpos[enCycle]
                                del EnemiesYpos[enCycle]
                                self.after(10,destroyEnemy)
                                self.shot.destroy()
                                del Shots[cycle]
                                del ShotsXpos[cycle]
                                del ShotsYpos[cycle]
                                del ShotDir[cycle]
                            else:
                                self.shot.destroy()
                                del Shots[cycle]
                                del ShotsXpos[cycle]
                                del ShotsYpos[cycle]
                                del ShotDir[cycle]
                                EnemiesDmg[enCycle] += 1
                                if EnemiesDmg[enCycle] == 0:
                                    EnemyColor = "darkviolet"
                                else:
                                    EnemyColor = "violet"
                                self.enemy.itemconfig(self.enemy.polygon,fill=EnemyColor)
                        enCycle += 1
                #Damage Enemy2
                enCycle = 0
                for self.enemy2 in Enemies2:
                    if destroy == -1:
                        if Enemies2Xpos[enCycle] + 30 >= ShotsXpos[cycle] >= Enemies2Xpos[enCycle] - 10 and Enemies2Ypos[enCycle] + 30 >= ShotsYpos[cycle] >= Enemies2Ypos[enCycle] - 10:
                            destroy = 0
                            self.explode = Canvas(bg="black",highlightthickness=0,width=30,height=30)
                            self.explode.place(x=Enemies2Xpos[enCycle],y=Enemies2Ypos[enCycle])
                            self.explode.create_polygon(0,15,13,13,15,0,17,13,30,15,17,17,15,30,13,17,fill="orange")
                            Explosions.append(self.explode)
                            self.enemy2.destroy()
                            del Enemies2[enCycle]
                            del Enemies2Xpos[enCycle]
                            del Enemies2Ypos[enCycle]
                            self.shot.destroy()
                            del Shots[cycle]
                            del ShotsXpos[cycle]
                            del ShotsYpos[cycle]
                            del ShotDir[cycle]
                            self.after(10,destroyEnemy)
                        enCycle += 1
                #Damage Enemy3
                enCycle = 0
                for self.enemy3 in Enemies3:
                    if destroy == -1:
                        if Enemies3Xpos[enCycle] + 30 >= ShotsXpos[cycle] >= Enemies3Xpos[enCycle] - 10 and Enemies3Ypos[enCycle] + 30 >= ShotsYpos[cycle] >= Enemies3Ypos[enCycle] - 10:
                            destroy = 0
                            if Enemies3Dmg[enCycle] == 4:
                                self.explode = Canvas(bg="black",highlightthickness=0,width=30,height=30)
                                self.explode.place(x=Enemies3Xpos[enCycle],y=Enemies3Ypos[enCycle])
                                self.explode.create_polygon(0,15,13,13,15,0,17,13,30,15,17,17,15,30,13,17,fill="orange")
                                Explosions.append(self.explode)
                                self.enemy3.destroy()
                                del Enemies3[enCycle]
                                del Enemies3Dmg[enCycle]
                                del Enemies3Xpos[enCycle]
                                del Enemies3Ypos[enCycle]
                                self.after(10,destroyEnemy)
                                self.shot.destroy()
                                del Shots[cycle]
                                del ShotsXpos[cycle]
                                del ShotsYpos[cycle]
                                del ShotDir[cycle]
                            else:
                                self.shot.destroy()
                                del Shots[cycle]
                                del ShotsXpos[cycle]
                                del ShotsYpos[cycle]
                                del ShotDir[cycle]
                                Enemies3Dmg[enCycle] += 1
                                if Enemies3Dmg[enCycle] == 0:
                                    Enemy3Color = "navy"
                                elif Enemies3Dmg[enCycle] == 1:
                                    Enemy3Color = "darkblue"
                                elif Enemies3Dmg[enCycle] == 2:
                                    Enemy3Color = "dodgerblue"
                                elif Enemies3Dmg[enCycle] == 3:
                                    Enemy3Color = "deepskyblue"
                                else:
                                    Enemy3Color = "lightskyblue"
                                self.enemy3.itemconfig(self.enemy3.polygon,fill=Enemy3Color)
                        enCycle += 1
                #Damage Enemy4
                enCycle = 0
                for self.enemy4 in Enemies4:
                    if destroy == -1:
                        if Enemies4Xpos[enCycle] + 30 >= ShotsXpos[cycle] >= Enemies4Xpos[enCycle] - 10 and Enemies4Ypos[enCycle] + 30 >= ShotsYpos[cycle] >= Enemies4Ypos[enCycle] - 10:
                            destroy = 0
                            self.explode = Canvas(bg="black",highlightthickness=0,width=30,height=30)
                            self.explode.place(x=Enemies4Xpos[enCycle],y=Enemies4Ypos[enCycle])
                            self.explode.create_polygon(0,15,13,13,15,0,17,13,30,15,17,17,15,30,13,17,fill="orange")
                            Explosions.append(self.explode)
                            self.enemy4.destroy()
                            del Enemies4[enCycle]
                            del Enemies4Xpos[enCycle]
                            del Enemies4Ypos[enCycle]
                            self.shot.destroy()
                            del Shots[cycle]
                            del ShotsXpos[cycle]
                            del ShotsYpos[cycle]
                            del ShotDir[cycle]
                            self.after(10,destroyEnemy)
                        enCycle += 1
                #Damage Enemy5
                enCycle = 0
                for self.enemy5 in Enemies5:
                    if destroy == -1:
                        if Enemies5Xpos[enCycle] + 30 >= ShotsXpos[cycle] >= Enemies5Xpos[enCycle] - 10 and Enemies5Ypos[enCycle] + 30 >= ShotsYpos[cycle] >= Enemies5Ypos[enCycle] - 10:
                            destroy = 0
                            if Enemies5Dmg[enCycle] == 1:
                                self.explode = Canvas(bg="black",highlightthickness=0,width=30,height=30)
                                self.explode.place(x=Enemies5Xpos[enCycle],y=Enemies5Ypos[enCycle])
                                self.explode.create_polygon(0,15,13,13,15,0,17,13,30,15,17,17,15,30,13,17,fill="orange")
                                Explosions.append(self.explode)
                                self.enemy5.destroy()
                                del Enemies5[enCycle]
                                del Enemies5Dmg[enCycle]
                                del Enemies5Xpos[enCycle]
                                del Enemies5Ypos[enCycle]
                                del Enemies5Wall[enCycle]
                                self.after(10,destroyEnemy)
                                self.shot.destroy()
                                del Shots[cycle]
                                del ShotsXpos[cycle]
                                del ShotsYpos[cycle]
                                del ShotDir[cycle]
                            else:
                                self.shot.destroy()
                                del Shots[cycle]
                                del ShotsXpos[cycle]
                                del ShotsYpos[cycle]
                                del ShotDir[cycle]
                                Enemies5Dmg[enCycle] += 1
                                if Enemies5Dmg[enCycle] == 0:
                                    Enemy5Color = "darkorange2"
                                else:
                                    Enemy5Color = "orange"
                                self.enemy5.itemconfig(self.enemy5.polygon,fill=Enemy5Color)
                        enCycle += 1
                #Damage Enemy6
                enCycle = 0
                for self.enemy6 in Enemies6:
                    if destroy == -1:
                        if Enemies6Xpos[enCycle] + 30 >= ShotsXpos[cycle] >= Enemies6Xpos[enCycle] - 10 and Enemies6Ypos[enCycle] + 30 >= ShotsYpos[cycle] >= Enemies6Ypos[enCycle] - 10:
                            destroy = 0
                            if Enemies6Dmg[enCycle] == 5:
                                self.explode = Canvas(bg="black",highlightthickness=0,width=30,height=30)
                                self.explode.place(x=Enemies6Xpos[enCycle],y=Enemies6Ypos[enCycle])
                                self.explode.create_polygon(0,15,13,13,15,0,17,13,30,15,17,17,15,30,13,17,fill="orange")
                                Explosions.append(self.explode)
                                self.enemy6.destroy()
                                del Enemies6[enCycle]
                                del Enemies6Dmg[enCycle]
                                del Enemies6Xpos[enCycle]
                                del Enemies6Ypos[enCycle]
                                del Enemies6Type[enCycle]
                                self.after(10,destroyEnemy)
                                self.shot.destroy()
                                del Shots[cycle]
                                del ShotsXpos[cycle]
                                del ShotsYpos[cycle]
                                del ShotDir[cycle]
                            else:
                                self.shot.destroy()
                                del Shots[cycle]
                                del ShotsXpos[cycle]
                                del ShotsYpos[cycle]
                                del ShotDir[cycle]
                                Enemies6Dmg[enCycle] += 1
                                if Enemies6Dmg[enCycle] == 0:
                                    Enemy6Color = "gray20"
                                elif Enemies6Dmg[enCycle] == 1:
                                    Enemy6Color = "gray30"
                                elif Enemies6Dmg[enCycle] == 2:
                                    Enemy6Color = "gray40"
                                elif Enemies6Dmg[enCycle] == 3:
                                    Enemy6Color = "gray50"
                                elif Enemies6Dmg[enCycle] == 4:
                                    Enemy6Color = "gray60"
                                elif Enemies6Dmg[enCycle] == 5:
                                    Enemy6Color = "gray70"
                                self.enemy6.itemconfig(self.enemy6.oval,fill=Enemy6Color)
                        enCycle += 1
                #Destroy Shot at Boundary
                if destroy == -1:
                    if ShotsXpos[cycle] < 0 or ShotsXpos[cycle] > 830 or ShotsYpos[cycle] < 0 or ShotsYpos[cycle] > 680:
                        self.shot.destroy()
                        del Shots[cycle]
                        del ShotsXpos[cycle]
                        del ShotsYpos[cycle]
                        del ShotDir[cycle]
                cycle += 1

    def enShotMove():
        global gameover
        if gameover != 1:
            self.after(10,enShotMove)
            cycle = 0
            for self.enShot in enShots:
                enDestroy = -1
                if enShotDir[cycle] == "N":
                    enShotsYpos[cycle] -= 10
                elif enShotDir[cycle] == "E":
                    enShotsXpos[cycle] += 10
                elif enShotDir[cycle] == "S":
                    enShotsYpos[cycle] += 10
                elif enShotDir[cycle] == "W":
                    enShotsXpos[cycle] -= 10
                self.enShot.place(x=enShotsXpos[cycle],y=enShotsYpos[cycle])
                #Game Over
                for Pcycle in range(0,2):
                    if gameover != 1:
                        if PlayersXpos[Pcycle] + 30 >= enShotsXpos[cycle] >= PlayersXpos[Pcycle] - 10 and PlayersYpos[Pcycle] + 30 >= enShotsYpos[cycle] >= PlayersYpos[Pcycle] - 10:
                            enDestroy = 0
                            self.enShot.destroy()
                            del enShots[cycle]
                            del enShotsXpos[cycle]
                            del enShotsYpos[cycle]
                            del enShotDir[cycle]
                            GameOver()
                #Destroy Shot at Boundary
                if enDestroy == -1:
                    if enShotsXpos[cycle] < 0 or enShotsXpos[cycle] > 830 or enShotsYpos[cycle] < 0 or enShotsYpos[cycle] > 680:
                        self.enShot.destroy()
                        del enShots[cycle]
                        del enShotsXpos[cycle]
                        del enShotsYpos[cycle]
                        del enShotDir[cycle] 
                cycle += 1

    def destroyEnemy():
        destroyed = 0
        for self.explode in Explosions:
            self.explode.destroy()
            del Explosions[destroyed]
            destroyed += 1            

    def Summon():
        global wave
        time = 0
        wave += 1
        #Wave 1
        if wave == 1:
            E = 0
            while E < W1E1:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < W1E2:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
            E = 0
            while E < W1E3:
                self.after(time,CreateEnemy3)
                E += 1
                time += 250
            E = 0
            while E < W1E4:
                self.after(time,CreateEnemy4)
                E += 1
                time += 250
            E = 0
            while E < W1E5:
                self.after(time,CreateEnemy5)
                E += 1
                time += 250
            E = 0
            while E < W1E6:
                self.after(time,CreateEnemy6)
                E += 1
                time += 250
        #Wave 2
        if wave == 2:
            E = 0
            while E < W2E1:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < W2E2:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
            E = 0
            while E < W2E3:
                self.after(time,CreateEnemy3)
                E += 1
                time += 250
            E = 0
            while E < W2E4:
                self.after(time,CreateEnemy4)
                E += 1
                time += 250
            E = 0
            while E < W2E5:
                self.after(time,CreateEnemy5)
                E += 1
                time += 250
            E = 0
            while E < W2E6:
                self.after(time,CreateEnemy6)
                E += 1
                time += 250
        #Wave 3
        if wave == 3:
            E = 0
            while E < W3E1:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < W3E2:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
            E = 0
            while E < W3E3:
                self.after(time,CreateEnemy3)
                E += 1
                time += 250
            E = 0
            while E < W3E4:
                self.after(time,CreateEnemy4)
                E += 1
                time += 250
            E = 0
            while E < W3E5:
                self.after(time,CreateEnemy5)
                E += 1
                time += 250
            E = 0
            while E < W3E6:
                self.after(time,CreateEnemy6)
                E += 1
                time += 250
        #Wave 4
        if wave == 4:
            E = 0
            while E < W4E1:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < W4E2:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
            E = 0
            while E < W4E3:
                self.after(time,CreateEnemy3)
                E += 1
                time += 250
            E = 0
            while E < W4E4:
                self.after(time,CreateEnemy4)
                E += 1
                time += 250
            E = 0
            while E < W4E5:
                self.after(time,CreateEnemy5)
                E += 1
                time += 250
            E = 0
            while E < W4E6:
                self.after(time,CreateEnemy6)
                E += 1
                time += 250
        #Wave 5
        if wave == 5:
            E = 0
            while E < W5E1:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < W5E2:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
            E = 0
            while E < W5E3:
                self.after(time,CreateEnemy3)
                E += 1
                time += 250
            E = 0
            while E < W5E4:
                self.after(time,CreateEnemy4)
                E += 1
                time += 250
            E = 0
            while E < W5E5:
                self.after(time,CreateEnemy5)
                E += 1
                time += 250
            E = 0
            while E < W5E6:
                self.after(time,CreateEnemy6)
                E += 1
                time += 250
        #Wave 6
        if wave == 6:
            E = 0
            while E < W6E1:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < W6E2:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
            E = 0
            while E < W6E3:
                self.after(time,CreateEnemy3)
                E += 1
                time += 250
            E = 0
            while E < W6E4:
                self.after(time,CreateEnemy4)
                E += 1
                time += 250
            E = 0
            while E < W6E5:
                self.after(time,CreateEnemy5)
                E += 1
                time += 250
            E = 0
            while E < W6E6:
                self.after(time,CreateEnemy6)
                E += 1
                time += 250
        #Wave 7
        if wave == 7:
            E = 0
            while E < W7E1:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < W7E2:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
            E = 0
            while E < W7E3:
                self.after(time,CreateEnemy3)
                E += 1
                time += 250
            E = 0
            while E < W7E4:
                self.after(time,CreateEnemy4)
                E += 1
                time += 250
            E = 0
            while E < W7E5:
                self.after(time,CreateEnemy5)
                E += 1
                time += 250
            E = 0
            while E < W7E6:
                self.after(time,CreateEnemy6)
                E += 1
                time += 250
        #Wave 8
        if wave == 8:
            E = 0
            while E < W8E1:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < W8E2:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
            E = 0
            while E < W8E3:
                self.after(time,CreateEnemy3)
                E += 1
                time += 250
            E = 0
            while E < W8E4:
                self.after(time,CreateEnemy4)
                E += 1
                time += 250
            E = 0
            while E < W8E5:
                self.after(time,CreateEnemy5)
                E += 1
                time += 250
            E = 0
            while E < W8E6:
                self.after(time,CreateEnemy6)
                E += 1
                time += 250
        #Wave 9
        if wave == 9:
            E = 0
            while E < W9E1:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < W9E2:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
            E = 0
            while E < W9E3:
                self.after(time,CreateEnemy3)
                E += 1
                time += 250
            E = 0
            while E < W9E4:
                self.after(time,CreateEnemy4)
                E += 1
                time += 250
            E = 0
            while E < W9E5:
                self.after(time,CreateEnemy5)
                E += 1
                time += 250
            E = 0
            while E < W9E6:
                self.after(time,CreateEnemy6)
                E += 1
                time += 250
        #Wave 10
        if wave == 10:
            E = 0
            while E < W10E1:
                self.after(time,CreateEnemy)
                E += 1
                time += 250
            E = 0
            while E < W10E2:
                self.after(time,CreateEnemy2)
                E += 1
                time += 250
            E = 0
            while E < W10E3:
                self.after(time,CreateEnemy3)
                E += 1
                time += 250
            E = 0
            while E < W10E4:
                self.after(time,CreateEnemy4)
                E += 1
                time += 250
            E = 0
            while E < W10E5:
                self.after(time,CreateEnemy5)
                E += 1
                time += 250
            E = 0
            while E < W10E6:
                self.after(time,CreateEnemy6)
                E += 1
                time += 250
        #Win
        if wave == 11:
            Winner()

    def NextWave():
        global wave
        global gameover
        if gameover == 0:
            self.after(10,NextWave)
            if not Enemies and not Enemies2 and not Enemies3 and not Enemies4 and not Enemies5 and not Enemies6:
                Summon()
                if wave != 11:
                    self.lbScore.config(text="Wave: "+str(wave)+"  Press 'p' to pause")

    def Winner():
        global gameover
        if gameover == 0:
            gameover = 1
            self.unbind('<Left>')
            self.unbind('<Right>')
            self.unbind('<Up>')
            self.unbind('<Down>')
            self.unbind('<space>')
            self.after_cancel(EnemyMove)
            self.after_cancel(Enemy2Move)
            self.after_cancel(Enemy3Move)
            self.after_cancel(Enemy4Move)
            self.after_cancel(Enemy5Move)
            self.after_cancel(CreateEnemy)
            self.after_cancel(CreateEnemy2)
            self.after_cancel(CreateEnemy3)
            self.after_cancel(CreateEnemy4)
            self.after_cancel(CreateEnemy5)
            self.after_cancel(CreateEnemy6)
            self.after_cancel(Generate)
            self.after_cancel(NextWave)
            self.after_cancel(ShotMove)
            self.after_cancel(enShotMove)
            for self.shot in Shots:
                self.shot.destroy()
            self.lbScore.destroy()
            self.lbWinner = Label(text="You Win!!!",bg="black",fg="white")
            self.lbWinner.pack(fill=BOTH,expand=1)
            self.btnMainMenu = Button(text="Main Menu")
            self.btnMainMenu.pack(side=LEFT)
            self.btnMainMenu.bind('<Button>',StartMainMenu)

    def GameOver():
        global gameover
        global wave
        if gameover == 0:
            gameover = 1
            self.unbind('<Left>')
            self.unbind('<Right>')
            self.unbind('<Up>')
            self.unbind('<Down>')
            self.unbind('<space>')
            self.after_cancel(EnemyMove)
            self.after_cancel(Enemy2Move)
            self.after_cancel(Enemy3Move)
            self.after_cancel(Enemy4Move)
            self.after_cancel(Enemy5Move)
            self.after_cancel(CreateEnemy)
            self.after_cancel(CreateEnemy2)
            self.after_cancel(CreateEnemy3)
            self.after_cancel(CreateEnemy4)
            self.after_cancel(CreateEnemy5)
            self.after_cancel(CreateEnemy6)
            self.after_cancel(Generate)
            self.after_cancel(NextWave)
            self.after_cancel(ShotMove)
            self.after_cancel(enShotMove)
            for self.shot in Shots:
                self.shot.destroy()
            self.lbScore.destroy()
            self.lbGameOver = Label(text="Game Over" + "\n" "You survived to wave " + str(wave) + "\n" + "Click here to restart",bg="black",fg="white")
            self.lbGameOver.pack(fill=BOTH,expand=1)
            self.lbGameOver.bind('<Button>',Restart)
            self.btnMainMenu = Button(text="Main Menu")
            self.btnMainMenu.pack(side=LEFT)
            self.btnMainMenu.bind('<Button>',StartMainMenu)

    def Restart(event):
        self.destroy()
        TenWaveChallengeMultiPlayer()

    def Pause(event):
        global pause
        global gameover
        if pause == 0:
            gameover = 1
            pause = 1
            self.unbind('<Left>')
            self.unbind('<Right>')
            self.unbind('<Up>')
            self.unbind('<Down>')
            self.unbind('<space>')
            self.after_cancel(EnemyMove)
            self.after_cancel(Enemy2Move)
            self.after_cancel(Enemy3Move)
            self.after_cancel(Enemy4Move)
            self.after_cancel(Enemy5Move)
            self.after_cancel(CreateEnemy)
            self.after_cancel(CreateEnemy2)
            self.after_cancel(CreateEnemy3)
            self.after_cancel(CreateEnemy4)
            self.after_cancel(CreateEnemy5)
            self.after_cancel(CreateEnemy6)
            self.after_cancel(Generate)
            self.after_cancel(NextWave)
            self.after_cancel(ShotMove)
            self.after_cancel(enShotMove)
            for self.shot in Shots:
                self.shot.destroy()
            self.lbScore.destroy()
            self.lbPause = Label(text="Paused"+"\n"+"Press 'p' to Unpause",bg="black",fg="white")
            self.lbPause.pack(fill=BOTH,expand=1)
            self.btnMainMenu = Button(text="Main Menu")
            self.btnMainMenu.pack(side=LEFT)
            self.btnMainMenu.bind('<Button>',StartMainMenu)
        elif pause == 1:
            gameover = 0
            pause = 0
            self.bind('<Left>',LeftKey)
            self.bind('<Right>',RightKey)
            self.bind('<Up>',UpKey)
            self.bind('<Down>',DownKey)
            self.bind('<space>',Shoot)
            EnemyMove()
            Enemy2Move()
            Enemy3Move()
            Enemy4Move()
            Enemy5Move()
            Generate()
            ShotMove()
            enShotMove()
            self.lbScore = Label(text="Wave: "+str(wave)+"  Press 'p' to pause",bg="black",fg="white")
            self.lbScore.place(x=165,y=680,width=500,height=20)
            NextWave()
            self.lbPause.destroy()
            self.btnMainMenu.unbind('<Button>')
            self.btnMainMenu.destroy()

    def Exit(event):
        self.destroy()

    def StartMainMenu(event):
        self.destroy()
        MainMenu()

    #Bindings
    self.bind('<Left>',LeftKey)
    self.bind('<Right>',RightKey)
    self.bind('<Up>',UpKey)
    self.bind('<Down>',DownKey)
    self.bind('<a>',AKey)
    self.bind('<d>',DKey)
    self.bind('<w>',WKey)
    self.bind('<s>',SKey)
    self.bind('<Escape>',Exit)
    self.bind('<space>',Shoot)
    self.bind('<Tab>',Shoot2)
    self.bind('<p>',Pause)

    EnemyMove()
    Enemy2Move()
    Enemy3Move()
    Enemy4Move()
    Enemy5Move()
    Generate()
    ShotMove()
    enShotMove()
        
    #Frame settings
    self.geometry("830x700")
    self.title("Space Assault")
    self.configure(bg="black")

MainMenu()
