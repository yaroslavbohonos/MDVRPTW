
class Solution():
    
    def __init__ (self, routes, fitness, isFeasible):
        self.routes = routes
        self.fitness = fitness
        self.isFeasible = isFeasible

    # For heapq insert comparison
    def __lt__(self, other):
        return self.fitness < other.fitness
    
    
         