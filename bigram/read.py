#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
from config import *
from csv import DictReader
from math import exp, log, sqrt
import math
import sys
from densy import *
import random

denesy = Denesy()
dropout = 0.9
def getBiFeature(key, cckey):
    if cckey < 1000:
        return key
    else:
        return str(cckey)

class Feature:
    def __init__(self, row):
        self.data = [0]
        quKey = sys.argv[1]
        cckey = denesy.getNum(quKey, row[quKey])

        quKey2 = sys.argv[2]
        apkey = denesy.getNum(quKey2, row[quKey2])
        xy = getBiFeature(quKey, cckey) + getBiFeature(quKey2, apkey)
        #xy = getBiFeature(quKey, cckey)
        self.dayIndex = int(row['hour'][4:6])-21
        row['hour'] = row['hour'][6:]
        for (key,value) in row.items():
            # one-hot encode everything with hash trick
            if key[0] != 'C' and denesy.getNum(key, value) < 10:
                index = abs(hash(xy + key)) % D
            else:
                index = abs(hash(xy + "_" + key + '_' + value)) % D
            self.data.append(index)
        if cckey < 0:
            cckey = -cckey
        if cckey < 100:
            self.isMore = False
        else:
            self.isMore = True
        self.weight = math.sqrt(1.0 / cckey)

import random
def data(path, D, train):
    cc = 0
    dropout = 0.6
    for t, row in enumerate(DictReader(open(path))):
        cc += 1
        # process id
        ID = row['id']
        del row['id']

        # process clicks
        y = 0.
        if 'click' in row:
            if row['click'] == '1':
                y = 1.
            """
            else:
                if train and random.random() > dropout:
                    continue
            """
            del row['click']

        # extract date

        date = int(row['hour'][4:6])
        x = Feature(row)
        yield t, date, ID, x, y
