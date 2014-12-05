#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'

dict1 = {}
dict0 = {}
for line in open("train"):
    arr = line[:50].strip().split(",")
    time = arr[2]
    label = arr[1]

    if label == "0":
        dict0[time] = dict0.get(time, 0) + 1
    else:
        dict1[time] = dict1.get(time, 0) + 1

for k in dict0:
    v0 = dict0[k]
    v1 = dict1[k]
    print k[4:6],k[6:], v0, v1, 1000*v1/(v0+v1)
