import cv2
import numpy as np
from vehicle import Vehicle
class FeatureExtractor:
    def __init__(self):
        is_cv3 = cv2.__version__.startswith("3.")
        if is_cv3:
                self.detector = cv2.SimpleBlobDetector_create()
        else:
                self.detector = cv2.SimpleBlobDetector()

    def sendFeaturesFrom(self, vehicle, imageBlob, vehicles):
        feature_vec = []
        ## Adding positions
        feature_vec += vehicle.pos[:-1]
        ## Adding velocities
        feature_vec += vehicle.velocity[:-1]
        ## Adding distance from the middle edge of the road
        feature_vec.append(10 - vehicle.pos[1])

        ## For each of the vehicles add their velocities, distances from the target vehicle
        for veh in vehicles:
            #print(veh.idno, veh.velocity, veh.pos, veh.stopped)
            if veh.idno == vehicle.idno:
                continue
            if veh.pos[1] > vehicle.pos[1] and veh.pos[1] < 50:
                feature_vec += [veh.pos[0] - vehicle.pos[0], veh.pos[1] - vehicle.pos[1]]
                feature_vec += [veh.velocity[0], veh.velocity[1]]
            else:
                feature_vec += [100, 100]  ## Far far away
                feature_vec += [0, 0] ## and they dont have velocities
        feature_vec.append(vehicle.orientation)
        #print("accleration feature ", vehicle.velocity, vehicle.prev_vel)
        feature_vec += [vehicle.velocity[0] - vehicle.prev_vel[0], vehicle.velocity[1] - vehicle.prev_vel[1]]
        feature_vec += self.featuresFromBlob(imageBlob)
        #print("feature vector", feature_vec, len(feature_vec))
        return feature_vec

    def featuresFromBlob(self, imageBlob):
        #print("image blob ", imageBlob.shape)
        keypoints = self.detector.detect(imageBlob)
        #print("keypoints", (len(keypoints)))
        return []
