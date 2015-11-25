# -*- coding:utf8 -*-
import re
import sys
import os
from PyQt4 import QtCore, QtGui, uic
import rdcCtl

qtCreatorFile = "rdcD.ui"

Ui_QDialog, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyDialog(QtGui.QDialog, Ui_QDialog):

    def __init__(self):
        QtGui.QDialog.__init__(self)
        Ui_QDialog.__init__(self)
        self.setupUi(self)
        # self.connBtn.clicked.connect(self.connectFunc)
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

        self.initEquipConent()

        self.resize(391, 151)

        self.rdpFilePath = ''
        self.tmpFilePath = ''
        self.fromDefault = True

        self.rdcCtl = rdcCtl.RdcCtl()
        #self.setGeometry(300, 300, 250, 150)
        # self.connect(self.accountEdit, SIGNAL("returnPressed(void)"),
        #              self.runCommand

    def initEquipConent(self):
        self.drives = QtGui.QTreeWidgetItem(self.equipTreeWidget)
        self.drives.setText(0, u'驱动器')
        self.drives.setFlags(self.drives.flags() |
                             QtCore.Qt.ItemIsUserCheckable)
        self.drives.setCheckState(0, QtCore.Qt.Unchecked)
        p1=re.compile('\s')
        data = os.popen('wmic logicaldisk  get VolumeName,Name').read()
        dataItem = data.split('\n')
        for i in range(1, len(dataItem)):
            dataItem[i] = p1.sub('', dataItem[i])
            item = dataItem[i].split(':')
            length = len(item)
            if(length > 1):
                itemStr = item[1] + ' (' + item[0] + ':)'
                itemDive = QtGui.QTreeWidgetItem(self.drives)
                itemDive.setText(0, itemStr.decode('GBK'))
                itemDive.setFlags(itemDive.flags() |
                                  QtCore.Qt.ItemIsUserCheckable)
                itemDive.setCheckState(0, QtCore.Qt.Unchecked)
                self.drives.addChild(itemDive)

        dynamicDrive = QtGui.QTreeWidgetItem(self.drives)
        dynamicDrive.setText(0, u'稍后插入的驱动器')
        dynamicDrive.setFlags(dynamicDrive.flags() |
                              QtCore.Qt.ItemIsUserCheckable)
        dynamicDrive.setCheckState(0, QtCore.Qt.Unchecked)
        self.drives.addChild(dynamicDrive)

        self.devices = QtGui.QTreeWidgetItem(self.equipTreeWidget)
        self.devices.setText(0, u'其他支持的即插即用(PnP)设备')
        self.devices.setFlags(self.devices.flags() |
                              QtCore.Qt.ItemIsUserCheckable)
        self.devices.setCheckState(0, QtCore.Qt.Unchecked)

        dynamicDevice = QtGui.QTreeWidgetItem(self.devices)
        dynamicDevice.setText(0, u'稍后插入的设备')
        dynamicDevice.setFlags(dynamicDevice.flags() |
                               QtCore.Qt.ItemIsUserCheckable)
        dynamicDevice.setCheckState(0, QtCore.Qt.Unchecked)
        self.equipTreeWidget.itemClicked.connect(self.equipClicked)
        # self.devices.itemChanged.connect(self.equipClicked)

        '''
        model=QtGui.QStandardItemModel(self.equipTreeView)
        item=QtGui.QStandardItem()
        model->appendRow(itemProject);  
        model->setItem(model->indexFromItem(itemProject).row(),1,new QStandardItem(QStringLiteral("项目信息说明")));  
        QStandardItem* itemFolder = new QStandardItem(m_publicIconMap[QStringLiteral("treeItem_folder")],QStringLiteral("文件夹1"));  
        itemProject->appendRow(itemFolder);  
        itemProject->setChild(itemFolder->index().row(),1,new QStandardItem(QStringLiteral("信息说明")));  
        itemFolder = new QStandardItem(m_publicIconMap[QStringLiteral("treeItem_folder")],QStringLiteral("文件夹2"));  
        itemProject->appendRow(itemFolder);  '''

    def equipParentChangeWithChild(self, item):
        length = item.childCount()
        checkedSize = 0
        for i in range(0, length):
            if(item.child(i).checkState(0) == QtCore.Qt.Checked):
                checkedSize += 1
        if(checkedSize == length):
            item.setCheckState(0, QtCore.Qt.Checked)
        elif(checkedSize == 0):
            item.setCheckState(0, QtCore.Qt.Unchecked)
        else:
            item.setCheckState(0, QtCore.Qt.PartiallyChecked)

    def equipClicked(self, item):
        if(isinstance(item.parent(), QtGui.QTreeWidgetItem)):
            self.equipParentChangeWithChild(item.parent())
        self.setQTreeWidgetItems(item, item.checkState(0))

    def toOptionDWidget(self):
        # self.tmpFilePath=os.getcwd()+'\\tmp\\rdp_'+self.cmpLineEdit_2.text()+'.rdp'
        self.resize(411, 346)
        self.defaultWidget.hide()
        self.optionWidget.show()
        # self.adjustSize()

    def toDefaultDWidget(self):
        self.resize(391, 151)
        self.optionWidget.hide()
        self.defaultWidget.show()
        # self.adjustSize()

    def runCommand(self, cmdStr):
        stdouterr = os.popen4(str(cmdStr))[1].read()
        # print '--'+stdouterr+'--'
        # if(len(stdouterr)==0):
        #     self.close()

    def defaultConnectFunc(self):
        if(self.isValidIP(self.cmpLineEdit.text())):
            self.runCommand('mstsc /v:' + self.cmpLineEdit.text())
        else:
            QtGui.QMessageBox.question(
                self, 'Message', u'请输入合法的IP地址', QtGui.QMessageBox.Yes, QtGui.QMessageBox.Yes)

    def optionConnectFunc(self):
        if(self.isValidIP(self.cmpLineEdit_2.text())):
            self.updataRdpFile()
            self.runCommand('mstsc ' + self.tmpFilePath)
        else:
            QtGui.QMessageBox.question(
                self, 'Message', u'请输入合法的IP地址', QtGui.QMessageBox.Yes, QtGui.QMessageBox.Yes)

    def openFile(self):
        fd = QtGui.QFileDialog(self).getOpenFileName()
        if os.path.isfile(fd):
            self.fromDefault = False
            self.rdpFilePath = fd
            self.updateView()

    def saveFile(self):
        if(self.fromDefault):
            self.saveTmpFileFromDefault()
            if(len(self.tmpFilePath) == 0):
                self.tmpFilePath = os.getcwd() + '\\tmp\\rdp_' + \
                    self.cmpLineEdit_2.text() + '.rdp'
            if(len(self.rdpFilePath) == 0):
                self.rdpFilePath = self.tmpFilePath
        else:
            self.saveTmpFileFromRDP()
        self.rdcCtl.writeFile(self.rdpFilePath)

    def saveAsFile(self):
        saveasFilePath = QtGui.QFileDialog(self).getSaveFileName()
        if(len(saveasFilePath) != 0):
            if(self.fromDefault):
                self.rdpFilePath = saveasFilePath
                self.saveTmpFileFromDefault()
            else:
                self.saveTmpFileFromRDP()
                self.rdpFilePath = saveasFilePath
            self.rdcCtl.writeFile(self.rdpFilePath)

    def updataRdpFile(self):
        if(len(self.tmpFilePath) == 0):
            self.tmpFilePath = os.getcwd() + '\\tmp\\rdp_' + \
                self.cmpLineEdit_2.text() + '.rdp'
        if(self.fromDefault):
            self.saveTmpFileFromDefault()
        else:
            self.saveTmpFileFromRDP()
        self.rdcCtl.writeFile(self.tmpFilePath)

    def saveTmpFileFromDefault(self):
        self.rdcCtl.initDefaultContent(self.fromDefault)
        content = []
        content.append('displayconnectionbar:i:1' if self.connBarCheckBox.checkState(
        ) == QtCore.Qt.Checked else 'displayconnectionbar:i:0')
        content.append('redirectprinters:i:1' if self.printCheckBox.checkState(
        ) == QtCore.Qt.Checked else 'redirectprinters:i:0')
        content.append('redirectclipboard:i:1' if self.cliCheckBox.checkState(
        ) == QtCore.Qt.Checked else 'redirectclipboard:i:0')
        content.append('autoreconnection enabled:i:1' if self.reconnCheckBox.checkState(
        ) == QtCore.Qt.Checked else 'autoreconnection enabled:i:0')
        content.append('authentication level:i:' +
                       str(self.authComboBox.currentIndex()))
        content.append('authentication level:i:' +
                       str(self.authComboBox.currentIndex()))
        content.append('full address:s:' + str(self.cmpLineEdit_2.text()))
        content.append('audiocapturemode:i:' +
                       str(self.audioCaptureComBox.currentIndex()))
        content.append('audiomode:i:' +
                       str(self.audioPlayComBox.currentIndex()))
        content.append('keyboardhook:i:' + str(self.keyComBox.currentIndex()))
        content.append('redirectsmartcards:i:1' if self.smartCardCheckBox.checkState()
                       == QtCore.Qt.Checked else 'redirectsmartcards:i:0')
        content.append('redirectcomports:i:1' if self.portCheckBox.checkState()
                       == QtCore.Qt.Checked else 'redirectcomports:i:0')
        if(self.drives.checkState(0) == QtCore.Qt.Checked):
            content.append('drivestoredirect:s:*')
        if(self.devices.checkState(0) == QtCore.Qt.Checked):
            content.append('devicestoredirect:s:*')

        self.rdcCtl.appendDefautContent(content)

        '''self.rdcCtl.appendDefautContent('displayconnectionbar:i:1' if self.connBarCheckBox.checkState() == QtCore.Qt.Checked else 'displayconnectionbar:i:0')

        self.rdcCtl.appendDefautContent('redirectprinters:i:1' if self.printCheckBox.checkState() == QtCore.Qt.Checked else 'redirectprinters:i:0')
        
        self.rdcCtl.appendDefautContent('redirectclipboard:i:1' if self.cliCheckBox.checkState() == QtCore.Qt.Checked else 'redirectclipboard:i:0')
        
        self.rdcCtl.appendDefautContent('autoreconnection enabled:i:1' if self.reconnCheckBox.checkState() == QtCore.Qt.Checked else 'autoreconnection enabled:i:0')

        self.rdcCtl.appendDefautContent('authentication level:i:' +str(self.authComboBox.currentIndex()))
        
        self.rdcCtl.appendDefautContent('full address:s:' +str(self.cmpLineEdit_2.text()))
        
        self.rdcCtl.appendDefautContent('audiocapturemode:i:' +str(self.audioCaptureComBox.currentIndex()))
        
        self.rdcCtl.appendDefautContent('audiomode:i:' +str(self.audioPlayComBox.currentIndex()))
        
        self.rdcCtl.appendDefautContent('keyboardhook:i:' +str(self.keyComBox.currentIndex()))

        self.rdcCtl.appendDefautContent('redirectsmartcards:i:1' if self.smartCardCheckBox.checkState()
             == QtCore.Qt.Checked else 'redirectsmartcards:i:0')

        self.rdcCtl.appendDefautContent('redirectcomports:i:1' if self.portCheckBox.checkState()
             == QtCore.Qt.Checked else 'redirectcomports:i:0')

        self.rdcCtl.appendDefautContent('redirectcomports:i:1' if self.portCheckBox.checkState()
             == QtCore.Qt.Checked else 'redirectcomports:i:0')

        if(self.drives.checkState(0) == QtCore.Qt.Checked):
            self.rdcCtl.appendDefautContent('drivestoredirect:s:*')
        if(self.devices.checkState(0) == QtCore.Qt.Checked):
            self.rdcCtl.appendDefautContent('devicestoredirect:s:*')'''

    def saveTmpFileFromRDP(self):
        self.rdcCtl.setContentFromOpenFile('displayconnectionbar:i:', '1' if self.connBarCheckBox.checkState(
        ) == QtCore.Qt.Checked else '0')

        self.rdcCtl.setContentFromOpenFile('redirectprinters:i:', '1' if self.printCheckBox.checkState(
        ) == QtCore.Qt.Checked else '0')

        self.rdcCtl.setContentFromOpenFile('redirectclipboard:i:', '1' if self.cliCheckBox.checkState(
        ) == QtCore.Qt.Checked else '0')

        self.rdcCtl.setContentFromOpenFile('autoreconnection enabled:i:', '1' if self.reconnCheckBox.checkState(
        ) == QtCore.Qt.Checked else '0')

        self.rdcCtl.setContentFromOpenFile(
            'authentication level:i:', str(self.authComboBox.currentIndex()))

        self.rdcCtl.setContentFromOpenFile(
            'full address:s:', str(self.cmpLineEdit_2.text()))

        self.rdcCtl.setContentFromOpenFile(
            'audiocapturemode:i:', str(self.audioCaptureComBox.currentIndex()))

        self.rdcCtl.setContentFromOpenFile(
            'audiomode:i:', str(self.audioPlayComBox.currentIndex()))

        self.rdcCtl.setContentFromOpenFile(
            'keyboardhook:i:', str(self.keyComBox.currentIndex()))

        self.rdcCtl.setContentFromOpenFile('redirectsmartcards:i:', '1' if self.smartCardCheckBox.checkState(
        ) == QtCore.Qt.Checked else '0')

        self.rdcCtl.setContentFromOpenFile('redirectcomports:i:', '1' if self.portCheckBox.checkState(
        ) == QtCore.Qt.Checked else '0')

        self.rdcCtl.setContentFromOpenFile('drivestoredirect:s:', '*' if self.drives.checkState(0
        ) == QtCore.Qt.Checked else '')

        self.rdcCtl.setContentFromOpenFile('devicestoredirect:s:', '*' if self.devices.checkState(0
        ) == QtCore.Qt.Checked else '')

    def updateView(self):
        self.rdcCtl.initDefaultContent(self.rdpFilePath)
        add = self.rdcCtl.getValueByKeyStr('full address:s:')
        if(len(add) > 0):
            self.cmpLineEdit_2.setText(add[0])

        disConnBar = self.rdcCtl.getValueByKeyStr('displayconnectionbar:i:')
        if(len(disConnBar) > 0):
            if(str(self.connBarCheckBox.checkState()) != disConnBar[0]):
                self.connBarCheckBox.setCheckState(QtCore.Qt.Unchecked if disConnBar[
                                                   0] == '0' else QtCore.Qt.Checked)

        printChkB = self.rdcCtl.getValueByKeyStr('redirectprinters:i:')
        if(len(printChkB) > 0):
            if(str(self.printCheckBox.checkState()) != printChkB[0]):
                self.printCheckBox.setCheckState(QtCore.Qt.Unchecked if printChkB[
                                                 0] == '0' else QtCore.Qt.Checked)

        cliChkB = self.rdcCtl.getValueByKeyStr('redirectclipboard:i:')
        if(len(cliChkB) > 0):
            if(str(self.cliCheckBox.checkState()) != cliChkB[0]):
                self.cliCheckBox.setCheckState(QtCore.Qt.Unchecked if cliChkB[
                                               0] == '0' else QtCore.Qt.Checked)

        reconnChkB = self.rdcCtl.getValueByKeyStr(
            'autoreconnection enabled:i:')
        if(len(reconnChkB) > 0):
            if(str(self.reconnCheckBox.checkState()) != reconnChkB[0]):
                self.reconnCheckBox.setCheckState(QtCore.Qt.Unchecked if reconnChkB[
                                                  0] == '0' else QtCore.Qt.Checked)

        authlevelComB = self.rdcCtl.getValueByKeyStr('authentication level:i:')
        if(len(authlevelComB) > 0):
            curIndex = int(authlevelComB[0])
            if(self.authComboBox.currentIndex() != curIndex):
                self.authComboBox.setCurrentIndex(curIndex)

        audioCaptureComB = self.rdcCtl.getValueByKeyStr('audiocapturemode:i:')
        if(len(audioCaptureComB) > 0):
            curIndex = int(audioCaptureComB[0])
            if(self.audioCaptureComBox.currentIndex() != curIndex):
                self.audioCaptureComBox.setCurrentIndex(curIndex)

        audioPlayComB = self.rdcCtl.getValueByKeyStr('audiomode:i:')
        if(len(audioPlayComB) > 0):
            curIndex = int(audioPlayComB[0])
            if(self.audioPlayComBox.currentIndex() != curIndex):
                self.audioPlayComBox.setCurrentIndex(curIndex)

        keyComB = self.rdcCtl.getValueByKeyStr('keyboardhook:i:' )
        if(len(keyComB) > 0):
            curIndex = int(keyComB[0])
            if(self.keyComBox.currentIndex() != curIndex):
                self.keyComBox.setCurrentIndex(curIndex)

        smartCardChkB = self.rdcCtl.getValueByKeyStr('redirectsmartcards:i:')
        if(len(smartCardChkB) > 0):
            if(str(self.smartCardCheckBox.checkState()) != smartCardChkB[0]):
                self.smartCardCheckBox.setCheckState(QtCore.Qt.Unchecked if smartCardChkB[
                                                     0] == '0' else QtCore.Qt.Checked)

        portChkB = self.rdcCtl.getValueByKeyStr('redirectcomports:i:')
        if(len(portChkB) > 0):
            if(str(self.portCheckBox.checkState()) != portChkB[0]):
                self.portCheckBox.setCheckState(QtCore.Qt.Unchecked if portChkB[
                                                0] == '0' else QtCore.Qt.Checked)

        drivesChkB = self.rdcCtl.getValueByKeyStr('drivestoredirect:s:')
        if(len(drivesChkB) > 0):
            if(drivesChkB[0] == '*'):
                if(self.drives.checkState(0) == QtCore.Qt.Unchecked):
                    self.drives.setCheckState(0, QtCore.Qt.Checked)
                    self.setQTreeWidgetItems(self.drives, QtCore.Qt.Checked)
        else:
            if(self.drives.checkState(0) == QtCore.Qt.Checked):
                self.drives.setCheckState(0, QtCore.Qt.Unchecked)
                self.setQTreeWidgetItems(self.drives, QtCore.Qt.Unchecked)

        devicesChkB = self.rdcCtl.getValueByKeyStr('devicestoredirect:s:')
        if(len(devicesChkB) > 0):
            if(devicesChkB[0] == '*'):
                if(self.devices.checkState(0) == QtCore.Qt.Unchecked):
                    self.devices.setCheckState(0, QtCore.Qt.Checked)
                    self.setQTreeWidgetItems(self.devices, QtCore.Qt.Checked)
        else:
            if(self.devices.checkState(0) == QtCore.Qt.Checked):
                self.devices.setCheckState(0, QtCore.Qt.Unchecked)
                self.setQTreeWidgetItems(self.devices, QtCore.Qt.Unchecked)

    def setQTreeWidgetItems(self, item, state):
        itemSize = item.childCount()
        for i in range(0, itemSize):
            item.child(i).setCheckState(0, state)

    '''def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(
            self, 'Message', 'Are you sure to quit?', QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()'''

    def isValidIP(self, ipStr):
        if(len(ipStr) < 8):
            return False
        reip = re.compile(
            '^((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)$')
        return reip.match(ipStr)

    def closeEvent(self, event):
        sys.exit()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    dialog = MyDialog()
    dialog.show()
    sys.exit(app.exec_())
