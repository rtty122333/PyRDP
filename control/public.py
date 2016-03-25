# -*- coding:utf8 -*-
import subprocess
import re
import sys
import os

def cur_file_dir():
    path = sys.path[0]
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path) 

def isValidIP(ipStr):
    if(len(ipStr) < 8):
        return False
    reip = re.compile(
        '^((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)$')
    return reip.match(ipStr)

def netSetting():
    cmd = 'explorer.exe ::{7007ACC7-3202-11D1-AAD2-00805FC1270E}'
    process = subprocess.Popen(cmd, shell=True)
    process.wait()
    process.terminate()