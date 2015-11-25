# -*- coding:utf8 -*-
import re
import sys
import os
from PyQt4 import QtCore, QtGui, uic

qtCreatorFile = "rdcD.ui"

Ui_QDialog, QtBaseClass = uic.loadUiType(qtCreatorFile)


class RdcCtl():

    def __init__(self):
        self.defaultContent=''
        self.regixMap={}

    def initDefaultContent(self,path):
        self.defaultContent = open(path, 'r+').read()

    def setRegixMap(self,setStr):
        regix=re.compile('(?<='+setStr+').*')
        self.regixMap[setStr]=regix

    def getValueByKeyStr(self,setStr):
        if setStr not in self.regixMap.keys():
            self.setRegixMap(setStr)
        return self.regixMap[setStr].findall(self.defaultContent)

    def setContentAfterRe(self,setStr,val):
        if setStr not in self.regixMap.keys():
            self.setRegixMap(setStr)
        self.defaultContent = self.regixMap[setStr].sub(val, self.defaultContent)

    def setContentFromOpenFile(self,keyStr,val):
        if(self.defaultContent.find(keyStr) < 0):
            #self.appendDefautContent(keyStr+val)
            self.defaultContent += keyStr+val+'\n'
        else:
            self.setContentAfterRe(keyStr,val)

    def appendDefautContent(self,valList):
        for i in range(0,len(valList)):
            self.defaultContent += valList[i]+'\n'

    def writeFile(self,path):
        rdpFile = open(path, 'w')
        rdpFile.write(self.defaultContent)