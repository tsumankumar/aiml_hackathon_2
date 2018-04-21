from vehicle import Vehicle, VehicleUpdater
from math import cos, sin, radians
class Actions:
    def __init__(self):
        self.vehicleUpdater = VehicleUpdater()
        pass

    def rotateVec(self, vec, angle):
        x = vec[0]
        y = vec[1]
        x1 = x*cos(radians(angle)) - y*sin(radians(angle))
        y1 = x*sin(radians(angle)) + y*cos(radians(angle))
        return[x1, y1, vec[2]]

    def act(self, vehicle, commands):
        if not isinstance(commands,(list,)):
            commands = [commands]
        print("commands", commands)
        for command in commands:
            if command == "DOWN":
                #print("decrease the velocity")
                ## Find the velocity to be added by rotating unit velocity
                vel_to_be_added = self.rotateVec([0, -0.05, 0], vehicle.orientation)
            
                new_vel = [sum(x) for x in zip(vehicle.velocity, vel_to_be_added)]
                if new_vel[0] < 0 or new_vel[1] < 0:
                    return
                self.vehicleUpdater.updateVelocity(vehicle, new_vel)
            
            elif command == "UP":
                #print("increase the velocity")
                ## Find the velocity to be added by rotating unit velocity
                vel_to_be_added = self.rotateVec([0, 0.05, 0], vehicle.orientation)

                new_vel = [sum(x) for x in zip(vehicle.velocity, vel_to_be_added)]
                self.vehicleUpdater.updateVelocity(vehicle, new_vel)

            elif command == "LEFT":
                #print("rotate to the left by decreasing the angle")
                new_orientation = vehicle.orientation + 2

                ## Update velocity also by rotating it
                self.vehicleUpdater.updateVelocity(vehicle, self.rotateVec(vehicle.velocity, 2))
                self.vehicleUpdater.updateOrientation(vehicle, new_orientation)

            elif command == "RIGHT":
                #print("rotate to the right by increasing the angle")
                new_orientation = vehicle.orientation - 2

                ## Update velocity also by rotating it
                self.vehicleUpdater.updateVelocity(vehicle, self.rotateVec(vehicle.velocity, -2))
                self.vehicleUpdater.updateOrientation(vehicle, new_orientation)

            elif "ACCORIENT" in command:
                acc = float(command.split("_")[1])
                act = str(command.split("_")[-1])
                self.vehicleUpdater.updateAcc(vehicle, acc)

                if act == "LEFT":
                    change_orientation = 2
                elif act == "RIGHT":
                    change_orientation = -2
                new_orientation = vehicle.orientation + change_orientation
                self.vehicleUpdater.updateVelocity(vehicle, self.rotateVec(vehicle.velocity, change_orientation))
                self.vehicleUpdater.updateOrientation(vehicle, new_orientation)

            elif "ACC"  in command:
                acc = float(command.split("_")[-1])
                #print("acc action ", acc)
                self.vehicleUpdater.updateAcc(vehicle, acc)
            else:
                #print("Unknown Command")
                pass
