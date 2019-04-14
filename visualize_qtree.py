import sys, pygame
from bin.quadtree import *

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
