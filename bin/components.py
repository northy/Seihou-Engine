import numpy as np
import pygame, os, sys
from timeit import default_timer as timer

def truncate(a,b) -> np.array :
    if np.linalg.norm(a)>b :
        a/=np.linalg.norm(a)
        a*=b
    return a

def drawText(surface:pygame.surface.Surface,text:str,size:int,pos:tuple,color:tuple=(0,0,0),fontName:str=None) :
    try :
        font = pygame.font.Font(fontName,size)
    except :
        font = pygame.font.SysFont(fontName,size)
    render = font.render(text,True,color)
    surface.blit(render,pos)

def loadImage(location:str,w:int=None,h:int=None) -> pygame.Surface:
    try:
        sFile = os.path.abspath(sys.modules['__main__'].__file__)
    except:
        sFile = sys.executable
    location=os.path.dirname(sFile)+'/'+location
    location = location.replace('/', os.sep).replace('\\', os.sep) #canonicalize path
    image=pygame.image.load(location).convert_alpha()
    if not(w is None and h is None) :
        image=pygame.transform.scale(image,(w,h))
    return image
        
def getDegree(vec:np.array) :
    vec[1]*=-1
    return np.degrees(np.arctan2(*vec.T[::-1])) % 360.0

class Sprite(object) :
    def __init__(self,ct,*image) :
        self.current=None #Surface
        self.i=0
        self.imageList=[] #[Surface]
        self.lastChange=None #Timer
        self.changeTimer=ct #float

        for x in image :
            self.imageList.append(x)

    def addImage(self, image:pygame.Surface) -> None :
        self.imageList.append(image)
    
    def get(self) -> pygame.Surface :
        if self.current == None :
            if len(self.imageList)==0 :
                print("Insuficient images in sprite to draw")
                exit(1)
            self.current = self.imageList[0]
        if len(self.imageList)==1 :
            return self.current
        try :
            return self.current
        finally:
            self.current=self.imageList[self.i]
            if self.lastChange is None or timer()-self.lastChange>=self.changeTimer :
                self.lastChange=timer()
                self.i = 0 if self.i+1==len(self.imageList) else self.i+1
    
    def getAngled(self,degree:float) -> pygame.Surface :
        image = self.get()
        w=image.get_rect().w
        h=image.get_rect().h
        image = pygame.transform.rotate(image, degree-90) #-90 because images imported are vertical
        image = pygame.transform.scale(image,(w,h))
        return image
    
    def getWithoutChanging(self) :
        if self.current is None :
            print("Insuficient images in sprite to draw")
            exit(1)
        return self.current
    
    def getAngledWithoutChanging(self,degree:float) :
        image = self.getWithoutChanging()
        w=image.get_rect().w
        h=image.get_rect().h
        image = pygame.transform.rotate(image, degree-90) #-90 because images imported are vertical
        image = pygame.transform.scale(image,(w,h))
        return image