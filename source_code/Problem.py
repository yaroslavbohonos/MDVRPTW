from Depot import Depot
from Customer import Customer
import numpy as np

class Problem():
    
    def __init__(self):
        self.customers = []
        self.depots = []
        self.numCustomers = 0
        self.numDepots = 0
        self.twRange = []
        self.distMatrix = None

    @staticmethod
    def calculatePythagoras(x1, x2, y1, y2):
        return np.sqrt( (x1 - x2)**2 + (y1 - y2)**2 )


    def calculateDistMatrix(self):
        points = self.depots + self.customers
        pointsSize = len(points)
        distMatrix = np.zeros((pointsSize, pointsSize))        
        for i in range(pointsSize):
            for j in range(pointsSize):
                distMatrix[i][j] = self.calculatePythagoras(points[i].X, points[j].X, points[i].Y, points[j].Y)
                #print(f"[i,j] [{i,j}]")
        self.distMatrix = distMatrix     

    
    def calculateTwRrange(self):
        minTW = min([depot.TW[0] for depot in self.depots])
        maxTW = max([depot.TW[1] for depot in self.depots])
        self.twRange = [minTW, maxTW]
        

    def recordProblemData(self):
        pass