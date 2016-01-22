import socket
import time
import re,urllib2
import os
import uuid
assert 'SYSTEMROOT' in os.environ

bufSize=1024

def client(msg,host,port,finalCb,cb):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host,port))
        time.sleep(2)
        sock.send(msg)
        sock.settimeout(5)
        rst=[]
        while True:
            buf=sock.recv(bufSize)
            if buf[len(buf)-1]=='|':
                buf=buf[0:-1]
                rst.append(buf)
                break
            else:
                rst.append(buf)
        return cb(None,''.join(rst),finalCb)

    except:
        #print 'fail to connect to ther server '+host+':'+str(port)
        return cb('fail to connect to server '+host+':'+str(port),None,finalCb)
    #time.sleep(10)
    finally:
        sock.close()

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