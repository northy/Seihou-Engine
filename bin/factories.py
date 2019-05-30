import pygame
from entities import *
import copy

class bulletFactory(object) :
    def __init__(self) :
        self.blueprints=[]
    
    def addBullet(self,b:Bullet) :
        self.blueprints.append(b)
        
    def spawn(self,g:pygame.sprite.Group) :
        for b in self.blueprints :
            g.add(b.copy())