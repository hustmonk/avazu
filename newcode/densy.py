#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
class Denesy():
    def __init__(self):
        self.indexs = {}
        self.counts = {}
        k = {}
        """
        for line in open("../data/bias/sort.wy.IDX"):
            if len(k) > 1000:
                break
            arr = line.strip().split(" ")
            k[arr[0]+"_"+arr[1]] = 1
        """
        for line in open("../todensy/0"):
            arr = line.strip().split("\t")
            if arr[0] in k:
                print arr[0]
                continue
            self.counts[arr[0]] = int(arr[1])
            self.indexs[arr[0]] = len(self.indexs)

    def getNum(self, head, v):
        key = head + "_" + v
        c = self.counts.get(key, -1)
        #if c > 100:
        #    c = 101
        return c
