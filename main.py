from quadtree import *


qtree=Quadtree(Rectangle(Point(0,0),200,200),4)

qtree.addPoint(Point(20,20))
qtree.addPoint(Point(20,20))
qtree.addPoint(Point(20,20))
qtree.addPoint(Point(20,20))
qtree.addPoint(Point(20,20))

while True :
    x,y=map(int,input("x y = ").split())
    print("NW Contains:",qtree.nw.contains(Point(x,y)))
    print("NE Contains:",qtree.ne.contains(Point(x,y)))
    print("SW Contains:",qtree.sw.contains(Point(x,y)))
    print("SE Contains:",qtree.se.contains(Point(x,y)))
