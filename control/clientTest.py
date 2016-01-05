# -*- coding:utf8 -*-
import clientCtl



def loginCb(err,msg):
	print err,msg

def queryUserCb(err,msg):
	print err,msg

def queryVmCb(err,msg):
	print err,msg

def queryRoleCb(err,msg):
	print err,msg

def addUserCb(err,msg):
	print err,msg

def addVmCb(err,msg):
	print err,msg

def addUserVmCb(err,msg):
	print err,msg

def removeUserVmCb(err,msg):
	print err,msg




clientCtl=clientCtl.clientCtl()
clientCtl.initServerSetting('127.0.0.1',8894)
clientCtl.login('admin','111',u'管理员',loginCb)

# clientCtl.queryUser('admin',queryUserCb)
# clientCtl.login('user','111',u'普通用户',loginCb)

# clientCtl.queryUser('user',queryUserCb)

# clientCtl.queryVm('1',queryVmCb)

# clientCtl.queryRole(queryRoleCb)

# clientCtl.addUser('user4','111',u'普通用户',addUserCb)

clientCtl.addVm('5', 'vm5','vm5','192.168.1.107',addVmCb)

# clientCtl.addUserVm('user2',3,addUserVmCb)

# clientCtl.removeUserVm(2,removeUserVmCb)


print clientCtl.getSelfIP()
print clientCtl.getOutIP()