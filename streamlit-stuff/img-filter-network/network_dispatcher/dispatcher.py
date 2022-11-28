import socket
from threading import Thread
import json
import numpy as np
from time import sleep
class Dispatcher():
    returned_chunks = []
    clients = []
    initialized = False
    sendAmount = 0
    finished = False
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

        print("Dispatcher initialized")
        if not Dispatcher.initialized:
            self.createSocket(hostname, port)
        Dispatcher.initialized = True

    def createSocket(self, hostname, port):
        ## open a websocket
        self.server  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("0.0.0.0",2711))
        self.server.listen()
        runner = Thread(target=self.runner)
        runner.start()
        
    
    def runner(self):
        while True:
            (clientConnected, clientAdress) = self.server.accept()
            print("Client connected: ", clientAdress)
            self.clients.append(clientConnected)

    def handler(self):
        for element in self.clients:
            try:

                data = element.recv(200)
                length = int(data.decode())
                sleep(0.2)
                element.send("ACK".encode())
                data = element.recv(length)
                print("precieved length: "+ str(length))
                while len(data) < length:
                    data += element.recv(length)
                print("Received data: " + str(len(data.decode())))
            except Exception as e:
                print(e)
                print("Client disconnected")
                self.clients.remove(element)
                continue
            c = Chunk(1,1,1,1,1,1)
            self.returned_chunks.append(c.fromStr(data.decode()))
            if len(self.returned_chunks) == self.sendAmount:
                self.finished = True
                break

    def dispatch(self, filter,r,g,b, image, args):
        numOfWorkers = len(self.clients)
        self.sendAmount = numOfWorkers
        handle = Thread(target=self.handler)
        handle.start()

        if numOfWorkers == 0:
            raise Warning("No workers connected")

        elif numOfWorkers == 1:
            c = Chunk(r,g,b,1,filter,args)

            cstr = c.getStr().encode()
            print("Sending Length")
            self.clients[0].send(("Length: " + str(len(cstr))).encode())
            sleep(0.1)
            print("Sending Data")
            self.clients[0].send(cstr)

        else:
            if numOfWorkers % 2 != 0:
                numOfWorkers-=1
            currindx = 0
            chunksize = len(r)//numOfWorkers
            for i in range(0, numOfWorkers):
                c = Chunk(r[currindx:chunksize], g[currindx:chunksize], b[currindx:chunksize], i, filter, args)
                cstr = c.getStr().encode()
                self.clients[i].send(("Length: " + str(len(cstr))).encode())
                sleep(0.1)
                self.clients[i].sendall(cstr)
        print("Waiting for chunks")
        handle.join()
        print("Chunks received")
        return self.createRGB(self.returned_chunks)

    def createRGB(self, chunks):
        r = []
        g = []
        b = []
        chunks.sort(key=lambda x: x.id)
        for c in chunks:
            r.append(c.r)
            g.append(c.g)
            b.append(c.b)
        r = np.array(r, np.uint8).astype(np.uint8)
        g = np.array(g, np.uint8).astype(np.uint8)
        b = np.array(b, np.uint8).astype(np.uint8)
        return r[0], g[0], b[0]    

class Chunk():
    def __init__(self, r,g,b, id, filter, args):
        self.r = r
        self.g = g
        self.b = b
        self.id = id
        self.filter = filter
        self.args = args

    def getStr(self):
        return json.dumps({
            "r": self.r.tolist(),
            "g": self.g.tolist(),
            "b": self.b.tolist(),
            "id": self.id,
            "filter": self.filter,
            "args": self.args
        })
    
    def __repr__(self) -> str:
        return "Chunk: " + str(self.id)
        
    def fromStr(self, inp):
        customobj = json.loads(inp)
        self.r = np.asarray(customobj["r"]).astype(np.uint8)
        self.g = np.asarray(customobj["g"]).astype(np.uint8)
        self.b = np.asarray(customobj["b"]).astype(np.uint8)
        self.id = customobj["id"]
        self.filter = customobj["filter"]
        self.args = customobj["args"]
        return self