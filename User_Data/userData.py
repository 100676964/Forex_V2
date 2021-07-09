import os, sys
from tkinter.constants import E
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from User_Data import simple_encryption

def load_user(key,hashname):
    try:
        f = open(os.getcwd()+"/saves/"+hashname+".save","r",encoding='utf-8')
        content = f.readlines()
#         for i in range(len(content)):
#             content[i] = content[i][:-1]
        f.close()
    except:
        return 0,0,0
    
    destr=simple_encryption.decode(str(key),content[0])
    splittedstr=destr.split()
    # print(destr," ",key)
    
    
    try:
        return splittedstr[0],splittedstr[1],splittedstr[2]
    except:
        return 0,0,0


#return 0 means user already registed
#return 1 means user registration failed
#return 2 means registration succeded
def create_user(name,key,ID,token,hashname):
    try:
        
        f = open(os.getcwd()+"/saves/"+hashname+".save","r",encoding='utf-8')
        f.close()
        return 0
    except:
        try:
            f = open(os.getcwd()+"/saves/"+hashname+".save","w+",encoding='utf-8')
            string= name+" "+ID+" "+token
            # print(string," ",str(key))
            enstr=simple_encryption.encode(str(key),string)
            # print(enstr)
            f.write(enstr)
            f.close()
        except Exception as e:
            
            print(e)
            return 1
    return 2