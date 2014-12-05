#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
class Denesy():
    def __init__(self):
        self.dict = {}
        for line in open("../todensy/0"):
            arr = line.strip().split("\t")
            self.dict[arr[0]] = int(arr[1])

    def getNum(self, head, v):
        key = head + "_" + v
        c = self.dict.get(key, 1)
        if c > 100:
            c = 101
        return c
