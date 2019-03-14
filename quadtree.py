from objects import *

class Quadtree :
    def __init__(self,boundary,capacity) :
        self.boundary=boundary
        self.points=[]
        self.capacity=capacity
        self.isSplitted=False
        self.nw=None
        self.ne=None
        self.sw=None
        self.se=None
    
    def addPoint(self,point) :
        if not(self.contains(point)) : return False
        if self.isSplitted :
            added=False
            if self.nw.addPoint(point) or self.ne.addPoint(point) or self.sw.addPoint(point) or self.se.addPoint(point): added=True
            print(added)
        else :
            if len(self.points)<self.capacity :
                self.points.append(point)
            else :
                self._split()
                self.nw.addPoint(point)
                self.ne.addPoint(point)
                self.sw.addPoint(point)
                self.se.addPoint(point)
                for p in self.points :
                    self.nw.addPoint(p)
                    self.ne.addPoint(p)
                    self.sw.addPoint(p)
                    self.se.addPoint(p)
                self.points=[]
        return True

    def contains(self,point) :
        x=self.boundary.x
        y=self.boundary.y
        w=self.boundary.w
        h=self.boundary.h
        if (point.x >= x and point.x < x+w) and (point.y >= y and point.y < y+h) :
            return True
        else :
            return False

    def _split(self) :
        self.isSplitted=True
        x=self.boundary.x
        y=self.boundary.y
        w=self.boundary.w
        h=self.boundary.h
        self.nw=Quadtree(Rectangle(x,y,w//2,h//2),self.capacity)
        self.ne=Quadtree(Rectangle(x,y+(y//2),w//2,h//2),self.capacity)
        self.sw=Quadtree(Rectangle(x+(x//2),y,w//2,h//2),self.capacity)
        self.se=Quadtree(Rectangle(x+(x//2),y+(y//2),w//2,h//2),self.capacity)