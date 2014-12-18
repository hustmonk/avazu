#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""
from config import *
__revision__ = '0.1'
import logging
import logging.config
logging.config.fileConfig("log.conf")
LOG_FILE = 'logtrain/mtst.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5)
logger = logging.getLogger("example")
logger.addHandler(handler)
fin = open("sub.csv")
head = fin.next()
loss = 0
fout = open("subx.csv", "w")
fout.write(head)
c = 0
class M1:
    def predict(self, arr):
        more = int(arr[2])
        if len(arr) < 5:
            return 0
        preds = [float(k)  for k in arr[3:]]

        preda = preds[0]
        return [preda]
        predm = preds[1]
        
        predl = preds[2]
        predc = predl
        if more:
            predc = predm
        predx = sum(sorted(preds[3:]))/(len(preds) - 3)
    
        pred = (preda + predm + predx) / 3
        return [preda, predm, pred, predc]

        pred = (predx + preda + predm + predl) / 4
        return [predx, preda, predm, predl, pred]

m1 = M1()
loss = [0] * 5
for line in fin:
    arr = line.strip().split(",")
    y = int(arr[1])
    preds = m1.predict(arr)
    for i in range(len(preds)):
        loss[i] += logloss(preds[i], y)
    c += 1
    fout.write("%s,%f\n" % (arr[0], preds[0]))
loss = ["%.4f" % (k/c) for k in loss]
fout.close()
logger.info("%s", ",".join(loss))
