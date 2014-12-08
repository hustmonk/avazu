#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
import logging
import logging.config
from datetime import datetime
import math
from math import exp, log, sqrt
from learner import *
from read import *
from valid import *

logging.config.fileConfig("log.conf")

TEST_MODE = 1
dir = "../data/"
post = ".less3"
newstam = datetime.now().strftime('%d-%H-%M-%S')
valid = Valid(post)
if TEST_MODE:
    train = dir + 'train1028.rand' + ".less3"              # path to training file
    test1 = dir + 'valid1030' + post                 # path to testing file
    test2 = dir + 'valid1029' + post                 # path to testing file
    LOG_FILE = 'dlog/tst.log' + newstam
    epoch = 1       # learn training data for N passes
else:
    train = dir + 'train'              # path to training file
    test = dir + 'test' + post               # path to testing file
    LOG_FILE = 'log/tst.log' + newstam
    epoch = 3       # learn training data for N passes

submission = 'submission1234.csv' + post  # path of to be outputted submission file
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5)
logger = logging.getLogger("example")
logger.addHandler(handler)


# start training #############################################################
start = datetime.now()
# initialize ourselves a learner
learner = ftrl_proximal(alpha, beta, L1, L2, D, interaction)
# start training
for e in xrange(epoch):
    loss = 0.
    count = 0

    for t, date, ID, x, y, weight in data(train, D):  # data is a generator
        p = learner.predict(x)
        learner.update(x, p, y, weight)

        if (holdafter and date > holdafter) or (holdout and t % holdout == 0):
            loss += learner.logloss(p, y)
            count += 1
            if count % 50000 == 0:
                l1,l2,lx = 0,0,0
                if TEST_MODE:
                    l1,l2,lx = valid.loss(learner)

                logger.info('Epoch %d finished[%d][%d], validation logloss: [%f], test : [%f][%f][%f], elapsed time: %s' % (e, count, date, loss/count, l1, l2, lx, str(datetime.now() - start)))
                break
            # step 2-2, update learner with label (click) information

    logger.info('Epoch %d finished, validation logloss: %f, elapsed time: %s' % ( e, loss/count, str(datetime.now() - start)))


##############################################################################
# start testing, and build Kaggle's submission file ##########################
##############################################################################
def predictR(testfile):
    loss = 0
    count = 0
    with open(submission, 'w') as outfile:
        outfile.write('id,click\n')
        for t, date, ID, x, y, weight in data(testfile, D):
            p = learner.predict(x)
            outfile.write('%s,%s\n' % (ID, str(p)))
            if TEST_MODE:
                loss += learner.logloss(p, y)
                count += 1
                if count % 50000 == 0:
                    logger.info('validation[%s] logloss: %f, elapsed time: %s' % ( testfile, loss/count, str(datetime.now() - start)))

if TEST_MODE:
    predictR(test1)
    predictR(test2)
else:
    predictR(test)
