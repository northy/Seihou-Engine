import pygame
from bin.shapes import *
import numpy as np
from bin.components import *
from timeit import default_timer as timer

class Entity(pygame.sprite.Sprite) :
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.image = None #pygame Surface
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
        surface.blit(self.image,self.rect)
    
    def print(self) :
        print("Entity at: ")
        self.rect.print()

class Player(Entity) :
    def __init__(self) :
        Entity.__init__(self)
        self.hitbox = None #Circle
        self.moveSpeed= None #int

    # moves left by the move speed
    def moveLeft(self,boundary:Rectangle) :
        self.__checkAndMove(-self.moveSpeed,0,boundary)
    # moves right by the move speed
    def moveRight(self,boundary:Rectangle) :
        self.__checkAndMove(self.moveSpeed,0,boundary)
    # moves up by the move speed
    def moveUp(self,boundary:Rectangle) :
        self.__checkAndMove(0,-self.moveSpeed,boundary)
    # moves down by the move speed
    def moveDown(self,boundary:Rectangle) :
        self.__checkAndMove(0,self.moveSpeed,boundary)

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

    def drawHitbox(self,surface:pygame.surface.Surface) :
        self.hitbox.draw(surface,(self.rect.getX()+self.rect.getW()//2,self.rect.getY()+self.rect.getH()//2))

class Bullet(Entity) :
    def __init__(self) :
        Entity.__init__(self)
        self.velocity=None #numpy array
    
    def copy(self) :
        new = Bullet()
        new.velocity=self.velocity
        new.image=self.image
        new.rect=self.rect.copy()
        return new

    def move(self) :
        super().move(self.velocity[0],self.velocity[1])

    def isOutOfBounds(self,boundary:Rectangle) -> bool :
        return True if not(boundary.collides(self.rect)) else False

class SeekingBullet(Bullet) :
    def __init__(self) :
        Bullet.__init__(self)
        self.maxVelocity=None #int
        self.maxForce=None #int

    def move(self,other:Entity) :
        if (self.rect.getY()+self.rect.getW()<other.rect.getY()+other.rect.getH()) :
            self.seek(other)
        Bullet.move(self)
    
    def seek(self,other:Entity) :
        selfpos = np.array([self.rect.getX(),self.rect.getY()])
        otherpos = np.array([other.rect.getX(),other.rect.getY()])

        desiredVelocity = ((otherpos-selfpos)/np.linalg.norm(otherpos-selfpos)) * self.maxVelocity
        steering = desiredVelocity

        self.velocity = truncate(steering + self.velocity,self.maxVelocity)

class Enemy(Entity) :
    def __init__(self) :
        Entity.__init__(self)
        self.targetPos = None #np array
        self.pattern=[] #pattern[x][0] = delay for fresh start(int); pattern[x][1] = delay between factories spawn; pattern[x][2] = [bulletFactory]
        self.lifes=None #int
        self.step=0
        self.waitFor=0
        self.velocity=None #numpy array
        self.maxVelocity=None #int
        self.maxForce=None #int
        self.lastSurge=None #timer object

    def think(self, bullets:pygame.sprite.Group) :
        if (self.targetPos!=None) :
            self.move()
            if (self.rect.x==self.targetPos[0] and self.rect.y==self.targetPos[1]) :
                self.targetPos=None
        else :
            if (self.step==len(self.pattern[self.lifes][2])) :
                self.step=0
                self.waitFor=self.pattern[self.lifes][0]
                self.lastSurge=timer()
                #TODO: reset circle
            if (self.lastSurge!=None and timer()-self.lastSurge<self.waitFor) :
                return
            
            self.pattern[self.lifes][2][self.step].spawn(bullets)
            self.waitFor=self.pattern[self.lifes][1]
            self.step+=1
    
    def move(self) :
        selfpos = np.array([self.rect.getX(),self.rect.getY()])
        
        desiredVelocity = ((self.targetPos-selfpos)/np.linalg.norm(self.targetPos-selfpos)) * self.maxVelocity
        steering = desiredVelocity

        self.velocity = truncate(steering + self.velocity,self.maxVelocity)

        super().move(self.velocity[0],self.velocity[1])

    def isDead(self) -> bool :
        if self.lifes==-1 :
            return True
        return False