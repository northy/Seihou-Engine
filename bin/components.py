import numpy as np
import pygame

def truncate(a,b) :
    if np.linalg.norm(a)>b :
        a/=np.linalg.norm(a)
        a*=b
    return a

def drawText(surface:pygame.surface.Surface,text:str,size:int,pos:tuple,color:tuple=(0,0,0),fontName:str=None) :
    font = pygame.font.SysFont(fontName,size)
    render = font.render(text,True,color)
    surface.blit(render,pos)