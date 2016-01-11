# -*- coding:utf8 -*-
from PyQt4 import QtGui, QtCore
import vmTreeWidgetItem
from control import public
from control import clientCtl


class UserTreeWidgetItem(QtGui.QTreeWidgetItem):

    def __init__(self, parent, userInfo,rdpIndex):
        super(UserTreeWidgetItem, self).__init__(parent,QtGui.QTreeWidgetItem.Type)
        self.rdpIndex=rdpIndex
        self.flag='user'
        self.userId = userInfo["userId"]
        self.userName = userInfo["userName"]
        self.setText(0, self.userName)
        self.refreshSelf(userInfo)

    def refreshSelf(self,userInfo):
        self.state = userInfo["userState"]
        self.stateTime = userInfo["stateTime"]
        while(self.child(0)):
            self.removeChild(self.child(0))
        if userInfo['userState']==1:
            self.setIcon(0, QtGui.QIcon("img/userOnline.png"))
        else:
            self.setIcon(0, QtGui.QIcon("img/userOffline.png"))
        for index in range(0, len(userInfo['vmMap'])):
            vm = userInfo['vmMap'][index]
            vmItem=vmTreeWidgetItem.VmTreeWidgetItem(self,vm,index,self.rdpIndex)
            self.addChild(vmItem)

    def refreshItem(self,cb):
        self.rdpIndex.clientCtl.queryUserInfo(self.userId,cb)

    def addVm(self,vmInfo):
        vmItem = vmTreeWidgetItem.VmTreeWidgetItem(self,vmInfo,self.childCount(),self.rdpIndex)
        self.addChild(vmItem)