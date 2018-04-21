from vehicle import Vehicle
import random
class TrafficInjection:
    def __init__(self):
        pass

    def getVehicles(self):
        return []

    def resetVehicles(self):
        pass

class UniformTrafficInjection(TrafficInjection):
    def __init__(self):
        self.start_time = 0
        
    def getVehicles(self):
        self.vehicles = [Vehicle(1, (1, 2, 1), (5, 50, 0), (1,0,0), self.start_time, [0, -1.6,  0]),
                        Vehicle(2, (1, 2, 1), (5, 50, 0), (0,1,0), self.start_time + 25, [0, -1.6, 0]),
                        Vehicle(3, (1, 2, 1), (5, 50, 0), (0,0,1), self.start_time + 50, [0, -1.6, 0])]
        self.start_time = 50
        return self.vehicles

    def restartVehiclesIfReq(self, time_units):
        for vehicle in self.vehicles:
            if vehicle.stopped:
                vehicle.stopped = False
                self.start_time += 25
                vehicle.start_time = self.start_time
        return self.vehicles

    def resetVehicles(self):
        self.start_time = -25
        for vehicle in self.vehicles[:-1]:
            vehicle.reset()
            self.start_time += 25
            vehicle.start_time = self.start_time
        self.vehicles[-1].reset()
        return self.vehicles

    def printVehicles(self):
        for vehicle in self.vehicles:
            print(vehicle.idno, vehicle.pos, vehicle.velocity, vehicle.start_time)

class RandomTrafficInjection(TrafficInjection):
    def __init__(self):
        self.start_time = 0

    def getVehicles(self):
        st1 = self.start_time + int(5*random.random())
        st2 = st1 + 10 + int(20*random.random())
        st3 = st2 + 10 + int(20*random.random())
        vel = -0.8 - 1.2*random.random()
        self.vehicles = [Vehicle(1, (1, 2, 1), (5, 50, 0), (1,0,0), st1, [0, vel,  0]),
                        Vehicle(2, (1, 2, 1), (5, 50, 0), (0,1,0), st2, [0, vel, 0]),
                        Vehicle(3, (1, 2, 1), (5, 50, 0), (0,0,1), st3, [0, vel, 0])]
        self.start_time = st3
        return self.vehicles

    def restartVehiclesIfReq(self, time_units):
        self.start_time = time_units
        stopped = 0
        for vehicle in self.vehicles:
            if vehicle.stopped:
                stopped += 1
        if stopped >= len(self.vehicles) - 1:
            vel =  -0.8 - 1.2*random.random()
            for vehicle in self.vehicles[:-1]:
                vehicle.stopped = False
                self.start_time += 10 + int(20*random.random())
                vehicle.start_time = self.start_time
                vehicle.velocity = [0, vel, 0]
        return self.vehicles

    def resetVehicles(self):
        self.start_time = 0
        for vehicle in self.vehicles[:-1]:
            vehicle.reset()
            if self.start_time < 0:
                self.start_time = 0
            else:
                self.start_time += 10 + int(20*random.random())
            vehicle.start_time = self.start_time
        self.vehicles[-1].reset()
        return self.vehicles

    def printVehicles(self):
        for vehicle in self.vehicles:
            print(vehicle.idno, vehicle.pos, vehicle.velocity, vehicle.start_time)
