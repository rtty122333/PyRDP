def authUser(userName, password,roleName, ip):
    msg = {};
    msg['type'] = 'auth';
    content = {};
    content['userName']=userName;
    content['password']=password;
    content['role']=roleName;
    content['ip']=ip;
    msg['content']=content;
    return msg;
def logout(userName,ip):
    msg = {};
    msg['type'] = 'logout';
    content = {};
    content['userName']=userName;
    content['ip']=ip;
    msg['content']=content;
    return msg;
def queryUser(userName):
    msg = {};
    msg['type'] = 'queryUser';
    content = {};
    content['userName']=userName;
    msg['content']=content;
    return msg;
def queryUserInfo(userName):
    msg = {};
    msg['type'] = 'queryUserInfo';
    content = {};
    content['userName']=userName;
    msg['content']=content;
    return msg;
def queryVm(vmId):
    msg = {};
    msg['type'] = 'queryVm';
    content = {};
    content['vmId']=vmId;
    msg['content']=content;
    return msg;
def queryRole(ip):
    msg = {};
    msg['type'] = 'queryRole';
    content = {};
    content['ip']=ip;
    msg['content']=content;
    return msg;

def addUser(adminId,adminIp,userName, password,roleName):
    msg = {};
    msg['type'] = 'addUser';
    content = {};
    content['adminId']=adminId;
    content['adminIp']=adminIp;
    content['userName']=userName;
    content['password']=password;
    content['role']=roleName;
    msg['content']=content;
    return msg;

def addVm(adminId,adminIp,vmId,userName,vmName,ip,pwd):
    msg = {};
    msg['type'] = 'addVm';
    content = {};
    content['adminId']=adminId;
    content['adminIp']=adminIp;
    content['vmId']=vmId;
    content['userName']=userName;
    content['vmName']=vmName;
    content['ip']=ip;
    content['password']=pwd;
    msg['content']=content;
    return msg;

def addUserVm(adminId,adminIp,userName,vmInfo):
    msg = {};
    msg['type'] = 'addUserVm';
    content = {};
    content['adminId']=adminId;
    content['adminIp']=adminIp;
    content['userName']=userName;
    content['vmId']=vmInfo['vmId'];
    content['vmName']=vmInfo['vmName'];
    msg['content']=content;
    return msg;
    
def removeUserVm(adminId,adminIp,vmInfo,userName):
    msg = {};
    msg['type'] = 'removeUserVm';
    content = {};
    content['adminId']=adminId;
    content['adminIp']=adminIp;
    content['vmId']=vmInfo['vmId'];
    content['vmName']=vmInfo['vmName'];
    content['state']=vmInfo['state'];
    content['userName']=userName;
    msg['content']=content;
    return msg;

def userConnVm(ip,userName,vmInfo):
    msg = {};
    msg['type'] = 'userConnVm';
    content = {};
    content['ip']=ip;
    content['userName']=userName;
    content['vmId']=vmInfo['vmId'];
    content['vmName']=vmInfo['vmName'];
    msg['content']=content;
    return msg;

def userDisConnVm(ip,userName,vmInfo):
    msg = {};
    msg['type'] = 'userDisConnVm';
    content = {};
    content['ip']=ip;
    content['userName']=userName;
    content['vmId']=vmInfo['vmId'];
    content['vmName']=vmInfo['vmName'];
    msg['content']=content;
    return msg;