# -*- coding:utf8 -*-
import re
import sys
import os
from PyQt4 import QtCore, QtGui, uic
from control import rdcCtl
import win32api
import ctypes
from control import public

curdir = public.cur_file_dir()

qtCreatorFile = curdir+"/ui/rdcD.ui"

Ui_QDialog, QtBaseClass = uic.loadUiType(qtCreatorFile)


class RDPDialog(QtGui.QDialog, Ui_QDialog):

    def __init__(self,rdpIndex,info):
        QtGui.QDialog.__init__(self)
        Ui_QDialog.__init__(self)
        self.setupUi(self)
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("rdcCtl")
        self.rdpIndex=rdpIndex
        self.info=info
        self.cmpLineEdit.setText(self.info['ip'])
        self.accountTxtLable.setText(self.info['userName'])
        self.cmpLineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.cmpLineEdit_2.setEchoMode(QtGui.QLineEdit.Password);
        self.cmpLineEdit.setReadOnly(True)
        self.cmpLineEdit_2.setReadOnly(True)
        self.statusLabel.setStyleSheet("color:#ff0000")
        self.statusLabel_2.setStyleSheet("color:#ff0000")
        self.optionWidget.hide()
        self.optionToolBtn.clicked.connect(self.toOptionDWidget)
        self.optionToolBtn_2.clicked.connect(self.toDefaultDWidget)
        self.connBtn.clicked.connect(self.defaultConnectFunc)
        self.connBtn_2.clicked.connect(self.optionConnectFunc)
        # self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        self.openBtn.clicked.connect(self.openFile)
        self.saveBtn.clicked.connect(self.saveFile)
        self.saveasBtn.clicked.connect(self.saveAsFile)

        self.connTypeComboBox.currentIndexChanged.connect(self.connTypeChanged)
        self.horizontalSlider.valueChanged.connect(self.deskSizeChanged)

        self.initEquipConent()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(curdir+'/img/rdc.ico'),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.initDeskSize()

        self.resize(391, 151)
        self.defaultRdpPath = os.getcwd() + "\\config\\.tmpRdp.rdp"
        self.tmpFileFolder = os.getcwd() + '\\tmp'
        self.rdpFilePath = ''
        self.tmpFilePath = ''
        self.fromDefault = True

        self.rdcCtl = rdcCtl.RdcCtl()

        self.initTmpFolder()

    def initTmpFolder(self):
        if(os.path.isdir(self.tmpFileFolder)):
            pass
        else:
            os.mkdir(self.tmpFileFolder)

    def initEquipConent(self):
        self.drives = QtGui.QTreeWidgetItem(self.equipTreeWidget)
        self.drives.setText(0, u'驱动器')
        self.drives.setFlags(self.drives.flags() |
                             QtCore.Qt.ItemIsUserCheckable)
        self.drives.setCheckState(0, QtCore.Qt.Unchecked)
        p1 = re.compile('\s')
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
                #itemDive.setCheckState(0, QtCore.Qt.Unchecked)
                self.drives.addChild(itemDive)

        dynamicDrive = QtGui.QTreeWidgetItem(self.drives)
        dynamicDrive.setText(0, u'稍后插入的驱动器')
        dynamicDrive.setFlags(dynamicDrive.flags() |
                              QtCore.Qt.ItemIsUserCheckable)
        #dynamicDrive.setCheckState(0, QtCore.Qt.Unchecked)
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
        #dynamicDevice.setCheckState(0, QtCore.Qt.Unchecked)
        self.equipTreeWidget.itemClicked.connect(self.equipClicked)
        # self.devices.itemChanged.connect(self.equipClicked)

    def initDeskSize(self):
        self.initMetics()
        size = len(self.metricsMap)
        self.horizontalSlider.setRange(0, size)

        self.horizontalSlider.setValue(size)
        self.deskSizeLabel.setText(u'   全屏')

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

    def connTypeChanged(self, index):
        index = self.connTypeComboBox.currentIndex()
        if index == 0:
            self.backCheckBox.setCheckState(QtCore.Qt.Unchecked)
            self.fontCheckBox.setCheckState(QtCore.Qt.Unchecked)
            self.backCssCheckBox.setCheckState(QtCore.Qt.Unchecked)
            self.dragCheckBox.setCheckState(QtCore.Qt.Unchecked)
            self.menuCheckBox.setCheckState(QtCore.Qt.Unchecked)
            self.viewCheckBox.setCheckState(QtCore.Qt.Unchecked)
            self.bitMapCheckBox.setCheckState(QtCore.Qt.Checked)
        elif index == 1:
            self.backCheckBox.setCheckState(QtCore.Qt.Unchecked)
            self.fontCheckBox.setCheckState(QtCore.Qt.Unchecked)
            self.backCssCheckBox.setCheckState(QtCore.Qt.Unchecked)
            self.dragCheckBox.setCheckState(QtCore.Qt.Unchecked)
            self.menuCheckBox.setCheckState(QtCore.Qt.Unchecked)
            self.viewCheckBox.setCheckState(QtCore.Qt.Checked)
            self.bitMapCheckBox.setCheckState(QtCore.Qt.Checked)
        elif index == 2 or index == 3:
            self.backCheckBox.setCheckState(QtCore.Qt.Unchecked)
            self.fontCheckBox.setCheckState(QtCore.Qt.Unchecked)
            self.backCssCheckBox.setCheckState(QtCore.Qt.Checked)
            self.dragCheckBox.setCheckState(QtCore.Qt.Unchecked)
            self.menuCheckBox.setCheckState(QtCore.Qt.Unchecked)
            self.viewCheckBox.setCheckState(QtCore.Qt.Checked)
            self.bitMapCheckBox.setCheckState(QtCore.Qt.Checked)
        else:
            self.backCheckBox.setCheckState(QtCore.Qt.Checked)
            self.fontCheckBox.setCheckState(QtCore.Qt.Checked)
            self.backCssCheckBox.setCheckState(QtCore.Qt.Checked)
            self.dragCheckBox.setCheckState(QtCore.Qt.Checked)
            self.menuCheckBox.setCheckState(QtCore.Qt.Checked)
            self.viewCheckBox.setCheckState(QtCore.Qt.Checked)
            self.bitMapCheckBox.setCheckState(QtCore.Qt.Checked)

    def deskSizeChanged(self, event):
        if(event == len(self.metricsMap)):
            self.deskSizeLabel.setText(u'   全屏')
        else:
            sizeLabel = str(self.metricsMap[event][
                            0]) + ' * ' + str(self.metricsMap[event][1]) + u'像素'
            self.deskSizeLabel.setText(sizeLabel)

    def toOptionDWidget(self):
        # self.tmpFilePath=os.getcwd()+'\\tmp\\rdp_'+self.cmpLineEdit_2.text()+'.rdp'
        text=str(self.cmpLineEdit.text())
        if len(text):
            self.cmpLineEdit_2.setText(text)
        self.accountTxtLable_2.setText(self.accountTxtLable.text())
        self.resize(411, 346)
        self.defaultWidget.hide()
        self.optionWidget.show()
        # self.adjustSize()

    def toDefaultDWidget(self):
        text=str(self.cmpLineEdit_2.text())
        if len(text):
            self.cmpLineEdit.setText(text)
        self.resize(391, 151)
        self.optionWidget.hide()
        self.defaultWidget.show()
        # self.adjustSize()

    def runCommand(self, cmdStr):
        public.userConnVm(self.rdpIndex.clientCtl,str(cmdStr),self.rdpIndex.userName,self.info)
        # stdouterr = os.popen4(str(cmdStr))[1].read()

    def defaultConnectFunc(self):
        if(public.isValidIP(self.cmpLineEdit.text())):
            self.statusLabel.clear()
            self.runCommand('mstsc /v:' + self.cmpLineEdit.text())
        else:
            self.statusLabel.setText(u'请输入合法的IP地址')

    def optionConnectFunc(self):
        if(public.isValidIP(self.cmpLineEdit_2.text())):
            self.updataRdpFile()
            self.statusLabel_2.clear()
            self.runCommand('mstsc ' + self.tmpFilePath)
        else:
            self.statusLabel_2.setText(u'请输入合法的IP地址')

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
                self.tmpFilePath = self.tmpFileFolder + '\\rdp_' + \
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
            self.tmpFilePath = self.tmpFileFolder + '\\rdp_' + \
                self.cmpLineEdit_2.text() + '.rdp'
        if(self.fromDefault):
            self.saveTmpFileFromDefault()
        else:
            self.saveTmpFileFromRDP()
        self.rdcCtl.writeFile(self.tmpFilePath)

    def saveTmpFileFromDefault(self):
        self.rdcCtl.initDefaultContent(self.defaultRdpPath)
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

        content.append('session bpp:i:' +
                       str(self.getColorComVal(self.colorComboBox.currentIndex())))
        content.append('connection type:i:' +
                       str(self.connTypeComboBox.currentIndex() + 1))
        content.append('disable wallpaper:i:0' if self.backCheckBox.checkState(
        ) == QtCore.Qt.Checked else 'disable wallpaper:i:1')
        content.append('allow font smoothing:i:1' if self.fontCheckBox.checkState(
        ) == QtCore.Qt.Checked else 'allow font smoothing:i:0')
        content.append('allow desktop composition:i:1' if self.backCssCheckBox.checkState(
        ) == QtCore.Qt.Checked else 'allow desktop composition:i:0')
        content.append('disable full window drag:i:0' if self.dragCheckBox.checkState(
        ) == QtCore.Qt.Checked else 'disable full window drag:i:1')
        content.append('disable menu anims:i:0' if self.menuCheckBox.checkState(
        ) == QtCore.Qt.Checked else 'disable menu anims:i:1')
        content.append('disable themes:i:0' if self.viewCheckBox.checkState(
        ) == QtCore.Qt.Checked else 'disable themes:i:1')
        content.append('bitmapcachepersistenable:i:1' if self.bitMapCheckBox.checkState(
        ) == QtCore.Qt.Checked else 'bitmapcachepersistenable:i:0')

        index = self.horizontalSlider.value()
        if index == len(self.metricsMap):
            index = index - 1
        content.append('desktopwidth:i:' + str(self.metricsMap[index][0]))
        content.append('desktopheight:i:' + str(self.metricsMap[index][1]))

        self.rdcCtl.appendDefautContent(content)

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

        self.rdcCtl.setContentFromOpenFile(
            'session bpp:i:', str(self.getColorComVal(self.colorComboBox.currentIndex())))

        self.rdcCtl.setContentFromOpenFile(
            'connection type:i:', str(self.connTypeComboBox.currentIndex() + 1))

        self.rdcCtl.setContentFromOpenFile(
            'disable wallpaper:i:', '0' if self.backCheckBox.checkState() == QtCore.Qt.Checked else '1')
        self.rdcCtl.setContentFromOpenFile(
            'allow font smoothing:i:', '1' if self.fontCheckBox.checkState() == QtCore.Qt.Checked else '0')
        self.rdcCtl.setContentFromOpenFile(
            'allow desktop composition:i:', '1' if self.backCssCheckBox.checkState() == QtCore.Qt.Checked else '0')
        self.rdcCtl.setContentFromOpenFile(
            'disable full window drag:i:', '0' if self.dragCheckBox.checkState() == QtCore.Qt.Checked else '1')
        self.rdcCtl.setContentFromOpenFile(
            'disable menu anims:i:', '0' if self.menuCheckBox.checkState() == QtCore.Qt.Checked else '1')
        self.rdcCtl.setContentFromOpenFile(
            'disable themes:i:', '0' if self.viewCheckBox.checkState() == QtCore.Qt.Checked else '1')
        self.rdcCtl.setContentFromOpenFile(
            'bitmapcachepersistenable:i:', '1' if self.bitMapCheckBox.checkState() == QtCore.Qt.Checked else '0')

        index = self.horizontalSlider.value()
        if index == len(self.metricsMap):
            index = index - 1
        self.rdcCtl.setContentFromOpenFile(
            'desktopwidth:i:', str(self.metricsMap[index][0]))
        self.rdcCtl.setContentFromOpenFile(
            'desktopheight:i:', str(self.metricsMap[index][1]))

    def updateView(self):
        self.rdcCtl.initDefaultContent(self.rdpFilePath)
        add = self.rdcCtl.getValueByKeyStr('full address:s:')
        if(add is not None):
            self.cmpLineEdit_2.setText(add)

        disConnBar = self.rdcCtl.getValueByKeyStr('displayconnectionbar:i:')
        if(disConnBar is not None):
            if(str(self.connBarCheckBox.checkState()) != disConnBar):
                self.connBarCheckBox.setCheckState(
                    QtCore.Qt.Unchecked if disConnBar == '0' else QtCore.Qt.Checked)

        printChkB = self.rdcCtl.getValueByKeyStr('redirectprinters:i:')
        if(printChkB is not None):
            if(str(self.printCheckBox.checkState()) != printChkB):
                self.printCheckBox.setCheckState(
                    QtCore.Qt.Unchecked if printChkB == '0' else QtCore.Qt.Checked)

        cliChkB = self.rdcCtl.getValueByKeyStr('redirectclipboard:i:')
        if(cliChkB is not None):
            if(str(self.cliCheckBox.checkState()) != cliChkB):
                self.cliCheckBox.setCheckState(
                    QtCore.Qt.Unchecked if cliChkB == '0' else QtCore.Qt.Checked)

        reconnChkB = self.rdcCtl.getValueByKeyStr(
            'autoreconnection enabled:i:')
        if(reconnChkB is not None):
            if(str(self.reconnCheckBox.checkState()) != reconnChkB):
                self.reconnCheckBox.setCheckState(
                    QtCore.Qt.Unchecked if reconnChkB == '0' else QtCore.Qt.Checked)

        authlevelComB = self.rdcCtl.getValueByKeyStr('authentication level:i:')
        if(authlevelComB is not None):
            curIndex = int(authlevelComB)
            if(self.authComboBox.currentIndex() != curIndex):
                self.authComboBox.setCurrentIndex(curIndex)

        audioCaptureComB = self.rdcCtl.getValueByKeyStr('audiocapturemode:i:')
        if(audioCaptureComB is not None):
            curIndex = int(audioCaptureComB)
            if(self.audioCaptureComBox.currentIndex() != curIndex):
                self.audioCaptureComBox.setCurrentIndex(curIndex)

        audioPlayComB = self.rdcCtl.getValueByKeyStr('audiomode:i:')
        if(audioPlayComB is not None):
            curIndex = int(audioPlayComB)
            if(self.audioPlayComBox.currentIndex() != curIndex):
                self.audioPlayComBox.setCurrentIndex(curIndex)

        keyComB = self.rdcCtl.getValueByKeyStr('keyboardhook:i:')
        if(keyComB is not None):
            curIndex = int(keyComB)
            if(self.keyComBox.currentIndex() != curIndex):
                self.keyComBox.setCurrentIndex(curIndex)

        smartCardChkB = self.rdcCtl.getValueByKeyStr('redirectsmartcards:i:')
        if(smartCardChkB is not None):
            if(str(self.smartCardCheckBox.checkState()) != smartCardChkB):
                self.smartCardCheckBox.setCheckState(
                    QtCore.Qt.Unchecked if smartCardChkB == '0' else QtCore.Qt.Checked)

        portChkB = self.rdcCtl.getValueByKeyStr('redirectcomports:i:')
        if(portChkB is not None):
            if(str(self.portCheckBox.checkState()) != portChkB):
                self.portCheckBox.setCheckState(
                    QtCore.Qt.Unchecked if portChkB == '0' else QtCore.Qt.Checked)

        drivesChkB = self.rdcCtl.getValueByKeyStr('drivestoredirect:s:')
        if(drivesChkB is not None):
            if(drivesChkB == '*'):
                if(self.drives.checkState(0) == QtCore.Qt.Unchecked):
                    self.drives.setCheckState(0, QtCore.Qt.Checked)
                    self.setQTreeWidgetItems(self.drives, QtCore.Qt.Checked)
        else:
            if(self.drives.checkState(0) == QtCore.Qt.Checked):
                self.drives.setCheckState(0, QtCore.Qt.Unchecked)
                self.setQTreeWidgetItems(self.drives, QtCore.Qt.Unchecked)

        devicesChkB = self.rdcCtl.getValueByKeyStr('devicestoredirect:s:')
        if(devicesChkB is not None):
            if(devicesChkB == '*'):
                if(self.devices.checkState(0) == QtCore.Qt.Unchecked):
                    self.devices.setCheckState(0, QtCore.Qt.Checked)
                    self.setQTreeWidgetItems(self.devices, QtCore.Qt.Checked)
        else:
            if(self.devices.checkState(0) == QtCore.Qt.Checked):
                self.devices.setCheckState(0, QtCore.Qt.Unchecked)
                self.setQTreeWidgetItems(self.devices, QtCore.Qt.Unchecked)

        colorComB = self.rdcCtl.getValueByKeyStr('session bpp:i:')
        if(colorComB is not None):
            curVal = int(colorComB)
            if(curVal != self.getColorComVal(self.colorComboBox.currentIndex())):
                self.colorComboBox.setCurrentIndex((curVal - 16) / 8 + 1)

        connTypeComB = self.rdcCtl.getValueByKeyStr('connection type:i:')
        if(connTypeComB is not None):
            curIndex = int(connTypeComB) - 1
            if(curIndex != self.connTypeComboBox.currentIndex()):
                self.connTypeComboBox.setCurrentIndex(curIndex)

        backChkB = self.rdcCtl.getValueByKeyStr('disable wallpaper:i:')
        if(backChkB is not None):
            if((self.backCheckBox.checkState() == QtCore.Qt.Checked and backChkB == '1')or (self.backCheckBox.checkState() == QtCore.Qt.Unchecked and backChkB == '0')):
                self.backCheckBox.setCheckState(
                    QtCore.Qt.Checked if backChkB == '0' else QtCore.Qt.Unchecked)

        fontChkB = self.rdcCtl.getValueByKeyStr('allow font smoothing:i:')
        if(fontChkB is not None):
            if((self.fontCheckBox.checkState() == QtCore.Qt.Checked and fontChkB == '0')or (self.fontCheckBox.checkState() == QtCore.Qt.Unchecked and fontChkB == '1')):
                self.fontCheckBox.setCheckState(
                    QtCore.Qt.Checked if fontChkB == '1' else QtCore.Qt.Unchecked)
        layoutChkB = self.rdcCtl.getValueByKeyStr(
            'allow desktop composition:i:')
        if(layoutChkB is not None):
            if((self.backCssCheckBox.checkState() == QtCore.Qt.Checked and layoutChkB == '0')or (self.backCssCheckBox.checkState() == QtCore.Qt.Unchecked and layoutChkB == '1')):
                self.backCssCheckBox.setCheckState(
                    QtCore.Qt.Checked if layoutChkB == '1' else QtCore.Qt.Unchecked)

        dragChkB = self.rdcCtl.getValueByKeyStr('disable full window drag:i:')
        if(dragChkB is not None):
            if((self.dragCheckBox.checkState() == QtCore.Qt.Checked and dragChkB == '1')or (self.dragCheckBox.checkState() == QtCore.Qt.Unchecked and dragChkB == '0')):
                self.dragCheckBox.setCheckState(
                    QtCore.Qt.Checked if dragChkB == '0' else QtCore.Qt.Unchecked)

        menuChkB = self.rdcCtl.getValueByKeyStr('disable menu anims:i:')
        if(menuChkB is not None):
            if((self.menuCheckBox.checkState() == QtCore.Qt.Checked and menuChkB == '1')or (self.menuCheckBox.checkState() == QtCore.Qt.Unchecked and menuChkB == '0')):
                self.menuCheckBox.setCheckState(
                    QtCore.Qt.Checked if menuChkB == '0' else QtCore.Qt.Unchecked)

        viewChkB = self.rdcCtl.getValueByKeyStr('disable themes:i:')
        if(viewChkB is not None):
            if((self.viewCheckBox.checkState() == QtCore.Qt.Checked and viewChkB == '1')or (self.viewCheckBox.checkState() == QtCore.Qt.Unchecked and viewChkB == '0')):
                self.viewCheckBox.setCheckState(
                    QtCore.Qt.Checked if viewChkB == '0' else QtCore.Qt.Unchecked)

        bitMapChkB = self.rdcCtl.getValueByKeyStr(
            'bitmapcachepersistenable:i:')
        if(bitMapChkB is not None):
            if((self.bitMapCheckBox.checkState() == QtCore.Qt.Checked and bitMapChkB == '0')or (self.bitMapCheckBox.checkState() == QtCore.Qt.Unchecked and bitMapChkB == '1')):
                self.bitMapCheckBox.setCheckState(
                    QtCore.Qt.Checked if bitMapChkB == '1' else QtCore.Qt.Unchecked)

        wid = self.rdcCtl.getValueByKeyStr(
            'desktopwidth:i:')
        hig = self.rdcCtl.getValueByKeyStr(
            'desktopheight:i:')
        if wid is not None and hig is not None:
            val = int(wid) + int(hig)
            if val in self.metricsInvertMap.keys():
                self.horizontalSlider.setValue(self.metricsInvertMap[val])

    def getColorComVal(self, index):  # 0:15 1:16 2:24 3:32
        if(index == 0):
            return 15
        else:
            return 15 + 1 + (index - 1) * 8

    def getMinIndexUp(self, val, numSet):
        low = 0
        high = len(numSet) - 1
        while low <= high:
            mid = (low + high) / 2
            midVal = numSet[mid]
            if(midVal < val):
                low = mid + 1
            elif midVal > val:
                high = mid - 1
            else:
                return mid
        return low - 1

    def initMetics(self):
        width = []
        width.append(640)
        width.append(800)
        width.append(1024)
        width.append(1280)
        width.append(1366)
        width.append(1440)
        width.append(1600)
        width.append(1680)
        width.append(1920)
        height = []
        height.append(480)
        height.append(600)
        height.append(720)
        height.append(768)
        height.append(800)
        height.append(900)
        height.append(1024)
        height.append(1050)
        height.append(1080)

        wi = win32api.GetSystemMetrics(0)
        hi = win32api.GetSystemMetrics(1)
        wIndex = self.getMinIndexUp(wi, width)
        hIndex = self.getMinIndexUp(hi, height)
        self.metricsMap = []
        self.metricsInvertMap = {}
        for i in range(0, wIndex + 1):
            if(i <= hIndex):
                self.metricsMap.append([width[i], height[i]])
                self.metricsInvertMap[width[i] + height[i]] = i
            else:
                self.metricsMap.append([width[i], height[hIndex]])
                self.metricsInvertMap[width[i] + height[hIndex]] = i
        if wIndex < hIndex:
            for i in(wIndex + 1, hIndex):
                self.metricsMap.append([width[wIndex], height[i]])
                self.metricsInvertMap[width[wIndex] + height[i]] = i

        if(width[wIndex] != wi or height[hIndex] != hi):
            self.metricsMap.append([wi, hi])
            self.metricsInvertMap[wi + hi] = len(self.metricsMap - 1)

    def setQTreeWidgetItems(self, item, state):
        itemSize = item.childCount()
        for i in range(0, itemSize):
            item.child(i).setCheckState(0, state)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    dialog = RDPDialog('192.168.160.18','hi')
    dialog.show()
    sys.exit(app.exec_())
