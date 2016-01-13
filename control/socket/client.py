import socket
import time
import re,urllib2
import os
import uuid
assert 'SYSTEMROOT' in os.environ



def client(msg,host,port,finalCb,cb):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rst=''
    try:
        sock.connect((host,port))
        time.sleep(2)
        sock.send(msg)
        sock.settimeout(5)
        rst=sock.recv(8092)
        sock.close()
        return cb(None,rst,finalCb)
    except:
        #print 'fail to connect to ther server '+host+':'+str(port)
        sock.close()
        if len(rst)==0:
            return cb('fail to connect to server '+host+':'+str(port),None,finalCb)
    #time.sleep(10)
    # finally:
    #     sock.close()

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