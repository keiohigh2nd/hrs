#!/usr/bin/env python
import argparse

import numpy as np
import six

import chainer
from chainer import computational_graph as c
from chainer import cuda
import chainer.functions as F
from chainer import optimizers



parser = argparse.ArgumentParser(description='HRS')
parser.add_argument('--gpu', '-g', default=-1, type=int,
                    help='GPU ID (negative value indicates CPU)')
args = parser.parse_args()
if args.gpu >= 0:
    cuda.check_cuda_available()
xp = cuda.cupy if args.gpu >= 0 else np

batchsize = 30
n_epoch = 20
n_units = 1000

# Prepare dataset
data = np.loadtxt("../input_data/data_for_program_bp_cre_basic_data.csv",delimiter=",").astype(np.float32)
target = np.loadtxt("../input_data/target_data_for_program_bp_cre_basic_data.csv",delimiter=",").astype(np.int32)

print data
print target

N = 400
x_train, x_test = np.split(data,   [N])
y_train, y_test = np.split(target, [N])
N_test = y_test.size

# Prepare multi-layer perceptron model
model = chainer.FunctionSet(l1=F.Linear(5, n_units),
                            l2=F.Linear(n_units, n_units),
                            l3=F.Linear(n_units, 2))
if args.gpu >= 0:
    cuda.get_device(args.gpu).use()
    model.to_gpu()


def forward(x_data, y_data, train=True):
    # Neural net architecture
    x, t = chainer.Variable(x_data), chainer.Variable(y_data)
    h1 = F.dropout(F.relu(model.l1(x)),  train=train)
    h2 = F.dropout(F.relu(model.l2(h1)), train=train)
    y = model.l3(h2)
    return F.softmax_cross_entropy(y, t), F.accuracy(y, t)


# Setup optimizer
optimizer = optimizers.Adam()
optimizer.setup(model)

# Learning loop
for epoch in six.moves.range(1, n_epoch + 1):
    print('epoch', epoch)

    # training
    perm = np.random.permutation(N)
    sum_accuracy = 0
    sum_loss = 0
    for i in six.moves.range(0, N, batchsize):
        x_batch = xp.asarray(x_train[perm[i:i + batchsize]])
        y_batch = xp.asarray(y_train[perm[i:i + batchsize]])

        optimizer.zero_grads()
        loss, acc = forward(x_batch, y_batch)
        loss.backward()
        optimizer.update()

        if epoch == 1 and i == 0:
            with open("graph.dot", "w") as o:
                o.write(c.build_computational_graph((loss, )).dump())
            with open("graph.wo_split.dot", "w") as o:
                g = c.build_computational_graph((loss, ),
                                                remove_split=True)
                o.write(g.dump())
            print('graph generated')

        sum_loss += float(loss.data) * len(y_batch)
        sum_accuracy += float(acc.data) * len(y_batch)

    print('train mean loss={}, accuracy={}'.format(
        sum_loss / N, sum_accuracy / N))

    # evaluation
    sum_accuracy = 0
    sum_loss = 0
    for i in six.moves.range(0, N_test, batchsize):
        x_batch = xp.asarray(x_test[i:i + batchsize])
        y_batch = xp.asarray(y_test[i:i + batchsize])

        loss, acc = forward(x_batch, y_batch, train=False)

        sum_loss += float(loss.data) * len(y_batch)
        sum_accuracy += float(acc.data) * len(y_batch)

    print('test  mean loss={}, accuracy={}'.format(
        sum_loss / N_test, sum_accuracy / N_test))
