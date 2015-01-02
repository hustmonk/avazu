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
files = ["sub.csvapp_id", "sub.csvsite_id", "sub.csvC1", "sub.csvbanner_pos"]
files = ["sub.csvapp_id", "sub.csvsite_id", "sub.csvbanner_pos"]
fins = []
for f in files:
    fin = open(f)
    head = fin.next()
    fins.append(fin)
loss = 0
fout = open("subx.csv", "w")
fout.write(head)
import math
for line in fins[0]:
    arr = line.strip().split(",")
    y = int(arr[1])
    weights = 2
    pred = float(arr[3]) * float(arr[3])
    for i in range(1, len(fins)):
        fin = fins[i]
        arr = fin.next().strip().split(",")
        if i == 1:
            pred = pred * float(arr[3]) * float(arr[3])
        else:
            pred = pred * float(arr[3])
    pred = math.pow(pred, 1.0/5)
    fout.write("%s,%f\n" % (arr[0], pred))
fout.close()
