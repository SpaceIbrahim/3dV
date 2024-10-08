from vpython import *
import numpy as np
import time
import serial
import math
from objects import *

ser = serial.Serial('/dev/ttyUSB0', 115200)
time.sleep(1)  # wait for the serial connection to initialize


scene.range = 5
toRad=2*np.pi/360
toDeg=1/toRad

scene.forward = vector(-1,-1,-1)

scene.width = 800
scene.height = 600

xArrow = arrow(length=2, axis=vector(1,0,0), color=color.red)
yArrow = arrow(length=2, axis=vector(0,1,0), color=color.green)
zArrow = arrow(length=2, axis=vector(0,0,1), color=color.blue)

xArrow.shaftwidth = 0.1
yArrow.shaftwidth = 0.1
zArrow.shaftwidth = 0.1

frontArrow = arrow(length=4, shaftWidth=0.1, axis=vector(1,0,0), color=color.purple)
sideArrow = arrow(length=2, shaftWidth=0.1, axis=vector(0,1,0), color=color.orange)
upArrow = arrow(length=1, shaftWidth=0.1, axis=vector(0,0,1), color=color.magenta)

myObj = drone_object()

yaw = 0
pitch = 0
roll = 0

tester = False
while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        parts = line.split('\t')

        # Extract the Euler angles, assuming correct format 'ypr\t<yaw>\t<pitch>\t<roll>'
        if len(parts) == 4 and parts[0] == 'ypr':
            try:
                yaw = float(parts[1])
                pitch = float(parts[2])
                roll = float(parts[3])
                tester = True
            except ValueError:
                print("Error")
                pass  # If conversion fails, return None
    
    if tester:
        tester = False
        yaw = yaw*toRad
        pitch = pitch*toRad
        roll = roll*toRad
    print(f"Yaw: {yaw}, Pitch: {pitch}, Roll: {roll}")
    rate(60)
    k = vector(math.cos(yaw)*math.cos(pitch), math.sin(pitch), math.sin(yaw)*math.cos(pitch))

    y = vector(0,1,0)
    s = cross(y,k)
    v = cross(s,k)

    vrot = rotate(v, angle=roll, axis=k)

    srot = rotate(s, angle=roll, axis=k)
    frontArrow.axis = k
    frontArrow.length = 4
    frontArrow.shaftwidth = 0.1
    sideArrow.axis = srot
    sideArrow.length = 2
    sideArrow.shaftwidth = 0.1
    upArrow.axis = -vrot
    upArrow.length = 2
    upArrow.shaftwidth = 0.1

    myObj.axis = k
    myObj.up = -vrot
    # time.sleep(0.1)