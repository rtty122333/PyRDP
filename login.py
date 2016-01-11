# -*- coding: utf-8 -*-

import sys
from control import clientCtl
from PyQt4 import QtCore, QtGui, uic

reload(sys)
sys.setdefaultencoding( "utf-8" )

qtCreatorFile = "ui/login.ui"

Ui_QDialog, QtBaseClass = uic.loadUiType(qtCreatorFile)


class LoginDialog(QtGui.QDialog, Ui_QDialog):
    def __init__(self, result):
        self.result = result
        self.result['success']=False
        QtGui.QDialog.__init__(self)
        Ui_QDialog.__init__(self)
        self.setupUi(self)
        self.configPath='config/config.ini'
        self.clientCtl=clientCtl.clientCtl()
        self.statusLabel.clear()
        self.statusLabel.setScaledContents(True)
        self.statusLabel.setStyleSheet("color:#ff0000")
        self.initConfig()
        self.loginButton.clicked.connect(self.loginClicked)

    def loginClicked(self):
        self.loginButton.setEnabled(False)
        if(len(self.uNameEdit.text())==0 or len(self.passwdEdit.text())==0):
            self.statusLabel.setText(u'请输入完整信息')
        else:
            self.statusLabel.clear()
            self.clientCtl.login(str(self.uNameEdit.text()),str(self.passwdEdit.text()),u'普通用户',self.loginCb)
        self.loginButton.setEnabled(True)

    def loginCb(self,err,msg):
        self.result['success'] = True
        self.result['uname'] = str(self.uNameEdit.text())
        self.result['vmMap'] = 'hahahah'
        self.close()
        return
        if self.isSthWrong(err,msg,self.statusLabel):
            pass
        else:
            if msg['auth']=='success':
                self.result['success'] = True
                self.result['uname'] = str(self.uNameEdit.text())
                self.result['vmMap'] = msg['content']['vmMap']
                self.close()
            else:
                self.statusLabel.setText(u'错误的用户名或密码')

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

    def initConfig(self):
        settings = QtCore.QSettings(self.configPath, QtCore.QSettings.IniFormat)  # 当前目录的INI文件
        settings.beginGroup('server')
        settings.setIniCodec('UTF-8')
        host = settings.value(r'host').toString()
        port = settings.value(r'port').toString()
        self.clientCtl.initServerSetting(host,int(port))
        settings.endGroup()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    result = {}
    dialog = LoginDialog(result)
    dialog.exec_()
    print result
    #sys.exit(app.exec_())