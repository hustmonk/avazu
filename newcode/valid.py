#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""
from read import *
from config import *

__revision__ = '0.1'

class Valid:
    def __init__(self):
        dir = "../newv/"
        debug1 = dir + 'debug1030'
        debug2 = dir + 'debug1029'
        self.valid_test_2 = []
        for t, date, ID, x, y in data(debug2, D, False):
            self.valid_test_2.append([x, y])

        self.valid_test_1 = []
        for t, date, ID, x, y in data(debug1, D, False):
            self.valid_test_1.append([x, y])

    def _loss(self, learner, data):
        loss = 0
        learner.printr()
        for (x1, y1) in data:
            p1 = learner.valid(x1)
            loss += logloss(sum(p1)/len(p1), y1)
        return loss/len(data)

    def loss(self, learner):
        loss1 = self._loss(learner, self.valid_test_1)
        loss2 = self._loss(learner, self.valid_test_2)
        return loss1,loss2,(loss1+loss2)/2
