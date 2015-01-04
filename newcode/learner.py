#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""
from config import *
from math import exp, log, sqrt
import random
__revision__ = '0.1'
# B, model
alpha = .1  # learning rate
beta = 1.   # smoothing parameter for adaptive learning rate
L1 = 1.     # L1 regularization, larger value means more regularized
L2 = 1.     # L2 regularization, larger value means more regularized

class ftrl_proximal(object):
    ''' Our main algorithm: Follow the regularized leader - proximal

        In short,
        this is an adaptive-learning-rate sparse logistic-regression with
        efficient L1-L2-regularization

        Reference:
        http://www.eecs.tufts.edu/~dsculley/papers/ad-click-prediction.pdf
    '''

    def __init__(self, argv, more):
        # parameters
        self.count = 0
        alpha, beta, L1, L2, D, interaction = argv
        self.alpha = alpha
        self.beta = beta
        self.L1 = L1
        self.L2 = L2
        self.start = False
        self.more = more
        """
        if more == False:
            self.L1 = self.L1 / 2.0
        """

        # feature related parameters
        self.D = D
        self.interaction = interaction

        # model
        # n: squared sum of past gradients
        # z: weights
        # w: lazy weights
        self.n = [0.] * D
        self.z = [0.] * D
        self.w = []

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
        w = [0] * len(x)

        # wTx is the inner product of w and x
        wTx = 0.
        for idx in range(len(x)):
            i = x[idx]
            sign = -1. if z[i] < 0 else 1.  # get sign of z[i]

            # build w on the fly using z and n, hence the name - lazy weights
            # we are doing this at prediction instead of update time is because
            # this allows us for not storing the complete w
            wi = 0
            if sign * z[i] > L1:
                # apply prediction time L1, L2 regularization to z and get w
                wi = (sign * L1 - z[i]) / ((beta + sqrt(n[i])) / alpha + L2)

            wTx += wi
            w[idx] = [i, wi]

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
        if self.more:
            weight = 1
        if weight < 0.01:
            weight = 0.01
        self.count += 1

        # parameter
        self.start = True
        alpha = self.alpha

        # model
        n = self.n
        z = self.z
        w = self.w

        # gradient under logloss
        g = p - y
        dropout = 0.6
        ws = 1
        """
        if y == 0:
            ws = 1 / dropout
        """

        # update z and n
        for (i, wi) in w:
            """
            if random.random() > dropout:
                continue
            """
            sigma = (sqrt(n[i] + g * g) - sqrt(n[i])) / alpha
            z[i] += (g - sigma * wi) * weight * ws
            n[i] += (g * g) * weight * ws

    def pr(self):
        print self.count

    def printr(self):
        k = 0
        for i in self.z:
            if i > 1 or i < -1:
                k += 1
        return k
