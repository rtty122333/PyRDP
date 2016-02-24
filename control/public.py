# -*- coding:utf8 -*-
import subprocess
import re
import clientCtl
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

def userConnVm(clientCtl, commandStr, userName, vmInfo):
    addCmdkeyEnv(vmInfo)
    clientCtl.userConnVm(userName, vmInfo, userConnVmCb)
    subPro = subprocess.Popen(commandStr, shell=False)
    subPro.wait()
    subPro.terminate()
    removeCmdkeyEnv(vmInfo['ip'])
    clientCtl.userDisConnVm(userName, vmInfo, userConnVmCb)

def userConnVmCb(err, msg):
    if err:
        print 'user conn vm log write error ', err
    else:
        print 'user conn vm log write succeed'


def userDisConnVmCb(err, msg):
    if err:
        print 'user disconn vm log write error ', err
    else:
        print 'user disconn vm log write succeed'

def cleanCmdkeyEnv():
    process = subprocess.Popen(
        'cmdkey /list', shell=False, stdout=subprocess.PIPE)
    while process.poll() == None:
        line = process.stdout.readlines()
        for index in line:
            lineShuzu = index.strip().split('\r\n')
            for val in lineShuzu:
                if len(val) > 0 and 'target' in val:
                    target = val.split(':')
                    if len(target) == 3:
                        name = target[2]
                        name = name[name.index('=') + 1:]
                        if public.isValidIP(name):
                            delePro = subprocess.Popen(
                                'cmdkey /delete:' + name, shell=False)
                            delePro.wait()
                            delePro.terminate()
    process.terminate()

def initCmdkeyEnv(vmInfoList):
    for item in vmInfoList:
        target = item['ip']
        user = item['userName']
        pwd = item['password']
        cmd = 'cmdkey /add:' + target + ' /user:' + user + ' /pass:' + pwd
        process = subprocess.Popen(cmd, shell=False)
        process.wait()
        process.terminate()

def addCmdkeyEnv(vmInfo):
    target = vmInfo['ip']
    user = vmInfo['userName']
    pwd = vmInfo['password']
    cmd = 'cmdkey /add:' + target + ' /user:' + user + ' /pass:' + pwd
    process = subprocess.Popen(cmd, shell=False)
    process.wait()
    process.terminate()

def removeCmdkeyEnv(IP):
    delePro = subprocess.Popen('cmdkey /delete:' + IP, shell=False)
    delePro.wait()
    delePro.terminate()

def netSetting():
    cmd = 'ncpa.cpl'
    process = subprocess.Popen(cmd, shell=True)
    process.wait()
    process.terminate()