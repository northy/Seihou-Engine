import os, sys, pygame
from bin.colors import *
from bin.components import *
import game.level

class Handler() :
    def __init__(self) :
        self.controller=HandlerController(self)

        self.fullscreen = False

        #menuBtns: [[unselectedSurface,SelectedSurface]]
        #0=Level 0
        #1=Settings
        self.menuBtns=[
            [pygame.Surface((50,20)),pygame.Surface((50,20)),(40,100)],
            [pygame.Surface((50,20)),pygame.Surface((50,20)),(40,140)],
            [pygame.Surface((50,20)),pygame.Surface((50,20)),(40,180)]
        ]
        self.menuBtns[0][0].fill(green)
        self.menuBtns[0][1].fill(blue)
        drawText(self.menuBtns[0][0],"Level 0",22,(0,3),white)
        drawText(self.menuBtns[0][1],"Level 0",22,(0,3),white)
        
        self.menuBtns[1][0].fill(green)
        self.menuBtns[1][1].fill(blue)
        drawText(self.menuBtns[1][0],"Settings",18,(0,3),white)
        drawText(self.menuBtns[1][1],"Settings",18,(0,3),white)

        self.menuBtns[2][0].fill(green)
        self.menuBtns[2][1].fill(blue)
        drawText(self.menuBtns[2][0],"Exit",22,(0,3),white)
        drawText(self.menuBtns[2][1],"Exit",22,(0,3),white)

        self.settingsBtns=[
            [pygame.Surface((70,20)),pygame.Surface((70,20)),(40,100)],
            [pygame.Surface((60,20)),pygame.Surface((60,20)),(120,100)],
            [pygame.Surface((30,20)),pygame.Surface((30,20)),(130,140)],
            [pygame.Surface((30,20)),pygame.Surface((30,20)),(170,140)],
            [pygame.Surface((50,20)),pygame.Surface((50,20)),(40,180)]
        ]
        self.settingsBtns[0][0].fill(green)
        self.settingsBtns[0][1].fill(blue)
        drawText(self.settingsBtns[0][0],"1280x960",22,(0,3),white)
        drawText(self.settingsBtns[0][1],"1280x960",22,(0,3),white)

        self.settingsBtns[1][0].fill(green)
        self.settingsBtns[1][1].fill(blue)
        drawText(self.settingsBtns[1][0],"640x480",22,(0,3),white)
        drawText(self.settingsBtns[1][1],"640x480",22,(0,3),white)

        self.settingsBtns[2][0].fill(green)
        self.settingsBtns[2][1].fill(blue)
        drawText(self.settingsBtns[2][0],"On",22,(0,3),white)
        drawText(self.settingsBtns[2][1],"On",22,(0,3),white)

        self.settingsBtns[3][0].fill(green)
        self.settingsBtns[3][1].fill(blue)
        drawText(self.settingsBtns[3][0],"Off",22,(0,3),white)
        drawText(self.settingsBtns[3][1],"Off",22,(0,3),white)

        self.settingsBtns[4][0].fill(green)
        self.settingsBtns[4][1].fill(blue)
        drawText(self.settingsBtns[4][0],"Return",22,(0,3),white)
        drawText(self.settingsBtns[4][1],"Return",22,(0,3),white)

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
        pygame.display.set_caption("Seihou Engine")
        pygame.display.set_icon(loadImage("game/assets/icon.png",32,32))

        self.level = None #Level
        self.points = 0 #int

        self.pgclock = pygame.time.Clock()

    def processMenu(self, events) :
        self.display.fill(black)

        drawText(self.display,"西方 Engine",35,(400,100),white,"game/assets/chihaya-jun.ttf")
        
        for i in range(len(self.menuBtns)) :
            if (i==self.selectedBtn) : self.display.blit(self.menuBtns[i][1],self.menuBtns[i][2])
            else : self.display.blit(self.menuBtns[i][0],self.menuBtns[i][2])

        for event in events :
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selectedBtn=max(0,self.selectedBtn-1)
                if event.key == pygame.K_DOWN:
                    self.selectedBtn=min(len(self.menuBtns)-1,self.selectedBtn+1)
                if event.key == pygame.K_RETURN:
                    if (self.selectedBtn==0) :
                        self.level = game.level.Level0(self.game,self.gWidth,self.gHeight,self.controller)
                        self.state = 1
                        self.points = 0
                    if (self.selectedBtn==1) :
                        self.state=2
                        self.selectedBtn=0
                    if (self.selectedBtn==2) :
                        pygame.quit()
                        sys.exit()

    def processGame(self) :
        self.display.fill(black)
        ret = self.level.process()
        self.display.blit(self.game,self.gamePadding)
        self.controller.addPoints(0.25)
        self.drawGameInfo()
        return ret
    
    def processSettings(self, events) :
        self.display.fill(black)

        drawText(self.display,"Fullscreen:",22,(40,142),white)

        for i in range(len(self.settingsBtns)) :
            if (i==self.selectedBtn) : self.display.blit(self.settingsBtns[i][1],self.settingsBtns[i][2])
            else : self.display.blit(self.settingsBtns[i][0],self.settingsBtns[i][2])

        for event in events :
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if (self.selectedBtn==1) :
                        self.selectedBtn = 0
                    elif (self.selectedBtn==3) :
                        self.selectedBtn = 2
                if event.key == pygame.K_RIGHT:
                    if (self.selectedBtn==0) :
                        self.selectedBtn = 1
                    elif (self.selectedBtn==2) :
                        self.selectedBtn = 3
                if event.key == pygame.K_UP:
                    if (self.selectedBtn==2 or self.selectedBtn==3) :
                        self.selectedBtn = 0
                    elif (self.selectedBtn==4) :
                        self.selectedBtn = 2
                if event.key == pygame.K_DOWN:
                    if (self.selectedBtn==0 or self.selectedBtn==1) :
                        self.selectedBtn = 2
                    elif (self.selectedBtn==2 or self.selectedBtn==3) :
                        self.selectedBtn = 4
                if event.key == pygame.K_RETURN:
                    if (self.selectedBtn==0) :
                        self.screensize = self.sWidth, self.sHeight = 1280,960
                        if (self.fullscreen) :
                            self.screen = pygame.display.set_mode(self.screensize,pygame.FULLSCREEN)
                        else :
                            self.screen = pygame.display.set_mode(self.screensize)
                    elif (self.selectedBtn==1) :
                        self.screensize = self.sWidth, self.sHeight = 640,480
                        if (self.fullscreen) :
                            self.screen = pygame.display.set_mode(self.screensize,pygame.FULLSCREEN)
                        else :
                            self.screen = pygame.display.set_mode(self.screensize)
                    elif (self.selectedBtn==2) :
                        self.screen = pygame.display.set_mode(self.screensize,pygame.FULLSCREEN)
                        self.fullscreen = True
                    elif (self.selectedBtn==3) :
                        self.screen = pygame.display.set_mode(self.screensize)
                        self.fullscreen = False
                    elif (self.selectedBtn==4) :
                        self.state = 0
                        self.selectedBtn = 1

    def handle(self) :
        while True :
            events = pygame.event.get()
            for event in events :
                if event.type == pygame.QUIT : pygame.quit(); sys.exit()

            if (self.state==0) :
                self.processMenu(events)
            elif (self.state==1) :
                ret = self.processGame() #returns: 0=normal, 1=enemy died, 2=player died
                if ret==1 or ret==2:
                    self.state = 0
            elif (self.state==2) :
                self.processSettings(events)

            drawText(self.display,"fps: "+str(int(self.pgclock.get_fps())),10,(self.dWidth/2,0),white,"droidsans")

            pygame.transform.scale(self.display,(self.sWidth,self.sHeight),self.screen)
            pygame.display.flip()

            self.pgclock.tick_busy_loop(60) #make fps <= 60
    
    def drawGameInfo(self) :
        drawText(self.display,"Points:",30,(450,30),white)
        drawText(self.display,"0"*(14-len(str(int(self.points))))+str(int(self.points)),30,(450,50),white)
        drawText(self.display,f"Enemy lifes: {self.level.enemy.lifes}",30,(450,70),white)

class HandlerController(object) :
    def __init__(self,handler:Handler) :
        self.handler = handler

    def addPoints(self,p) :
        self.handler.points+=p

    def setState(self,state) :
        self.handler.state = state