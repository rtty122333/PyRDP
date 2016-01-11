import re

def isValidIP(ipStr):
    if(len(ipStr) < 8):
        return False
    reip = re.compile(
        '^((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)$')
    return reip.match(ipStr)
