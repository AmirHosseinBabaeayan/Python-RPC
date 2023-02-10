from rpcClass.rpcClass import rpcClinet
import time

ADDRESS = '127.0.0.1'
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
        rt = -1
        try :
            client = rpcClinet(ADDRESS, PORT, mode = 'JSON', buferSize = BUFERSIZE, headSize=HEADSIZE)
            x = dict()
            x['FUNC'] = 'calcuteBMI'
            x['weight'] = self.weight
            x['height'] = self.height
            client.sendMesssgeClient(x) #without error
            _, rt = client.reciveMessageClient()
            client.closeConnection()
            client.closeRemote()
        except Exception as e:
            print("------ Error -----------")

        return rt

def calcuteBMIwithsendHumanClass(h : human):
    rt = -1
    try:
        client = rpcClinet(ADDRESS, PORT, mode = 'JSON', buferSize = BUFERSIZE, headSize=HEADSIZE)
        h_dict = dict()
        h_dict['FUNC'] = 'HumanClass'
        h_dict['name'] = h.name
        h_dict['family'] = h.family
        h_dict['weight'] = h.weight
        h_dict['height'] = h.height
        h_dict['salary'] = h.salary
        client.sendMesssgeClient(h_dict)
        _, rt = client.reciveMessageClient()
        client.closeConnection()
        client.closeRemote()
    except Exception as e:
        print('-------------Error-----------')
    return rt

ahb = human(
    name="Amirhossein",
    family="Babaeayan",
    weight=94,
    height=187,
    salary=2000
)

bmi_result = ahb.calcuteBMI()
print(f"BMI result: {bmi_result}")

time.sleep(5)

bmi_result_with_send_class = calcuteBMIwithsendHumanClass(ahb)
print(f"BMI Class result: {bmi_result_with_send_class}")