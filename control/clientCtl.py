from socket import client
from socket import clientPackHandler
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

    def queryUserInfo(self,userId,cb):
        msg=clientPackHandler.queryUserInfo(userId)
        client.client(json.dumps(msg),self.HOST,self.PORT,cb,self.cbTmp)

    def queryVm(self,vmId,cb):
        msg=clientPackHandler.queryVm(vmId)
        client.client(json.dumps(msg),self.HOST,self.PORT,cb,self.cbTmp)

    def queryRole(self,cb):
        msg=clientPackHandler.queryRole(self.IP)
        client.client(json.dumps(msg),self.HOST,self.PORT,cb,self.cbTmp)

    def addUser(self,userName,password,role,cb):
        msg=clientPackHandler.addUser(userName, password,role)
        client.client(json.dumps(msg),self.HOST,self.PORT,cb,self.cbTmp)

    def addVm(self,vmId,userName,vmName,ip,cb):
        msg=clientPackHandler.addVm(vmId,userName,vmName,ip)
        client.client(json.dumps(msg),self.HOST,self.PORT,cb,self.cbTmp)

    def addUserVm(self,userId,vmId,cb):
        msg=clientPackHandler.addUserVm(userId,vmId)
        client.client(json.dumps(msg),self.HOST,self.PORT,cb,self.cbTmp)

    def removeUserVm(self,vmId,state,userId,cb):
        msg=clientPackHandler.removeUserVm(vmId,state,userId)
        client.client(json.dumps(msg),self.HOST,self.PORT,cb,self.cbTmp)

    def cbTmp(self,err,msg,cb):
        # print 'cb err:',err,' msg:',msg
        if msg is None:
            return cb(err+' reply is null',None)
        else:
            return cb(err,json.loads(msg))