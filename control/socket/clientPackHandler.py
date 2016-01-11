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
def logout(userId,ip):
    msg = {};
    msg['type'] = 'logout';
    content = {};
    content['userId']=userId;
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
def queryUserInfo(userId):
    msg = {};
    msg['type'] = 'queryUserInfo';
    content = {};
    content['userId']=userId;
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

def addVm(adminId,adminIp,vmId,userName,vmName,ip):
    msg = {};
    msg['type'] = 'addVm';
    content = {};
    content['adminId']=adminId;
    content['adminIp']=adminIp;
    content['vmId']=vmId;
    content['userName']=userName;
    content['vmName']=vmName;
    content['ip']=ip;
    msg['content']=content;
    return msg;

def addUserVm(adminId,adminIp,userId,vmId):
    msg = {};
    msg['type'] = 'addUserVm';
    content = {};
    content['adminId']=adminId;
    content['adminIp']=adminIp;
    content['userId']=userId;
    content['vmId']=vmId;
    msg['content']=content;
    return msg;
    
def removeUserVm(adminId,adminIp,vmId,state,userId):
    msg = {};
    msg['type'] = 'removeUserVm';
    content = {};
    content['adminId']=adminId;
    content['adminIp']=adminIp;
    content['vmId']=vmId;
    content['state']=state;
    content['userId']=userId;
    msg['content']=content;
    return msg;