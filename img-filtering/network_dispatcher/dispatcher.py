from image_chunk import Chunk
class Dispatcher():
    returned_chunks = []
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port
        self.createSocket(hostname, port)

    def createSocket(hostname, port):
        # onmessage append message to returned chunks, maybe make a message queue for this
        pass
def dispatch(self, filter,r,g,b, image, args):
    numOfWorkers = self.server.getClients()
    if numOfWorkers % 2 != 0:
        numOfWorkers-=1
    currindx = 0
    chunksize = len(r)//numOfWorkers
    for i in range(0, numOfWorkers):
        c = Chunk(r[currindx:chunksize], g[currindx:chunksize], b[currindx:chunksize], i, filter, args)
        self.clients[i].send(c.asStr())



    pass