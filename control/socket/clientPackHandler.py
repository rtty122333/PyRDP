def login(userName, password,mac):
    msg = {};
    content = {};
    content['userName']=userName;
    content['password']=password;
    content['mac']=mac;
    msg['content']=content;
    return msg;
def logout(userName,roleName,ip,mac):
    msg = {};
    msg['type'] = 'logout';
    content = {};
    content['userName']=userName;
    content['role']=roleName;
    content['ip']=ip;
    content['mac']=mac;
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

def addUser(adminName,adminIp,adminMac,userName, password,roleName):
    msg = {};
    msg['type'] = 'addUser';
    content = {};
    content['adminName']=adminName;
    content['adminIp']=adminIp;
    content['adminMac']=adminMac;
    content['userName']=userName;
    content['password']=password;
    content['role']=roleName;
    msg['content']=content;
    return msg;

def addVm(adminName,adminIp,adminMac,vmId,userName,vmName,ip,pwd):
    msg = {};
    msg['type'] = 'addVm';
    content = {};
    content['adminName']=adminName;
    content['adminIp']=adminIp;
    content['adminMac']=adminMac;
    content['vmId']=vmId;
    content['userName']=userName;
    content['vmName']=vmName;
    content['ip']=ip;
    content['password']=pwd;
    msg['content']=content;
    return msg;

def addUserVm(adminName,adminIp,adminMac,userName,vmInfo):
    msg = {};
    msg['type'] = 'addUserVm';
    content = {};
    content['adminName']=adminName;
    content['adminIp']=adminIp;
    content['adminMac']=adminMac;
    content['userName']=userName;
    content['vmId']=vmInfo['vmId'];
    content['vmName']=vmInfo['vmName'];
    msg['content']=content;
    return msg;
    
def removeUserVm(adminName,adminIp,adminMac,userName,vmInfo):
    msg = {};
    msg['type'] = 'removeUserVm';
    content = {};
    content['adminName']=adminName;
    content['adminIp']=adminIp;
    content['adminMac']=adminMac;
    content['vmId']=vmInfo['vmId'];
    content['vmName']=vmInfo['vmName'];
    content['state']=vmInfo['state'];
    content['userName']=userName;
    msg['content']=content;
    return msg;

def userConnVm(ip,mac,userName,vmInfo):
    msg = {};
    msg['type'] = 'userConnVm';
    content = {};
    content['ip']=ip;
    content['mac']=mac;
    content['userName']=userName;
    content['vmId']=vmInfo['vmId'];
    content['vmName']=vmInfo['vmName'];
    msg['content']=content;
    return msg;

def userDisConnVm(ip,mac,userName,vmInfo):
    msg = {};
    msg['type'] = 'userDisConnVm';
    content = {};
    content['ip']=ip;
    content['mac']=mac;
    content['userName']=userName;
    content['vmId']=vmInfo['vmId'];
    content['vmName']=vmInfo['vmName'];
    msg['content']=content;
    return msg;