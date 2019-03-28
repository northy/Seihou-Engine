from quadtree import *

qtree=Quadtree(Rectangle(0,0,200,200),4)
qtree._split()

while True :
    x,y=map(int,input("x y = ").split())
    print("NW Contains:",qtree.nw.contains(Point(x,y)))
    print("NE Contains:",qtree.ne.contains(Point(x,y)))
    print("SW Contains:",qtree.sw.contains(Point(x,y)))
    print("SE Contains:",qtree.se.contains(Point(x,y)))