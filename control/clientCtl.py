# from socket import requestClient as client
from socket import client
from socket import clientPackHandler
import json
import public
import subprocess


class clientCtl():

    def __init__(self):
        self.HOST = ''
        self.PORT = 8894
        self.IP=client.getSelfIP()
        self.outIP=client.getOutIP()
        self.MAC=client.getMacAddr()

    def initServerSetting(self,host,port):
        self.HOST=host
        self.PORT=port

    def getSelfIP(self):
        return self.IP

    def getOutIP(self):
        return self.outIP

    def getMacAddr(self):
        return self.MAC

    def login(self,userName,password,role,cb):
        msg=clientPackHandler.authUser(userName,password,role,self.IP,self.MAC)
        client.client(json.dumps(msg),self.HOST,self.PORT,cb,self.cbTmp)

    def logout(self,userName,roleName,cb):
        msg=clientPackHandler.logout(userName,roleName,self.IP,self.MAC)
        client.client(json.dumps(msg),self.HOST,self.PORT,cb,self.cbTmp)

    def queryUser(self,userName,cb):
        msg=clientPackHandler.queryUser(userName)
        client.client(json.dumps(msg),self.HOST,self.PORT,cb,self.cbTmp)

    def queryUserInfo(self,userName,cb):
        msg=clientPackHandler.queryUserInfo(userName)
        client.client(json.dumps(msg),self.HOST,self.PORT,cb,self.cbTmp)

    def queryVm(self,vmId,cb):
        msg=clientPackHandler.queryVm(vmId)
        client.client(json.dumps(msg),self.HOST,self.PORT,cb,self.cbTmp)

    def queryRole(self,cb):
        msg=clientPackHandler.queryRole(self.IP)
        client.client(json.dumps(msg),self.HOST,self.PORT,cb,self.cbTmp)

    def addUser(self,adminId,userName,password,role,cb):
        msg=clientPackHandler.addUser(adminId,self.IP,self.MAC,userName, password,role)
        client.client(json.dumps(msg),self.HOST,self.PORT,cb,self.cbTmp)

    def addVm(self,adminId,vmId,userName,vmName,ip,pwd,cb):
        msg=clientPackHandler.addVm(adminId,self.IP,self.MAC,vmId,userName,vmName,ip,pwd)
        client.client(json.dumps(msg),self.HOST,self.PORT,cb,self.cbTmp)

    def addUserVm(self,adminId,userName,vmInfo,cb):
        msg=clientPackHandler.addUserVm(adminId,self.IP,self.MAC,userName,vmInfo)
        client.client(json.dumps(msg),self.HOST,self.PORT,cb,self.cbTmp)

    def removeUserVm(self,adminId,vmInfo,userName,cb):
        msg=clientPackHandler.removeUserVm(adminId,self.IP,self.MAC,userName,vmInfo)
        client.client(json.dumps(msg),self.HOST,self.PORT,cb,self.cbTmp)

    def userConnVm(self,userName,vmInfo,cb):
        msg=clientPackHandler.userConnVm(self.IP,self.MAC,userName,vmInfo)
        client.client(json.dumps(msg),self.HOST,self.PORT,cb,self.cbTmp)

    def userDisConnVm(self,userName,vmInfo,cb):
        msg=clientPackHandler.userDisConnVm(self.IP,self.MAC,userName,vmInfo)
        client.client(json.dumps(msg),self.HOST,self.PORT,cb,self.cbTmp)

    def cbTmp(self,err,msg,cb):
        # print 'cb err:',err,' msg:',msg
        if msg is None:
            return cb(err+' reply is null',None)
        else:
            return cb(err,json.loads(msg))