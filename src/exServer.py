from rpcClass.rpcClass import rpcServer
import json

#ADDRESS = '127.0.0.1'
PORT = 7731
BUFERSIZE = 8194
HEADSIZE= 4

class human:

    def __init__(self,name, family, weight, height, salary):
        self.name = name
        self.family = family
        self.weight = weight
        self.height = height
        self.salary = salary
    
    def calcuteBMI(self):
        return self.weight/((0.01*self.height)**2)



def fff(data):
    if data['FUNC']=='calcuteBMI':
        print('we have a function call from client:')
        print(data)
        bmi = int(data['weight'])/((0.01*int(data['height']))**2)
    if data['FUNC'] == 'HumanClass':
        print('we have a human class from client :')
        print(data)
        hp = human(
            name=data['name'],
            family=data['family'],
            weight=data['weight'],
            height=data['height'],
            salary=data['salary']
        )
        bmi = hp.calcuteBMI()
    return bmi



server = rpcServer(PORT, mode = 'JSON', buferSize = BUFERSIZE, headSize=HEADSIZE)
print("xxxxx")
server.loop(callBack=fff)
