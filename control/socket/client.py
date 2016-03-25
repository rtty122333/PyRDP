import socket
import requests
import time
import re,urllib2
import os
import uuid
assert 'SYSTEMROOT' in os.environ

def client(msg,host,port,action,finalCb,cb):
    url='http://'+host+':'+port+'/'+action
    try:
        print 'url:',url,'msg:',msg
        response = requests.get(url, data=msg)
        result = response._content
        return cb(None,result,finalCb)
    except:
        return cb('fail to connect to server url '+url,None,finalCb)

def getSelfIP():
    ipInfoList=socket.gethostbyname_ex(socket.gethostname())
    lenIpInfo=len(ipInfoList)
    if lenIpInfo>0 :
        ipList=ipInfoList[len(ipInfoList)-1]
    if len(ipList)==1:
        return ipList[0]
    else:
        localIP=socket.gethostbyname(socket.gethostname())
        for ipItem in ipList:
            if ipItem!=localIP:
                return ipItem


class Getmyip:
    def getip(self):
        try:
            myip = self.visit("http://www.whereismyip.com/")
        except:
            try:
                myip = self.visit("http://www.bliao.com/ip.phtml")
            except:
                try:
                    myip = self.visit("http://www.ip138.com/ip2city.asp")
                except:
                    myip = None
        return myip
    def visit(self,url):
        opener = urllib2.urlopen(url)
        if url == opener.geturl():
            str = opener.read()
        return re.search('\d+\.\d+\.\d+\.\d+',str).group(0)
    #print re.search('\d+\.\d+\.\d+\.\d+',urllib2.urlopen("http://www.whereismyip.com").read()).group(0)

def getOutIP():
    getmyip = Getmyip()
    return getmyip.getip()

def getMacAddr(): 
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:] 
    return ":".join([mac[e:e+2] for e in range(0,11,2)])