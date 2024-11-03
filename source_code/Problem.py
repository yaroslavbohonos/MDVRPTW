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
        

    def calculatePythagoras(x1, x2, y1, y2):
        return np.sqrt( (x1 - x2)**2 + (y1 - y2)**2 )


    def calculateDistMatrix(self):
        points = self.depots + self.customers
        distMatrix = np.zeros(points, points)        
        for i in range(points):
            for j in range(points):
                distMatrix[i][j] = self.calculatePythagoras(points[i].X, points[j].X, points[i].Y, points[j].Y)
        self.distMatrix = distMatrix     

    
    def calculateTwRrange(self):
        minTW = min([depot.TW[0] for depot in self.depots])
        maxTW = max([depot.TW[1] for depot in self.depots])
        self.twRange = [minTW, maxTW]
        

    def recordProblemData(self):
        from app import GA, DB
        problemIndex = GA.currProblemIndex()
        
        depots = DB.returnDepotData(problemIndex)
        for depot in depots:
            self.depots.append(Depot(depot[0], depot[1], depot[2], depot[3], depot[4]) )
        
        customers = DB.returnCustomerData(problemIndex)
        for customer in customers:
            self.customers.append(Customer(customer[0], customer[1], customer[2], customer[3], customer[4]) )

        self.numCustomers = len(customers)
        self.numDepots = len(depots)
        
        self.calculateDistMatrix()   
        self.calculateTwRange()