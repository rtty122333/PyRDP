# -*- coding:utf8 -*-
from PyQt4 import QtGui, QtCore
from control import public
from control import clientCtl


class VmTreeWidgetItem(QtGui.QTreeWidgetItem):

    def __init__(self, parent, vmInfo,index,rdpIndex):
        if rdpIndex==None:
            super(VmTreeWidgetItem, self).__init__(
                parent, vmInfo,QtGui.QTreeWidgetItem.Type)
            self.rdpIndex=vmInfo.rdpIndex
            self.index=index
            self.flag = 'vm'
            self.info=vmInfo.info
            self.txt = vmInfo.txt
            self.setText(0, self.txt)
            self.refreshSelf(self.info)
        else:
            super(VmTreeWidgetItem, self).__init__(
                parent, QtGui.QTreeWidgetItem.Type)
            self.rdpIndex=rdpIndex
            self.index=index
            self.flag = 'vm'
            # self.vmId = vmInfo["vmId"]
            # self.userName = vmInfo["userName"]
            # self.vmName = vmInfo["vmName"]
            # self.ip = vmInfo["ip"]
            # self.state = vmInfo["state"]
            # self.stateTime = vmInfo["stateTime"]
            self.info=vmInfo
            self.txt = vmInfo['vmId'] + ' ' + vmInfo['userName'] + ' ' + vmInfo['vmName'] + ' ' + vmInfo['ip']
            self.setText(0, self.txt)
            self.refreshSelf(self.info)
            
    def refreshSelf(self,vmInfo ):
        if vmInfo['state'] == 2:
            self.setIcon(0, QtGui.QIcon("img/cmpOnline.png"))
        else:
            self.setIcon(0, QtGui.QIcon("img/cmpOffline.png"))

    def refreshItem(self,cb):
        self.rdpIndex.clientCtl.queryVm(self.info['vmId'],cb)

    def removeItem(self,cb):
        removeMsg=QtGui.QMessageBox()
        removeMsg.setWindowTitle(u'警告')
        yesBtn=removeMsg.addButton(u"确定",QtGui.QMessageBox.AcceptRole)
        noBtn=removeMsg.addButton(u"取消",QtGui.QMessageBox.RejectRole)
        if self.info['state']==4:
            removeMsg.setText(u'确定将虚拟机 '+self.txt+u' 移入待分配设备吗？')
            removeMsg.exec_()
            if removeMsg.clickedButton()==yesBtn:
                self.rdpIndex.clientCtl.removeUserVm(self.info['vmId'],4,self.parent().userId,cb)
        else:
            removeMsg.setText(u'确定删除 '+self.parent().userName+u' 的虚拟机 '+self.txt+u' 吗？')
            removeMsg.exec_()
            if removeMsg.clickedButton()==yesBtn:
                self.rdpIndex.clientCtl.removeUserVm(self.info['vmId'],self.info['state'],self.parent().userId,cb)

    def setState(self,stateTmp):
        self.info['state']=stateTmp

    def setStateTime(self,time):
        self.info['stateTime']=time