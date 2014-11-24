#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

import logging
import logging.config
from datetime import datetime

logging.config.fileConfig("log.conf")

newstam = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
logger = logging.getLogger("example")

from math import exp, log, sqrt
__revision__ = '0.1'
def loss(p, y):
    p = max(min(p, 1. - 10e-15), 10e-15)
    return -log(p) if y == 1. else -log(1. - p)
ys = []
for line in open("y"):
    ys.append(int(line.strip()))
preds = []
for line in open("rotten.rawpreds.txt"):
    pred = line.strip().split(" ")[0]
    if float(pred) < -3:
        pred = 0
    else:
        pred = 1. / (1. + exp(-max(min(float(pred), 35.), -35.)))
    preds.append(pred)
loss_sum = 0
for i in range(len(ys)):
    ls = loss(preds[i], ys[i])
    loss_sum += ls
logger.info(loss_sum / len(ys))
