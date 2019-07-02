import os, sys, pygame
from bin.colors import *
from bin.components import *
import game.level

class Handler() :
    def __init__(self) :
        self.controller=HandlerController(self)

        #menuBtns: [[unselectedSurface,SelectedSurface]]
        #0=PLAY
        self.menuBtns=[[pygame.Surface((50,20)),pygame.Surface((50,20)),(40,100)]]
        self.menuBtns[0][0].fill(green)
        self.menuBtns[0][1].fill(blue)
        drawText(self.menuBtns[0][0],"Level 0",26,(0,3),white)
        drawText(self.menuBtns[0][1],"Level 0",22,(0,3),white)

        self.selectedBtn = 0

        #STATE: 0=menu, 1=ingame, 2=settings
        self.state = 0

        self.resolution = self.dWidth, self.dHeight = 640,480
        self.screensize = self.sWidth, self.sHeight = 1280,960
        self.gameSize = self.gWidth, self.gHeight = 400,445
        self.gamePadding = 32, 17

        self.screen = pygame.display.set_mode(self.screensize)
        self.display = pygame.Surface(self.resolution)
        self.game = pygame.Surface(self.gameSize)

        self.level = None #Level
        self.points = 0 #int

        self.pgclock = pygame.time.Clock()

    def processMenu(self) :
        self.display.fill(black)
        
        for i in range(len(self.menuBtns)) :
            if (i==self.selectedBtn) : self.display.blit(self.menuBtns[i][1],self.menuBtns[i][2])
            else : self.display.blit(self.menuBtns[i][0],self.menuBtns[i][2])

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN] :
            if (self.selectedBtn==0) :
                self.level = game.level.Level0(self.game,self.gWidth,self.gHeight,self.controller)
                self.state=1
                self.points=0

    def processGame(self) :
        self.display.fill(black)
        ret = self.level.process()
        self.display.blit(self.game,self.gamePadding)
        self.controller.addPoints(0.25)
        self.drawGameInfo()
        return ret

    def handle(self) :
        while True :
            for event in pygame.event.get() :
                if event.type == pygame.QUIT : pygame.quit(); sys.exit()

            if (self.state==0) :
                self.processMenu() #returns: 0=normal, 1=enemy died, 2=player died
            elif (self.state==1) :
                ret = self.processGame()
                if ret==1 or ret==2:
                    self.state=0

            drawText(self.display,"fps: "+str(int(self.pgclock.get_fps())),10,(self.dWidth/2,0),white,"droidsans")

            pygame.transform.scale(self.display,(self.sWidth,self.sHeight),self.screen)
            pygame.display.flip()

            self.pgclock.tick_busy_loop(60) #make fps <= 60
    
    def drawGameInfo(self) :
        drawText(self.display,"Points:",30,(450,30),white)
        drawText(self.display,"0"*(14-len(str(int(self.points))))+str(int(self.points)),30,(450,50),white)

class HandlerController(object) :
    def __init__(self,handler:Handler) :
        self.handler=handler

    def addPoints(self,p) :
        self.handler.points+=p
