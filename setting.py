# -*- coding:utf8 -*-
import re
import sys
import os
from PyQt4 import QtCore, QtGui, uic
import clientCtl

reload(sys) 
sys.setdefaultencoding( "utf-8" )

qtCreatorFile = "setting.ui"

Set_QWidget, QtBaseClass = uic.loadUiType(qtCreatorFile)


class SettingWidget(QtGui.QWidget, Set_QWidget):

    def __init__(self,clientCtl):
        QtGui.QWidget.__init__(self)
        Set_QWidget.__init__(self)
        self.setupUi(self)
        self.clientCtl=clientCtl
        self.setSurePBtn.clicked.connect(self.settingFunc)
        self.setCancelPBtn.clicked.connect(self.cancelFunc)
        self.setFixedSize(self.width(), self.height()); 
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('setting.png'),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

    def settingFunc(self):
        if len(self.hostLineEdit.text())==0 or len(self.portLineEdit.text())==0:
            self.setStatusLabel.setText(u'请输入完整信息。')
        else:
            if(self.isValidIP(self.hostLineEdit.text())):
                self.clientCtl.initServerSetting(self.hostLineEdit.text(),int(self.portLineEdit.text()))
                self.close()
            else:
                self.setStatusLabel.setText(u'请输入合法的IP地址。')
                

    def cancelFunc(self):
        self.close()

    def isValidIP(self,ipStr):
        if(len(ipStr) < 8):
            return False
        reip = re.compile(
            '^((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)$')
        return reip.match(ipStr)


    # def closeEvent(self, event):
    #     sys.exit()