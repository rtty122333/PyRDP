# -*- coding:utf8 -*-
import os
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
import rdpConn


class cmpWidget(QtGui.QWidget):

    def __init__(self,parentPos, width, height, text, imgPath,ip,vmId):

        super(cmpWidget, self).__init__()
        self.parentPos=parentPos
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
        # 必须将ContextMenuPolicy设置为Qt.CustomContextMenu
        # 否则无法使用customContextMenuRequested信号
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)
        self.contextMenu = QtGui.QMenu(self)
        self.connAction = self.contextMenu.addAction(u'连接')
        self.connAction.triggered.connect(self.connHandler)
        self.rdpConn=rdpConn.RDPDialog(self.ip)


    def mouseDoubleClickEvent(self,event):
        '''
        self.reply=QtGui.QMessageBox()
        self.reply.setWindowTitle(u'消息')
        self.reply.setText(u'您正在连接机器\n'+self.text)
        self.reply.setStandardButtons(QtGui.QMessageBox.Yes|QtGui.QMessageBox.No)
        self.reply.setButtonText(QtGui.QMessageBox.Yes,u"是")
        self.reply.setButtonText(QtGui.QMessageBox.No,u"否")
        #reply = QtGui.QMessageBox.question(self,u'消息',u'您正在连接机器\n'+self.text,QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,QtGui.QMessageBox.No)
        self.reply.show()
        if self.reply==QtGui.QMessageBox.Yes:
            stdouterr = os.popen4(str('mstsc /v:' + self.ip))[1].read()
        else:
            event.ignore()
        '''
        reply = QtGui.QMessageBox.question(self,u'消息',u'您正在连接机器\n'+self.text,QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,QtGui.QMessageBox.No)
        if reply==QtGui.QMessageBox.Yes:
            stdouterr = os.popen4(str('mstsc /v:' + self.ip))[1].read()
        else:
            event.ignore()

    def showContextMenu(self,pos):
        self.contextMenu.move(self.pos() + pos+self.parentPos)
        self.contextMenu.show()
    def connHandler(self):
        self.rdpConn.show()