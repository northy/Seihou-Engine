import pygame
from shapes import *
from components import *

class Entity(pygame.sprite.Sprite) :
    def __init__(self) :
        pygame.sprite.Sprite.__init__(self)
        self.image = None
        self.rect = None
    
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
        self.image = pygame.Surface((45,50))
        self.image.fill((0,255,0))
        self.rect = Rectangle(0,0,45,50)
        self.hitbox = Circle(5)
        self.moveSpeed=1

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
        self.velocity=Vector2D(0,0)
    
    def isOutOfBounds(self,boundary:Rectangle) :
        return True if not(boundary.collides(this.rect)) else False

class SeekingBullet(Bullet) :
    def __init__(self) :
        Bullet.__init__(self)
        self.maxVelocity=Vector2D(1,1)
        self.maxForce=Vector2D(0.01,0.01)
    
    def seek(self,other) :
        desiredVelocity = Vector2D(other.rect.getX(),other.rect.getY())
        print(desiredVelocity.vec,"x,y")
        desiredVelocity = desiredVelocity.sub(Vector2D(self.rect.getX(),self.rect.getY()))
        print(desiredVelocity.vec,"sub")
        desiredVelocity = desiredVelocity.normalize()
        print(desiredVelocity.vec,"norm")
        desiredVelocity = desiredVelocity.multiply(self.maxVelocity)
        print(desiredVelocity.vec,"mul")

        steering = Vector2D().add(desiredVelocity).sub(self.velocity)
        steering = steering.truncate(self.maxForce)

        velocity = Vector2D().add(steering).truncate(self.maxVelocity)

        self.move(velocity.vec[0],velocity.vec[1])
