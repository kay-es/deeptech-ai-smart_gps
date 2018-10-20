import torch
import os
import torch.nn as nn
import torch.optim as optim
import numpy as np
import npdata
from torch.autograd import Variable
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence, pack_sequence, pad_sequence

# READ DATA AND DEFINE SOME SIZES
training_data = torch.load('traindata_backup.pt')
input_size = 3
hidden_size = 10
n_batches = len(training_data)

class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        # RNN with LSTM and Linear activation function for regression
        self.lstm = nn.LSTM(input_size, hidden_size, 2)
        self.linear = nn.Linear(hidden_size, 1) # 1 output for regression

    def forward(self, input_seq):
        output_seq, _ = self.lstm(input_seq)
        last_output = output_seq[-1]
        class_predictions = self.linear(last_output)
        return class_predictions


# INIT MODEL FROM SCRATCH OR EXISTING
net_available = False
model = None
if (os.path.isfile("model.pt")):
    model = torch.load("model.pt")
    net_available = True
else:
    model = Model()

# Hyperparams
optimizer = optim.SGD(model.parameters(), lr=0.1, momentum=0.8)
criterion = nn.MSELoss()

# just for sorting
def getLen(item):
    return len(item)

# PREPARE DATA FOR TRAINING
sorted_data = sorted(training_data, key=getLen, reverse=True)
prepared_data = [[seq[1:4] for seq in x] for x in sorted_data]
packed_data = pack_sequence([torch.tensor(x) for x in prepared_data])

prepared_targets = [[seq[4:5] for seq in x] for x in sorted_data]
max_size = len(sorted_data[0])

batches, dimensions = pad_packed_sequence(packed_data)

# TRAINING
for i in range(len(sorted_data)):
    for _ in range(20):

        # INPUT DATA FOR NEURONS
        batch = batches[:, i:i+1]
        input_seq = Variable(batch).float()
        target = Variable(torch.tensor([prepared_targets[i][0]])).float()

        # FORWARD PASS
        model.train()
        output = model(input_seq)
        loss = criterion(output, target.float())

        # BACKPROPAGATION AND UPDATE WEIGHTS
        optimizer.zero_grad()
        loss.backward()
        print("prediction: ", output.item(), "; target: ", target.item(), "; loss: ", loss.item())
        optimizer.step()

        #save model after every update
        torch.save(model, open('model.pt', 'wb'))