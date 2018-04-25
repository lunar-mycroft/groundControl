from digi.xbee.devices import XBeeDevice
from utility import getOpts, floatToHex,hexToFloat
from rocket import Flight

logFile=open("Launch1Log.TXT")

lines=[]
for line in logFile:
    lines.append(line[:32])

for line in lines[1:]:
    print(line)