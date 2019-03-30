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

    def getAllPoints(self) :
        if not(self.isSplitted) :
            return self.points
        else :
            points=[]
            points+=self.nw.getAllPoints()
            points+=self.sw.getAllPoints()
            points+=self.ne.getAllPoints()
            points+=self.se.getAllPoints()
            return points

    def addPoint(self,point) :
        if not(self.containsPoint(point)) : return False
        if self.isSplitted :
            added=False
            if self.nw.addPoint(point) or self.ne.addPoint(point) or self.sw.addPoint(point) or self.se.addPoint(point): added=True
        else :
            if len(self.points)<self.capacity :
                self.points.append(point)
            else :
                self.__split()
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

    def containsPoint(self,point) :
        x=self.boundary.pos.x
        y=self.boundary.pos.y
        w=self.boundary.w
        h=self.boundary.h
        if (point.x >= x and point.x < x+w) and (point.y >= y and point.y < y+h) :
            return True
        else :
            return False

    def containsRectangle(self,rect:Rectangle) -> bool:
        rtl=(rect.pos.x,rect.pos.y)
        rtr=(rect.pos.x+rect.w,rect.pos.y)
        rbl=(rect.pos.x,rect.pos.y+rect.h)
        rbr=(rect.pos.x+rect.w,rect.pos.y+rect.h)
        sx=self.boundary.pos.x
        sy=self.boundary.pos.y
        sw=self.boundary.w
        sh=self.boundary.h

        if (rbr[0]>=sx and rbr[0]<sx+sw) and (rbr[1]>=sy and rbr[1]<sy+sh) :
            return True
        if (rbl[0]>=sx and rbl[0]<sx+sw) and (rbl[1]>=sy and rbl[1]<sy+sh) :
            return True
        if (rtr[0]>=sx and rtr[0]<sx+sw) and (rtr[1]>=sy and rtr[1]<sy+sh) :
            return True
        if (rtl[0]>=sx and rtl[0]<sx+sw) and (rtl[1]>=sy and rtl[1]<sy+sh) :
            return True

    def queryRectangle(self, rect:Rectangle) -> list :
        if not(self.containsRectangle(rect)) : return []
        points=[]

        if self.isSplitted :
            points+=self.nw.queryRectangle(rect)
            points+=self.ne.queryRectangle(rect)
            points+=self.sw.queryRectangle(rect)
            points+=self.se.queryRectangle(rect)
            return points

        rx=rect.pos.x
        ry=rect.pos.y
        rh=rect.h
        rw=rect.w

        for p in self.points :
            px=p.x
            py=p.y

            if (px>=rx and px<rx+rw) and (py>=ry and py<ry+rh) :
                points.append(p)

        return points

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

    def printPoints(self) :
        for x in self.points :
            x.print()
