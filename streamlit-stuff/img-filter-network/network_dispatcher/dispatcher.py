import socket
from threading import Thread
import json
import numpy as np
import logging 
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
            self.setupLogger()
        Dispatcher.initialized = True

    def createSocket(self, hostname, port):
        ## open a websocket
        self.server  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("0.0.0.0",2720))
        self.server.listen()
        runner = Thread(target=self.runner)
        runner.start()
        
    
    def runner(self):
        while True:
            (clientConnected, clientAdress) = self.server.accept()
            logging.info("Client connected: " + str(clientAdress))
            self.clients.append(clientConnected)

    def handler(self):
        for element in self.clients:
            try:
                logging.info("---------------------Handler---------------------")
                data = element.recv(200)
                length = int(data.decode())
                sleep(0.2)
                element.send("ACK".encode())
                data = element.recv(length)
                logging.info("precieved length: "+ str(length))
                while len(data) < length:
                    data += element.recv(length)
                logging.info("Received data: " + str(len(data.decode())))
            except Exception as e:
                logging.warn("Client disconnected: " + str(element.getpeername()))
                self.clients.remove(element)
                continue
            c = Chunk(1,1,1,1,1,1)
            self.returned_chunks.append(c.fromStr(data.decode()))
            if len(self.returned_chunks) == self.sendAmount:
                self.finished = True
                break

    def dispatch(self, filter,r,g,b, image, needsMore, args):
        numOfWorkers = len(self.clients)
        self.sendAmount = numOfWorkers
        self.needsMore = needsMore
        handle = Thread(target=self.handler)
        handle.start()

        if numOfWorkers == 0:
            raise Warning("No workers connected")

        elif numOfWorkers == 1:
            c = Chunk(r,g,b,1,filter,args)
            cstr = c.getStr().encode()
            self.clients[0].send(("Length: " + str(len(cstr))).encode())
            sleep(0.1)
            self.clients[0].send(cstr)

        else:
            if numOfWorkers % 2 != 0:
                numOfWorkers-=1
            currindx = 0
            chunksize = len(r)//numOfWorkers
            for i in range(0, numOfWorkers):
                
                
                if i != 0 and i != numOfWorkers-1:
                    c = Chunk(r[currindx-needsMore:chunksize+needsMore], g[currindx-needsMore:chunksize+needsMore], b[currindx-needsMore:chunksize+needsMore], i, filter, args)
                    logging.info("Send middle chunk")
                    logging.info("Sending from " + str(currindx-needsMore) + " to " + str(chunksize+needsMore))
                elif i == 0:
                    c = Chunk(r[currindx:chunksize+needsMore], g[currindx:chunksize+needsMore], b[currindx:chunksize+needsMore], i, filter, args)
                    logging.info("Send first chunk")
                    logging.info("Sending from " + str(currindx) + " to " + str(chunksize+needsMore))
                else:
                    c = Chunk(r[currindx-needsMore:chunksize], g[currindx-needsMore:chunksize], b[currindx-needsMore:chunksize], i, filter, args)
                    logging.info("Send last chunk")
                    logging.info("Sending from " + str(currindx-needsMore) + " to " + str(chunksize))

                cstr = c.getStr().encode()
                self.clients[i].send(("Length: " + str(len(cstr))).encode())
                sleep(0.1)
                self.clients[i].sendall(cstr)
                sleep(0.1)
                currindx += chunksize
                chunksize += currindx
       
        logging.info("Chunks send. Waiting for response chunks")

        handle.join()
        logging.info("All chunks received")
        return self.createRGB(self.returned_chunks)

    def createRGB(self, chunks):
        logging.info("---------------------Image Builder---------------------")
        r = []
        g = []
        b = []
        logging.info(f"Handling {len(chunks)} chunks")
        chunks.sort(key=lambda x: x.id)
        
        for c in chunks:
            # remove the last line of each chunk
            logging.info(f"Shape of chunk {c.id}: {np.shape(c.r)}")

            if c.id != 0 and c.id != len(chunks)-1:
                logging.info("Handling middle chunk")
                c.r = c.r[self.needsMore:-self.needsMore]
                c.g = c.g[self.needsMore:-self.needsMore]
                c.b = c.b[self.needsMore:-self.needsMore]
            elif c.id == 0:
                logging.info("Handling first chunk")
                c.r = c.r[0:-self.needsMore]
                c.g = c.g[0:-self.needsMore]
                c.b = c.b[0:-self.needsMore]
            elif c.id == len(chunks)-1:
                logging.info("Handling last chunk")
                c.r = c.r[self.needsMore:]
                c.g = c.g[self.needsMore:]
                c.b = c.b[self.needsMore:]
            r.append(c.r)
            g.append(c.g)
            b.append(c.b)

        r = np.array(r, np.uint8).astype(np.uint8)
        g = np.array(g, np.uint8).astype(np.uint8)
        b = np.array(b, np.uint8).astype(np.uint8)
        r = np.reshape(r, (len(r)*len(r[0]), len(r[0][0])))
        g = np.reshape(g, (len(g)*len(g[0]), len(g[0][0])))
        b = np.reshape(b, (len(b)*len(b[0]), len(b[0][0])))
        
        self.cleanup()

        return r, g, b    

    def cleanup(self):
        self.returned_chunks = []
        self.sendAmount = 0
        self.finished = False

    def setupLogger(self):
        pass
      


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
        try:
            self.filter = customobj["filter"]
            self.args = customobj["args"]
        except:
            pass
        return self