# -*- coding:utf8 -*-
class Config():

    def __init__(self):
        self.roleMap={}
        self.roleMap['管理员']='admin'
        self.roleMap['普通用户']='user'
        self.roleMap['admin']='管理员'
        self.roleMap['user']='普通用户'

    def getRoleMap(self):
    	return self.roleMap