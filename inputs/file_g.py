class Calculator:
    def subtract(self, x):
        self.value -= x
        return self.value
    
    def add(self, x):
        self.value += x
        return self.value
        
    def __init__(self):
        self.value = 0