from digi.xbee.devices import XBeeDevice
from utility import getOpts, floatToHex,hexToFloat,hexToInt
from rocket import Flight
from math import pi

logFile=open("FLOGGER1.TXT")

lines=[]
for line in logFile:
    lines.append(line[:24])
logFile.close()


for line in lines[1:]:
    print("Timestamp "+str(hexToInt(line[0:8]))+", roll "+str(hexToFloat(line[8:16])*(180/pi))+", pitch "+str(hexToFloat(line[16:24])*(180/pi)))
    #hexToFloat(line[16:23])

