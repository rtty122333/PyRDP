import re
import os
import clientCtl 

def isValidIP(ipStr):
    if(len(ipStr) < 8):
        return False
    reip = re.compile(
        '^((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)$')
    return reip.match(ipStr)

def userConnVm(clientCtl,commandStr,userName,vmInfo):
	clientCtl.userConnVm(userName,vmInfo,userConnVmCb)
	stdouterr = os.popen4(commandStr)[1].read()
	clientCtl.userDisConnVm(userName,vmInfo,userConnVmCb)


def userConnVmCb(err,msg):
	if err:
		print 'user conn vm log write error ',err
	else:
		print 'user conn vm log write succeed'

def userDisConnVmCb(err,msg):
	if err:
		print 'user disconn vm log write error ',err
	else:
		print 'user disconn vm log write succeed'






