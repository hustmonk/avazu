#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'

key_idx = {}
for line in open("../todensy/0"):
    key,value = line.strip().split("\t")
    key_idx[key] = int(value)

def write(fin_name):
    fin = open(fin_name)
    head_line = fin.next().strip()
    head = head_line.split(",")
    device_ip_idx = 0
    for i in range(len(head)):
        if head[i] == "device_ip":
            device_ip_idx = i
            break
    foutless3 = open(fin_name+".less3", "w")
    foutmore3 = open(fin_name+".more3", "w")
    foutless3.write(head_line+"\n")
    foutmore3.write(head_line+"\n")

    for line in fin:
        arr = line.strip().split(",")
        key = "device_ip_" + arr[device_ip_idx]
        if key_idx[key] > 10:
            foutmore3.write(line)
        else:
            foutless3.write(line)
    foutless3.close()
    foutmore3.close()
write("../data/train1029.rand")
write("train1028.rand")
#write("../data/valid1030")
#write("train")
#write("test")
