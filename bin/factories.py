import pygame
from bin.entities import *

class bulletFactory(object) :
    def __init__(self) :
        self.prototypes=[]
    
    def addBullet(self,b:Bullet) :
        self.prototypes.append(b)
        
    def spawn(self,g:pygame.sprite.Group,x:int,y:int) :
        for b in self.prototypes :
            bul=b.copy()
            bul.go(bul.rect.getX()+x,bul.rect.getY()+y)
            g.add(bul)