import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from User_Data import userData
import hashlib

def check_user(name,password):
    # print(name," ",password)
    line=name+password
    key = hashlib.sha224(line.encode('utf-8')).hexdigest() #hash(name+password)
    hashname = hashlib.sha224(name.encode('utf-8')).hexdigest()
    userinfo, userID, userToken = userData.load_user(key,hashname)
    if userinfo == 0:
        return False,None,None
    elif userinfo == name:
        return True,userID,userToken
    else:
        return False,None,None

def create_new_user(name,password,ID,token):
    # print(name," ",password)
    line=name+password
    key = hashlib.sha224(line.encode('utf-8')).hexdigest() #hash(name+password)
    hashname = hashlib.sha224(name.encode('utf-8')).hexdigest()
    return userData.create_user(name,key,ID,token,hashname)