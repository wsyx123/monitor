#!/usr/bin/env python
#_*_ coding:utf-8 _*_ 

def _read_network_traffic(netcard):
    with open('/proc/net/dev','r') as f:
        for line in f:
            ln = line.split()
            if ln[0].startswith(netcard):
                return ln

def network(netcard):
    traffic = {}
    traffic_list = _read_network_traffic(netcard)
    receive_total = round(float(traffic_list[1])/1024,2)
    transmit_total = round(float(traffic_list[9])/1024,2)
    drop_total = round(float(traffic_list[4]+traffic_list[12])/1024,2)
    return {'receive_total':receive_total,'transmit_total':transmit_total,'drop_total':drop_total}

