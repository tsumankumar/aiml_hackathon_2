import numpy as np
import h5py
import math, numpy.linalg as la
class Commander:
    def __init__(self):
       pass

    ## function to get collision costs over all t1 and the acceleration cost
    ## you might want to change this function according to your intuition
    def getCostForTs(self, t0, t1, dist, vel):
        collision_cost = 0.0
        ## add gaussian costs, where mean of gaussian is t1, std dev is 10 and cost is calculated for t0
        for t in t1:
            collision_cost += self.normpdf(t0, t, 10)

        acc_cost = 0
        acc = ((dist - vel*t0)*2.0)/(t0*t0)   ## s=(u*t)+(a*(t*t)/2)
        acc_cost = abs(acc)     ## cost for acceleration in case its too big
        return 2*collision_cost, acc_cost
        
    ## get cost for x using gaussian(mean, sd)
    def normpdf(self, x, mean, sd):
        var = float(sd)**2
        pi = math.pi
        denom = (2*pi*var)**.5
        num = math.exp(-(float(x)-float(mean))**2/(2*var))
        return num*1.0/denom

    ## function to get optimal time at which our car should reach the junction
    ## you might want to change this function according to your intuition
    def getOptimumt0(self, t1, dist, vel):
        costs = []
        index = []
        minimum = int(min(t1))
        maximum = int(max(t1))
        ## search between times at which the first car reaches junction and last car raches junction + 20
        for i in range(minimum, maximum+20):
            if i <= 0:
                continue
            costs.append(self.getCostForTs(i, t1, dist, vel)[0])  ## we haven't added cost for too much acceleration   
            index.append(i)
        # print("costs:", costs)
        ## return time for which cost is minimum
        return index[np.argmin(costs)]
    
    ## Refer to the documentation on how the path using physics is calculated
    def getCommand(self,featureVecs):
        ## Calculate the time taken by vehicles coming from opposite direction to reach the intersection
        t1 = []
        for i in range(3):
            posY = featureVecs[1] + featureVecs[6+(i*4)]      ##indices 6,10,14 give relative Y dist of car A/B/C from car X
            velY = featureVecs[8+i*4]   ## indices 8,12,16 give Y velocities of car X/Y/Z, there was a small error in the first doc where they were 7,11,15
            #print(posY, velY)
            if posY > 49:
                continue
            ## only considering cars above origin
            if posY > 0 and velY != 0 and featureVecs[6+(i*4)] > 0:
                t1.append((posY)/abs(velY))
        
        ## Calculating t0, the time taken by target(yellow vehicle) to take the right turn if it follows a fixed path
        distance = 0
        posy = featureVecs[1]
        orientation = featureVecs[17]
        ## optimal path is straight line till -10 and curve afterward
        ## quarter curve is essentially (2*pi*R)/4 where R is 10
        if posy <= -10:
            distance += abs(-10-posy) + 2*(math.pi*10)/4 + 5 
            #print("remaining distance ", distance)
        elif posy > -10:
            distance += (2*math.pi*10)*(90-abs(featureVecs[17]))/360 + 5
            #print("remaining distance2 ", distance)
        
        ## If velocity and acceleration are in different directions then acceleration is negative
        if (featureVecs[2]*featureVecs[18] < 0) or (featureVecs[3]*featureVecs[19]) < 0:
            acc = -1*math.sqrt((featureVecs[18]*featureVecs[18]) + (featureVecs[19]*featureVecs[19]))
        else:
            acc = math.sqrt((featureVecs[18]*featureVecs[18]) + (featureVecs[19]*featureVecs[19]))
        
        ## Absolute velocity of the target vehicle
        vel = math.sqrt((featureVecs[2]*featureVecs[2]) + (featureVecs[3]*featureVecs[3]))
        
        ## If there are vehicles in the front get optimum t0 (as referred to the document). The new acceleration
        ## is calculated using s = u*t + 1/2*a*t*t. If there are no vehicles in the front then the acceleration is 0
        if len(t1) != 0:
            ## get optimal time at which our car should reach the junction
            new_t0 = self.getOptimumt0(t1, distance, vel)
            ## get our car's acceleration according to optimal time and approximate distance it has to travel
            new_acc = ((distance - vel*new_t0)*2)/(new_t0*new_t0)
        else:
            new_acc = 0

        return new_acc 