#!/bin/usr/env python
#_*_ coding:utf-8 _*_ 

import os 

def disk(path):
    try:
        disk=os.statvfs(path)
    except:
        return {'total':'','used':''}
    diskUsed=(disk.f_blocks - disk.f_bfree) * disk.f_bsize
    diskTotal=disk.f_blocks * disk.f_bsize
    #diskUsage=float(diskUsed)/float(diskTotal) * 100
    return {'total':round(float(diskTotal)/1024/1000/1000,2),'used':round(float(diskUsed)/1024/1000/1000,2)}

