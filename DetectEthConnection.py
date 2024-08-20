import psutil
import os
import subprocess


def check_eth_port(camera_ip): 
    addrs = psutil.net_if_addrs()
    eth_port_flag = False
    if 'eth0' in addrs:
        for addr in addrs['eth0']:
            if addr.family == 2:
                eth_port_flag = True
                break

#    camera_ip = "192.168.1.108"
    ping_flag = False

    try:
        output = subprocess.check_output(['ping', '-c', '1', camera_ip],stderr =subprocess.STDOUT, universal_newlines = True)
    except subprocess.CalledProcessError:
        ping_flag = False
        output = 'shabi'
    if "1 packets transmitted, 1 received" in output:
        ping_flag = True
    else:
        ping_flag = False
    
    return eth_port_flag, ping_flag
        
