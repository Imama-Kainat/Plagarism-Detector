class Calculator:
    def __init__(self):
        self.value = 0
        
    def add(self, x):
        self.value += x
        return self.value
        
    def subtract(self, x):
        self.value -= x
        return self.value