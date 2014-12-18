#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
import logging
import logging.config
from datetime import datetime
from learner import *
from read import *
from valid import *
from ensemble import *

logging.config.fileConfig("log.conf")

TEST_MODE = 0
dir = "../data/"
newstam = datetime.now().strftime('%d-%H-%M-%S')
valid = Valid()
if TEST_MODE:
    train = dir + 'train1028.rand'              # path to training file
    test1 = dir + 'valid1030'                 # path to testing file
    test2 = dir + 'valid1029'                # path to testing file
    LOG_FILE = 'logtrain/tst.log' + newstam
    epoch = 1       # learn training data for N passes
else:
    train = dir + 'train'              # path to training file
    test = dir + 'test'               # path to testing file
    LOG_FILE = 'logsub/tst.log' + newstam
    epoch = 3       # learn training data for N passes

handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5)
logger = logging.getLogger("example")
logger.addHandler(handler)

# start training #############################################################
start = datetime.now()
# initialize ourselves a learner
learner = Ensemble()
# start training
for e in xrange(epoch):
    loss = 0.
    count = 0

    for t, date, ID, x, y in data(train, D, True):  # data is a generator
        
        p = learner.predict(x)
        learner.update(x, y)

        loss += logloss(p, y)
        count += 1

        if count % 200000 == 0:
            l1,l2,lx = 0,0,0
            if TEST_MODE:
                l1,l2,lx = valid.loss(learner)

            logger.info('Epoch %d finished[%d][%d], validation logloss: [%f], test : [%f][%f][%f], elapsed time: %s' % (e, count, date, loss/count, l1, l2, lx, str(datetime.now() - start)))
            # step 2-2, update learner with label (click) information

    logger.info('Epoch %d finished, validation logloss: %f, elapsed time: %s' % ( e, loss/count, str(datetime.now() - start)))


##############################################################################
# start testing, and build Kaggle's submission file ##########################
##############################################################################
def predictR(testfile, submission):
    loss = 0
    count = 1
    with open(submission, 'w') as outfile:
        outfile.write('id,click\n')
        for t, date, ID, x, y in data(testfile, D, False):
            ps = learner.valid(x)
            p = sum(ps)/len(ps)
            outfile.write('%s,%d,%d,%s,%s\n' % (ID, y, x.isMore, str(p), ",".join([str(i) for i in ps])))
            if TEST_MODE:
                loss += logloss(p, y)
                count += 1
                if count % 50000 == 0:
                    logger.info('validation[%s] logloss: %f, elapsed time: %s' % ( testfile, loss/count, str(datetime.now() - start)))
    logger.info('VVvalidation[%s] logloss: %f, elapsed time: %s' % ( testfile, loss/count, str(datetime.now() - start)))

learner.pr()
if TEST_MODE:
    predictR(test1, "sub1.csv")
    predictR(test2, "sub2.csv")
else:
    predictR(test, "sub.csv")
