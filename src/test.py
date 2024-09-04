from vpython import *
import numpy as np
import time
import serial
import math

scene.range = 5
toRad=2*np.pi/360
toDeg=1/toRad

scene.forward = vector(-1,-1,-1)

scene.width = 800
scene.height = 600

xArrow = arrow(length=2, shaftWidth=0.1, axis=vector(1,0,0), color=color.red)
yArrow = arrow(length=2, shaftWidth=0.1, axis=vector(0,1,0), color=color.green)
zArrow = arrow(length=2, shaftWidth=0.1, axis=vector(0,0,1), color=color.blue)

# bBoard = box(length=4, height=.2, width=2, color=color.white, opacity=0.8, pos=vector(0,0,0))
# bn = box(length=1, height=0.1, width=.72, color=color.blue, opacity=0.8, pos=vector(0.5,0.15,0))

yaw = 0
pitch = 0
roll = 0

# Define the body of the drone
body = box(pos=vector(0, 0, 0), size=vector(1, 0.25, 1.5), color=color.gray(0.5))

# Define the arms of the drone
arm1 = cylinder(pos=vector(0.5, 0, 0.5), axis=vector(1, 0, 0.5), radius=0.1, color=color.white)
arm2 = cylinder(pos=vector(-0.5, 0, 0.5), axis=vector(-1, 0, 0.5), radius=0.1, color=color.white)
arm3 = cylinder(pos=vector(0.5, 0, -0.5), axis=vector(1, 0, -0.5), radius=0.1, color=color.white)
arm4 = cylinder(pos=vector(-0.5, 0, -0.5), axis=vector(-1, 0, -0.5), radius=0.1, color=color.white)

# Define the rotors
rotor1 = cylinder(pos=vector(1.5, 0.1, 1), axis=vector(0, 0.1, 0), radius=0.15, color=color.blue)
rotor2 = cylinder(pos=vector(-1.5, 0.1, 1), axis=vector(0, 0.1, 0), radius=0.15, color=color.blue)
rotor3 = cylinder(pos=vector(1.5, 0.1, -1), axis=vector(0, 0.1, 0), radius=0.15, color=color.blue)
rotor4 = cylinder(pos=vector(-1.5, 0.1, -1), axis=vector(0, 0.1, 0), radius=0.15, color=color.blue)

myObj = compound([body, arm1, arm2, arm3, arm4, rotor1, rotor2, rotor3, rotor4])

# myObj = compound([bBoard, bn])
while True:

    rate(60)
    k = vector(math.cos(yaw)*math.cos(pitch), math.sin(pitch), math.sin(yaw)*math.cos(pitch))

    y = vector(0,1,0)
    s = cross(y,k)
    v = cross(s,k)

    myObj.axis = k
    myObj.up = -v
    # time.sleep(0.1)