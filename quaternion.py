from vector import Vector, normalize
from math import sqrt,cos,sin,acos

class Quaternion:
    def __init__(self,vec=Vector((0,0,0)),w=0):
        self.vec=vec
        self.w=w

    def __abs__(self):
        return sqrt(abs(self.vec)**2+self.w**2)

    def normalize(self):
        self.vec=self.vec*abs(self)
        self.w=self.w*abs(self)

    def rotateVector(self,vec):
        t=self.vec.cross(vec)*2
        return vec+t*self.w+self.v.cross(t)

    def fromAxisAngle(self,axis,theta):
        self.w=cos(theta/2)
        sht=sin(theta/2)
        self.vec=normalize(axis)*sht

    def fromTwoVectors(self,orig,target):
        self.fromAxisAngle(orig.cross(target),acos(orig.dot(target)))

    