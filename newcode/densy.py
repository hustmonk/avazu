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
        for line in open("../todensy/0"):
            arr = line.strip().split("\t")
            self.counts[arr[0]] = int(arr[1])
            self.indexs[arr[0]] = len(self.indexs)

    def getNum(self, head, v):
        key = head + "_" + v
        c = self.counts.get(key, -1)
        #if c > 100:
        #    c = 101
        return c
