# -*- coding:utf8 -*-
import re
import sys
import os
from PyQt4 import QtCore, QtGui, uic
import ctypes
from control import public
from control import clientCtl
import setting

reload(sys) 
sys.setdefaultencoding( "utf-8" )


class MyDialog(QtGui.QDialog):

    def __init__(self):
        QtGui.QDialog.__init__(self)
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("loginRdp")

        self.currentDir = public.cur_file_dir()
        self.configPath=self.currentDir+'/config/config.ini'
        self.clientCtl=clientCtl.clientCtl()

        self.initLoginWidget()
        
        # self.showFullScreen()

    def initLoginWidget(self):
        geometry = QtGui.QApplication.desktop().screenGeometry()
        self.winWidth=geometry.width()
        self.winHight=geometry.height()

        self.backWidget = QtGui.QWidget(self)
        self.loginWidget=QtGui.QWidget(self)
        self.loginWidget.resize(self.winWidth/4,self.winHight/6)
        self.loginWidget.move(self.winWidth/2-self.loginWidget.width()/2,self.winHight/2)

        logodir = os.path.join(self.currentDir,"img","logo.png")
        logodir = logodir.replace('\\','/')
        backstylesheet = "QWidget{background:url(%s);background-attachment:fixed;background-repeat:no-repeat}" % logodir
        self.backWidget.setStyleSheet(backstylesheet)
        self.backWidget.setGeometry(self.winWidth/2-250,self.winHight/2-300,500,168)

        

        self.loginWidget.setStyleSheet("QLabel{color:#000;font-size:16px;font-weight:bold;font-family:Agency FB;};QLineEdit{color:#000;font-size:16px;font-weight:bold;font-family:Agency FB;}")
        userNameLabel = QtGui.QLabel(u'用户名')
        pwdLabel = QtGui.QLabel(u'密码')
        statusLabel = QtGui.QLabel(u'')

        setPBtn=QtGui.QPushButton(u'设置')
        loginPBtn=QtGui.QPushButton(u'登录')

        self.userNameEdit = QtGui.QLineEdit()
        self.pwdEdit = QtGui.QLineEdit()

        statusLabel.setStyleSheet("color:red;font-size:13px;")
        
        self.pwdEdit.setEchoMode(QtGui.QLineEdit.Password)
        
        grid = QtGui.QGridLayout()
        # grid.setSpacing(8)
        grid.setVerticalSpacing(5)
        grid.setHorizontalSpacing(8)
        # grid.setMargin(20)
 
        grid.addWidget(userNameLabel,0,0)
        grid.addWidget(QtGui.QLabel(''),0,1)
        grid.addWidget(self.userNameEdit,0,2,1,6)

        grid.addWidget(QtGui.QLabel(''),1,1)

        grid.addWidget(pwdLabel,2,0)
        grid.addWidget(QtGui.QLabel(''),2,1)
        grid.addWidget(self.pwdEdit,2,2,1,6)

        # grid.addWidget(QtGui.QLabel(''),3,1)

        grid.addWidget(QtGui.QLabel(''),3,0,1,4)
        grid.addWidget(statusLabel,3,5,1,2)

        # grid.addWidget(QtGui.QLabel(''),5,1)

        grid.addWidget(QtGui.QLabel(''),4,0,1,5)
        grid.addWidget(setPBtn,4,5)
        grid.addWidget(loginPBtn,4,7)
        # quitPBtn.resize(winWidth/4,winHight/8)
 
        self.loginWidget.setLayout(grid)

        powerIcon = QtGui.QIcon()
        powerPixMap=QtGui.QPixmap(self.currentDir+'/img/power.png')
        powerPixMap.scaled(50,50,QtCore.Qt.KeepAspectRatioByExpanding)
        powerIcon.addPixmap(powerPixMap,
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        quitPushButton=QtGui.QPushButton(powerIcon,'',self)
        quitPushButton.setIconSize(QtCore.QSize(30,30))
        quitPushButton.move(self.winWidth/10*9,self.winHight/10*9)

        loginPBtn.clicked.connect(self.login)
        setPBtn.clicked.connect(self.settingFunc)
        quitPushButton.clicked.connect(self.closeFunc)
        
        
    def login(self):
        self.clientCtl.login(str(self.userNameEdit.text()),str(self.pwdEdit.text()),self.loginCb)

    def loginCb(self,err,msg):
        print err,msg

    def settingFunc(self):
        self.settingDialog=setting.SettingWidget(self)
        self.settingDialog.show()

    def closeFunc(self):
        '''shutdown=QtGui.QMessageBox()
        shutdown.setWindowTitle(u'警告')
        shutdown.setText(u'现在关闭此系统吗？')
        yesBtn=shutdown.addButton(u"确定",QtGui.QMessageBox.AcceptRole)
        noBtn=shutdown.addButton(u"取消",QtGui.QMessageBox.RejectRole)
        shutdown.exec_()
        if shutdown.clickedButton()==yesBtn:
            # self.close()
            os.popen4('shutdown -s -t 0')'''
        sys.exit()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    dialog = MyDialog()
    dialog.show()
    sys.exit(app.exec_())