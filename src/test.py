#from rpcClass.rpcClass import rpcClinet, rpcServer

#x = rpcClinet('192.168.1.1', port=547, headSize=123, mode = 'STR', buferSize=255 )
#y = rpcServer(port=1234, mode="STR", buferSize=1234)

class human:

    def __init__(self,name, family, weight, height, salary):
        self.name = name
        self.family = family
        self.weight = weight
        self.height = height
        self.salary = salary
    
    def calcuteBMI(self):
        return self.weight/((0.01*self.height)**2)



h = human("amir", "babaeayan", 94, 187, 2000)
print(h.calcuteBMI())



import json

_dic = {
    "weight": 94,
    "height": 197,
    "FUNC": "calcuteBMI"
}

str_dic = json.dumps(_dic)
byte_str_dict = bytes(str_dic, 'utf-8')
print(byte_str_dict)

decodec_byte_str_dict = byte_str_dict.decode('utf-8')
print(decodec_byte_str_dict)

json_dict = json.loads(decodec_byte_str_dict)
print(json_dict)


CLOSED_REMOTE = -2

byte_CLOES_REMOTE = CLOSED_REMOTE.to_bytes(4, byteorder='little', signed=True)

print(byte_CLOES_REMOTE)