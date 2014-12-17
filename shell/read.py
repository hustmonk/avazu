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
from densy import *
import random

denesy = Denesy()
dropout = 0.9
def getXY(row):
    key = "site_category"
    value = row[key]
    if denesy.getNum(key, value) < 300:
        return key
    else:
        return value
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

        # turn hour really into hour, it was originally YYMMDDHH
        row['hour'] = row['hour'][6:]

        # build x
        x = []
        weight = math.sqrt(1.0 / denesy.getNum("device_ip", row["device_ip"]))
        del row['hour']
        del row["device_ip"]
        del row["device_id"]
        C16 = row["C16"]
        if denesy.getNum("C16", C16) < 1000:
            C16 = "CCCY"
        xy = getXY(row)
        for key in row:
            value = row[key]

            # one-hot encode everything with hash trick
            index = abs(hash(xy + "_" + key + '_' + value)) % D
            x.append(index)
            """
            index = abs(hash(C16 + "_" + key + '_' + value)) % D
            x.append(index)
            """
            """
            if key == "device_ip" or key == "device_id":
                v = denesy.getNum(key, value)
                index = abs(hash(key + 'X_' + str(v))) % D
                x.append(index)
            """
        """
        ip_num = denesy.getNum("device_ip", row["device_ip"])
        id_num = denesy.getNum("device_id", row["device_id"])
        other = 1
        if ip_num > 5 and id_num > 5:
            other = abs(hash(row["device_ip"] + row["device_id"])) % D
        x.append(other)
        """
        #weight = 1
        yield t, date, ID, x, y, weight
