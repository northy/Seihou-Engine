import os, sys, pygame
sys.path.append("bin/")
from quadtree import *

black = 0,0,0
white = 255,255,255
green = 0,255,0
red = 255,0,0

pygame.init()

resolution = dWidth, dHeight = 640,480
screensize = sWidth, sHeight = 1280,960
gameSize = gWidth, gHeight = 400,445
gamePadding = 32, 17

qtree = Quadtree(Rectangle(0,0,gWidth,gHeight),4)

screen = pygame.display.set_mode(screensize)
display = pygame.Surface(resolution)
game = pygame.Surface(gameSize)

clock = pygame.time.Clock()

font = pygame.font.Font(None, 30)

player = Player()

entity1,entity2,entity3,entity4,entity5=Entity(),Entity(),Entity(),Entity(),Entity()
entity1.rect=Rectangle(0,0,20,40)
entity2.rect=Rectangle(200,90,20,40)
entity3.rect=Rectangle(120,350,20,40)
entity4.rect=Rectangle(350,120,20,40)
entity5.rect=Rectangle(90,200,20,40)

qtree.addEntity(entity1)
qtree.addEntity(entity2)
qtree.addEntity(entity3)
qtree.addEntity(entity4)
qtree.addEntity(entity5)

c = Circle(5)

while True :
    for event in pygame.event.get() :
        if event.type == pygame.QUIT : pygame.quit(); sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP] : player.moveUp(qtree.boundary)
    if keys[pygame.K_DOWN] : player.moveDown(qtree.boundary)
    if keys[pygame.K_LEFT] : player.moveLeft(qtree.boundary)
    if keys[pygame.K_RIGHT] : player.moveRight(qtree.boundary)

    display.fill(black)

    game.fill(white)

    qtree.drawLines(game,black)

    player.draw(game)
    player.drawHitbox(game)

    fps = font.render(str(int(clock.get_fps())), True, white)
    display.blit(fps, (610, 460))

    display.blit(game,gamePadding)
    pygame.transform.scale(display,(sWidth,sHeight),screen)
    pygame.display.flip()

    clock.tick_busy_loop(60)
