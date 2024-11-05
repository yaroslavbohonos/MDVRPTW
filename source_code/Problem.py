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
        pointsNumber = len(points)
        distMatrix = np.zeros((pointsNumber, pointsNumber))        
        for i in range(pointsNumber):
            for j in range(pointsNumber):
                distMatrix[i][j] = self.calculatePythagoras(points[i].X, points[j].X, points[i].Y, points[j].Y)
                #print(f"[i,j] [{i,j}]")
        self.distMatrix = distMatrix     

    
    def calculateTwRrange(self):
        minTW = min([depot.TW[0] for depot in self.depots])
        maxTW = max([depot.TW[1] for depot in self.depots])
        self.twRange = [minTW, maxTW]
        

    def recordProblemData(self, GA, DB):
        problemIndex = GA.currProblemIndex
        #print(f"Current problem index recorded: {problemIndex}")
        
        depots = DB.returnDepotData(problemIndex)
        for depot in depots:
            self.depots.append(Depot(depot[0], depot[1], depot[2], depot[3], depot[4], depot[5]))
        
        #print(f"Depots populated: {self.depots}")  # Debug statement

        customers = DB.returnCustomerData(problemIndex)
        for customer in customers:
            self.customers.append(Customer(len(depots) + customer[0], customer[1], customer[2], customer[3], customer[4], customer[5]) )

        #print(f"Customers populated: {self.customers}")  # Debug statement

        self.numCustomers = len(customers)
        self.numDepots = len(depots)
        
        self.calculateDistMatrix()   
        self.calculateTwRrange()