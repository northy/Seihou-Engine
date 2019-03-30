import sys, pygame
from quadtree import *

black = 0,0,0
white = 255,255,255
green = 0,255,0

def drawLines(s,q) :
    if not(q.isSplitted) : return
    pygame.draw.line(s,white,(q.boundary.pos.x+(q.boundary.w)//2,q.boundary.pos.y),(q.boundary.pos.x+(q.boundary.w)//2,q.boundary.pos.y+q.boundary.h))
    pygame.draw.line(s,white,(q.boundary.pos.x,q.boundary.pos.y+(q.boundary.h)//2),(q.boundary.pos.x+q.boundary.w,q.boundary.pos.y+(q.boundary.h)//2))
    drawLines(s,q.nw)
    drawLines(s,q.sw)
    drawLines(s,q.ne)
    drawLines(s,q.se)

pygame.init()

size = width, height = 400,400

qtree = Quadtree(Rectangle(Point(0,0),width,height),4)

screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

while True :
    mouseX,mouseY=pygame.mouse.get_pos()

    for event in pygame.event.get() :
        if event.type == pygame.QUIT : sys.exit()
        if event.type==pygame.MOUSEBUTTONDOWN :
            qtree.addPoint(Point(mouseX,mouseY))

    screen.fill(black)

    for p in qtree.getAllPoints() :
        p.draw(screen,white,2)

    mouseRectangle=Rectangle(Point(mouseX-20,mouseY-20),40,40)

    mouseRectangle.draw(screen,green,2)

    for p in qtree.queryRectangle(mouseRectangle) :
        p.draw(screen,green,2)

    drawLines(screen,qtree)

    pygame.display.flip()

    clock.tick(60)
