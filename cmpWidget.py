# -*- coding:utf8 -*-
from PyQt4 import QtGui, QtCore
import rdpConn
from control import public


class cmpWidget(QtGui.QWidget):

    def __init__(self,rdpIndex,parentPos, width, height,imgPath,vmInfo):
        super(cmpWidget, self).__init__()
        self.rdpIndex=rdpIndex
        self.parentPos=parentPos
        self.info=vmInfo
        self.text=u'用户名：'+self.info['userName']+'\r\n'+u'虚拟机：'+self.info['vmName']
        hVBox=QtGui.QVBoxLayout()
        self.setMinimumSize(width,height)
        
        picBtn=QtGui.QLabel()
        pixMap=QtGui.QPixmap(imgPath)
        pixMap=pixMap.scaled(width,width,QtCore.Qt.KeepAspectRatioByExpanding)
        picBtn.setPixmap(pixMap)

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

    def mouseDoubleClickEvent(self,event):
        reply=QtGui.QMessageBox()
        reply.setWindowTitle(u'提示')
        reply.setText(u'您正在连接机器\n'+self.text)
        yesBtn=reply.addButton(u"是",QtGui.QMessageBox.AcceptRole)
        noBtn=reply.addButton(u"否",QtGui.QMessageBox.RejectRole)
        reply.exec_()
        if reply.clickedButton()==yesBtn:
            public.userConnVm(self.rdpIndex.clientCtl,str('mstsc /v:' + self.ip),self.rdpIndex.userName,self.info)
        else:
            event.ignore()

    def showContextMenu(self,pos):
        self.contextMenu.move(self.pos() + pos+self.parentPos)
        self.contextMenu.show()

    def connHandler(self):
        self.rdpConn=rdpConn.RDPDialog(self.rdpIndex,self.info)
        self.rdpConn.show()