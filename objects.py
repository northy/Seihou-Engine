import pygame

class Point() :
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def print(self) :
        print("x:", self.x, "| y:", self.y)

    def draw(self,surface:pygame.Surface,color=(0,0,0),radius=1,width=0) :
        pygame.draw.circle(surface,color,(self.x,self.y),radius)

class Rectangle() :
    def __init__(self,pos:Point,w:int,h:int) :
        self.pos=pos
        self.w=w
        self.h=h

    def print(self) :
        print("x:", self.pos.x, "| y:", self.y, "| w:", self.pos.w, "| h:", self.h)

    def draw(self,surface:pygame.Surface,color=(0,0,0),width=0) :
        pygame.draw.rect(surface,color,(self.pos.x,self.pos.y,self.w,self.h),width)
