from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from cuboid import Cuboid
from road import Road
from vehicle import Vehicle, VehicleUpdater
from trip import Trip
from math import cos, sin, radians
import time
from action import Actions
from featureExtractor import FeatureExtractor
from PIL import Image
import numpy as np
import time
#from commander_right_left import Commander
#from commander_acc_dec import Commander
from commander import Commander as nn_manual_commander
from commander_physics import Commander as physics_commander
from trafficInjection import UniformTrafficInjection, RandomTrafficInjection
import random
ESCAPE = '\033'
 
window = 0

def InitGL(Width, Height): 
        glClearColor(1.0, 1.0, 1.0, 1.0) 
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)   
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(90.0, float(Width)/float(Height), 0.1, 1000.0)
        glMatrixMode(GL_MODELVIEW)

## view = 0 is top view, view = 1 is first person view
view = 0

## level = 0 is the vehicles go with same velocity and at equal intervals. 
## For level = 1, the vehicles go with random velocity and at unequal intervals
level = 0
prev_level = 0
game_modes = ["MANUAL" , "NETWORK"]
path_constraints = ["FREE", "CONSTRAINED"]
mode = 1
path_mode = 0
def keyPressed(*args):
        global view
        global level
        global mode
        global path_mode
        print("Did you come here keypressed ", args[0])
        if args[0] == ESCAPE:
                sys.exit()
        if args[0] == b'a':
                view = (view+1)%2
        if args[0] == b'l':
                level = (level+1)%2
        if args[0] == b'm':
                mode  = (mode+1)%2
        if args[0] == b'p':
                path_mode = (path_mode+1)%2
                init_vehicles()

def rotateVec(vec, angle):
    x = vec[0]
    y = vec[1]
    x1 = x*cos(radians(angle)) - y*sin(radians(angle))
    y1 = x*sin(radians(angle)) + y*cos(radians(angle))
    return[x1, y1, vec[2]]


def keySpecial (key, x, y):
        global time_units
        global mode
        global path_mode
        if game_modes[mode] != "MANUAL":
            return
        control = "No_Control"
        if key == GLUT_KEY_LEFT and path_constraints[path_mode] != "CONSTRAINED":
            control = "LEFT"
            actions.act(vehicles[-1], "LEFT")

        if key == GLUT_KEY_RIGHT and path_constraints[path_mode] != "CONSTRAINED":
            control = "RIGHT"
            actions.act(vehicles[-1], "RIGHT") 

        if key == GLUT_KEY_UP:
            control = "UP"
            actions.act(vehicles[-1], "UP")

        if key == GLUT_KEY_DOWN:
            control = "DOWN"
            actions.act(vehicles[-1], "DOWN")
        
        trip.check_trip_status_update(road, vehicles, control)

## Initializations
vehicleUpdater = VehicleUpdater()
if level == 0:
    trafficInjection = UniformTrafficInjection()
else:
    trafficInjection = RandomTrafficInjection()
vehicles = trafficInjection.getVehicles()
## Adding the target vehicle
vehicles.append(Vehicle(4, (1, 2, 1), (-5, -40, 0), (1,1,0), 0, [0, 0.2, 0], False, "manual" if path_mode == 0 else "physics"))
#print("vehicles returned are ", vehicles)
actions = Actions()
road = Road()
time_units = 0
trip = Trip(vehicles[-1])
if path_constraints[path_mode] == "FREE":
    commander = nn_manual_commander()
else:
    commander = nn_manual_commander()
    #commander = physics_commander()

featureExtractor = FeatureExtractor()   

def init_vehicles():
    ## Set of vehicles moving in the car.
    global level
    global trafficInjection
    global vehicles
    global time_units
    global trip
    global path_mode
    global commander
    if level == 0:
        trafficInjection = UniformTrafficInjection()
    else:
        trafficInjection = RandomTrafficInjection()
    vehicles = trafficInjection.getVehicles()
    if path_constraints[path_mode] == "FREE":
        commander = nn_manual_commander()
    else:
        print("PHYSICS")
        commander = physics_commander()
    ## Adding the target vehicle
    vehicles.append(Vehicle(4, (1, 2, 1), (-5, -40, 0), (1,1,0), 0, [0, 0.2, 0], False, "manual" if path_mode == 0 else "physics"))
    trip = Trip(vehicles[-1])
    time_units = 0

def firstPersonView():
    xPos = vehicles[-1].pos[0]
    yPos = vehicles[-1].pos[1]
    zPos = vehicles[-1].pos[2]
    addition = rotateVec([0, 2, 5], vehicles[-1].orientation)
    xPos += addition[0]
    yPos += addition[1]
    zPos += addition[2]
    lookAngle = radians(vehicles[-1].orientation)
    atx = xPos - sin(lookAngle)
    aty = yPos + cos(lookAngle)
    thetha = 1
    gluLookAt(xPos, yPos, zPos, atx, aty, zPos-thetha, 0.0, 0.0, 1.0)

def topView():
    gluLookAt(0, 0, 75, 0, 0, 0, 0, 1, 0)


def printText(x, y, z, text):
    glPushMatrix()
    #glLoadIdentity()
    glColor3f(0, 0, 0)
    glRasterPos3f(x,y,z)
    length = len(text)
    for i in range(length):
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, text[i])
    glPopMatrix()

