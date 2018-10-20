import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import npdata
from torch.autograd import Variable
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence, pack_sequence, pad_sequence

#data = npdata.data
data = torch.load('traindata.pt')
#print(len(data))
#m, n = data.shape
input_size = 3
hidden_size = 10
n_batches = len(data)

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

optimizer = optim.SGD(model.parameters(), lr=0.1, momentum=0.8)
criterion = nn.MSELoss()


def getLen(item):
    return len(item)

sorted_data = sorted(data, key=getLen, reverse=True)
prepared_data = [[seq[1:4] for seq in x] for x in sorted_data]
packed_data = pack_sequence([torch.tensor(x) for x in prepared_data])

prepared_targets = [[seq[4:5] for seq in x] for x in sorted_data]
packed_targets = pack_sequence([torch.tensor(x) for x in prepared_data])
max_size = len(sorted_data[0])

for _ in range(20):

    #for batch in data:
     #   np_batch = np.array(batch)
      #  input_data = np_batch[:, [1, 2, 3]]

        batches, dimensions = pad_packed_sequence(packed_data)
        targets, dimensions_target = pad_packed_sequence(packed_targets)

        for i, batch in enumerate(batches):


            #input_data = batches.reshape(max_size, n_batches, input_size)
            input_seq = Variable(batch).float()

            target = Variable(targets[i]).float()

            model.train()
            output = model(input_seq)
            loss = criterion(output, target.float())


            optimizer.zero_grad()
            loss.backward()
            print("prediction: ", output.item(), "; target: ", target.item(), "; loss: ", loss.item())
            optimizer.step()