#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'

#fin = open("../data/valid1030")
fin = open("../data/valid1030")
head = fin.next().strip().split(",")
dict = {}
idx = 0
for line in fin:
    arr = line.strip().split(",")
    for i in range(2, len(arr)):
        if head[i][:6] != "device":
            continue
        key = head[i] +"_"+ arr[i]
        if key not in dict:
            dict[key] = 1
        else:
            dict[key] = dict.get(key, 0) + 1

fin.close()
fout = open("train.reducex", "w")
fin = open("../data/train1029.rand")
head = fin.next()
fout.write(head)
head = head.strip().split(",")
for line in fin:
    arr = line.strip().split(",")
    delete = 0
    for i in range(3, len(arr)):
        if head[i][:6] != "device":
            continue
        key = head[i] +"_"+ arr[i]
        if key not in dict:
            delete += 1
    if delete > 0:
        fout.write(line)
fout.close()
