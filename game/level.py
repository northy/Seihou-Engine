import pygame
import numpy as np
import random
from bin.colors import *
from bin.components import *
from bin.factories import *
from bin.quadtree import *
from bin.shapes import *
from timeit import default_timer as timer
from game.handler import *

class Level(object) :
    def __init__(self,game:pygame.surface.Surface,gWidth:int,gHeight:int,controller) :
        self.game = game
        self.gWidth = gWidth
        self.gHeight = gHeight
        self.controller = controller
        self.qtree = None #Quadtree

        self.photoActive = False
        self.photoTimer = None #timer object

        self.powerCount = 0
        self.lastPowerGain = timer() #timer object
        self.powerEachXSecs = 0.2
        self.powerCharging = False

        self.background = None #Sprite

    def process(self) -> int:
        if self.enemy.isDead() :
            return 1

        self.qtree = Quadtree(Rectangle(0,0,self.gWidth,self.gHeight),4)

        self.game.blit(self.background.get(),(0,0))

        #enemies + bullets processing
        for x in self.enemies :
            if not(x.rect.collides(Rectangle(0,0,self.gWidth,self.gHeight))) :
                self.enemies.remove(x)
                continue
            self.qtree.addEntity(x)
            if isinstance(x,Bullet) :
                x.move()
        
        #keys processing
        keys = pygame.key.get_pressed()
        self.player.slow = True if keys[pygame.K_LSHIFT] else False
        self.powerCharging = True if keys[pygame.K_LSHIFT] and keys[pygame.K_z] else False
        if keys[pygame.K_z] and (self.photoActive or (self.powerCount==100 and not(keys[pygame.K_LSHIFT]))) :
            if not(self.photoActive) :
                self.photoRect=Rectangle(self.player.rect.getX()-230//2+self.player.rect.getW()//2,self.player.rect.getY()-170,230,170)
                self.photoActive=True
                self.photoTimer=timer()
            if keys[pygame.K_UP] :
                self.photoRect.setY(self.photoRect.getY()-1)
            if keys[pygame.K_DOWN] :
                self.photoRect.setY(self.photoRect.getY()+1)
            if keys[pygame.K_LEFT] :
                self.photoRect.setX(self.photoRect.getX()-2)
            if keys[pygame.K_RIGHT] :
                self.photoRect.setX(self.photoRect.getX()+1)
        else :
            if keys[pygame.K_UP] : self.player.moveUp(self.qtree.boundary)
            if keys[pygame.K_DOWN] : self.player.moveDown(self.qtree.boundary)
            if keys[pygame.K_LEFT] : self.player.moveLeft(self.qtree.boundary)
            if keys[pygame.K_RIGHT] : self.player.moveRight(self.qtree.boundary)
            if keys[pygame.K_ESCAPE] : self.controller.setState(0); return

        #Process the photo
        if (self.photoActive) :
            if not(keys[pygame.K_z]) or timer()-self.photoTimer>=0.75 :
                self.photoActive=False
                self.powerCount=0
                shot = self.qtree.queryRectangle(self.photoRect)
                enemyFound = False
                for x in shot :
                    if (isinstance(x,Bullet)) :
                        self.enemies.remove(x)
                        self.controller.addPoints(500)
                    elif isinstance(x,Enemy):
                        enemyFound=True
                if not(enemyFound) : self.powerCount=50
                else :
                    self.enemy.lifes-=1
                    self.controller.addPoints(10000)
            else :
                self.photoRect.setH(self.photoRect.getH()-2)
                self.photoRect.setX(self.photoRect.getX()+1)
                self.photoRect.setW(self.photoRect.getW()-2)
                self.photoRect.draw(self.game,black,1)

        #player processing
        for x in self.qtree.queryRectangle(self.player.hitboxRect) :
            if (self.player.pixelPerfectHitboxCollision(x)) : return 2
        if (self.powerCount<100 and timer()-self.lastPowerGain>=(self.powerEachXSecs if not(self.powerCharging) else self.powerEachXSecs/3)) :
            self.powerCount+=1
            self.lastPowerGain = timer()
        if self.powerCharging :
            self.player.drawPowerCircle(self.game)
        drawText(self.game,f"{self.powerCount}%",12,(self.player.rect.getX()+self.player.rect.getW()+5,self.player.rect.getY()-5),color=red)
        self.player.draw(self.game)
        if (keys[pygame.K_LSHIFT]) : self.player.drawHitbox(self.game)

        #enemy processing
        self.enemy.think(self.enemies,self.gWidth,self.gHeight)
        self.enemy.draw(self.game)

        for x in self.enemies :
            if isinstance(x,Bullet) :
                x.draw(self.game)

        return 0

class Level0(Level) :
    def __init__(self,game:pygame.surface.Surface,gWidth:int,gHeight:int,controller) :
        Level.__init__(self,game,gWidth,gHeight,controller)

        #Background
        self.background=Sprite(0.1)
        self.background.addImage(loadImage("game/assets/bg0.png",400,445))
        self.background.addImage(loadImage("game/assets/bg1.png",400,445))
        self.background.addImage(loadImage("game/assets/bg2.png",400,445))
        self.background.addImage(loadImage("game/assets/bg3.png",400,445))
        self.background.addImage(loadImage("game/assets/bg4.png",400,445))
        self.background.addImage(loadImage("game/assets/bg5.png",400,445))
        self.background.addImage(loadImage("game/assets/bg6.png",400,445))
        self.background.addImage(loadImage("game/assets/bg7.png",400,445))
        self.background.addImage(loadImage("game/assets/bg8.png",400,445))
        self.background.addImage(loadImage("game/assets/bg9.png",400,445))
        self.background.addImage(loadImage("game/assets/bg10.png",400,445))
        self.background.addImage(loadImage("game/assets/bg11.png",400,445))
        self.background.addImage(loadImage("game/assets/bg12.png",400,445))
        self.background.addImage(loadImage("game/assets/bg13.png",400,445))
        self.background.addImage(loadImage("game/assets/bg14.png",400,445))
        self.background.addImage(loadImage("game/assets/bg15.png",400,445))
        self.background.addImage(loadImage("game/assets/bg16.png",400,445))
        self.background.addImage(loadImage("game/assets/bg17.png",400,445))
        self.background.addImage(loadImage("game/assets/bg18.png",400,445))
        self.background.addImage(loadImage("game/assets/bg19.png",400,445))
        self.background.addImage(loadImage("game/assets/bg20.png",400,445))
        self.background.addImage(loadImage("game/assets/bg21.png",400,445))
        self.background.addImage(loadImage("game/assets/bg22.png",400,445))
        self.background.addImage(loadImage("game/assets/bg23.png",400,445))
        self.background.addImage(loadImage("game/assets/bg24.png",400,445))
        self.background.addImage(loadImage("game/assets/bg25.png",400,445))
        self.background.addImage(loadImage("game/assets/bg26.png",400,445))
        self.background.addImage(loadImage("game/assets/bg27.png",400,445))
        self.background.addImage(loadImage("game/assets/bg28.png",400,445))
        self.background.addImage(loadImage("game/assets/bg29.png",400,445))
        self.background.addImage(loadImage("game/assets/bg30.png",400,445))
        self.background.addImage(loadImage("game/assets/bg31.png",400,445))
        
        #########CREATE PLAYER#########
        self.player = Player((5,-1),(-10,-7))
        self.player.hitbox = Sprite(0,loadImage("game/assets/hitbox.png",10,10))
        self.player.hitboxRect = Rectangle(0,0,10,10)

        #player sprite
        self.player.sprite = Sprite(0.1)
        self.player.sprite.addImage(loadImage("game/assets/pl0.png",30,48))
        self.player.sprite.addImage(loadImage("game/assets/pl1.png",30,48))
        self.player.sprite.addImage(loadImage("game/assets/pl2.png",30,48))
        self.player.sprite.addImage(loadImage("game/assets/pl3.png",30,48))
        self.player.sprite.addImage(loadImage("game/assets/pl4.png",30,48))
        self.player.sprite.addImage(loadImage("game/assets/pl5.png",30,48))
        self.player.sprite.addImage(loadImage("game/assets/pl6.png",30,48))
        self.player.sprite.addImage(loadImage("game/assets/pl7.png",30,48))
        self.player.sprite.addImage(loadImage("game/assets/pl8.png",30,48))
        self.player.sprite.addImage(loadImage("game/assets/pl9.png",30,48))
        self.player.sprite.addImage(loadImage("game/assets/pl10.png",30,48))
        self.player.sprite.addImage(loadImage("game/assets/pl11.png",30,48))
        self.player.sprite.addImage(loadImage("game/assets/pl12.png",30,48))

        self.player.powerCircle = Sprite(0,loadImage("game/assets/powercircle.png",60,60))

        self.player.rect = Rectangle(0,0,30,48)
        self.player.moveSpeed = 4
        self.player.rect.setX(gWidth/2)
        self.player.rect.setY(gHeight/2+gHeight/4)
        self.player.updateHitbox()
        ###############################

        #########CREATE ENEMY#########
        #Patterns
        bullet1 = loadImage("game/assets/bullet1.png",10,10)
        bullet2 = loadImage("game/assets/bullet2.png",10,20)

        se = Bullet()
        se.sprite=Sprite(0,bullet1)
        se.rect=Rectangle(0,0,10,10)
        se.velocity = np.array([2,2])

        ne = Bullet()
        ne.sprite=Sprite(0,bullet1)
        ne.rect=Rectangle(0,0,10,10)
        ne.velocity = np.array([2,-2])

        sw = Bullet()
        sw.sprite=Sprite(0,bullet1)
        sw.rect=Rectangle(0,0,10,10)
        sw.velocity = np.array([-2,2])

        nw = Bullet()
        nw.sprite=Sprite(0,bullet1)
        nw.rect=Rectangle(0,0,10,10)
        nw.velocity = np.array([-2,-2])

        n = Bullet()
        n.sprite=Sprite(0,bullet1)
        n.rect=Rectangle(0,0,10,10)
        n.velocity = np.array([0,-2])

        s = Bullet()
        s.sprite=Sprite(0,bullet1)
        s.rect=Rectangle(0,0,10,10)
        s.velocity = np.array([0,2])

        e = Bullet()
        e.sprite=Sprite(0,bullet1)
        e.rect=Rectangle(0,0,10,10)
        e.velocity = np.array([2,0])

        w = Bullet()
        w.sprite=Sprite(0,bullet1)
        w.rect=Rectangle(0,0,10,10)
        w.velocity = np.array([-2,0])

        ns = UpSeekingBullet(self.player)
        ns.sprite = Sprite(0,bullet2)
        ns.rect = Rectangle(0,0,10,20)
        ns.velocity=[0,-1]
        ns.maxVelocity = 2
        ns.maxForce = 3

        ss = DownSeekingBullet(self.player)
        ss.sprite = Sprite(0,bullet2)
        ss.rect = Rectangle(0,0,10,20)
        ss.velocity=[0,1]
        ss.maxVelocity = 2
        ss.maxForce = 3

        es = RightSeekingBullet(self.player)
        es.sprite = Sprite(0,bullet2)
        es.rect = Rectangle(0,0,10,20)
        es.velocity=[1,0]
        es.maxVelocity = 2
        es.maxForce = 3

        ws = LeftSeekingBullet(self.player)
        ws.sprite = Sprite(0,bullet2)
        ws.rect = Rectangle(0,0,10,20)
        ws.velocity=[-1,0]
        ws.maxVelocity = 2
        ws.maxForce = 3

        st = bulletFactory()
        st.addBullet(n)
        st.addBullet(s)
        st.addBullet(w)
        st.addBullet(e)

        ts = bulletFactory()
        ts.addBullet(ne)
        ts.addBullet(nw)
        ts.addBullet(se)
        ts.addBullet(sw)

        seek = bulletFactory()
        seek.addBullet(ws)
        seek.addBullet(es)
        seek.addBullet(ns)
        seek.addBullet(ss)

        #Enemy
        self.enemy=Enemy()

        #enemy sprite
        self.enemy.sprite = Sprite(0.1)
        self.enemy.sprite.addImage(loadImage("game/assets/en0.png",30,48))
        self.enemy.sprite.addImage(loadImage("game/assets/en1.png",30,48))
        self.enemy.sprite.addImage(loadImage("game/assets/en2.png",30,48))
        self.enemy.sprite.addImage(loadImage("game/assets/en3.png",30,48))
        self.enemy.sprite.addImage(loadImage("game/assets/en4.png",30,48))
        self.enemy.sprite.addImage(loadImage("game/assets/en5.png",30,48))
        self.enemy.sprite.addImage(loadImage("game/assets/en6.png",30,48))
        self.enemy.sprite.addImage(loadImage("game/assets/en7.png",30,48))
        self.enemy.sprite.addImage(loadImage("game/assets/en8.png",30,48))
        self.enemy.sprite.addImage(loadImage("game/assets/en9.png",30,48))
        self.enemy.sprite.addImage(loadImage("game/assets/en10.png",30,48))
        self.enemy.sprite.addImage(loadImage("game/assets/en11.png",30,48))
        self.enemy.sprite.addImage(loadImage("game/assets/en12.png",30,48))
        self.enemy.sprite.addImage(loadImage("game/assets/en13.png",30,48))
        self.enemy.sprite.addImage(loadImage("game/assets/en14.png",30,48))
        self.enemy.sprite.addImage(loadImage("game/assets/en15.png",30,48))
        self.enemy.sprite.addImage(loadImage("game/assets/en16.png",30,48))

        self.enemy.rect = Rectangle(0,0,30,48)
        self.enemy.lifes=4
        self.enemy.pattern=[
            [1,0.2,[st,ts,seek,st,ts,seek,st,ts]],
            [1,0.3,[st,ts,seek,st,ts]],
            [1,0.5,[st,ts,seek]],
            [1,0.5,[st,ts]]
            ]
        self.enemy.maxForce=2
        self.enemy.maxVelocity=4
        self.enemy.rect.setX(gWidth/2)
        self.enemy.rect.setY(gHeight/4)

        self.enemies=pygame.sprite.Group()
        self.enemies.add(self.enemy)
        ##############################