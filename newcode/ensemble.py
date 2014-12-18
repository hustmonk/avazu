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
        self.learnMore = ftrl_proximal(argv, True)
        self.learnLess = ftrl_proximal(argv, False)

    def predict(self, x):
        self.p1 = self.learnMore.predict(x.data)
        self.p2 = self.learnLess.predict(x.data)
        if x.isMore:
            return self.p1
        else:
            return self.p2

    def update(self, x, y):
        self.learnMore.update(x.data, self.p1, y, x.weight)
        self.learnLess.update(x.data, self.p2, y, x.weight)

    def valid(self, x):
        if x.isMore:
            return [self.learnMore.predict(x.data)]
        else:
            return [self.learnLess.predict(x.data)]

    def pr(self):
        self.learnMore.pr()
        self.learnLess.pr()
