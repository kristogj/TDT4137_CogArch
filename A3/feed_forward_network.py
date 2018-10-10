from pybrain.datasets.supervised import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import TanhLayer
from pybrain.supervised.trainers import BackpropTrainer

# Make the DataSet
ds = SupervisedDataSet(1,1)  # Input and output is in one dimension
for x in range(1,9):
    ds.addSample(x,x)

# Build the network with 1 input, 8 hidden and 1 output
net = buildNetwork(1,8,1, hiddenclass=TanhLayer)


# Train the network
trainer = BackpropTrainer(net, ds)
trainer.trainUntilConvergence(verbose=False, validationProportion=0.15, maxEpochs=1000, continueEpochs=10)

# Activate, try changing the number of hidden nodes, and see the result being worse and worse
for x in range(1,9):
    print(net.activate([x]))




