import pygame

class Rectangle(pygame.rect.Rect) :
    def __init__(self,x:int,y:int,w:int,h:int) :
        self.x=x
        self.y=y
        self.w=w
        self.h=h

    def print(self) :
        print("x:", self.x, "| y:", self.y, "| w:", self.pos.w, "| h:", self.h)

    def draw(self,surface:pygame.Surface,color=(0,0,0),width=0) :
        pygame.draw.rect(surface,color,self,width)

    def collides(self,other) -> bool :
        if (self.x < other.x + other.w and
            self.x + self.w > other.x and
            self.y < other.y + other.h and
            self.y + self.h > other.y) :
            return True

        return False
