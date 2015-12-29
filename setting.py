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

    def __init__(self,parent):
        QtGui.QWidget.__init__(self)
        Set_QWidget.__init__(self)
        self.setupUi(self)
        self.clientCtl=parent.clientCtl
        self.configPath=parent.configPath
        self.setSurePBtn.clicked.connect(self.settingFunc)
        self.setCancelPBtn.clicked.connect(self.cancelFunc)
        self.setFixedSize(self.width(), self.height()); 
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('setting.png'),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.hostLineEdit.setText(self.clientCtl.HOST)
        self.portLineEdit.setText(str(self.clientCtl.PORT))
        self.setStatusLabel.setStyleSheet("color:#ff0000")

    def settingFunc(self):
        if len(self.hostLineEdit.text())==0 or len(self.portLineEdit.text())==0:
            self.setStatusLabel.setText(u'请输入完整信息。')
        else:
            if(self.isValidIP(self.hostLineEdit.text())):
                self.clientCtl.initServerSetting(self.hostLineEdit.text(),int(self.portLineEdit.text()))
                self.updateConfig()
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

    def updateConfig(self):
        settings = QtCore.QSettings(self.configPath, QtCore.QSettings.IniFormat)  # 当前目录的INI文件
        settings.beginGroup('server')
        settings.setIniCodec('UTF-8')
        s1 = settings.setValue(r'host', self.hostLineEdit.text())
        s2 = settings.setValue(r'port', self.portLineEdit.text())
        settings.endGroup()

    # def closeEvent(self, event):
    #     sys.exit()