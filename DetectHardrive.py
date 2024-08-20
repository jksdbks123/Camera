import os
import subprocess
import psutil


def scan_hardrive():
    partitions = psutil.disk_partitions()
    drives = []
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        drives.append({'device':partition.device, 'mountpoint':partition.mountpoint,'total': usage.total,'used':usage.used, 'free': usage.free, 'percent': usage.percent})
        
    find_flag = False
    for d in drives:
        if 'Extreme SSD' in d['mountpoint'].split('/'):
            find_flag = True
            break
    if find_flag:
        outpath = d['mountpoint']
        return outpath
    else:
        return None
