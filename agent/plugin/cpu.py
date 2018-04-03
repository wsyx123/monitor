#!/usr/bin/env python
#_*_ coding:utf-8 _*_

'''
cat /proc/stat  
total     user    nice system  idle      iowait irq  softirq  steal guest  guest_nice
cpu       46612   38   16901   4975005   22939   2   1615      0     0      0

1jiffies=0.01秒

计算总的Cpu时间片totalCpuTime
         把所有cpu使用情况求和，得到total;

计算总的繁忙时间
         用total-idle,得到 usage

cpu 使用率
         (usage2-usage1)/(total2-total1)
'''
from time import sleep

def _read_cpu_time():
    with open("/proc/stat", 'r') as fd:
        lines = fd.readlines()  
    for line in lines:
        ln = line.split()
        if len(ln) < 5:
            continue
        if ln[0].startswith('cpu'):
            return ln
    return []

def _get_cpu_total_time():
    total_time_list = _read_cpu_time()
    if not total_time_list:
        return 0
    total_time_long = long(total_time_list[1])+long(total_time_list[2])+long(total_time_list[3])+\
            long(total_time_list[4])+long(total_time_list[5])+long(total_time_list[6])+long(total_time_list[7])
    return total_time_long

def _get_cpu_usage_time():
    usage_time_list = _read_cpu_time()
    if not usage_time_list:
        return 0
    usage_time_long = long(usage_time_list[1])+long(usage_time_list[2])+long(usage_time_list[3])+\
            long(usage_time_list[5])+long(usage_time_list[6])+long(usage_time_list[7])
    return usage_time_long

def _get_iowait_time():
    iowait_time_list = _read_cpu_time()
    if not iowait_time_list:
        return 0
    iowait_time_long = long(iowait_time_list[5])
    return iowait_time_long

def usage():
    total1 = _get_cpu_total_time()
    usage1 = _get_cpu_usage_time()
    sleep(2)
    total2 = _get_cpu_total_time()
    usage2 = _get_cpu_usage_time()
    return round((float(usage2-usage1)/float(total2-total1)),4)

def iowait():
    iowait_time1 = _get_iowait_time()
    total1 = _get_cpu_total_time()
    sleep(2)
    iowait_time2 = _get_iowait_time()
    total2 = _get_cpu_total_time()
    return round((float(iowait_time2-iowait_time1)/float(total2-total1)),4)

def cpu():
    return {'usage':usage(),'iowait':iowait()}
