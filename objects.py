class Rectangle() :
    def __init__(self,x,y,w,h) :
        self.x=x
        self.y=y
        self.w=w
        self.h=h
    
    def print(self) :
        print("x:", self.x, "| y:", self.y, "| w:", self.w, "| h:", self.h)

class Point() :
    def __init__(self,x,y) :
        self.x=x
        self.y=y
    
    def print(self) :
        print("x:", self.x, "| y:", self.y)