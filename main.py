from quadtree import *


qtree=Quadtree(Rectangle(Point(0,0),200,200),4)

qtree.addPoint(Point(20,20))
qtree.addPoint(Point(20,20))
qtree.addPoint(Point(20,20))
qtree.addPoint(Point(20,20))
qtree.addPoint(Point(20,20))

while True :
    x,y,w,h=map(int,input("x y w h= ").split())
    rect=Rectangle(Point(x,y),w,h)
    print("NW Contains:",qtree.nw.containsRectangle(rect))
    print("NE Contains:",qtree.ne.containsRectangle(rect))
    print("SW Contains:",qtree.sw.containsRectangle(rect))
    print("SE Contains:",qtree.se.containsRectangle(rect))
