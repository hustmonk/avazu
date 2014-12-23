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
    if cckey < 300:
        return key
    else:
        return str(cckey)

class Feature:
    def __init__(self, row):
        self.data = [0]
        quKey = sys.argv[1]
        cckey = denesy.getNum(quKey, row[quKey])
        xy = getBiFeature(quKey, cckey)
        self.dayIndex = int(row['hour'][4:6])-21
        row['hour'] = row['hour'][6:]
        for (key,value) in row.items():
            # one-hot encode everything with hash trick
            if denesy.getNum(key, value) < 10:
                index = abs(hash(xy + key)) % D
            else:
                index = abs(hash(xy + "_" + key + '_' + value)) % D
            self.data.append(index)
        if cckey < 0:
            cckey = -cckey
        if cckey < 10:
            self.isMore = False
        else:
            self.isMore = True
        self.weight = math.sqrt(1.0 / cckey)

def data(path, D, train):
    cc = 0
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
            del row['click']

        # extract date

        date = int(row['hour'][4:6])
        x = Feature(row)
        yield t, date, ID, x, y
