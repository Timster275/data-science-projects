from time import sleep
class Database():
    def __init__(self):
        self.secure_current_value = 0
        self.unsecure_current_value = 0
        self.hits = 0
    
    def evalueate(self):
        # sleep(0.000000001)
        if self.secure_current_value != self.unsecure_current_value:
            self.hits += 1
        print(f"")
        self.secure_current_value = 0
        self.unsecure_current_value = 0
