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
def queryUser(userName):
    msg = {};
    msg['type'] = 'queryUser';
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

def addUser(userName, password,roleName):
    msg = {};
    msg['type'] = 'addUser';
    content = {};
    content['userName']=userName;
    content['password']=password;
    content['role']=roleName;
    msg['content']=content;
    return msg;

def addVm(vmId,userName,vmName,ip):
    msg = {};
    msg['type'] = 'addVm';
    content = {};
    content['vmId']=vmId;
    content['userName']=userName;
    content['vmName']=vmName;
    content['ip']=ip;
    msg['content']=content;
    return msg;

def addUserVm(userName,vmId):
    msg = {};
    msg['type'] = 'addUserVm';
    content = {};
    content['userName']=userName;
    content['vmId']=vmId;
    msg['content']=content;
    return msg;
    
def removeUserVm(vmId):
    msg = {};
    msg['type'] = 'removeUserVm';
    content = {};
    content['vmId']=vmId;
    msg['content']=content;
    return msg;