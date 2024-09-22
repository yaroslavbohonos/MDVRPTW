
class Customer():
    
    def __init__ (self, x, y, demand, start, end):
        self.X = x
        self.Y = y
        self.DEMAND = demand
        self.TW = (start, end)