frame_start_time = 0
frame_end_time = 0
total_time_in_millis = 0
count = 0
def DrawGLScene():
        global frame_start_time
        global frame_end_time
        global total_time_in_millis
        global count
        global time_units
        global view
        global window
        global vehicles
        global level, prev_level
        global mode, path_mode, game_modes, path_constraints
        if prev_level != level:
            init_vehicles()
        prev_level = level
        time_units += 1
        if frame_start_time != 0:
            frame_end_time = int(round(time.time() * 1000))
        #print("Time per frame = ", frame_end_time - frame_start_time, frame_start_time, frame_end_time, time.time())
        total_time_in_millis += frame_end_time - frame_start_time
        count += 1
        #print("Average and total time ", total_time_in_millis/(count*1.0), total_time_in_millis)
        frame_start_time = int(round(time.time() * 1000))
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        firstPersonView()
        draw()
        status, score = trip.check_trip_status_update(road, vehicles, "No_Control")
        if status:
            print("New Trip1, show new trip!!")
            time_units = 0
            #print("vehicle last ", vehicles[-1].prev_vel, vehicles[-1].velocity)
            vehicles_reset = trafficInjection.resetVehicles()
            #print("vehicle last ", vehicles[-1].prev_vel, vehicles[-1].velocity)
            #time.sleep(2)

        score = "Score: " + "{0:.3f}".format(score)
        score = score.encode('utf-8')

        blob = trip.getblob(0, 0, 700, 850) 
        ## Get the feature vector of the scene and get the action from the machine learning model.
        feature_vec = featureExtractor.sendFeaturesFrom(vehicles[-1], blob, vehicles)
        if time_units >= 0 and game_modes[mode] == "NETWORK":
            command = commander.getCommand(feature_vec)
        else:
            command = "No_Control"
        actions.act(vehicles[-1], command)
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        if view == 0:
            topView()
            level_dis = "Level: " + str(level+1)
            level_dis = level_dis.encode('utf-8')
            mode_str = "Mode: " + game_modes[mode]
            mode_str = mode_str.encode('utf-8')
            path_cons_str = "Path: " + path_constraints[path_mode]
            path_cons_str = path_cons_str.encode('utf-8')
            vels = str(vehicles[-1].velocity[0]) + "," + str(vehicles[-1].velocity[1])
            positions = str(vehicles[-1].pos[0]) + "," + str(vehicles[-1].pos[1])
            vels = vels.encode('utf-8')
            printText(-9, -55, 0, score)
            printText(-20, 70, 0, b"TAKE RIGHT TO WIN")
            printText(15, -20, 0, level_dis)
            #printText(15, -60, 0, vels)
            printText(15, -30, 0, mode_str)
            printText(15, -40, 0, path_cons_str)
            #printText(15, -40, 0, "Press 'p': CONSTRAINT vs FREE")
            #printText(15, -50, 0, "Press 'a': TOP vs FIRST PERSON VIEW")
        else:
            firstPersonView()
            #new_vec = rotateVec([-60, 70, -0], vehicles[-1].orientation)
            #printText(new_vec[0], new_vec[1], new_vec[2], score)
        draw() 
        for vehicle in vehicles:
            vehicle.updatePos(time_units, vehicles)
        #time.sleep(1)
        glutSwapBuffers()
        vehicles = trafficInjection.restartVehiclesIfReq(time_units)

def draw():
    for vehicle in vehicles:
        vehicle.draw(time_units)
        #print("vehicle ", vehicle.idno, vehicle.pos, vehicle.velocity)
    road.drawBasicRoad()


def DrawGLScene_WithMultipleViews():
    global time_units
    global view
    global window
    time_units += 1
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    w = 1400
    w_1 = 900
    w_2 = 600
    h = 1000
    h_2 = 600
    h_1 = 400
    glViewport(0, 0, w, h_1)
    glLoadIdentity()
    firstPersonView()
    draw()

    status, score  = trip.check_trip_status_update(road, vehicles, "No_Control")
    if status:
        print("New Trip, show new trip!!")
        time.sleep(3)

    blob = trip.getblob(0, 0, w, h_1) 
    ## Get the feature vector of the scene and get the action from the machine learning model.
    feature_vec = featureExtractor.sendFeaturesFrom(vehicles[-1], blob, vehicles)
    command = commander.getCommand(feature_vec)
    actions.act(vehicles[-1], command)
    
    #glViewport(w_1, h_1, w_2, h_2)
    glViewport(0, 0, w, h_1)
    glLoadIdentity()
    topView()
    draw()

    glutSwapBuffers()

def main():
        global window
        global total_time_in_millis
        global count
        width = 700
        #width = 1400
        height = 850
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(width, height)
        glutInitWindowPosition(0,0)

        window = glutCreateWindow('OpenGL Python Cube')
        
        glutDisplayFunc(DrawGLScene)
        glutIdleFunc(DrawGLScene)
        #glutDisplayFunc(DrawGLScene_WithMultipleViews)
        #glutIdleFunc(DrawGLScene_WithMultipleViews)
        glutKeyboardFunc(keyPressed)
        glutSpecialFunc(keySpecial)
        InitGL(width, height)
        glutMainLoop()
        print("Average and total time ", total_time_in_millis/(count*1.0), total_time_in_millis) 
if __name__ == "__main__":
        main() 
