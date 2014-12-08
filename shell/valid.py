#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""
from learner import *
from read import *

__revision__ = '0.1'

class Valid:
    def __init__(self, post):
        dir = "../data/"
        debug1 = dir + 'debug1030' + post
        debug2 = dir + 'debug1029' + post
        self.valid_test_2 = []
        for t, date, ID, x, y, weight in data(debug2, D, 100000):
            self.valid_test_2.append([x, y])

        self.valid_test_1 = []
        for t, date, ID, x, y, weight in data(debug1, D, 100000):
            self.valid_test_1.append([x, y])

    def _loss(self, learner, data):
        loss = 0
        for (x1, y1) in data:
            p1 = learner.predict(x1)
            loss += learner.logloss(p1, y1)
        return loss/len(data)

    def loss(self, learner):
        loss1 = self._loss(learner, self.valid_test_1)
        loss2 = self._loss(learner, self.valid_test_2)
        return loss1,loss2,(loss1+loss2)/2
