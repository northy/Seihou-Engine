import pygame
import numpy as np
import random
from bin.colors import *
from bin.components import *
from bin.factories import *
from bin.quadtree import *
from bin.shapes import *

class Level0() :
    def __init__(self,game:pygame.surface.Surface,gWidth:int,gHeight:int) :
        self.game = game
        self.qtree = Quadtree(Rectangle(0,0,gWidth,gHeight),4)
        
        self.player = Player()
        self.player.hitbox = Circle(5)
        self.player.image = pygame.Surface((20,30))
        self.player.rect = Rectangle(0,0,20,30)
        self.player.moveSpeed = 15

        self.b = Bullet()
        self.b.image=pygame.Surface((5,5))
        self.b.rect=Rectangle(0,0,5,5)
        self.b.velocity = np.array([2,2])

        self.bp = bulletFactory()
        self.bp.addBullet(self.b)

        self.enemy=Enemy()
        self.enemy.image = pygame.Surface((10,10))
        self.enemy.rect = Rectangle(0,0,10,10)
        self.enemy.lifes=0
        self.enemy.pattern=[[1,1,[self.bp]]]
        self.enemy.maxForce=2
        self.enemy.maxVelocity=3

        self.group=pygame.sprite.Group()

    def process(self) :
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] : self.player.moveUp(self.qtree.boundary)
        if keys[pygame.K_DOWN] : self.player.moveDown(self.qtree.boundary)
        if keys[pygame.K_LEFT] : self.player.moveLeft(self.qtree.boundary)
        if keys[pygame.K_RIGHT] : self.player.moveRight(self.qtree.boundary)

        self.game.fill(white)

        self.enemy.think(self.group,self.qtree.boundary.getW(),self.qtree.boundary.getH())
        self.enemy.draw(self.game)

        self.player.draw(self.game)
        self.player.drawHitbox(self.game)

        for bul in self.group :
            bul.move()
            bul.draw(self.game)
