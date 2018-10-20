import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import npdata
from torch.autograd import Variable

data = npdata.data
m, n = data.shape
input_size = n - 2
hidden_size = 10
n_batches = 1

class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, 2)
        self.linear = nn.Linear(hidden_size, 1) # 1 output for regression

    def forward(self, input_seq):
        output_seq, _ = self.lstm(input_seq)
        last_output = output_seq[-1]
        class_predictions = self.linear(last_output)
        return class_predictions


model = Model()

input_data = data[:, [1, 2, 3]]
input_data = input_data.reshape((m, n_batches, input_size))
input_seq = Variable(torch.from_numpy(input_data)).float()
optimizer = optim.SGD(model.parameters(), lr=0.1, momentum=0.8)
criterion = nn.MSELoss()
for _ in range(100):
    model.train()
    output = model(input_seq)
    a = np.array([[data[m - 1, 4]]])
    target = torch.tensor(a)
    loss = criterion(output, target.float())
    optimizer.zero_grad()
    loss.backward()
    print("prediction: ", output.item(), "; target: ", target.item(), "; loss: ", loss.item())
    optimizer.step()