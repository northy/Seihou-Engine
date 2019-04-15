import sys
from shapes import *
from entities import *

class Quadtree(object) :
    def __init__(self,boundary:Rectangle,capacity:int,maximumSplits:int=4,curSplits:int=0) :
        self.boundary=boundary
        self.curSplits=curSplits
        self.maximumSplits=maximumSplits
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
        return self.curSplits==self.maximumSplits

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
            if not(self.__exceededCapacity()) or self.__exceededSplitLimit():
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
                if (rect.collides(r.rect)) :
                    res.append(r)

        return res

    # splits the quadtree and moves the currently contained points ahead
    def __split(self) :
        self.isSplitted=True
        x=self.boundary.x
        y=self.boundary.y
        w=self.boundary.w
        h=self.boundary.h
        self.nw=Quadtree(Rectangle(x,y,w//2,h//2),self.capacity,self.maximumSplits,self.curSplits+1)
        self.sw=Quadtree(Rectangle(x,y+(h//2),w//2,h//2),self.capacity,self.maximumSplits,self.curSplits+1)
        self.ne=Quadtree(Rectangle(x+(w//2),y,w//2,h//2),self.capacity,self.maximumSplits,self.curSplits+1)
        self.se=Quadtree(Rectangle(x+(w//2),y+(h//2),w//2,h//2),self.capacity,self.maximumSplits,self.curSplits+1)
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

# visualize the quadtree
def visualize() :
    black = 0,0,0
    white = 255,255,255
    green = 0,255,0
    red = 255,0,0

    pygame.init()

    size = width, height = 600,800

    qtree = Quadtree(Rectangle(0,0,width,height),4)

    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock()

    leftClick,rightClick=None,None

    while True :
        mouseX,mouseY=pygame.mouse.get_pos()

        for event in pygame.event.get() :
            if event.type == pygame.QUIT : sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN :
                mouseb=pygame.mouse.get_pressed()
                if mouseb[0] : leftClick=(mouseX,mouseY)
                if mouseb[2] : rightClick=(mouseX,mouseY)

        screen.fill(black)

        if leftClick and rightClick :
            entt=Entity()
            entt.rect=Rectangle(min(leftClick[0],rightClick[0]),min(leftClick[1],rightClick[1]),abs(leftClick[0]-rightClick[0]),abs(leftClick[1]-rightClick[1]))
            qtree.addEntity(entt)
            leftClick,rightClick=None,None

        for r in qtree.getAllEntities() :
            r.rect.draw(screen,white,2)

        mouseRectangle=Rectangle(mouseX-20,mouseY-20,40,40)

        mouseRectangle.draw(screen,green,2)

        for p in qtree.queryRectangle(mouseRectangle) :
            p.rect.draw(screen,green,2)

        qtree.drawLines(screen,white)

        pygame.display.flip()

        clock.tick(60)

if __name__=="__main__" :
    visualize()