# -*- coding:utf8 -*-
import re
import sys
import os
import shutil
from PyQt4 import QtCore, QtGui, uic

qtCreatorFile = "rdcD.ui"

Ui_QDialog, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyDialog(QtGui.QDialog, Ui_QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        Ui_QDialog.__init__(self)
        self.setupUi(self)
        #self.connBtn.clicked.connect(self.connectFunc)
        self.optionWidget.hide()
        self.optionToolBtn.clicked.connect(self.toOptionDWidget)
        self.optionToolBtn_2.clicked.connect(self.toDefaultDWidget)
        self.connBtn.clicked.connect(self.defaultConnectFunc)
        self.connBtn_2.clicked.connect(self.optionConnectFunc)
        #self.setGeometry(300, 300, 410, 180)
        #self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        self.openBtn.clicked.connect(self.openFile)
        self.saveBtn.clicked.connect(self.saveFile)
        self.saveasBtn.clicked.connect(self.saveAsFile)
        self.displayconnectionbar=QtCore.Qt.Checked
        self.defaultRdpPath=os.getcwd()+"\\.tmpRdp.rdp"
        self.rdpFilePath=''
        self.tmpFilePath=''
        self.saveAsFilePath=''

        #self.setGeometry(300, 300, 250, 150)
        # self.connect(self.accountEdit, SIGNAL("returnPressed(void)"),
        #              self.runCommand
    def toOptionDWidget(self):
        self.tmpFilePath=os.getcwd()+'\\tmp\\rdp_'+self.cmpLineEdit_2.text()+'.rdp'
        self.resize(411,346)
        self.defaultWidget.hide()
        self.optionWidget.show()
        #self.adjustSize()
            
    def toDefaultDWidget(self):
        self.resize(391,151)
        self.optionWidget.hide()
        self.defaultWidget.show()
        #self.adjustSize()
            

    def runCommand(self,cmdStr):
        stdouterr = os.popen4(str(cmdStr))[1].read()
        #self.te.setText(stdouterr)
        #os.popen(cmd)
        #conn = QtGui.QMessageBox.question(self,'Message','You are connecting server '+self.cmpEdit.text()+'/'+self.accountEdit.text(),QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,QtGui.QMessageBox.No)
    
    def defaultConnectFunc(self):
        if(self.isValidIP(self.cmpLineEdit.text())):
            self.runCommand('mstsc /v:'+self.cmpLineEdit.text())
        else:
            QtGui.QMessageBox.question(self,'Message',u'请输入合法的IP地址',QtGui.QMessageBox.Yes,QtGui.QMessageBox.Yes)
    def optionConnectFunc(self):
        if(self.isValidIP(self.cmpLineEdit_2.text())):
            self.updataRdpFile()
            self.runCommand('mstsc '+self.tmpFilePath)
        else:
            QtGui.QMessageBox.question(self,'Message',u'请输入合法的IP地址',QtGui.QMessageBox.Yes,QtGui.QMessageBox.Yes)
        
    def openFile(self):
        fd = QtGui.QFileDialog(self).getOpenFileName()
        if os.path.isfile(fd):
            self.rdpFilePath = fd
            self.updateView()
    def saveFile(self):
        if(len(self.rdpFilePath)==0):
            self.saveTmpFileFromDefault()
            if(len(self.saveAsFilePath)==0):
                tmpFile = open(self.tmpFilePath, 'w')
            else:
                tmpFile = open(self.saveAsFilePath, 'w')
            tmpFile.write(self.defaultContent)
        else:
            self.saveTmpFileFromRDP()
            rdpFile = open(self.rdpFilePath, 'w')
            rdpFile.write(self.defaultContent)

    def saveAsFile(self):
        saveasFilePath = QtGui.QFileDialog(self).getSaveFileName()
        if(len(saveasFilePath)!=0):
            if(len(self.rdpFilePath)==0):
                self.saveAsFilePath=saveasFilePath
                self.saveTmpFileFromDefault()
                tmpFile = open(self.saveAsFilePath, 'w')
                tmpFile.write(self.defaultContent)
            else:
                self.saveTmpFileFromRDP()
                self.rdpFilePath=saveasFilePath
                rdpFile = open(self.rdpFilePath, 'w')
                rdpFile.write(self.defaultContent)
        
    def updataRdpFile(self):
        if(len(self.rdpFilePath)==0):
            #self.tmpFilePath=os.getcwd()+'\\tmp\\rdp_'+self.cmpLineEdit_2.text()+'.rdp'
            self.saveTmpFileFromDefault()
        else:
            self.tmpFilePath=self.rdpFilePath
            self.saveTmpFileFromRDP()
        tmpFile = open(self.tmpFilePath, 'w')
        tmpFile.write(self.defaultContent)

    def saveTmpFileFromDefault(self):
        self.defaultContent=open(self.defaultRdpPath,'r+').read()
        if self.connBarCheckBox.checkState()==QtCore.Qt.Checked:
            self.defaultContent+='displayconnectionbar:i:1\n'
        else:
            self.defaultContent+='displayconnectionbar:i:0\n'
        if self.printCheckBox.checkState()==QtCore.Qt.Checked:
            self.defaultContent+='redirectprinters:i:1\n'
        else:
            self.defaultContent+='redirectprinters:i:0\n'
        if self.cliCheckBox.checkState()==QtCore.Qt.Checked:
            self.defaultContent+='redirectclipboard:i:1\n'
        else:
            self.defaultContent+='redirectclipboard:i:0\n'
        if self.reconnCheckBox.checkState()==QtCore.Qt.Checked:
            self.defaultContent+='autoreconnection enabled:i:1\n'
        else:
            self.defaultContent+='autoreconnection enabled:i:0\n'
        self.defaultContent+='authentication level:i:'+str(self.authComboBox.currentIndex())+'\n'
        self.defaultContent+='full address:s:'+str(self.cmpLineEdit_2.text())+'\n'
    def saveTmpFileFromRDP(self):
        if(self.defaultContent.find('displayconnectionbar:i:')<0):
            self.defaultContent+='displayconnectionbar:i:1' if self.connBarCheckBox.checkState()==QtCore.Qt.Checked else 'displayconnectionbar:i:0'
        else:
            self.disConnBarRe.sub('1' if self.connBarCheckBox.checkState()==QtCore.Qt.Checked else '0',self.defaultContent)
        if(self.defaultContent.find('redirectprinters:i:')<0):
            self.defaultContent+='redirectprinters:i:1' if self.printCheckBox.checkState()==QtCore.Qt.Checked else 'redirectprinters:i:0'
        else:
            self.printRe.sub('1' if self.printCheckBox.checkState()==QtCore.Qt.Checked else '0',self.defaultContent)
        if(self.defaultContent.find('redirectclipboard:i:')<0):
            self.defaultContent+='redirectclipboard:i:1' if self.cliCheckBox.checkState()==QtCore.Qt.Checked else 'redirectclipboard:i:0'
        else:
            self.cliRe.sub('1' if self.cliCheckBox.checkState()==QtCore.Qt.Checked else '0',self.defaultContent)
        if(self.defaultContent.find('autoreconnection enabled:i:')<0):
            self.defaultContent+='autoreconnection enabled:i:1' if self.reconnCheckBox.checkState()==QtCore.Qt.Checked else 'autoreconnection enabled:i:0'
        else:
            self.reconnRe.sub('1' if self.reconnCheckBox.checkState()==QtCore.Qt.Checked else '0',self.defaultContent)
        if(self.defaultContent.find('authentication level:i:')<0):
            self.defaultContent+='authentication level:i:'+self.authComboBox.currentIndex()
        else:
            self.authlevelRe.sub(str(self.authComboBox.currentIndex()),self.defaultContent)
        if(self.defaultContent.find('full address:s:')<0):
            self.defaultContent+='full address:s:'+self.cmpLineEdit_2.text()
        else:
            self.addressRe.sub(str(self.cmpLineEdit_2.text()),self.defaultContent)
    
    def updateView(self):
        self.defaultContent = open(self.rdpFilePath,'r+').read()
        print self.defaultContent
        self.addressRe=re.compile('(?<=full\\saddress:s:).*')
        add= self.addressRe.findall(self.defaultContent)
        if(len(add)>0):
            self.cmpLineEdit_2.setText(add[0])

        self.disConnBarRe=re.compile('(?<=displayconnectionbar:i:).*')
        disConnBar= self.disConnBarRe.findall(self.defaultContent)
        if(len(disConnBar)>0):
            if(str(self.connBarCheckBox.checkState())!=disConnBar[0]):
                self.connBarCheckBox.setCheckState(QtCore.Qt.Unchecked if disConnBar[0]=='0' else QtCore.Qt.Checked)

        self.printRe=re.compile('(?<=redirectprinters:i:).*')
        printChkB= self.printRe.findall(self.defaultContent)
        if(len(printChkB)>0):
            if(str(self.printCheckBox.checkState())!=printChkB[0]):
                self.printCheckBox.setCheckState(QtCore.Qt.Unchecked if printChkB[0]=='0' else QtCore.Qt.Checked)

        self.cliRe=re.compile('(?<=redirectclipboard:i:).*')
        cliChkB= self.cliRe.findall(self.defaultContent)
        if(len(cliChkB)>0):
            if(str(self.cliCheckBox.checkState())!=cliChkB[0]):
                self.cliCheckBox.setCheckState(QtCore.Qt.Unchecked if cliChkB[0]=='0' else QtCore.Qt.Checked)

        self.reconnRe=re.compile('(?<=autoreconnection\\senabled:i:).*')
        reconnChkB= self.reconnRe.findall(self.defaultContent)
        if(len(reconnChkB)>0):
            if(str(self.reconnCheckBox.checkState())!=reconnChkB[0]):
                self.reconnCheckBox.setCheckState(QtCore.Qt.Unchecked if reconnChkB[0]=='0' else QtCore.Qt.Checked)

        self.authlevelRe=re.compile('(?<=authentication\\slevel:i:).*')
        authlevelComB= self.authlevelRe.findall(self.defaultContent)
        if(len(authlevelComB)>0):
            curIndex=int(authlevelComB[0])
            if(self.authComboBox.currentIndex()!=curIndex):
                self.authComboBox.setCurrentIndex(curIndex)

    def closeEvent(self,event):
        reply = QtGui.QMessageBox.question(self,'Message','Are you sure to quit?',QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,QtGui.QMessageBox.No)
        
        if reply==QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    def isValidIP(self,ipStr):
        if(len(ipStr)<8):
            return False
        reip  = re.compile('^((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)$')
        return reip.match(ipStr)

    

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    dialog = MyDialog()
    dialog.show()
    sys.exit(app.exec_())
