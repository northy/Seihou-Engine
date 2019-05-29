import numpy as np
from math import sqrt

class Vector2D() :
    def __init__(self,arr) :
        self.vec=np.array(arr)
    
    def add(self,other) :
        res=Vector2D(0,0)
        res.vec=self.vec+other.vec)
        return res
    
    def sub(self,other) :
        res=Vector2D(0,0)
        res.vec=np.subtract(self.vec,other.vec)
        return res

    def neg(self) :
        return Vector2D(-self.vec[0],-self.vec[1])
    
    def truncate(self,other) :
        return Vector2D(max(self.vec[0],other.vec[0]),max(self.vec[1],other.vec[1]))
    
    def multiply(self,other) :
        v=Vector2D()
        v.vec=np.multiply(self.vec,other.vec)
        return v
    
    def divide(self,other) :
        v=Vector2D()
        v.vec=self.vec/other.vec
        return v

    def normalize(self) :
        m=Vector2D
        res=Vector2D()
        return self.divide(res)