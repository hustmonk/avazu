#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
from densy import *
densy = Denesy()
class SplitType:
    def __init__(self):
        self.D = 2 ** 30             # number of weights to use
        self.count = {}

        self.le10 = {}
        self.le100 = {}
        self.le10000 = {}
        self.mo10000 = {}
        for line in open("x.type"):
            arr = line.strip().split(" ")
            count = int(arr[1])
            self.count[arr[0]] = count

    def set_head(self, head):
        self.head = head
        for i in range(len(head)):
            key = head[i]
            if key not in self.count:
                continue
            count = self.count[key]
            if count < 10:
                self.le10[i] = 1
            elif count < 100:
                self.le100[i] = 1
            elif count < 10000:
                self.le10000[i] = 1
            else:
                self.mo10000[i] = 1

    def _feature(self, dict, info):
        buff = []
        for k in dict:
            k = densy.getNum(self.head[k], info[k])
            if k < 0:
                continue
            buff.append("%d" % k)
        return " ".join(buff)

    def get_feature(self, info):
        a = self._feature(self.le10, info)
        b = self._feature(self.le100, info)
        c = self._feature(self.le10000, info)
        d = self._feature(self.mo10000, info)
        return "a %s |b %s |c %s |d %s" % (a, b, c, d)

def write(fin, fout):
    split_type = SplitType()
    fin = open(fin)
    head = fin.next().strip().split(",")
    split_type.set_head(head)

    fout = open(fout, "w")
    for line in fin:
        arr = line.strip().split(",")
        feature = split_type.get_feature(arr)
        label = "-1"
        if head[1] == "click":
            label = arr[1]
            if label == "0":
                label = "-1"
        fout.write("%s %s|%s\n" % (label, arr[0], feature))
    fout.close()

write("../data/train1028.rand", "train.csv")
write("../data/valid1029", "test.csv.29")
write("../data/valid1030", "test.csv")
    
