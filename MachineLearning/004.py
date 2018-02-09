import torch as torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision as tv
from torch.autograd import Variable

###########
# OPTIONS #
###########

batch_size = 64
learning_rate = 0.01
momentum = 0.5
n_epochs = 10

################
# DATA LOADERS #
################

mnist_transform = tv.transforms.Compose([
        tv.transforms.ToTensor(),
        tv.transforms.Normalize((0.1307,), (0.3081,))
    ])
train_mnist = tv.datasets.MNIST("../../Data/MNIST", train=True, download=True, transform=mnist_transform)
test_mnist = tv.datasets.MNIST("../../Data/MNIST", train=False, download=True, transform=mnist_transform)
train_loader = torch.utils.data.DataLoader(train_mnist, batch_size=batch_size, shuffle=True)
test_loader = torch.utils.data.DataLoader(test_mnist, batch_size=batch_size, shuffle=True)

#########
# MODEL #
#########

class Net(torch.nn.Module):

    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.drop = nn.Dropout2d()
        self.fc1 = nn.Linear(320, 50)
        self.fc2 = nn.Linear(50, 10)

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = F.relu(self.fc1(x))
        x = F.dropout(x)
        x = self.fc2(x)
        return F.log_softmax(x, dim=1)

model = Net()
# model.cuda()

######################
# LOSS AND OPTIMIZER #
######################

loss_function = F.nll_loss
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate, momentum=momentum)

##################
# TRAIN AND TEST #
##################

def train():
    model.train() # turns on Dropout layers
    for i, (event, truth) in enumerate(train_loader):
        # event, truth = event.cuda(), truth.cuda()
        event, truth = Variable(event), Variable(truth)
        result = model(event)
        loss = loss_function(result, truth)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        # if (i%100 == 0):
            # print(loss.data[0])

def test():
    correct = 0

    model.eval() # turns off Dropout layers
    for event, truth in test_loader:
        # event, truth = event.cuda(), truth.cuda()
        event, truth = Variable(event), Variable(truth)
        result = model(event)

        predicted = result.data.max(1)[1] # max() returns (values, indices)
        correct += (predicted == truth.data).sum()

    print('Accuracy of the network on test samples: %f %%' % (100 * float(correct) / len(test_mnist)))

for epoch in range(n_epochs):
    train()
    test()
