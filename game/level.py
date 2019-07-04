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
        self.gWidth=gWidth
        self.gHeight=gHeight
        self.controller=controller
        self.qtree = None #Quadtree

        self.photoActive = False
        self.photoTimer = None #timer object

        self.powerCount=0
        self.lastPowerGain = timer() #timer object
        self.powerEachXSecs = 0.2
        self.powerCharging = False

    def process(self) -> int:
        if self.enemy.isDead() :
            return 1

        self.qtree = Quadtree(Rectangle(0,0,self.gWidth,self.gHeight),4)

        self.game.fill(white)

        #enemies + bullets processing
        for x in self.enemies :
            if not(x.rect.collides(Rectangle(0,0,self.gWidth,self.gHeight))) :
                self.enemies.remove(x)
                continue
            self.qtree.addEntity(x)
            if isinstance(x,Bullet) :
                x.move()
                x.draw(self.game)

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

        #Process the photo
        if (self.photoActive) :
            if not(keys[pygame.K_z]) or timer()-self.photoTimer>=0.75 :
                self.photoActive=False
                self.powerCount=0
                shot=self.qtree.queryRectangle(self.photoRect)
                enemyFound=False
                for x in shot :
                    if (isinstance(x,Bullet)) :
                        self.enemies.remove(x)
                        self.controller.addPoints(500)
                    else :
                        x.lifes-=1
                        enemyFound=True
                        self.controller.addPoints(10000)
                if not(enemyFound) : self.powerCount=50
            else :
                self.photoRect.setH(self.photoRect.getH()-2)
                self.photoRect.setX(self.photoRect.getX()+1)
                self.photoRect.setW(self.photoRect.getW()-2)
                self.photoRect.draw(self.game,black,1)

        #enemy processing
        self.enemy.think(self.enemies,self.gWidth,self.gHeight)
        self.enemy.draw(self.game)

        #player processing
        for x in self.qtree.queryRectangle(self.player.hitboxRect) :
            if (self.player.pixelPerfectHitboxCollision(x)) : return 2
        if (self.powerCount<100 and timer()-self.lastPowerGain>=(self.powerEachXSecs if not(self.powerCharging) else self.powerEachXSecs/3)) :
            self.powerCount+=1
            self.lastPowerGain=timer()
        drawText(self.game,f"{self.powerCount}%",12,(self.player.rect.getX()+self.player.rect.getW()+5,self.player.rect.getY()-5),color=red)
        self.player.draw(self.game)
        if (keys[pygame.K_LSHIFT]) : self.player.drawHitbox(self.game)

        return 0

class Level0(Level) :
    def __init__(self,game:pygame.surface.Surface,gWidth:int,gHeight:int,controller) :
        Level.__init__(self,game,gWidth,gHeight,controller)
        
        #########CREATE PLAYER#########
        self.player = Player()
        hb = pygame.Surface((10,10))
        hb.fill(red)
        self.player.hitbox = Sprite(hb)
        self.player.hitboxRect = Rectangle(0,0,10,10)
        self.player.sprite = Sprite(pygame.Surface((20,30)))
        self.player.rect = Rectangle(0,0,20,30)
        self.player.moveSpeed = 4
        self.player.rect.setX(gWidth/2)
        self.player.rect.setY(gHeight/2+gHeight/4)
        self.player.updateHitbox()
        ###############################

        #########CREATE ENEMY#########
        #Patterns
        se = Bullet()
        se.sprite=Sprite(pygame.Surface((5,5)))
        se.rect=Rectangle(0,0,5,5)
        se.velocity = np.array([2,2])

        ne = Bullet()
        ne.sprite=Sprite(pygame.Surface((5,5)))
        ne.rect=Rectangle(0,0,5,5)
        ne.velocity = np.array([2,-2])

        sw = Bullet()
        sw.sprite=Sprite(pygame.Surface((5,5)))
        sw.rect=Rectangle(0,0,5,5)
        sw.velocity = np.array([-2,2])

        nw = Bullet()
        nw.sprite=Sprite(pygame.Surface((5,5)))
        nw.rect=Rectangle(0,0,5,5)
        nw.velocity = np.array([-2,-2])

        n = Bullet()
        n.sprite=Sprite(pygame.Surface((5,5)))
        n.rect=Rectangle(0,0,5,5)
        n.velocity = np.array([0,-2])

        s = Bullet()
        s.sprite=Sprite(pygame.Surface((5,5)))
        s.rect=Rectangle(0,0,5,5)
        s.velocity = np.array([0,2])

        e = Bullet()
        e.sprite=Sprite(pygame.Surface((5,5)))
        e.rect=Rectangle(0,0,5,5)
        e.velocity = np.array([2,0])

        w = Bullet()
        w.sprite=Sprite(pygame.Surface((5,5)))
        w.rect=Rectangle(0,0,5,5)
        w.velocity = np.array([-2,0])

        ns = UpSeekingBullet(self.player)
        ns.sprite = Sprite(pygame.Surface((5,5)))
        ns.rect = Rectangle(0,0,5,5)
        ns.velocity=[0,-1]
        ns.maxVelocity = 2
        ns.maxForce = 3

        ss = DownSeekingBullet(self.player)
        ss.sprite = Sprite(pygame.Surface((5,5)))
        ss.rect = Rectangle(0,0,5,5)
        ss.velocity=[0,1]
        ss.maxVelocity = 2
        ss.maxForce = 3

        es = RightSeekingBullet(self.player)
        es.sprite = Sprite(pygame.Surface((5,5)))
        es.rect = Rectangle(0,0,5,5)
        es.velocity=[1,0]
        es.maxVelocity = 2
        es.maxForce = 3

        ws = LeftSeekingBullet(self.player)
        ws.sprite = Sprite(pygame.Surface((5,5)))
        ws.rect = Rectangle(0,0,5,5)
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
        self.enemy.sprite = Sprite(pygame.Surface((10,10)))
        self.enemy.rect = Rectangle(0,0,10,10)
        self.enemy.lifes=1
        self.enemy.pattern=[[1,0,[st,ts,seek]]]
        self.enemy.maxForce=2
        self.enemy.maxVelocity=3
        self.enemy.rect.setX(gWidth/2)
        self.enemy.rect.setY(gHeight/4)

        self.enemies=pygame.sprite.Group()
        self.enemies.add(self.enemy)
        ##############################