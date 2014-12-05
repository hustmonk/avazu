#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
for line in open("0"):
    arr = line.strip().split("\t")
    if int(arr[1]) < 10:
        continue
    print line.strip()
