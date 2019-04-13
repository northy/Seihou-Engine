from bin.shapes import *
from bin.entities import *

class Quadtree(object) :
    def __init__(self,boundary:Rectangle,capacity:int,__ob:Rectangle=None) :
        self.boundary=boundary
        self.__ob= boundary if type(__ob)!="None" else __ob
        self.entities=[]
        self.capacity=capacity
        self.isSplitted=False
        self.nw=None
        self.ne=None
        self.sw=None
        self.se=None

    # returns a list of all the objects in the whole quadtree
    def getAllEntities(self) -> list:
        if not(self.isSplitted) :
            return self.entities
        else :
            entities=[]
            entities+=self.nw.getAllEntities()
            entities+=self.sw.getAllEntities()
            entities+=self.ne.getAllEntities()
            entities+=self.se.getAllEntities()
            return entities

    # checks if the capacity is exceeded
    def __exceededCapacity(self) -> bool:
        return len(self.entities)>=self.capacity

    # checks if it can continue splitting or if the split size is too low
    def __exceededSplitLimit(self) :
        return self.boundary.x//2 < __ob.x*0.1 or self.boundary.y//2 < __ob.y*0.1

    # adds an entity on the quadtree
    def addEntity(self,entt:Entity) -> bool:
        if not(self.containsRectangle(entt.rect)) : return False
        if self.isSplitted :
            add1=self.nw.addEntity(entt)
            add2=self.sw.addEntity(entt)
            add3=self.ne.addEntity(entt)
            add4=self.se.addEntity(entt)
            return add1 or add2 or add3 or add4
        else :
            if not(self.__exceededCapacity()) or __exceededSplitLimit():
                self.entities.append(entt)
            else :
                self.__split()
                self.nw.addEntity(entt)
                self.sw.addEntity(entt)
                self.ne.addEntity(entt)
                self.se.addEntity(entt)
        return True

    # returns whether the quadtree contains a rectangle
    def containsRectangle(self,rect:Rectangle) -> bool:
        return self.boundary.collides(rect)

    # returns all the entities that are colliding with the rectangle
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
            for r in self.entities :
                if (entt.rect.collides(r)) :
                    res.append(r)

        return res

    # splits the quadtree and moves the currently contained points ahead
    def __split(self) :
        self.isSplitted=True
        x=self.boundary.x
        y=self.boundary.y
        w=self.boundary.w
        h=self.boundary.h
        self.nw=Quadtree(Sprite(x,y,w//2,h//2),self.capacity,__ob)
        self.sw=Quadtree(Sprite(x,y+(h//2),w//2,h//2),self.capacity,__ob)
        self.ne=Quadtree(Sprite(x+(w//2),y,w//2,h//2),self.capacity,__ob)
        self.se=Quadtree(Sprite(x+(w//2),y+(h//2),w//2,h//2),self.capacity,__ob)
        for r in self.entities :
            self.nw.addEntity(r)
            self.ne.addEntity(r)
            self.sw.addEntity(r)
            self.se.addEntity(r)
        self.entities=[]

    # prints all entities
    def printEntities(self) :
        for x in self.entities :
            x.print()

    # draws the lines of the quadtree division
    def drawLines(self,s:pygame.surface.Surface,color:tuple=(255,255,255)) :
        if not(self.isSplitted) : return
        pygame.draw.line(s,color,(self.boundary.x+(self.boundary.w)//2,self.boundary.y),(self.boundary.x+(self.boundary.w)//2,self.boundary.y+self.boundary.h))
        pygame.draw.line(s,color,(self.boundary.x,self.boundary.y+(self.boundary.h)//2),(self.boundary.x+self.boundary.w,self.boundary.y+(self.boundary.h)//2))
        self.nw.drawLines(s,color)
        self.ne.drawLines(s,color)
        self.sw.drawLines(s,color)
        self.se.drawLines(s,color)
