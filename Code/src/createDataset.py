import  subprocess
import numpy as np
proc = subprocess.Popen(['ls', 'trips'], stdout=subprocess.PIPE)
stdout, stderr = proc.communicate()
trips = stdout.decode("ascii")
trips = trips.split("\n")[:-1]
data_set = []
dataset = "dataset_basic_"+str(len(trips))+"_trips"
for trip in trips:
    data_set.append(np.load("trips/" + trip)) # train_data.astype(float)
np.save(dataset, np.array(data_set))
