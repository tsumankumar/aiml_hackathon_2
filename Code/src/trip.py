from road import Road, RoadSegment
from vehicle import Vehicle
from featureExtractor import FeatureExtractor
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np
import time

class Trip:
    def __init__(self, vehicle):
        print("Trip Starts")
        self.vehicle = vehicle
        self.timer = 0
        self.data = []
        self.featureExtractor = FeatureExtractor()
        self.tripNo = 1

    def end_trip(self, status, vehicles):
        ## Calculate the score
        score = self.getScore()
        print("Score", score)
        if status == "successful":
            ## Write data in a file
            np.save("trips/trip"+str(int(time.time())), self.data)
            #print("Data ", self.data)
        if status == "collided":
            ## Write data in a file
            np.save("trips/trip"+str(int(time.time())) + "_collided", self.data)
            #print("Data ", self.data)
        self.reset_trip(vehicles)
        return score

    def reset_trip(self, vehicles):
        print("Previous Trip was for ", self.timer)
        self.timer = 0
        self.tripNo += 1
        for vehicle in vehicles:
            vehicle.reset()
        self.data = []

    def getblob(self, x, y, w, h):
        buffer = (GLubyte * (3*w*h))(0)
        glReadPixels(x, y, w, h, GL_RGB, GL_UNSIGNED_BYTE, buffer)
        # Use PIL to convert raw RGB buffer and flip the right way up
        image = Image.frombytes(mode="RGB", size=(w, h), data=buffer)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        img = np.array(image)
        #print(type(image), image.size)
        #image.save('jpap.png')
        return img

    def getFeatures(self, vehicles):
        #return self.vehicle.velocity
        blob = self.getblob(0, 0, 700, 850)
        return self.featureExtractor.sendFeaturesFrom(self.vehicle, blob, vehicles)

    def getScore(self):
        alpha1 = 0.1
        alpha2 = 0.1
        velocitiesX = []
        velocitiesY = []
        number_of_collisions = 0
        for dat in self.data:
            velocitiesX.append(dat[0])
            velocitiesY.append(dat[1])
            if dat[-2] != 0:
                number_of_collisions += 1
        #print("variance and number of collisions ", np.var(velocitiesX), np.var(velocitiesY), number_of_collisions)
        return alpha1*(np.var(velocitiesX) + np.var(velocitiesY))/2 + alpha2*number_of_collisions

    def check_trip_status_update(self, road, vehicles, control):
        ## If vehicle has finished movement or gone out of the screen end the trip and reset the trip
        is_in_collision = 0
        new_trip = False
        if self.out_of_road(road):
            print("Out of the Roads")
            score = self.end_trip("unsuccessful", vehicles)
            new_trip = True
        elif self.to_be_collided(vehicles, road):
            ## Change the color of the car or something like that.
            print("Collision")
            score = self.end_trip("collided", vehicles)
            new_trip = True
            is_in_collision = 1
        elif self.completed_trip():
            print("Completed Trip")
            score = self.end_trip("successful", vehicles)
            new_trip = True
        #if control != "No_Control":
        features = self.getFeatures(vehicles)
        if new_trip == False:
            score = self.getScore()

        features.append(score)
        features.append(is_in_collision)
        features.append(control)
        self.data.append(features)
        #print("features ", features)
        self.update_trip()
        return new_trip, score

    def completed_trip(self):
        #print("Completed Trip thing ", self.vehicle.pos)
        return self.vehicle.pos[0] > 10 and self.vehicle.pos[1] > -10 and self.vehicle.pos[1] < 10

    def to_be_collided(self, vehicles, road):
        ret = False
        for vehicle in vehicles:
            if vehicle.idno == self.vehicle.idno:
                continue
            v1_bottomx = self.vehicle.pos[0] - self.vehicle.size[0]/2
            v1_bottomy = self.vehicle.pos[1] - self.vehicle.size[1]/2
            v1_topx    = self.vehicle.pos[0] + self.vehicle.size[0]/2
            v1_topy    = self.vehicle.pos[1] + self.vehicle.size[1]/2
            v2_bottomx = vehicle.pos[0] - vehicle.size[0]/2
            v2_bottomy = vehicle.pos[1] - vehicle.size[1]/2
            v2_topx    = vehicle.pos[0] + vehicle.size[0]/2
            v2_topy    = vehicle.pos[1] + vehicle.size[1]/2
            if(not ((v1_topx < v2_bottomx or v2_topx < v1_bottomx) or (v1_topy + 1 < v2_bottomy or v2_topy + 1 < v1_bottomy))):
                ret = ret or True
                #print("Vehicle 1 and 2 ", v1_bottomx, v1_bottomy, v1_topx, v1_topy, v2_bottomx, v2_bottomy, v2_topx, v2_topy)
                #print("Colliding vehicles", vehicle.idno, self.vehicle.idno)
        return ret
    
    def out_of_road(self, road):
        ret = True
        for roadSegment in road.getBasicRoad():
            left_bottom = [roadSegment.x, roadSegment.y]
            right_top = [roadSegment.x + roadSegment.width, roadSegment.y + roadSegment.height]
            vehicle_posX = self.vehicle.pos[0]
            vehicle_posY = self.vehicle.pos[1]
            if ((vehicle_posX < left_bottom[0] or vehicle_posX > right_top[0]) or (vehicle_posY < left_bottom[1] or vehicle_posY > right_top[1])):
                ret = ret and True
            else:
                ret = ret and False
        return ret

    def update_trip(self):
        self.timer += 1
