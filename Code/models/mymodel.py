import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import math
import numpy as np
import numpy.linalg as la

from torch.autograd import Variable


from sklearn.preprocessing import LabelBinarizer

## define all your models here so that they can be called/chosen by a simple flag 
def make_model(inp_dimn, out_dimn, net, n_hidden=0):
    if net == "mlp_all_labels":
        class Net(nn.Module):
            def __init__(self):
                super(Net, self).__init__()
                self.hidden = nn.Linear(inp_dimn, n_hidden)
                self.out   = nn.Linear(n_hidden, out_dimn)

            def forward(self, x):
                x = F.relu(self.hidden(x))
                x = F.tanh(self.out(x))
                return x
        model = Net()
        optimizer = optim.Adam(model.parameters(), lr=0.001)
        criterion = nn.MSELoss()

    elif net == "orientation_regression":
        class Net(nn.Module):
            def __init__(self):
                super(Net, self).__init__()
                self.regress = nn.Linear(inp_dimn, out_dimn, bias=False)

            def forward(self, x):
                ## We don't need the softmax layer here since CrossEntropyLoss already
                ## uses it internally.
                x = self.regress(x)
                return x
        model = Net()
        optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
#         optimizer = optim.Adam(model.parameters(), lr=0.01)
        criterion = nn.MSELoss()
    else:
        print("model choice not available")
    return model, optimizer, criterion

## convert the integer labels using one hot encoding. [[ 4 -> [0 0 0 0 1]  ]]
def one_hot_encoding(train_label):
    # encode class values as integers
    # convert integers to dummy variables (i.e. one hot encoded)
    n_class = len(action)
    classes = np.array(range(n_class))
    hot_enc = LabelBinarizer()
    hot_enc = hot_enc.fit(classes)
    one_hot_label_data = hot_enc.transform(train_label)
    return one_hot_label_data

## predict model outputs
def predict(model, data):
    model.eval()
    data = Variable(torch.FloatTensor(data), requires_grad=False)
    preds = model(data)
    preds = preds.data.numpy()
    return preds
