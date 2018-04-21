from cuboid import Cuboid
from OpenGL.GL import *
from OpenGL.GLU import *
from operator import add
import math
from math import cos, sin, radians
from rectangles import Vector, Line, rectangle_vertices, intersection_area
class Vehicle:

    def __init__(self, idno, size, pos, color, start_time, velocity, stopped=False, mode="automatic", acc=None):
        ## 3 D size and position
        self.idno = idno
        self.size = size
        self.pos = pos
        self.init_vel = velocity
        self.init_pos = pos
        self.color = color
        self.mode = mode
        self.start_time = start_time
        self.velocity = velocity
        self.prev_vel = velocity
        self.stopped = stopped
        self.acc = [0, 0, 0]
        self.distance_travelled = 0
        self.total_distance = abs(-10 - self.pos[1]) + self.calculate_perimeter_circle(10)/4 + 5
        self.cuboid = Cuboid(size[0], size[1], size[2], color)
        self.orientation = 0

    def updatePos(self, time, vehicles):
        #print(self.idno, self.velocity, self.pos)
        self.updateVelocity([sum(x) for x in zip(self.velocity, self.rotateVec(self.acc, self.orientation))])
        if self.mode=="physics":
            #print("prev velocity ", self.prev_vel, self.velocity)
            self.updatePosByPhysics2()
            return 
        if time < self.start_time or self.stopped:
            return
        self.pos = [sum(x) for x in zip(self.pos, self.velocity)]
        #print("Updating remaining velocities ", self.pos, self.velocity)
        if self.mode == "automatic":
            collided, veh = self.checkCollision(vehicles, time)
            if collided:
                if veh.pos[1] < self.pos[1]:
                    self.pos = [pos1 - velocity1 for pos1, velocity1 in zip(self.pos, self.velocity)]
                    self.updateVelocity([self.velocity[0], self.velocity[1] + 0.05, self.velocity[2]])
                    veh.updateVelocity([veh.velocity[0], veh.velocity[1] - 0.1, veh.velocity[2]])
            if self.pos[1] < -50:
                self.pos = self.init_pos
                self.velocity = self.init_vel
                self.prev_vel = self.init_vel
                self.stopped = True

    def rotateVec(self, vec, angle):
        x = vec[0]
        y = vec[1]
        x1 = x*cos(radians(angle)) - y*sin(radians(angle))
        y1 = x*sin(radians(angle)) + y*cos(radians(angle))
        return[x1, y1, vec[2]]

    def calculate_perimeter_elipse(self, a, b):
         perimeter = math.pi * ( 3*(a+b) - math.sqrt( (3*a + b) * (a + 3*b) ) )
         return perimeter

    def calculate_perimeter_circle(self, a):
         perimeter = 2 * math.pi * a
         return perimeter

    def mag(self, x): 
            return math.sqrt(sum(i**2 for i in x))

    def updatePosByPhysics(self):
        d = 0
        if self.pos[1] < -10 or abs(self.orientation) >= 90 or self.pos[0] > 5:
            self.pos = [sum(x) for x in zip(self.pos, self.velocity)]
            #print("self pos2", self.pos)
            self.pos = [x - 1/2*a for x, a in zip(self.pos, self.rotateVec(self.acc, self.orientation))]
            if self.pos[1] > -10 and abs(self.orientation) == 0:
                d = self.pos[1] + 10
                #self.pos[1] = -10
            #print("self pos1", self.pos)
        else:
            remaining_distance = self.total_distance - self.distance_travelled - 5
            change_in_orientation = ((90 - abs(self.orientation))*self.mag(self.velocity))/remaining_distance
            #print("change in orientation", self.orientation, change_in_orientation, self.distance_travelled, self.total_distance)
            self.orientation -= change_in_orientation
            #self.updateVelocity(self.rotateVec(self.velocity, -1*change_in_orientation))
            self.velocity = self.rotateVec(self.velocity, -1*change_in_orientation)
            self.prev_vel = self.rotateVec(self.prev_vel, -1*change_in_orientation)
            self.pos = [sum(x) for x in zip(self.pos, self.velocity)]
            self.pos = [x - 1/2*a for x, a in zip(self.pos, self.rotateVec(self.acc, self.orientation))]
            #print("self pos1x ", self.pos)
        if self.pos[1] != -10:
            self.distance_travelled += self.mag(self.velocity) - 1/2*self.mag(self.acc)
        else:
            self.distance_travelled += d

    def updatePosByPhysics2(self):
        self.pos = [sum(x) for x in zip(self.pos, self.velocity)]
        self.pos = [x - 1/2*a for x, a in zip(self.pos, self.rotateVec(self.acc, self.orientation))]

    def reset(self):
        self.pos = self.init_pos
        self.velocity = self.init_vel
        self.prev_vel = self.init_vel
        self.orientation = 0
        self.stopped = False
        self.distance_travelled = 0
        self.acc = [0 , 0, 0]

    def checkCollision(self, vehicles, time):
        ret = False
        veh = None
        for vehicle in vehicles[:-1]:
            if vehicle.idno == self.idno or vehicle.start_time > time:
                continue
            v1_bottomx = self.pos[0] - self.size[0]/2
            v1_bottomy = self.pos[1] - self.size[1]/2
            v1_topx    = self.pos[0] + self.size[0]/2
            v1_topy    = self.pos[1] + self.size[1]/2
            v2_bottomx = vehicle.pos[0] - vehicle.size[0]/2
            v2_bottomy = vehicle.pos[1] - vehicle.size[1]/2
            v2_topx    = vehicle.pos[0] + vehicle.size[0]/2
            v2_topy    = vehicle.pos[1] + vehicle.size[1]/2
            ## self and vehicle undhi get the area of intersection
            '''
            r1 = (self.pos[0], self.pos[1], self.size[0], self.size[1], self.orientation)
            r2 = (vehicle.pos[0], vehicle.pos[1], vehicle.size[0], vehicle.size[1], vehicle.orientation)
            intersection_area1 = intersection_area(r1, r2)
            if intersection_area1 == 0:
                ret = ret or True
                veh = vehicle
            '''
            if(not ((v1_topx < v2_bottomx or v2_topx < v1_bottomx) or (v1_topy < v2_bottomy or v2_topy < v1_bottomy))):
                    ret = ret or True
                    veh = vehicle
                    #print("Vehicle 1 and 2 ", v1_bottomx, v1_bottomy, v1_topx, v1_topy, v2_bottomx, v2_bottomy, v2_topx, v2_topy)
                    #print("Colliding vehicles", vehicle.idno, self.idno, vehicle.start_time, self.start_time, time)111
        return ret, veh

    def updateOrientation(self, orientation):
        self.orientation = orientation

    def updateVelocity(self, velocity):
        self.prev_vel = self.velocity
        self.velocity = velocity

    def updateAcc(self, acc):
        #print("updated acc ", acc)
        #print("print rotated acc ", self.rotateVec([0, acc, 0], self.orientation))
        #self.acc = self.rotateVec([0, acc, 0], self.orientation)
        self.acc = [0, acc, 0]

    def draw(self, time):
        if time < self.start_time or self.stopped:
            return
        glPushMatrix()
        glTranslatef(self.pos[0], self.pos[1], self.pos[2])
        glRotatef(self.orientation, 0, 0, 1)
        self.cuboid.drawSolidCuboid()
        glPopMatrix()

class VehicleUpdater:

    def __init__(self):
        pass

    def updateVelocity(self, vehicle, velocity):
        vehicle.updateVelocity(velocity)

    def updateOrientation(self, vehicle, orientation):
        vehicle.updateOrientation(orientation)

    def updateAcc(self, vehicle, acc):
        vehicle.updateAcc(acc)

