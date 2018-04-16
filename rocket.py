from vector import Vector, normalize,getPerpComponent
from quaternion import Quaternion
from math import asin, acos,sqrt,pi
from utility import hexToFloat

class Rocket:
    def __init__(self):
        self.q=Quaternion()
        self.oldQ=Quaternion()

        #Absolute vectors
        self.up=Vector()
        self.north=Vector()
        self.east=Vector()

        #Position
        self.a=Vector()
        self.v=Vector()
        self.r=Vector()

        #relative vectors
        self.pointing=Vector((1,0,0))
        self.rollRef=Vector((0,1,0))

        self.event=0
        self.time=0
        self.lastTime=0
    def processTelemetry(self,line):
        self.oldQ.vec=Vector((self.q.vec.x,self.q.vec.y,self.q.vec.z))
        self.oldQ.w=self.q.w
        self.oldTime=self.time

        qx = hexToFloat(line[0:8])
        qy = hexToFloat(line[8:16])
        qz = hexToFloat(line[16:24])
        qw = hexToFloat(line[24:32])

        ax = hexToFloat(line[32:40])
        ay = hexToFloat(line[40:48])
        az = hexToFloat(line[48:56])

        self.q=Quaternion(Vector((qx,qy,qz)),qw)

        self.a=Vector((ax,ay,az))

        deltaT=(self.time-self.oldT)/1000000

        oldV=self.v
        self.v=self.v+self.q.rotateVector(self.a*deltaT)

        self.r=oldV*deltaT+self.q.rotateVector(self.a)*(deltaT**2)/2


    def getPitch(self):
        return asin(self.up.dot(self.q.rotateVector(self.pointing)))

    def getRoll(self):
        ref=None
        if self.getPitch()>pi/2-0.01:
            ref=self.q.rotateVector(self.rollRef)
        elif self.getPitch()<0.01-pi/2:
            ref=self.q.rotateVector(self.rollRef)*(-1)
        elif self.getPitch()>0:
            currentPoint=self.q.rotateVector(self.pointing)
            pitchFix=Quaternion
            pitchFix.fromTwoVectors(currentPoint,self.up)

            ref=pitchFix.rotateVector(self.q.rotateVector(self.pointing))


        else:
            currentPoint = self.q.rotateVector(self.pointing)
            pitchFix = Quaternion
            pitchFix.fromTwoVectors(currentPoint, self.up*(-1))

            ref = pitchFix.rotateVector(self.q.rotateVector(self.pointing))


        return (0 if self.east.dot(ref)>0 else pi)+acos(self.north.dot(ref))

    def getRollRate(self):
        deltaT=(self.time-self.lastTime)/1000000

        roll=self.getRoll()
        oldRoll=self.getOldRoll()

        if roll>7/4*pi and oldRoll<1/4*pi:
            return ((roll-2*pi)-oldRoll)/deltaT
        elif oldRoll>7/4*pi and roll<1/4*pi:
            return (roll-(oldRoll-2*pi))/deltaT
        else:
            return (roll-oldRoll)/deltaT

    def getOldRoll(self):
        ref = None
        if self.getPitch() > pi / 2 - 0.01:
            ref = self.oldQ.rotateVector(self.rollRef)
        elif self.getPitch() < 0.01 - pi / 2:
            ref = self.oldQ.rotateVector(self.rollRef) * (-1)
        elif self.getPitch() > 0:
            currentPoint = self.oldQ.rotateVector(self.pointing)
            pitchFix = Quaternion
            pitchFix.fromTwoVectors(currentPoint, self.up)

            ref = pitchFix.rotateVector(self.oldQ.rotateVector(self.pointing));

        else:
            currentPoint = self.oldQ.rotateVector(self.pointing)
            pitchFix = Quaternion
            pitchFix.fromTwoVectors(currentPoint, self.up * (-1))

            ref = pitchFix.rotateVector(self.oldQ.rotateVector(self.pointing));

        return (0 if self.east.dot(ref) > 0 else pi) + acos(self.north.dot(ref))

    def getYaw(self):
        ref=getPerpComponent(self.up,self.q.rotateVector(self.pointing))
        return (0 if self.east.dot(ref) > 0 else pi) + acos(self.north.dot(ref))

