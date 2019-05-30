import os, sys, pygame
from bin.colors import *
from bin.components import *
import game.level

class Handler() :
    def __init__(self) :
        #menuBtns: 0=PLAY
        self.menuBtns=[[pygame.Surface((50,20)),pygame.Surface((50,20)),(40,100)]]
        self.menuBtns[0][0].fill(green)
        self.menuBtns[0][1].fill(blue)

        self.selectedBtn=0

        #STATE: 0=menu, 1=ingame, 2=settings
        self.state = 0

        self.resolution = self.dWidth, self.dHeight = 640,480
        self.screensize = self.sWidth, self.sHeight = 1280,960
        self.gameSize = self.gWidth, self.gHeight = 400,445
        self.gamePadding = 32, 17

        self.screen = pygame.display.set_mode(self.screensize)
        self.display = pygame.Surface(self.resolution)
        self.game = pygame.Surface(self.gameSize)

        self.level = game.level.Level0(self.game,self.gWidth,self.gHeight)
        
        self.pgclock = pygame.time.Clock()

    def processMenu(self) :
        self.display.fill(black)
        
        for i in range(len(self.menuBtns)) :
            if (i==self.selectedBtn) : self.display.blit(self.menuBtns[i][1],self.menuBtns[i][2])
            else : self.display.blit(self.menuBtns[i][0],self.menuBtns[i][2])

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN] : self.state=1

    def processGame(self) :
        self.display.fill(black)
        self.level.process()
        self.display.blit(self.game,self.gamePadding)

    def handle(self) :
        while True :
            for event in pygame.event.get() :
                if event.type == pygame.QUIT : pygame.quit(); sys.exit()

            if (self.state==0) :
                self.processMenu()
            elif (self.state==1) :
                self.processGame()
            
            drawText(self.display,"fps: "+str(int(self.pgclock.get_fps())),10,(self.dWidth/2,0),white,"droidsans")

            pygame.transform.scale(self.display,(self.sWidth,self.sHeight),self.screen)
            pygame.display.flip()

            self.pgclock.tick_busy_loop(60) #make fps <= 60