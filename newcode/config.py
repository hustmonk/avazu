#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'


import math
import sys
from math import exp, log, sqrt

# C, feature/hash trick
D = 2 ** 24             # number of weights to use
interaction = False     # whether to enable poly2 feature interactions

# D, training/validation
holdafter = 9   # data after date N (exclusive) are used as validation
holdout = None  # use every N training instance for holdout validation

def logloss(p, y):
        p = max(min(p, 1. - 10e-15), 10e-15)
        return -log(p) if y == 1. else -log(1. - p)
import logging
import logging.config
import sys
from datetime import datetime

logging.config.fileConfig("log.conf")
where=sys.argv[1]

TEST_MODE = 0
dir = "../newv/"
newstam = datetime.now().strftime('%d-%H-%M-%S')
if TEST_MODE:
    train = dir + 'train1028.rand'              # path to training file
    test1 = dir + 'valid1030'                 # path to testing file
    test2 = dir + 'valid1029'                # path to testing file
    LOG_FILE = 'logtrain/' + where + 'tst.log' + newstam
    epoch = 1       # learn training data for N passes
else:
    train = dir + 'train'              # path to training file

    test = dir + 'test'               # path to testing file
    LOG_FILE = 'logsub/tst.log' + newstam
    epoch = 3       # learn training data for N passes

handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5)
logger = logging.getLogger("example")
logger.addHandler(handler)
