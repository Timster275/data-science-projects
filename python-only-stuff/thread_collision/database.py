class Database():
    def __init__(self):
        self.secure_current_value = 0
        self.unsecure_current_value = 0
        self.hits = 0

    def secure_increment(self):
        self.secure_current_value += 1
        
    
    def unsecure_increment(self):
        self.unsecure_current_value += 1
    
    def evalueate(self):
        print(f"")
        if self.secure_current_value != self.unsecure_current_value:
            self.hits += 1
        self.secure_current_value = 0
        self.unsecure_current_value = 0
