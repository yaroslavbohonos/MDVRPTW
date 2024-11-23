class Customer():
    
    def __init__ (self, index, x, y, demand, start, end):
        self.ID = index # Assigned as len(depots) + customerId
        self.X = x
        self.Y = y
        self.DEMAND = demand
        self.TW = (start, end)
        self.arrivesAt = None