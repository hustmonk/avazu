#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'

from config import *
from learner import *
from read import *
from valid import *
from ensemble import *

valid = Valid()
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

            logger.info('[%s] Epoch %d finished[%d][%d], validation logloss: [%f], test : [%f][%f][%f], elapsed time: %s' % (where, e, count, date, loss/count, l1, l2, lx, str(datetime.now() - start)))
            # step 2-2, update learner with label (click) information
            learner.pr()

    logger.info('[%s] Epoch %d finished, validation logloss: %f, elapsed time: %s' % (where, e, loss/count, str(datetime.now() - start)))


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
                    logger.info('[%s]validation[%s] logloss: %f, elapsed time: %s' % (where, testfile, loss/count, str(datetime.now() - start)))

        learner.pr()
    logger.info('[%s]VVvalidation[%s] logloss: %f, elapsed time: %s' % (where, testfile, loss/count, str(datetime.now() - start)))

learner.pr()
if TEST_MODE:
    predictR(test1, "sub1.csv")
    predictR(test2, "sub2.csv")
else:
    predictR(test, "sub.csv")
