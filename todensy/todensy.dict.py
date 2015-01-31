#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'

def write(dict, idx):
    fout = open(str(idx), "w")
    for (k,v) in dict.items():
        if v < 5:
            continue
        fout.write("%s\t%d\n" % (k,v))
    fout.close()
    
#fin = open("../data/valid1030")
dict = {}
idx = 0
def read(filename, start):
    global dict
    global idx
    fin = open(filename)
    head = fin.next().strip().split(",")
    for line in fin:
        arr = line.strip().split(",")
        for i in range(start, len(arr)):
            key = head[i] +"_"+ arr[i]
            key = arr[i] + "_" + head[i]
            if key not in dict:
                dict[key] = 1
                if len(dict) > 20000000:
                    write(dict, idx)
                    idx = idx + 1
                    dict = {}
            else:
                dict[key] = dict.get(key, 0) + 1

read("../data/train", 2)
read("../data/test", 1)
write(dict, idx)
