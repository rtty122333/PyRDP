# -*- coding:utf8 -*-
import re
import sys
import os
from PyQt4 import QtCore, QtGui, uic
from control import rdcCtl
import win32api
import ctypes
from control import clientCtl
import json
import math
import cmpWidget
import setting
import distributeVm
import userTreeWidgetItem
import vmTreeWidgetItem
from control import public

reload(sys) 
sys.setdefaultencoding( "utf-8" )

qtCreatorFile = "ui/rdpIndex.ui"

Ui_QDialog, QtBaseClass = uic.loadUiType(qtCreatorFile)



class MyDialog(QtGui.QDialog, Ui_QDialog):

    def __init__(self):
        QtGui.QDialog.__init__(self)
        Ui_QDialog.__init__(self)
        self.setupUi(self)
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("indexRdp")
        self.configPath='config/config.ini'
        self.clientCtl=clientCtl.clientCtl()
        #self.setStyleSheet("background-color:#2C3E50")
        self.statusLabel.clear()
        self.statusLabel.setScaledContents(True)
        self.statusLabel.setStyleSheet("color:#ff0000")
        self.statusLabel1.setStyleSheet("color:#ff0000")
        
        #clientCtl.queryRole(self.queryRoleCb)
        self.roleComboBox.addItem(u'普通用户')
        self.roleComboBox.addItem(u'管理员')

        self.initWin()
        self.initConfig()
        powerIcon = QtGui.QIcon()
        powerPixMap=QtGui.QPixmap('img/power.png')
        powerPixMap.scaled(50,50,QtCore.Qt.KeepAspectRatioByExpanding)
        powerIcon.addPixmap(powerPixMap,
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.quitPushButton=QtGui.QPushButton(powerIcon,'',self)
        self.quitPushButton.setIconSize(QtCore.QSize(30,30))
        self.quitPushButton.move(self.winWidth/10*9,self.winHight/10*9)
        self.quitPushButton.clicked.connect(self.closeFunc)
        self.loginPushButton.clicked.connect(self.login)
        self.logoutPushButton.clicked.connect(self.logout)
        self.loginRefreshPBtn.clicked.connect(self.refreshLogin)
        self.settingPBtn.clicked.connect(self.settingFunc)

        self.showFullScreen()

    def initWin(self):
        self.winWidth=win32api.GetSystemMetrics(0)
        self.winHight = win32api.GetSystemMetrics(1)
        self.loginWidget.move(self.winWidth/2-self.loginWidget.width()/2,self.winHight/2-self.loginWidget.height()/2)
        self.indexWidget.move(self.winWidth/2-self.indexWidget.width()/2,self.winHight/10)
        self.loginWidget.setStyleSheet("QWidget{background-color:#ffff00}");
        self.indexWidget.hide()

    def initConfig(self):
        settings = QtCore.QSettings(self.configPath, QtCore.QSettings.IniFormat)  # 当前目录的INI文件
        settings.beginGroup('server')
        settings.setIniCodec('UTF-8')
        host = settings.value(r'host').toString()
        port = settings.value(r'port').toString()
        self.clientCtl.initServerSetting(host,int(port))
        settings.endGroup()


    def settingFunc(self):
        self.settingDialog=setting.SettingWidget(self)
        self.settingDialog.show()

    def queryRoleCb(self,err,msg):
        if self.isSthWrong(err,msg,self.statusLabel):
            pass
        else:
            self.statusLabel.clear()
            self.roleComboBox.clear()
            for i in range(0,len(msg['content'])):
                self.roleComboBox.addItem(msg['content'][i])

    def login(self):
        if(len(self.userNameLineEdit.text())==0 or len(self.pwdLineEdit.text())==0):
            self.statusLabel.setText(u'请输入完整信息')
        else:
            self.statusLabel.clear()
            self.clientCtl.login(str(self.userNameLineEdit.text()),str(self.pwdLineEdit.text()),str(self.roleComboBox.currentText()),self.loginCb)

    def logout(self):
        self.statusLabel.clear()
        self.quitPushButton.show()
        self.indexWidget.hide()
        self.loginWidget.show()

    def loginCb(self,err,msg):
        if self.isSthWrong(err,msg,self.statusLabel):
            pass
        else:
            if msg['auth']=='success':
                self.loginWidget.hide()
                self.quitPushButton.hide()
                self.loginUserLabel.setText(self.userNameLineEdit.text())
                self.refreshVms(msg['content']['vmMap'])
                self.indexWidget.show()
            else:
                self.statusLabel.setText(u'错误的用户名或密码')

    def refreshLogin(self):
        self.clientCtl.queryRole(self.queryRoleCb)

    def refreshIndex(self):
        self.clientCtl.queryUser(str(self.userNameLineEdit.text()),self.queryUserCb)

    def queryUserCb(self,err,msg):
        if self.isSthWrong(err,msg,self.statusLabel1):
            pass
        else:
            self.refreshVms(msg['content']['vmMap'])

    def refreshVms(self,vms):
        self.statusLabel1.clear()

        #管理员
        if (self.roleComboBox.currentIndex()==1):
            self.usersVmsMap={}
            self.currentItem=None
            if self.vmsTreeWidget.topLevelItemCount()>0:
                self.vmsTreeWidget.clear()
            else:
                self.vmsTreeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                self.vmsTreeWidget.customContextMenuRequested.connect(self.showVmsTreeContextMenu)
                self.vmsTreeWidget.contextMenu = QtGui.QMenu(self.vmsTreeWidget)
                self.vmsTreeWidget.refreshIndexAction = QtGui.QAction(u'刷新All',self.vmsTreeWidget.contextMenu)
                self.vmsTreeWidget.refreshIndexAction.triggered.connect(self.refreshIndex)
                self.vmsTreeWidget.refreshAction = QtGui.QAction(u'刷新',self.vmsTreeWidget.contextMenu)
                self.vmsTreeWidget.refreshAction.triggered.connect(self.refreshItem)
                self.vmsTreeWidget.removeAction = QtGui.QAction(u'移除',self.vmsTreeWidget.contextMenu)
                self.vmsTreeWidget.removeAction.triggered.connect(self.removeItem)
                self.vmsTreeWidget.distributeAction = QtGui.QAction(u'分配',self.vmsTreeWidget.contextMenu)
                self.vmsTreeWidget.distributeAction.triggered.connect(self.distributeItem)
                self.vmsTreeWidget.contextMenu.addAction(self.vmsTreeWidget.refreshIndexAction)
                self.addUserPBtn.clicked.connect(self.addUser)
                self.addVmPBtn.clicked.connect(self.addVm)
                self.addUserLabel.setStyleSheet("color:#ff0000")
                self.addVmLabel.setStyleSheet("color:#ff0000")
                self.adminVmsStatusLabel.setStyleSheet("color:#ff0000")
                self.vmsTreeWidget.itemSelectionChanged.connect(self.itemChangedFunc)
                
            self.vmsTreeWidget.setHeaderLabel(u'详情')
            for userId in vms.keys():
                item=vms[userId]
                userItem=userTreeWidgetItem.UserTreeWidgetItem(self.vmsTreeWidget,item,self)
                self.usersVmsMap[userId]=userItem
            self.vmsWidget.hide()
            self.adminVmsWidget.show()
        else:
            if self.vmsWidget.layout():
                QtGui.QWidget().setLayout(self.vmsWidget.layout())
            else:
                self.vmsWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                self.vmsWidget.customContextMenuRequested.connect(self.showVmsContextMenu)
                self.vmsWidget.contextMenu = QtGui.QMenu(self.vmsWidget)
                self.vmsWidget.refreshAction = self.vmsWidget.contextMenu.addAction(u'刷新')
                self.vmsWidget.refreshAction.triggered.connect(self.refreshIndex)
            
            hBox = QtGui.QHBoxLayout()

            widget = QtGui.QWidget()
            grid = QtGui.QGridLayout()
            
            size=len(vms)
            xSize=5
            ySize=(size-1)/xSize+1
            grid.setVerticalSpacing(xSize)
            grid.setHorizontalSpacing(ySize)
            
            vmWidth=(self.vmsWidget.width()-150)/5
            vmHight=vmWidth*3/2#self.vmsWidget.height()/xSize
            index=0
            for xIndex in range(0,10):
                for yIndex in range(0,xSize):
                    if index<size:
                        widgetTmp=cmpWidget.cmpWidget(self.vmsWidget.pos()+self.detailWidget.pos()+self.indexWidget.pos(),vmWidth,vmHight,'img/cmp.png',vms[index]['userName'],vms[index]['vmName'],vms[index]['ip'],vms[index]['vmId'])
                        grid.addWidget(widgetTmp,xIndex,yIndex)
                    yIndex+=1
                    index+=1
                xIndex+=1

            widget.setLayout(grid)
            scroll = QtGui.QScrollArea()
            scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
            scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
            scroll.setWidgetResizable(False)
            scroll.setWidget(widget)
            hBox.addWidget(scroll)
            self.vmsWidget.setLayout(hBox)
            self.adminVmsWidget.hide()
            self.vmsWidget.show()

    def showVmsContextMenu(self,pos):
        self.vmsWidget.contextMenu.move(self.vmsWidget.pos()+ pos+self.detailWidget.pos()+self.indexWidget.pos())
        self.vmsWidget.contextMenu.show()

    def showVmsTreeContextMenu(self,pos):
        self.vmsTreeWidget.contextMenu.move(pos+self.vmsTreeWidget.pos()+self.adminVmsWidget.pos()+self.detailWidget.pos()+self.indexWidget.pos())
        self.vmsTreeWidget.contextMenu.show()

    def addUser(self):
        if(len(self.userNameLineEdit_user.text())==0 or len(self.pwdLineEdit_user.text())==0):
            self.addUserLabel.setText(u'请输入完整信息')
        else:
            self.addUserLabel.clear()
            self.clientCtl.addUser(str(self.userNameLineEdit_user.text()),str(self.pwdLineEdit_user.text()),str(self.roleComboBox_user.currentText()),self.addUserCb)

    def addVm(self):
        if(len(self.vmIdLineEdit.text())==0 or len(self.vmUserNameLineEdit.text())==0 or len(self.vmNameLineEdit.text())==0 or len(self.ipLineEdit.text())==0 ):
            self.addVmLabel.setText(u'请输入完整信息')
        else:
            if(public.isValidIP(self.ipLineEdit.text())):
                self.addVmLabel.clear()
                self.clientCtl.addVm(str(self.vmIdLineEdit.text()),str(self.vmUserNameLineEdit.text()),str(self.vmNameLineEdit.text()),str(self.ipLineEdit.text()),self.addVmCb)
            else:
                self.addVmLabel.setText(u'请输入合法IP信息')
            
    def addUserCb(self,err,msg):
        if self.isSthWrong(err,msg,self.addUserLabel):
            pass
        else:
            txt=msg['content']['userName']
            userItem = QtGui.QTreeWidgetItem(self.vmsTreeWidget)
            userItem.setText(0, txt)
            userItem.setIcon(0,QtGui.QIcon("img/user.png"))
            self.usersVmsMap[msg['content']['userId']]=userItem

    def addVmCb(self,err,msg):
        if self.isSthWrong(err,msg,self.addVmLabel):
            pass
        else:
            self.usersVmsMap['0'].addVm(msg['content'])

    def closeFunc(self):
        shutdown=QtGui.QMessageBox()
        shutdown.setWindowTitle(u'警告')
        shutdown.setText(u'现在关闭此系统吗？')
        yesBtn=shutdown.addButton(u"确定",QtGui.QMessageBox.AcceptRole)
        noBtn=shutdown.addButton(u"取消",QtGui.QMessageBox.RejectRole)
        shutdown.exec_()
        if shutdown.clickedButton()==yesBtn:
            self.close()

    def itemChangedFunc(self):
        if len(self.vmsTreeWidget.selectedItems())==1:
            item=self.vmsTreeWidget.selectedItems()[0]
            if self.currentItem==None or self.currentItem.flag!=item.flag or (item.flag=='vm' and (item.parent().userId+self.currentItem.parent().userId)!=0 and (item.parent().userId*self.currentItem.parent().userId)==0 ):
                self.vmsTreeWidget.contextMenu=QtGui.QMenu(self.vmsTreeWidget)
                self.vmsTreeWidget.contextMenu.addAction(self.vmsTreeWidget.refreshIndexAction)
                if item.flag=='vm':
                    self.vmsTreeWidget.contextMenu.addAction(self.vmsTreeWidget.refreshAction)
                    if item.parent().userId==0:
                        self.vmsTreeWidget.contextMenu.addAction(self.vmsTreeWidget.distributeAction)
                    else:
                        self.vmsTreeWidget.contextMenu.addAction(self.vmsTreeWidget.removeAction)
                elif item.flag=='user':
                    self.vmsTreeWidget.contextMenu.addAction(self.vmsTreeWidget.refreshAction)
            self.currentItem=item

    def refreshItem(self,item):
        self.currentItem.refreshItem(self.refreshItemsCb)
        # if self.currentItem.flag=='vm':
        #     self.clientCtl.queryVm(self.currentItem.vmId,self.refreshItemsCb)
        # elif self.currentItem.flag=='user':
        #     self.clientCtl.queryUserInfo(self.currentItem.userId,self.refreshItemsCb)

    def refreshItemsCb(self,err,msg):
        if self.isSthWrong(err,msg,self.adminVmsStatusLabel):
            pass
        else:
            self.currentItem.refreshSelf(msg['content'])

    def removeItem(self,item):
        self.currentItem.removeItem(self.removeItemCb)
        # removeMsg=QtGui.QMessageBox()
        # removeMsg.setWindowTitle(u'警告')
        # yesBtn=removeMsg.addButton(u"确定",QtGui.QMessageBox.AcceptRole)
        # noBtn=removeMsg.addButton(u"取消",QtGui.QMessageBox.RejectRole)
        # if self.currentItem.parent().userId==-1:
        #     removeMsg.setText(u'确定将虚拟机 '+self.currentItem.txt+u' 移入待分配设备吗？')
        #     removeMsg.exec_()
        #     if removeMsg.clickedButton()==yesBtn:
        #         self.clientCtl.removeUserVm(self.currentItem.vmId,self.currentItem.state,self.currentItem.parent().userId,self.removeItemCb)
        # else:
        #     removeMsg.setText(u'确定删除 '+self.currentItem.parent().userName+u' 的虚拟机 '+self.currentItem.txt+u' 吗？')
        #     removeMsg.exec_()
        #     if removeMsg.clickedButton()==yesBtn:
        #         self.clientCtl.removeUserVm(self.currentItem.vmId,self.currentItem.state,self.currentItem.parent().userId,self.removeItemCb)

    def removeItemCb(self,err,msg):
        if self.isSthWrong(err,msg,self.adminVmsStatusLabel):
            pass
        else:
            if self.currentItem.info['state']==4:
                self.currentItem.parent().removeChild(self.currentItem)
            else:
                self.updateVmItem(self.currentItem,self.usersVmsMap['-1'],msg)
                
    def updateVmItem(self,vmItem,toParent,msg):
        vmItem.parent().removeChild(vmItem)
        vmItem.setState(msg['content']['state'])
        vmItem.setStateTime(msg['content']['stateTime'])
        vmItem=vmTreeWidgetItem.VmTreeWidgetItem(toParent,vmItem,toParent.childCount(),None)
        toParent.addChild(vmItem)

    def distributeItem(self,item):
        self.distributeVm=distributeVm.DistributeVmWidget(self.currentItem,self)
        self.distributeVm.show()

    def userOfVmItem(self,userName):
        if self.usersVmsMap==None:
            return None
        else:
            for key in self.usersVmsMap.keys():
                userItem=self.usersVmsMap[key]
                if userItem.userName==userName:
                    return userItem
            return None

    def isSthWrong(self, err, msg, itemLable):
        if err is None:
            if msg['info'] == 'ok':
                itemLable.clear()
                return False
            else:
                itemLable.setText(msg['desc'])
                return True
        else:
            itemLable.setText(err + u'连接失败,请稍后重试.')
            return True

    def closeEvent(self, event):
        sys.exit()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    dialog = MyDialog()
    dialog.show()
    sys.exit(app.exec_())