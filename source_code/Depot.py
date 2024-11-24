class Depot():
    
    def __init__ (self, index, x, y, capacity, start, end):        
        self.ID = index
        self.X = x
        self.Y = y
        self.CAPACITY = capacity
        self.TW = (start, end)
        