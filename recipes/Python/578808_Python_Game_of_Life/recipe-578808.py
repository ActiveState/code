import pygame
import pygame._view
from pygame.locals import *
import sys
import random

pygame.init()

class Cell(pygame.sprite.Sprite):
    def __init__(self, game, pos, num):
        pygame.sprite.Sprite.__init__(self)

        self.game = game

        self.num = num
        self.color = self.getColor()
    
        self.parent = 0

        self.image = pygame.Surface([10,10])
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
        self.alive = False
        self.edge = False

        self.a_neighbors = []
        self.d_neighbors = []

        self.n = (num - 74) - 1
        self.e = (num + 1) - 1
        self.s = (num + 74) - 1
        self.w = (num - 1) - 1
        self.ne = (self.n + 1)
        self.se = (self.s + 1)
        self.nw = (self.n - 1)
        self.sw = (self.s - 1)

        self.cell_list = [
            self.n,
            self.e,
            self.s,
            self.w,
            self.ne,
            self.se,
            self.nw,
            self.sw]

        self.game.cells.append(self)
    def getColor(self):
        value = [i for i in range(100,255,25)]
        r = random.choice(value)
        g = random.choice(value)
        b = random.choice(value)
        return (r,g,b)
        
        
    def die(self):
        self.alive = False

    def live(self):
        self.alive = True
 
    def update(self):
        if not self.edge:
            self.a_neighbors = []
            self.d_neighbors = []
            neighbors = [self.game.cells[cell] for cell in self.cell_list]

            for n in neighbors:
                if n.alive:
                    self.a_neighbors.append(True)
                else:
                    self.d_neighbors.append(True)   

            if not self.game.running:
                    
                if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(self.game.mpos):
                    self.alive = True
                    self.image.fill(self.color)
                    
                if pygame.mouse.get_pressed()[2] and self.rect.collidepoint(self.game.mpos)and self.alive:
                    self.image.fill((0,0,0))
                    self.alive = False
                if self.alive:
                    self.image.fill(self.color)
            else:
                if self.alive:
                    self.image.fill(self.color)
                    
                if not self.alive:
                    self.image.fill((0, 0, 0))
                    
        else:
            self.image.fill((255, 255, 255))
        

            


class Game():
    def __init__(self):
        #window setup
        pygame.display.set_caption('Game Of Life')

        # initiate the clock and screen
        self.clock = pygame.time.Clock()
        self.last_tick = pygame.time.get_ticks()
        self.screen_res = [740, 490]

        self.font = pygame.font.SysFont("Impact", 19)

        self.sprites = pygame.sprite.Group()
        self.cells = []
        self.generation = 0
        self.population = 0

        self.screen = pygame.display.set_mode(self.screen_res, pygame.HWSURFACE, 32)

        self.running = False
        self.createGrid()
     
        while 1:
            self.Loop()

    def createGrid(self):
        col = 0
        row = 50
        cell_num = 0

        for y in xrange(44):
            for x in xrange(74):
                cell_num +=1
                cell = Cell(self, [col, row], cell_num)
                if row == 50 or row  == 480 or col == 0 or col == 730:
                    cell.edge = True
                self.sprites.add(cell)
                col += 10
            row += 10
            col = 0
          
    def Run(self):
        self.population = 0
        for cell in self.cells:
            if cell.alive:
                self.population += 1
                if len(cell.a_neighbors) < 2:
                    cell.die()
                elif len(cell.a_neighbors) > 3:
                    cell.die()
                elif len(cell.a_neighbors) == 2 or len(cell.a_neighbors) == 3:
                    cell.live()
            else:
                if len(cell.a_neighbors) == 3:
                    cell.live()
                    
    def blitDirections(self):
        text = self.font.render("Press Enter to begin, and Space to stop and clear board", 1, (255,255,255))
        generations = self.font.render("Generation: %s" %str(self.generation), 1, (255,255,255))
        pop = self.font.render("Pop: %s" %str(self.population), 1, (255,255,255))
        self.screen.blit(text, (10, 15))
        self.screen.blit(generations, (500, 15))
        self.screen.blit(pop, (650, 15))

    def Loop(self):
        # main game loop
        self.eventLoop()
        
        self.Tick()
        self.Draw()
        pygame.display.update()

    def eventLoop(self):
        # the main event loop, detects keypresses
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    self.running = True
                if event.key == K_SPACE:
                    self.running = False
                    self.sprites.empty()
                    self.cells = []
                    self.createGrid()


    def Tick(self):
        # updates to player location and animation frame
        self.ttime = self.clock.tick()
        self.mpos = pygame.mouse.get_pos()
        self.keys_pressed = pygame.key.get_pressed()
        if self.running:
            self.generation +=1
            self.Run()
        else:
            self.generation = 0
            self.population = 0


    def Draw(self):
        self.screen.fill(0)
        self.blitDirections()
        self.sprites.update()
        self.sprites.draw(self.screen)

Game()
