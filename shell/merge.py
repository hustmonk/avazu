#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'

rdict = {}
def read(filename):
    for line in open(filename):
        arr = line.strip().split(",")
        rdict[arr[0]] = arr[1]

read("submission1234.csv.less3")
read("submission1234.csv.more3")

for line in open("submission1234.csv"):
    arr = line.strip().split(",")
    print "%s,%s" % (arr[0],rdict[arr[0]])
