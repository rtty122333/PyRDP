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

    def logout(self,userName,cb):
        msg=clientPackHandler.logout(userName,self.IP)
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
        msg=clientPackHandler.addUser(adminId,self.IP,userName, password,role)
        client.client(json.dumps(msg),self.HOST,self.PORT,cb,self.cbTmp)

    def addVm(self,adminId,vmId,userName,vmName,ip,pwd,cb):
        msg=clientPackHandler.addVm(adminId,self.IP,vmId,userName,vmName,ip,pwd)
        client.client(json.dumps(msg),self.HOST,self.PORT,cb,self.cbTmp)

    def addUserVm(self,adminId,userName,vmInfo,cb):
        msg=clientPackHandler.addUserVm(adminId,self.IP,userName,vmInfo)
        client.client(json.dumps(msg),self.HOST,self.PORT,cb,self.cbTmp)

    def removeUserVm(self,adminId,vmInfo,userName,cb):
        msg=clientPackHandler.removeUserVm(adminId,self.IP,vmInfo,userName)
        client.client(json.dumps(msg),self.HOST,self.PORT,cb,self.cbTmp)

    def userConnVm(self,userId,vmId,cb):
        msg=clientPackHandler.userConnVm(self.IP,userId,vmId)
        client.client(json.dumps(msg),self.HOST,self.PORT,cb,self.cbTmp)

    def userDisConnVm(self,userId,vmId,cb):
        msg=clientPackHandler.userDisConnVm(self.IP,userId,vmId)
        client.client(json.dumps(msg),self.HOST,self.PORT,cb,self.cbTmp)


    def cbTmp(self,err,msg,cb):
        # print 'cb err:',err,' msg:',msg
        if msg is None:
            return cb(err+' reply is null',None)
        else:
            return cb(err,json.loads(msg))


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