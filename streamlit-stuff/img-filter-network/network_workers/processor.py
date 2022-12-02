import socket
from threading import Thread
from time import sleep
import json
import numpy as np
class Client():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(("127.0.0.1", 2718))
        worker = Thread(target=self.wait)
        worker.start()

    def wait(self):
        while True:
            # wait for metadata. Server provides us with length
            data = self.client.recv(200)
            incoming_length = int(data.decode().split(" ")[1])
            print("Incoming length: ", incoming_length)
            # recieve as long as not all the data is here.
            data = self.client.recv(incoming_length)
            while len(data) < incoming_length:
                data += self.client.recv(incoming_length)
            print("Received data: " + str(len(data.decode())))
            # Convert the image to a chunk. The Chunk is then filtered 
            image = Chunk(1,1,1,1,1,1)
            image.fromStr(data.decode())
            image.flt()
            # convert the chunk back to str-rep and transmit it back with the same scheme as we recieved it.
            data = image.getStr()
            self.client.send((str(len(data))).encode())
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

    def flt(self):
            exec(self.filter)
            print("Successfully executed filter: ", self.filtername)

        
    def fromStr(self, inp):
        customobj = json.loads(inp)
        self.r = np.asarray(customobj["r"]).astype(np.uint8)
        self.g = np.asarray(customobj["g"]).astype(np.uint8)
        self.b = np.asarray(customobj["b"]).astype(np.uint8)
        self.id = customobj["id"]
        self.args = customobj["args"]
        self.filtername = customobj["filter"].split("(")[0].split(" ")[1]
        self.filter = customobj["filter"] + "\nself.r, self.g, self.b ="+self.filtername+f"({self.r.tolist()}, {self.g.tolist()}, {self.b.tolist()}, {self.args})"
        
        print("Recieved Shape: ", self.r.shape)
        print("Recieved Shape: ", self.g.shape)
        print("Recieved Shape: ", self.b.shape)
        return self