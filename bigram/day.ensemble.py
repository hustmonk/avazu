#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'

from learner import *

class Ensemble():

    def __init__(self):
        argv = [alpha, beta, L1, L2, D, interaction]
        self.learnAll = ftrl_proximal(argv)
        self.learnMore = ftrl_proximal(argv)
        self.learnLess = ftrl_proximal(argv)
        self.learns = []
        for i in range(10):
            learn = ftrl_proximal(argv)
            self.learns.append(learn)

    def getLearn(self, x):
        if x.isMore:
            return self.learnMore
        else:
            return self.learnLess

    def predict(self, x):
        self.p1 = self.learnAll.predict(x.data)
        learn = self.getLearn(x)
        self.p2 = learn.predict(x.data)
        self.p3 = self.learns[x.dayIndex].predict(x.data)
        return (self.p1 + self.p2 + self.p3) / 3

    def update(self, x, y):
        self.learnAll.update(x.data, self.p1, y, x.weight)
        learn = self.getLearn(x)
        learn.update(x.data, self.p2, y, x.weight)
        self.learns[x.dayIndex].update(x.data, self.p3, y, x.weight)

    def valid(self, x):
        ps = []
        if self.learnAll.start:
            ps.append(self.learnAll.predict(x.data))
        if self.learnMore.start:
            ps.append(self.learnMore.predict(x.data))
        if self.learnLess.start:
            ps.append(self.learnLess.predict(x.data))
        for i in range(10):
            if self.learns[i].start:
                ps.append(self.learns[i].predict(x.data))
        return ps

    def pr(self):
        self.learnAll.pr()
        self.learnMore.pr()
        self.learnLess.pr()
        for i in range(10):
            self.learns[i].pr()
