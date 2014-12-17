#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
fouts = []
import random
for i in range(10):
    fout = open("bak/"+str(i), "w")
    fouts.append(fout)
count = 0
fin = open("train")
fin.next()
for line in fin:
    fouts[count%10].write(line)
    count += 1

for i in range(10):
    fouts[i].close()
for i in range(10):
    fin = open("bak/"+str(i))
    arr = []
    for line in fin:
        arr.append(line)
    fout = open("bak/"+str(i)+".rand", "w")
    idx = range(len(arr))
    random.shuffle(idx)
    for k in idx:
        fout.write(arr[k])
