import socket, json, time, array, typing


class rpcClass(object):

    #constructor
    def __init__(self, mode, headSize, buferSize):
        self.rpcSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mode = mode
        self.headsize = headSize
        self.buferSize = buferSize
        self.CLOSE_CONNECTION = -1
        self.CLOSE_REMOTE = -2


    def sendMesssge(self, rpcSocket, data):
        data = self.dataToByte(data)
        header = len(data).to_bytes(self.headsize, byteorder='little')
        packet = header + data
        print("in sendmessage rpc:")
        print(packet)
        rpcSocket.sendall(packet)
        self.logging(('sendMesssge', f'packetlen {len(packet)}'))


    def reciveMessage(self, rpcSocket, buferSize):
        # print("in recivemessage rpc:")
        packet = rpcSocket.recv(buferSize)
        # print(packet)
        if (not packet):
            return self.CLOSE_CONNECTION, None
        
        header = packet[:self.headsize]
        data = packet[self.headsize:]
        # print("header and data from rm:")
        # print(header, data)

        decoded_header = int.from_bytes(header, 'little', signed=True)
        if decoded_header in [self.CLOSE_CONNECTION, self. CLOSE_REMOTE]:
            return decoded_header, None
        # print(f"len-data: {len(data)}, header: {int.from_bytes(header, 'little')}")
        while (len(data) != int.from_bytes(header, 'little')):
            data += rpcSocket.recv(buferSize)
        packetLen = self.headsize + len(data)
        self.logging(('reciveMessage', f'packetlen {packetLen}'))
        return header, self.byteToData(data)


    def dataToByte(self, data) -> bytes:
        if (self.mode is None):
            return data
        
        if (self.mode == 'STR'):
            return data.encode()
        
        if (self.mode == 'JSON'):
            return bytes(json.dumps(data), 'utf-8')
        
        if (self.mode == "ARRAY"):
            return bytes(data)


    def byteToData(self, byteStream: bytes):
        if (self.mode is None):
            return byteStream
        
        if (self.mode == 'STR'):
            return byteStream.decode('utf-8')
        
        if (self.mode == 'JSON'):
            return json.loads(byteStream.decode('utf-8'))
        
        if (self.mode == "ARRAY"):
            d = array.array('d')
            d.frombytes(byteStream)
            return d

    def logging(self, log: typing.Tuple[str]):
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(' - '.join((t, *log)))
        


class rpcClinet(rpcClass):
    def __init__(self, address, port, **kwargs):
        super().__init__(**kwargs)
        self.rpcSocket.connect((address, port))
        self.logging(('connect', f'to {address}:{str(port)}'))
    
    
    def sendMesssgeClient(self, data):
        self.sendMesssge(self.rpcSocket, data)
    

    def reciveMessageClient(self):
        return self.reciveMessage(self.rpcSocket, self.buferSize)
    

    def close(self):
        self.rpcSocket.close()
        self.logging(('close', ))
    

    def closeConnection(self):
        packet = self.CLOSE_CONNECTION.to_bytes(self.headsize, byteorder='little', signed=True)
        self.rpcSocket.sendall(packet)
        self.close()
    

    def closeRemote(self):
        packet = self.CLOSE_REMOTE.to_bytes(self.headsize, byteorder='little', signed=True)
        self.rpcSocket.sendall(packet)
        self.logging(('close remote ...',))
        # self.close()
        


class rpcServer(rpcClass):
    def __init__(self, port, **kwargs):
        super(rpcServer, self).__init__(**kwargs)
        self.rpcSocket.bind(('localhost',port))
        self.rpcSocket.listen(5)
        self.logging(("listening ...",))
    

    def sendMesssgeServer(self, rpcSocket, data):
        self.sendMesssge(rpcSocket, data)


    def reciveMessageServer(self, rpcSocket):
        return self.reciveMessage(rpcSocket, self.buferSize)


    def close(self, rpcSocket):
        rpcSocket.close()


    def loop(self, callBack: callable):
        while (1):
            connection, address = self.rpcSocket.accept()
            self.logging(('connect', f'to {address[0]}:{str(address[1])}')) #address[1]:port
            while (1):
                header, data = self.reciveMessageServer(connection)
                print("from rpcClassServer: ", header, data)
                if (header == self.CLOSE_CONNECTION):
                    self.close(connection)
                    self.logging(('close', f'to {address[0]}:{str(address[1])}'))
                    break
                elif (header == self.CLOSE_REMOTE):
                    self.logging(('exit...',))
                    return
                else:
                    self.sendMesssgeServer(connection, callBack(data))
