import serial
import time
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Define the vertices of a cube
vertices = [
    [1, 1, -1],
    [1, -1, -1],
    [-1, -1, -1],
    [-1, 1, -1],
    [1, 1, 1],
    [1, -1, 1],
    [-1, -1, 1],
    [-1, 1, 1]
]

# Define the edges of the cube
edges = [
    [0, 1],
    [1, 2],
    [2, 3],
    [3, 0],
    [4, 5],
    [5, 6],
    [6, 7],
    [7, 4],
    [0, 4],
    [1, 5],
    [2, 6],
    [3, 7]
]

# Function to draw the cube
def draw_cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

# Initialize the Pygame window and OpenGL
def init_pygame():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    glEnable(GL_DEPTH_TEST)  # Enable depth testing for proper rendering

def get_ypr(line):
    # Split the line into a list of strings
    parts = line.split('\t')

    # Extract the Euler angles, assuming correct format 'ypr\t<yaw>\t<pitch>\t<roll>'
    if len(parts) == 4 and parts[0] == 'ypr':
        try:
            yaw = float(parts[1])
            pitch = float(parts[2])
            roll = float(parts[3])
            return yaw, pitch, roll
        except ValueError:
            pass  # If conversion fails, return None
    return None, None, None  # Return None if the format is unexpected

def initialize_serial_connection(port, baudrate):
    ser = serial.Serial(port, baudrate)
    time.sleep(1)  # wait for the serial connection to initialize
    return ser

# Initialize serial communication
ser = initialize_serial_connection('/dev/ttyUSB0', 115200)

def main():
    init_pygame()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                ser.close()  # Close serial connection on quit
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Get yaw, pitch, roll values from the MPU6050
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            yaw, pitch, roll = get_ypr(line)

            if yaw is not None and pitch is not None and roll is not None:
                print(f"Yaw: {yaw}, Pitch: {pitch}, Roll: {roll}")

                # Apply rotations based on yaw, pitch, and roll
                glLoadIdentity()
                glTranslatef(0.0, 0.0, -5)
                glRotatef(roll, 0, 0, 1)
                glRotatef(pitch, 1, 0, 0)
                glRotatef(yaw, 0, 1, 0)

        # Draw the cube
        draw_cube()

        # Update the display
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
