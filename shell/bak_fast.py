#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
import logging
import logging.config
import math
from datetime import datetime
from densy import *

logging.config.fileConfig("log.conf")
denesy = Denesy()

newstam = datetime.now().strftime('%d-%H-%M-%S')
LOG_FILE = 'log/tst.log' + newstam
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5)
logger = logging.getLogger("example")
logger.addHandler(handler)

'''
           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                   Version 2, December 2004

Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

Everyone is permitted to copy and distribute verbatim or modified
copies of this license document, and changing it is allowed as long
as the name is changed.

           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
  TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

 0. You just DO WHAT THE FUCK YOU WANT TO.
'''


from csv import DictReader
from math import exp, log, sqrt


# TL; DR, the main training process starts on line: 250,
# you may want to start reading the code from there


##############################################################################
# parameters #################################################################
##############################################################################

# A, paths
TEST_MODE = 0
dir = "../data/"
post = ".less3"
if TEST_MODE:
    post = ".less3"
    train = dir + 'train1029.rand' + ".less3"              # path to training file
    test = dir + 'valid1030' + post                 # path to testing file
    debug = dir + 'debug' + post
else:
    train = dir + 'train'              # path to training file
    test = dir + 'test' + post               # path to testing file
    debug = dir + 'debug' + post
submission = 'submission1234.csv' + post  # path of to be outputted submission file

# B, model
alpha = .1  # learning rate
beta = 1.   # smoothing parameter for adaptive learning rate
L1 = 1.     # L1 regularization, larger value means more regularized
L2 = 1.     # L2 regularization, larger value means more regularized

# C, feature/hash trick
D = 2 ** 24             # number of weights to use
interaction = False     # whether to enable poly2 feature interactions

# D, training/validation
epoch = 3       # learn training data for N passes
holdafter = 9   # data after date N (exclusive) are used as validation
holdout = None  # use every N training instance for holdout validation


##############################################################################
# class, function, generator definitions #####################################
##############################################################################

class ftrl_proximal(object):
    ''' Our main algorithm: Follow the regularized leader - proximal

        In short,
        this is an adaptive-learning-rate sparse logistic-regression with
        efficient L1-L2-regularization

        Reference:
        http://www.eecs.tufts.edu/~dsculley/papers/ad-click-prediction.pdf
    '''

    def __init__(self, alpha, beta, L1, L2, D, interaction):
        # parameters
        self.alpha = alpha
        self.beta = beta
        self.L1 = L1
        self.L2 = L2

        # feature related parameters
        self.D = D
        self.interaction = interaction

        # model
        # n: squared sum of past gradients
        # z: weights
        # w: lazy weights
        self.n = [0.] * D
        self.z = [0.] * D
        self.c = [0.] * D
        self.w = {}

    def _indices(self, x):
        ''' A helper generator that yields the indices in x

            The purpose of this generator is to make the following
            code a bit cleaner when doing feature interaction.
        '''

        # first yield index of the bias term
        yield 0

        # then yield the normal indices
        for index in x:
            yield index

        # now yield interactions (if applicable)
        if self.interaction:
            D = self.D
            L = len(x)

            x = sorted(x)
            for i in xrange(L):
                for j in xrange(i+1, L):
                    # one-hot encode interactions with hash trick
                    yield abs(hash(str(x[i]) + '_' + str(x[j]))) % D

    def predict(self, x):
        ''' Get probability estimation on x

            INPUT:
                x: features

            OUTPUT:
                probability of p(y = 1 | x; w)
        '''

        # parameters
        alpha = self.alpha
        beta = self.beta
        L1 = self.L1
        L2 = self.L2

        # model
        n = self.n
        z = self.z
        w = {}

        # wTx is the inner product of w and x
        wTx = 0.
        for i in self._indices(x):
            sign = -1. if z[i] < 0 else 1.  # get sign of z[i]

            # build w on the fly using z and n, hence the name - lazy weights
            # we are doing this at prediction instead of update time is because
            # this allows us for not storing the complete w
            if sign * z[i] <= L1:
                # w[i] vanishes due to L1 regularization
                w[i] = 0.
            else:
                # apply prediction time L1, L2 regularization to z and get w
                w[i] = (sign * L1 - z[i]) / ((beta + sqrt(n[i])) / alpha + L2)

            wTx += w[i]

        # cache the current w for update stage
        self.w = w

        # bounded sigmoid function, this is the probability estimation
        return 1. / (1. + exp(-max(min(wTx, 35.), -35.)))

    def update(self, x, p, y, weight):
        ''' Update model using x, p, y

            INPUT:
                x: feature, a list of indices
                p: click probability prediction of our model
                y: answer

            MODIFIES:
                self.n: increase by squared gradient
                self.z: weights
        '''

        # parameter
        alpha = self.alpha

        # model
        n = self.n
        z = self.z
        w = self.w

        # gradient under logloss
        g = p - y

        # update z and n
        for i in self._indices(x):
            self.c[i] += 1
            sigma = (sqrt(n[i] + g * g) - sqrt(n[i])) / alpha
            z[i] += (g - sigma * w[i]) * weight
            n[i] += (g * g) * weight

    def printc(self):
        for i in self._indices(x):
            if self.c[i] > 100:
                print i


