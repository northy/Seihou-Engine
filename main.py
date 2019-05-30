import os, sys, pygame
sys.path.append("bin/")
from quadtree import *
import numpy as np
from factories import *

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
player.hitbox = Circle(5)
player.image = pygame.Surface((20,30))
player.rect = Rectangle(0,0,20,30)
player.moveSpeed = 15

b = Bullet()
b.image=pygame.Surface((5,5))
b.rect=Rectangle(0,0,5,5)
b.velocity = np.array([2,2])

bp = bulletFactory()
bp.addBullet(b)

enemy=Enemy()
enemy.image = pygame.Surface((10,10))
enemy.rect = Rectangle(0,0,10,10)
enemy.lifes=0
enemy.pattern=[[1,0,[bp]]]

group=pygame.sprite.Group()

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

    enemy.think(group)
    enemy.draw(game)

    for bul in group :
        bul.move()
        bul.draw(game)

    player.draw(game)
    player.drawHitbox(game)

    fps = font.render(str(int(clock.get_fps())), True, white)
    display.blit(fps, (610, 460))

    display.blit(game,gamePadding)
    pygame.transform.scale(display,(sWidth,sHeight),screen)
    pygame.display.flip()

    clock.tick_busy_loop(60)
