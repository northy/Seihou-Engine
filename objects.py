import pygame

class Point() :
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def print(self) :
        print("x:", self.x, "| y:", self.y)

    def draw(self,surface:pygame.Surface,color=(0,0,0),radius=1,width=0) :
        pygame.draw.circle(surface,color,(self.x,self.y),radius)

class Rectangle(pygame.Surface) :
    def __init__(self,pos:Point,w:int,h:int) :
        self.pos=pos
        self.w=w
        self.h=h

    def print(self) :
        print("x:", self.pos.x, "| y:", self.y, "| w:", self.pos.w, "| h:", self.h)

    def draw(self,surface:pygame.Surface,color=(0,0,0),width=0) :
        pygame.draw.rect(surface,color,(self.pos.x,self.pos.y,self.w,self.h),width)

    def collides(self,other) -> bool :
        otl=(other.pos.x,other.pos.y)
        otr=(other.pos.x+other.w,other.pos.y)
        obl=(other.pos.x,other.pos.y+other.h)
        obr=(other.pos.x+other.w,other.pos.y+other.h)
        sx=self.pos.x
        sy=self.pos.y
        sw=self.w
        sh=self.h

        if (obr[0]>=sx and obr[0]<sx+sw) and (obr[1]>=sy and obr[1]<sy+sh) :
            return True
        if (obl[0]>=sx and obl[0]<sx+sw) and (obl[1]>=sy and obl[1]<sy+sh) :
            return True
        if (otr[0]>=sx and otr[0]<sx+sw) and (otr[1]>=sy and otr[1]<sy+sh) :
            return True
        if (otl[0]>=sx and otl[0]<sx+sw) and (otl[1]>=sy and otl[1]<sy+sh) :
            return True
        return False
