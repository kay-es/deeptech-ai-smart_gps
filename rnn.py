import torch
import os
import torch.nn as nn
import torch.optim as optim
from torch.autograd import Variable
from torch.nn.utils.rnn import pad_packed_sequence, pack_sequence

training = True

if training:
    print("test mode")
else:
    print("test mode")


print()

# READ DATA AND DEFINE SOME SIZES
data = torch.load('data.pt')
data_size = len(data)
split_index = int(data_size * 0.8)
training_data = data[:split_index]
test_data = data[split_index:]
training_data = test_data


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
if os.path.isfile("model.pt"):
    model = torch.load("model.pt")
    net_available = True
else:
    model = Model()


def test():
    sorted_test_data = sorted(test_data, key=getLen, reverse=True)
    prepared_test_data = [[seq[1:4] for seq in x] for x in sorted_test_data]
    packed_test_data = pack_sequence([torch.tensor(x) for x in prepared_test_data])

    prepared_test_targets = [[seq[4:5] for seq in x] for x in sorted_test_data]

    test_batches, test_dimensions = pad_packed_sequence(packed_test_data)

    model.eval() # Modell auf Test umstellen und Gewichte einfrieren
    test_loss = 0
    for i in range(len(sorted_test_data)):
        # INPUT DATA FOR NEURONS
        test_batch = test_batches[:, i:i+1]
        test_input_seq = Variable(test_batch).float()
        test_target = Variable(torch.tensor([prepared_test_targets[i][0]])).float()
        # FORWARD PASS
        test_output = model(test_input_seq)
        l = criterion(test_output, test_target.float())
        diff = test_output.item() - test_target.item()
        print("prediction: ", output.item(), "target: ", test_target.item(), "; loss (MSE): ", l.item(), ";\t Differenz in h: ", (diff / 1000 / 60 / 60))
        test_loss += l
    test_loss /= len(test_data)
    print('Durchschnittsloss: ', test_loss.item())


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
epochs = 30
# TRAINING OR TEST
if training:
    for k in range(epochs):
        for i in range(len(sorted_data)):
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
            diff = output.item() - target.item()
            print("prediction: ", output.item(), "; target: ", target.item(), "; loss: ", loss.item(), ";\t Differenz in h: ", (diff / 1000 / 60 / 60))
            optimizer.step()

            #save model after every update
            torch.save(model, open('model.pt', 'wb'))
else:
    test()
