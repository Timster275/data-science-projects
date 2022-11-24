from database import Database
from threading import Lock

class Worker():
    def __init__(self, id, database: Database, lock: Lock):
        self.lock = lock
        self.id = id
        self.db = database

    def run(self):
        self.db.unsecure_increment()
        self.lock.acquire()
        self.db.secure_increment()
        self.db.evalueate()
        self.lock.release()
        
