from shapes import *

class Quadtree :
    def __init__(self,boundary,capacity) :
        self.boundary=boundary
        self.rectangles=[]
        self.capacity=capacity
        self.isSplitted=False
        self.nw=None
        self.ne=None
        self.sw=None
        self.se=None

    def getAllRectangles(self) -> list:
        if not(self.isSplitted) :
            return self.rectangles
        else :
            rectangles=[]
            rectangles+=self.nw.getAllRectangles()
            rectangles+=self.sw.getAllRectangles()
            rectangles+=self.ne.getAllRectangles()
            rectangles+=self.se.getAllRectangles()
            return rectangles

    def __exceededCapacity(self) -> bool:
        return len(self.rectangles)>=self.capacity

    def addRectangle(self,rect:Rectangle) -> bool:
        if not(self.containsRectangle(rect)) : return False
        if self.isSplitted :
            add1=self.nw.addRectangle(rect)
            add2=self.sw.addRectangle(rect)
            add3=self.ne.addRectangle(rect)
            add4=self.se.addRectangle(rect)
            return add1 or add2 or add3 or add4
        else :
            if not(self.__exceededCapacity()) :
                self.rectangles.append(rect)
            else :
                self.__split()
                self.nw.addRectangle(rect)
                self.sw.addRectangle(rect)
                self.ne.addRectangle(rect)
                self.se.addRectangle(rect)
        return True

    def containsRectangle(self,rect:Rectangle) -> bool:
        return self.boundary.collides(rect)

    def queryRectangle(self, rect:Rectangle) -> list :
        if not(self.containsRectangle(rect)) : return []
        res=[]

        if self.isSplitted :
            res+=self.nw.queryRectangle(rect)
            res+=self.ne.queryRectangle(rect)
            res+=self.sw.queryRectangle(rect)
            res+=self.se.queryRectangle(rect)
            return res
        else :
            for r in self.rectangles :
                if (rect.collides(r)) :
                    res.append(r)

        return res

    def __split(self) :
        self.isSplitted=True
        x=self.boundary.x
        y=self.boundary.y
        w=self.boundary.w
        h=self.boundary.h
        self.nw=Quadtree(Rectangle(x,y,w//2,h//2),self.capacity)
        self.sw=Quadtree(Rectangle(x,y+(h//2),w//2,h//2),self.capacity)
        self.ne=Quadtree(Rectangle(x+(w//2),y,w//2,h//2),self.capacity)
        self.se=Quadtree(Rectangle(x+(w//2),y+(h//2),w//2,h//2),self.capacity)
        for r in self.rectangles :
            self.nw.addRectangle(r)
            self.ne.addRectangle(r)
            self.sw.addRectangle(r)
            self.se.addRectangle(r)
        self.rectangles=[]

    def printRectangles(self) :
        for x in self.rectangles :
            x.print()

    def drawLines(self,s:pygame.Surface,color:tuple=(255,255,255)) :
        if not(self.isSplitted) : return
        pygame.draw.line(s,color,(self.boundary.x+(self.boundary.w)//2,self.boundary.y),(self.boundary.x+(self.boundary.w)//2,self.boundary.y+self.boundary.h))
        pygame.draw.line(s,color,(self.boundary.x,self.boundary.y+(self.boundary.h)//2),(self.boundary.x+self.boundary.w,self.boundary.y+(self.boundary.h)//2))
        self.nw.drawLines(s,color)
        self.ne.drawLines(s,color)
        self.sw.drawLines(s,color)
        self.se.drawLines(s,color)
