#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""
import re

__revision__ = '0.1'
fin = open("../data/train")
head = fin.next().strip().split(",")
dict = {}
for k in head:
    dict[k] = {}
for line in open("../data/train"):
    arr = line.strip().split(",")
    for i in range(len(arr)):
        k = head[i]
        if len(dict[k]) > 1000000:
            continue
        dict[k][arr[i]] = 1

for k in dict:
    print k,len(dict[k])
