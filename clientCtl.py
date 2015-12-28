import client
import clientPackHandler
import json


class clientCtl():

    def __init__(self):
        self.HOST = ''
        self.PORT = 8894
        self.IP=client.getSelfIP()
        self.outIP=client.getOutIP()

    def initServerSetting(self,host,port):
        self.HOST=host
        self.PORT=port

    def getSelfIP(self):
        return self.IP

    def getOutIP(self):
        return self.outIP
        
    def login(self,userName,password,role,cb):
        msg=clientPackHandler.authUser(userName,password,role,self.IP)
        client.client(json.dumps(msg),self.HOST,self.PORT,cb,self.cbTmp)

    def queryUser(self,userName,cb):
        msg=clientPackHandler.queryUser(userName)
        client.client(json.dumps(msg),self.HOST,self.PORT,cb,self.cbTmp)

    def queryVm(self,vmId,cb):
        msg=clientPackHandler.queryVm(vmId)
        client.client(json.dumps(msg),self.HOST,self.PORT,cb,self.cbTmp)

    def queryRole(self,cb):
        msg=clientPackHandler.queryRole(self.IP)
        client.client(json.dumps(msg),self.HOST,self.PORT,cb,self.cbTmp)

    def cbTmp(self,err,msg,cb):
        if msg is None:
            return cb(err,None)
        else:
            return cb(err,json.loads(msg))