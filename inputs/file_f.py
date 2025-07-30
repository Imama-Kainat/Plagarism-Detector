class Calculator:
    def __init__(self):
        # Initialize with zero value
        self.value = 0
    
    def add(self, x):
        # Add x to current value
        self.value += x
        return self.value
    
    def subtract(self, x): 
        # Subtract x from value
        self.value -= x 
        return self.value