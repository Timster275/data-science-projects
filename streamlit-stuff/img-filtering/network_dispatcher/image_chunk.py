class Chunk():
    def __init__(self, r,g,b, id, filter, args):
        self.r = r
        self.g = g
        self.b = b
        self.id = id
        self.filter = filter
        self.args = args

    def __init__(self):
        pass

    def getStr(self):
        return "{0}-{1}-{2}-{3}-{4}".format(self.r,self.g,self.b,self.id,self.args)
        
    def fromStr(self, inp):
        self.r = inp.split("-")[0]
        self.g = inp.split("-")[1]
        self.b = inp.split("-")[2]
        self.id = inp.split("-")[3]
        