import numpy as np
import h5py
import math, numpy.linalg as la
from commander_physics import Commander as commander_physics
import torch
import copy

import sys
sys.path.insert(0, '../models')
from mymodel import make_model, predict
from sklearn.preprocessing import PolynomialFeatures

class Commander:
	def __init__(self):
		self.action = {0 : "UP", 1 : "DOWN",  2 : "LEFT", 3 : "RIGHT", 4: "No_Control"}
		self.loaded_model,_,_ = make_model(inp_dimn=65, out_dimn=1, net="orientation_regression", n_hidden=0)
		state = torch.load("../models/params/model_regression.pth")
		self.loaded_model.load_state_dict(state)
		self.commander_physics = commander_physics()
		self.threshold = 0

	def getCommand(self,featureVecs):
		## this function only works for orientation_regression right now...
		## as the function requires 23 features for mlp_all_labels, so change according to you model
		
		## make a copy of the original features
		features = copy.deepcopy(featureVecs)
		
		## extract features that you used to train your ML model 
		featureVecs, curr_orientation = self.extract_features_labels(featureVecs)
		# print(featureVecs.shape)

		## do feature processing as done in your ML model
		featureVecs = self.processing(featureVecs)
		out_orientation = predict(self.loaded_model, featureVecs)
		# print("current orientation:", curr_orientation, ",output orientation:", out_orientation)
		
		## decide whether to take a right/left based on current and expected orientation
		if np.abs(out_orientation-curr_orientation)>self.threshold:
			if out_orientation < curr_orientation:
				self.action = "RIGHT"
			else:
				self.action = "LEFT"
		else:
			self.action = "No_Command"
		command = self.action
		# print("Steering Command: ", command)

		## Fetch the accleration for controlling the vehicle to avoid collisions
		new_acc = self.commander_physics.getCommand(features)
		# if new_acc > 0:
		#     command1 = "UP"
		# else:
		#     command1 = "DOWN"
		
		## The ACCORIENT command will both update the acc and apply the steering command.
		return "ACCORIENT_" + str(new_acc) + "_" + str(command)
		#return [command, command1]

	def extract_features_labels(self, data):
		## make sure this matches your feature extraction in the models file that you have used
		def py_ang(v1, v2):
			cosang = np.dot(v1, v2)
			sinang = la.norm(np.cross(v1, v2))
			return np.arctan2(sinang, cosang)
		labels = data[17]    
		ref = [10,0]
		feat = [data[0], data[1], data[2], data[3], data[4], data[18], data[19]]
		feat.append(10 - data[0])    ## X distance from (10,10)

		d = np.square(data[0]-ref[0])+np.square(data[1]-ref[1])    ## abs dist of car from (10,0)
		feat.append(d)
	            
		vec1 = [10 - data[0], 10 - data[0]]    ## line connecting (10,10) and car X 
		vec2 = [10 - data[1], -10 - data[1]]   ## line connecting (10,-10) and car X
		ang = py_ang(vec1, vec2)*(180/math.pi)   ## angle formed by these lines
		feat.append(ang)    ##(angle at which car approaches the junction)
		feat = np.array(feat)
		feat = feat.reshape((-1, feat.shape[0]))
		return feat, labels

	## do processing like polynomial projection and min max scaling
	def processing(self, featureVecs):
		poly = PolynomialFeatures(degree=2, include_bias=False)
		params = np.load("../models/params/poly_params.npy").item()
		poly.fit(featureVecs)
		poly.set_params(**params)
		featureVecs = poly.transform(featureVecs)
		# print("feats after polynomial projection: ", featureVecs.shape)
		min_xval = np.load("../models/params/min_scale.npy")
		max_xval = np.load("../models/params/max_scale.npy")
		featureVecs = (featureVecs - min_xval)/(max_xval - min_xval)
		featureVecs = np.nan_to_num(featureVecs)
		return featureVecs
