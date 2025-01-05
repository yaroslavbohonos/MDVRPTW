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
        self.timeMatrix = None


    @staticmethod
    def calculatePythagoras(x1, x2, y1, y2):
        return np.sqrt( (x1 - x2)**2 + (y1 - y2)**2 )

    
    @staticmethod
    def calculateTravelTime(distance):
        # Average speed of all vehicles
        speed=30
        # Result of a travelling time is round to 1 d.p.
        return round((distance/speed), 1)


    def calculateDistMatrix(self):
        # Combine them as their ID attributes are formed in the way
        # So distances can be accessed using IDs of two objects in any matrix 
        points = self.depots + self.customers
        pointsSize = len(points)
        distMatrix = np.zeros((pointsSize, pointsSize))        
        for i in range(pointsSize):
            for j in range(pointsSize):
                distMatrix[i][j] = self.calculatePythagoras(points[i].X, points[j].X, points[i].Y, points[j].Y)
        self.distMatrix = distMatrix


    def calculateTimeMatrix(self):
        # Combine them as their ID attributes are formed in the way
        # So times can be accessed using IDs of two objects in any matrix 
        points = self.depots + self.customers
        pointsSize = len(points)
        timeMatrix = np.zeros((pointsSize, pointsSize))        
        for i in range(pointsSize):
            for j in range(pointsSize):
                timeMatrix[i][j] = self.calculateTravelTime(self.distMatrix[i][j])
        self.timeMatrix = timeMatrix
    
    
    def calculateTwRrange(self):
        minTW = min([depot.TW[0] for depot in self.depots])
        maxTW = max([depot.TW[1] for depot in self.depots])
        self.twRange = [minTW, maxTW]
        

    # To be overwritten after the class is inherited
    def recordProblemData(self):
        pass