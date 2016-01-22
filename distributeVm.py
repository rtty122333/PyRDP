# -*- coding:utf8 -*-
import re
import sys
import os
from PyQt4 import QtCore, QtGui, uic
from control import clientCtl
from control import public

reload(sys) 
sys.setdefaultencoding( "utf-8" )

qtCreatorFile = "ui/distributeVm.ui"

Distri_QWidget, QtBaseClass = uic.loadUiType(qtCreatorFile)


class DistributeVmWidget(QtGui.QWidget, Distri_QWidget):

    def __init__(self,vmItem,rdpIndex):
        QtGui.QWidget.__init__(self)
        Distri_QWidget.__init__(self)
        self.setupUi(self)
        self.vmItem=vmItem
        self.rdpIndex=rdpIndex
        self.vmInfoLabel.setText(self.vmItem.txt)
        self.distriStatusLabel.setStyleSheet("color:#ff0000")
        self.surePBtn.clicked.connect(self.sureFunc)
        self.cancelPBtn.clicked.connect(self.cancelFunc)
        self.setFixedSize(self.width(), self.height()); 

    def sureFunc(self):
        if len(self.userNameLineEdit.text())==0:
            self.distriStatusLabel.setText(u'请输入用户信息。')
        else:
            self.distriStatusLabel.clear()
            userItem=self.rdpIndex.userOfVmItem(self.userNameLineEdit.text())
            if userItem==None:
                self.distriStatusLabel.setText(u'找不到该用户。')
            else:
                self.distriStatusLabel.clear()
                self.toUserItem=userItem
                self.rdpIndex.clientCtl.addUserVm(self.rdpIndex.userName,userItem.userName,self.vmItem.info,self.addUserVmCb)

    def addUserVmCb(self,err,msg):
        if self.rdpIndex.isSthWrong(err,msg,self.distriStatusLabel):
            pass
        else:
            self.distriStatusLabel.clear()
            self.rdpIndex.updateVmItem(self.vmItem,self.toUserItem,msg)
            self.close()

    def cancelFunc(self):
        self.close()