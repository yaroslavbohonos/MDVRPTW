
class Depot():
    
    def __init__ (self, x, y, capacity, start, end):
        self.X = x
        self.Y = y
        self.CAPACITY = capacity
        self.TW = (start, end)