from rpcClass.rpcClass import rpcServer
import json

#ADDRESS = '127.0.0.1'
PORT = 11111
BUFERSIZE = 8194
HEADSIZE= 4


def sendServerForClient(data):
    if data['FUNC']=='GetServer':
        SERVERPORT = 7731
        return SERVERPORT


serverF = rpcServer(PORT, mode = 'JSON', buferSize = BUFERSIZE, headSize=HEADSIZE)
serverF.loop(callBack=sendServerForClient)