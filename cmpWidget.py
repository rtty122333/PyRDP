# -*- coding:utf8 -*-
import os
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
import rdpConn


class cmpWidget(QtGui.QWidget):

    def __init__(self, width, height, text, imgPath,ip,vmId):

        super(cmpWidget, self).__init__()
        self.ip=ip
        self.vmId=vmId
        self.text=text
        hVBox=QtGui.QVBoxLayout()
        self.setMinimumSize(width,height)
        
        picBtn=QtGui.QLabel()
        pixMap=QtGui.QPixmap(imgPath)
        pixMap=pixMap.scaled(width,width,QtCore.Qt.KeepAspectRatioByExpanding)
        picBtn.setPixmap(pixMap)
        #labelBtn.mouseReleaseEvent=self.mstscFunc
        #picBtn.resize(width,width)
        #widgetTmp.setStyleSheet("background-color:#2C3E50")
        hVBox.addWidget(picBtn)

        label=QtGui.QLabel()
        label.setText(self.text)

        hVBox.addWidget(label)
        self.setLayout(hVBox)
        self.rdpConn=rdpConn.RDPDialog(self.ip)


    def mouseDoubleClickEvent(self,event):
        QtGui.QMessageBox.question(
                self, 'Message', u'双击事件', QtGui.QMessageBox.Yes, QtGui.QMessageBox.Yes)

        reply = QtGui.QMessageBox.question(self,u'消息',u'您正在连接机器\n'+self.text,QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,QtGui.QMessageBox.No)
        
        if reply==QtGui.QMessageBox.Yes:
            stdouterr = os.popen4(str('mstsc /v:' + self.ip))[1].read()

        else:
            event.ignore()

    def mousePressEvent(self, event):    
        pass

    def mouseReleaseEvent(self, event):
        if event.button()==QtCore.Qt.RightButton:
            self.rdpConn.show()