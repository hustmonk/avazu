#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""
import math
__revision__ = '0.1'

print "Id,Predicted"
dict = {}

def zygmoid(x):
    return 1 / (1 + math.exp(-x))
for line in open("rotten.rawpreds.txt"):
    pred,id = line.strip().split("_")[0].split(" ")
    print "%s,%s" % (id, zygmoid(float(pred)))
