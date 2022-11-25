from database import Database
from threading import Lock

import random
class Worker():
    def __init__(self, id, database: Database, lock: Lock):
        self.lock = lock
        self.id = id
        self.db = database

    def run(self):
        num = random.randint(1, 10)
        uv = self.db.unsecure_current_value
        uv += num
        self.db.unsecure_current_value = uv
        self.lock.acquire()
        sv = self.db.secure_current_value
        sv += num
        self.db.secure_current_value = sv
        self.db.evalueate()
        self.lock.release()
        
