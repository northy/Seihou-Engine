from objects import *

class Quadtree :
    def __init__(self,boundary,capacity) :
        self.boundary=boundary
        self.points=[]
        self.rectangles=[]
        self.capacity=capacity
        self.isSplitted=False
        self.nw=None
        self.ne=None
        self.sw=None
        self.se=None

    def getAllPoints(self) -> list:
        if not(self.isSplitted) :
            return self.points
        else :
            points=[]
            points+=self.nw.getAllPoints()
            points+=self.sw.getAllPoints()
            points+=self.ne.getAllPoints()
            points+=self.se.getAllPoints()
            return points

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
        return (len(self.points)+len(self.rectangles))>=self.capacity

    def addRectangle(self,rect:Rectangle) -> bool:
        if not(self.containsRectangle(rect)) : return False
        if self.isSplitted :
            added=False
            added=added or self.nw.addRectangle(rect)
            added=added or self.sw.addRectangle(rect)
            added=added or self.ne.addRectangle(rect)
            added=added or self.se.addRectangle(rect)
            return added
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

    def __exceededCapacity(self) -> bool:
        return (len(self.points)+len(self.rectangles))>=self.capacity

    def addRectangle(self,rect:Rectangle) -> bool:
        if not(self.containsRectangle(rect)) : return False
        if self.isSplitted :
            added=False
            added=added or self.nw.addRectangle(rect)
            added=added or self.sw.addRectangle(rect)
            added=added or self.ne.addRectangle(rect)
            added=added or self.se.addRectangle(rect)
            return added
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

    def addPoint(self,point:Point) -> bool:
        if not(self.containsPoint(point)) : return False
        if self.isSplitted :
            added=False
            if self.nw.addPoint(point) or self.ne.addPoint(point) or self.sw.addPoint(point) or self.se.addPoint(point): added=True
            return added
        else :
            if not(self.__exceededCapacity()) :
                self.points.append(point)
            else :
                self.__split()
                self.nw.addPoint(point)
                self.ne.addPoint(point)
                self.sw.addPoint(point)
                self.se.addPoint(point)
        return True

    def containsPoint(self,point:Point) -> bool:
        x=self.boundary.pos.x
        y=self.boundary.pos.y
        w=self.boundary.w
        h=self.boundary.h
        if (point.x >= x and point.x < x+w) and (point.y >= y and point.y < y+h) :
            return True
        else :
            return False

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

        rx=rect.pos.x
        ry=rect.pos.y
        rh=rect.h
        rw=rect.w

        for p in self.points :
            px=p.x
            py=p.y

            if (px>=rx and px<rx+rw) and (py>=ry and py<ry+rh) :
                res.append(p)

        for r in self.rectangles :
            if (rect.collides(r)) :
                res.append(r)

        return res

    def __split(self) :
        self.isSplitted=True
        x=self.boundary.pos.x
        y=self.boundary.pos.y
        w=self.boundary.w
        h=self.boundary.h
        self.nw=Quadtree(Rectangle(Point(x,y),w//2,h//2),self.capacity)
        self.sw=Quadtree(Rectangle(Point(x,y+(h//2)),w//2,h//2),self.capacity)
        self.ne=Quadtree(Rectangle(Point(x+(w//2),y),w//2,h//2),self.capacity)
        self.se=Quadtree(Rectangle(Point(x+(w//2),y+(h//2)),w//2,h//2),self.capacity)
        for p in self.points :
            self.nw.addPoint(p)
            self.ne.addPoint(p)
            self.sw.addPoint(p)
            self.se.addPoint(p)
        self.points=[]
        for r in self.rectangles :
            self.nw.addRectangle(r)
            self.ne.addRectangle(r)
            self.sw.addRectangle(r)
            self.se.addRectangle(r)
        self.rectangles=[]

    def printPoints(self) :
        for x in self.points :
            x.print()
