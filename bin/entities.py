import pygame,random
import numpy as np
from bin.shapes import *
from bin.components import *
from timeit import default_timer as timer

class Entity(pygame.sprite.Sprite) :
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.sprite = None #Sprite
        self.rect = None #Rectangle

    # jumps to (x,y) coordinates
    def go(self,x:float,y:float) :
        self.rect.setX(x)
        self.rect.setY(y)

    # moves in place by x,y value
    def move(self,x:float,y:float) :
        self.rect.setX(self.rect.getX()+x)
        self.rect.setY(self.rect.getY()+y)

    # draws the entity in the surface
    def draw(self,surface:pygame.surface.Surface) :
        surface.blit(self.sprite.get(),self.rect)

    def print(self) :
        print("Entity at: ")
        self.rect.print()

class Player(Entity) :
    def __init__(self) :
        Entity.__init__(self)
        self.hitbox = None #Sprite
        self.hitboxRect = None #Rectangle
        self.moveSpeed = None #int
        self.slow = False
    
    def updateHitbox(self) :
        self.hitboxRect.setX(self.rect.getX()+self.rect.getW()//2-self.hitboxRect.getW()//2)
        self.hitboxRect.setY(self.rect.getY()+self.rect.getH()//2-self.hitboxRect.getH()//2)

    # moves left by the move speed
    def moveLeft(self,boundary:Rectangle) :
        vel = self.moveSpeed if not(self.slow) else self.moveSpeed//2
        self.__checkAndMove(-vel,0,boundary)
    # moves right by the move speed
    def moveRight(self,boundary:Rectangle) :
        vel = self.moveSpeed if not(self.slow) else self.moveSpeed//2
        self.__checkAndMove(vel,0,boundary)
    # moves up by the move speed
    def moveUp(self,boundary:Rectangle) :
        vel = self.moveSpeed if not(self.slow) else self.moveSpeed//2
        self.__checkAndMove(0,-vel,boundary)
    # moves down by the move speed
    def moveDown(self,boundary:Rectangle) :
        vel = self.moveSpeed if not(self.slow) else self.moveSpeed//2
        self.__checkAndMove(0,vel,boundary)

    # checks whether it's possible to move completely or if boundaries are on the way
    def __checkAndMove(self,x:float,y:float,boundary:Rectangle) :
        if self.rect.x+x<boundary.x :
            self.go(boundary.x,self.rect.y)
            x=0
        if self.rect.x+x+self.rect.w>boundary.x+boundary.w :
            self.go(boundary.x+boundary.w-self.rect.w,self.rect.y)
            x=0
        if self.rect.y+y<boundary.y :
            self.go(self.rect.x,boundary.y)
            y=0
        if self.rect.y+y+self.rect.h>boundary.y+boundary.h :
            self.go(self.rect.x,boundary.y+boundary.h-self.rect.h)
            y=0

        self.move(x,y)

        self.updateHitbox()

    def drawHitbox(self,surface:pygame.surface.Surface) :
        surface.blit(self.hitbox.get(),self.hitboxRect)
    
    def pixelPerfectHitboxCollision(self,other:Entity) -> bool :
        ox=int(self.hitboxRect.x-other.rect.x)
        oy=int(self.hitboxRect.y-other.rect.y)
        sm=pygame.mask.from_surface(self.hitbox.get())
        sm.invert()
        om=pygame.mask.from_surface(other.sprite.getWithoutChanging()) if not(isinstance(other,Bullet)) else pygame.mask.from_surface(other.sprite.getAngledWithoutChanging(getDegree(np.array(other.velocity))))
        om.invert()
        return True if om.overlap(sm,(ox,oy))!=None else False

class Bullet(Entity) :
    def __init__(self) :
        Entity.__init__(self)
        self.velocity=None #numpy array

    def copy(self) :
        new = Bullet()
        new.velocity=self.velocity
        new.sprite=self.sprite
        new.rect=self.rect.copy()
        return new

    def move(self) :
        super().move(self.velocity[0],self.velocity[1])

    def isOutOfBounds(self,boundary:Rectangle) -> bool :
        return True if not(boundary.collides(self.rect)) else False
    
    def draw(self,surface:pygame.surface.Surface) :
        surface.blit(self.sprite.getAngled(getDegree(np.array(self.velocity))),self.rect)

class SeekingBullet(Bullet) :
    def __init__(self,target:Entity) :
        Bullet.__init__(self)
        self.maxVelocity=None #int
        self.maxForce=None #int
        self.target=target
    
    def copy(self) :
        new = SeekingBullet(self.target)
        new.velocity=self.velocity
        new.sprite=self.sprite
        new.rect=self.rect.copy()
        new.maxVelocity=self.maxVelocity
        new.maxForce=self.maxForce
        return new

    def move(self) :
        self.seek()
        Bullet.move(self)

    def seek(self) :
        selfpos = np.array([self.rect.getX(),self.rect.getY()])
        otherpos = np.array([self.target.hitboxRect.getX(),self.target.hitboxRect.getY()])

        desiredVelocity = ((otherpos-selfpos)/np.linalg.norm(otherpos-selfpos)) * self.maxVelocity
        steering = desiredVelocity

        self.velocity = truncate(steering + self.velocity,self.maxVelocity)

class DownSeekingBullet(SeekingBullet) :
    def __init__(self, target:Entity) :
        SeekingBullet.__init__(self,target)
    
    def copy(self) :
        new = DownSeekingBullet(self.target)
        new.velocity=self.velocity
        new.sprite=self.sprite
        new.rect=self.rect.copy()
        new.maxVelocity=self.maxVelocity
        new.maxForce=self.maxForce
        return new

    def move(self) :
        if (self.rect.getY()<self.target.rect.getY()+self.target.rect.getH()) :
            self.seek()
        Bullet.move(self)

class UpSeekingBullet(SeekingBullet) :
    def __init__(self, target:Entity) :
        SeekingBullet.__init__(self,target)

    def copy(self) :
        new = UpSeekingBullet(self.target)
        new.velocity=self.velocity
        new.sprite=self.sprite
        new.rect=self.rect.copy()
        new.maxVelocity=self.maxVelocity
        new.maxForce=self.maxForce
        return new

    def move(self) :
        if (self.rect.getY()+self.rect.getH()>self.target.rect.getY()) :
            self.seek()
        Bullet.move(self)

class LeftSeekingBullet(SeekingBullet) :
    def __init__(self, target:Entity) :
        SeekingBullet.__init__(self,target)
    
    def copy(self) :
        new = LeftSeekingBullet(self.target)
        new.velocity=self.velocity
        new.sprite=self.sprite
        new.rect=self.rect.copy()
        new.maxVelocity=self.maxVelocity
        new.maxForce=self.maxForce
        return new

    def move(self) :
        if (self.rect.getX()+self.rect.getW()>self.target.rect.getX()) :
            self.seek()
        Bullet.move(self)

class RightSeekingBullet(SeekingBullet) :
    def __init__(self, target:Entity) :
        SeekingBullet.__init__(self,target)

    def copy(self) :
        new = RightSeekingBullet(self.target)
        new.velocity=self.velocity
        new.sprite=self.sprite
        new.rect=self.rect.copy()
        new.maxVelocity=self.maxVelocity
        new.maxForce=self.maxForce
        return new

    def move(self) :
        if (self.rect.getX()>self.target.rect.getX()+self.rect.getW()) :
            self.seek()
        Bullet.move(self)

class Enemy(Entity) :
    def __init__(self) :
        Entity.__init__(self)
        self.targetPos = np.array([]) #np array
        self.pattern=[] #pattern[x][0] = delay for fresh start(int); pattern[x][1] = delay between factories spawn; pattern[x][2] = [bulletFactory]
        self.lifes=None #int
        self.step=0
        self.waitFor=0
        self.velocity=np.array([0,0]) #numpy array
        self.maxVelocity=None #int
        self.maxForce=None #int
        self.lastSurge=None #timer object

    def think(self, bullets:pygame.sprite.Group,gameW:int,gameH:int) :
        if (self.lastSurge!=None and timer()-self.lastSurge<self.waitFor) :
            return
        if (self.targetPos.size!=0) :
            self.move()
            if (abs(self.velocity[0])<0.0005 and abs(self.velocity[1])<0.0005) :
                self.waitFor=self.pattern[self.lifes-1][0]
                self.lastSurge=timer()
                self.targetPos=np.array([])
        else :
            if (self.step==len(self.pattern[self.lifes-1][2])) :
                self.step=0
                self.waitFor=self.pattern[self.lifes-1][0]
                self.lastSurge=timer()
                posa=random.randint(1,gameW-self.rect.getW())
                posb=random.randint(1,gameH//2)
                self.targetPos=np.array([posa,posb])
                #TODO: reset circle

            self.pattern[self.lifes-1][2][self.step].spawn(bullets,self.rect.getX(),self.rect.getY())
            self.waitFor=self.pattern[self.lifes-1][1]
            self.step+=1
            self.lastSurge=timer()

    def move(self) :
        selfpos = np.array([self.rect.getX(),self.rect.getY()])

        desiredVelocity = ((self.targetPos-selfpos)/np.linalg.norm(self.targetPos-selfpos)) * self.maxVelocity
        steering = desiredVelocity

        self.velocity = truncate(steering + self.velocity,self.maxVelocity)

        super().move(self.velocity[0],self.velocity[1])

    def isDead(self) -> bool :
        return True if self.lifes<=0 else False
