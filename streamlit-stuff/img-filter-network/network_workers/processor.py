import socket
from threading import Thread
from time import sleep
import json
import numpy as np
class Client():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(("127.0.0.1", 2711))
        worker = Thread(target=self.wait)
        worker.start()

    def wait(self):

        data = self.client.recv(200)
        print(data.decode())
        incoming_length = int(data.decode().split(" ")[1])
        print("Incoming length: ", incoming_length)
        data = self.client.recv(incoming_length)
        while len(data) < incoming_length:
            data += self.client.recv(incoming_length)
        print("Received data: " + str(len(data.decode())))
        c = Chunk(1,1,1,1,1,1)
        c.fromStr(data.decode())
        data = c.getStr()
        self.client.send((str(incoming_length)).encode())
        d1 = self.client.recv(200)
        if d1.decode() == "ACK":
            print("Sending data")
            self.client.send(data.encode())
        

c = Client()

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
        })
    
    def __repr__(self) -> str:
        return f"Chunk({self.id}, {self.filter}, {self.args})"
        
    def fromStr(self, inp):
        customobj = json.loads(inp)
        self.r = np.asarray(customobj["r"]).astype(np.uint8)
        self.g = np.asarray(customobj["g"]).astype(np.uint8)
        self.b = np.asarray(customobj["b"]).astype(np.uint8)
        self.id = customobj["id"]
        self.args = customobj["args"]
        self.filtername = customobj["filter"].split("(")[0].split(" ")[1]
        self.filter = customobj["filter"] + "\n self.r, self.g, self.b ="+self.filtername+f"({self.r.tolist()}, {self.g.tolist()}, {self.b.tolist()}, {self.args})"
        try:
            exec(self.filter)
        except Exception as e:
            print(e)
            pass

        return self