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
fin1 = open("0.39209.site")
fin2 = open("0.3920695")
head = fin1.next()
head = fin2.next()
loss = 0
fout = open("subx.csv", "w")
fout.write(head)
import math
for line in fin1:
    arr2 = fin2.next().strip().split(",")
    arr = line.strip().split(",")
    y = int(arr[1])
    pred = (float(arr[3]) + float(arr2[3]))/2
    pred = math.sqrt(float(arr[3]) * float(arr2[3]))
    fout.write("%s,%f\n" % (arr[0], pred))
fout.close()
