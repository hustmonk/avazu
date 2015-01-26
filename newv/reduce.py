#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
def transfer(fin, fout, train):
    fout = open(fout, "w")
    line = "id,click,app,C0,C1,bs,ix,dn,cg,dd,dp,dl,de,dpe,C14,C15,C16,C17,C18,C19,C20,C21\n"
    newheads = line.strip().split(",")
    fout.write(line)
    start = 1
    if train:
        start = 2
    fin = open(fin)
    heads = fin.next().strip().split(",")
    for line in fin:
        arr = line.strip().split(",")
        id = arr[0]
        label = '0'
        arr[start] = arr[start][6:]
        if train and arr[1] == '1':
            label = '1'
        if arr[start + 3] == '85f751fd':
            newarr = [id, label, '1'] + arr[start:start+3] + arr[start+6:]
            """
            for i in range(len(arr)):
                print i, heads[i],arr[i]
            for i in range(len(newarr)):
                print i, newheads[i],newarr[i]
            break
            """
        else:
            newarr = [id, label, '0'] + arr[start:start+3] + arr[start+3:start+6]+ arr[start+9:]
        #if ()
        fout.write(",".join(newarr) +"\n")

#transfer("../data/train", "train", True)
transfer("../data/test", "test", False)
#transfer("../data/debug1029", "debug1029", True)
#transfer("../data/debug1030", "debug1030", True)
#transfer("../data/valid1029", "valid1029", True)
#transfer("../data/valid1030", "valid1030", True)
