import pygame

class Rectangle(pygame.rect.Rect) :
    def __init__(self,x:float,y:float,w:float,h:float) :
        self.x=x
        self.tmpX=x
        self.y=y
        self.tmpY=y
        self.w=w
        self.tmpW=w
        self.h=h
        self.tmpH=h
    
    def copy(self) :
        new = Rectangle(self.getX(),self.getY(),self.getW(),self.getH())
        return new

    # prints information about the rectangle
    def print(self) :
        print("x:", self.tmpX, "| y:", self.tmpY, "| w:", self.tmpW, "| h:", self.tmpH)

    # draws the rectangle on the surface
    def draw(self,surface:pygame.Surface,color:tuple=(0,0,0),width:int=0) :
        pygame.draw.rect(surface,color,self,width)

    # checks if the rectangle is colliding with another rectangle
    def collides(self,other) -> bool :
        if (self.x < other.x + other.w and
            self.x + self.w > other.x and
            self.y < other.y + other.h and
            self.y + self.h > other.y) :
            return True

        return False

    # setters
    def setX(self,x:float) :
        self.tmpX=x
        self.x=int(self.tmpX)

    def setY(self,y:float) :
        self.tmpY=y
        self.y=int(self.tmpY)

    def setW(self,w:float) :
        self.tmpW=w
        self.w=int(self.tmpW)
    
    def setH(self,h:float) :
        self.tmpH=h
        self.h=int(self.tmpH)
    
    # getters
    def getX(self) :
        return self.tmpX

    def getY(self) :
        return self.tmpY
    
    def getW(self) :
        return self.tmpW

    def getH(self) :
        return self.tmpH

class Circle(object) :
    def __init__(self,r:int,color:tuple=(255,0,0)) :
        self.r=r
        self.width=r*2
        self.height=r*2
        self.color=color
    
    def draw(self,surf:pygame.surface.Surface,pos:tuple,width:int=0) :
        pygame.draw.circle(surf,self.color,pos,self.r,width)