def logloss(p, y):
    ''' FUNCTION: Bounded logloss

        INPUT:
            p: our prediction
            y: real answer

        OUTPUT:
            logarithmic loss of p given y
    '''

    p = max(min(p, 1. - 10e-15), 10e-15)
    return -log(p) if y == 1. else -log(1. - p)


def data(path, D, Limit = 10000000000):
    ''' GENERATOR: Apply hash-trick to the original csv row
                   and for simplicity, we one-hot-encode everything

        INPUT:
            path: path to training or testing file
            D: the max index that we can hash to

        YIELDS:
            ID: id of the instance, mainly useless
            x: a list of hashed and one-hot-encoded 'indices'
               we only need the index since all values are either 0 or 1
            y: y = 1 if we have a click, else we have y = 0
    '''
    cc = 0
    for t, row in enumerate(DictReader(open(path))):
        cc += 1
        if cc > Limit:
            break
        # process id
        ID = row['id']
        del row['id']

        # process clicks
        y = 0.
        if 'click' in row:
            if row['click'] == '1':
                y = 1.
            del row['click']

        # extract date
        date = int(row['hour'][4:6])

        # turn hour really into hour, it was originally YYMMDDHH
        row['hour'] = row['hour'][6:]

        # build x
        x = []
        weight = math.sqrt(1.0 / denesy.getNum("device_ip", row["device_ip"]))
        del row['hour']
        del row["device_ip"]
        del row["device_id"]
        for key in row:
            value = row[key]

            # one-hot encode everything with hash trick
            index = abs(hash(key + '_' + value)) % D
            x.append(index)
            """
            if key == "device_ip" or key == "device_id":
                v = denesy.getNum(key, value)
                index = abs(hash(key + 'X_' + str(v))) % D
                x.append(index)
            """
        """
        ip_num = denesy.getNum("device_ip", row["device_ip"])
        id_num = denesy.getNum("device_id", row["device_id"])
        other = 1
        if ip_num > 5 and id_num > 5:
            other = abs(hash(row["device_ip"] + row["device_id"])) % D
        x.append(other)
        """
        #weight = 1
        yield t, date, ID, x, y, weight


##############################################################################
# start training #############################################################
##############################################################################

start = datetime.now()

# initialize ourselves a learner
learner = ftrl_proximal(alpha, beta, L1, L2, D, interaction)
valid_test = []
for t, date, ID, x, y, weight in data(debug, D, 100000):
    valid_test.append([x, y])


# start training
for e in xrange(epoch):
    loss = 0.
    count = 0

    for t, date, ID, x, y, weight in data(train, D):  # data is a generator
        #    t: just a instance counter
        # date: you know what this is
        #   ID: id provided in original data
        #    x: features
        #    y: label (click)

        # step 1, get prediction from learner
        p = learner.predict(x)
        learner.update(x, p, y, weight)

        if (holdafter and date > holdafter) or (holdout and t % holdout == 0):
            # step 2-1, calculate validation loss
            #           we do not train with the validation data so that our
            #           validation loss is an accurate estimation
            #
            # holdafter: train instances from day 1 to day N
            #            validate with instances from day N + 1 and after
            #
            # holdout: validate with every N instance, train with others
            loss += logloss(p, y)
            count += 1
            if count % 50000 == 0:
                loss1 = 0
                if TEST_MODE:
                    for (x1, y1) in valid_test:
                        p1 = learner.predict(x1)
                        loss1 += logloss(p1, y1)

                logger.info('Epoch %d finished[%d][%d], validation logloss: %f, test : %f, elapsed time: %s' % (e, count, date, loss/count, loss1/len(valid_test), str(datetime.now() - start)))
            # step 2-2, update learner with label (click) information

    logger.info('Epoch %d finished, validation logloss: %f, elapsed time: %s' % ( e, loss/count, str(datetime.now() - start)))


##############################################################################
# start testing, and build Kaggle's submission file ##########################
##############################################################################
loss = 0
count = 0
with open(submission, 'w') as outfile:
    outfile.write('id,click\n')
    for t, date, ID, x, y, weight in data(test, D):
        p = learner.predict(x)
        outfile.write('%s,%s\n' % (ID, str(p)))
        if TEST_MODE:
            loss += logloss(p, y)
            count += 1
            if count % 50000 == 0:
                logger.info('Epoch %d finished, validation logloss: %f, elapsed time: %s' % ( e, loss/count, str(datetime.now() - start)))