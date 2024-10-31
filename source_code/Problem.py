from Depot import Depot
from Customer import Customer
import numpy as np

class Problem():
    
    def __init__(self):
        self.customers = []
        self.depots = []
        self.num_customers = 0
        self.num_depots = 0
        self.tw_range = []
        self.dist_matrix = None
        

    def calculate_pythagoras(x1, x2, y1, y2):
        return np.sqrt( (x1 - x2)**2 + (y1 * y2)**2 )


    def calculate_dist_matrix(self):
        points = self.depots + self.customers
        dist_matrix = np.zeros(points, points)        

        for i in range(points):
            for j in range(points):
                dist_matrix[i][j] = self.calculate_pythagoras(points[i].x, points[j].x, points[i].y, points[j].y)
        return dist_matrix     

    
    def calculate_tw_range(self):
        self.tw_range[0] = min(self.depots, key=lambda x: x[4])
        self.tw_range[1] = max(self.depots, key=lambda x: x[4])
        

    def record_problem_data(self):
        from app import GA, DB
        problem_index = GA.curr_problem_index()
        
        depots = DB.returnDepotData(problem_index)
        for depot in depots:
            self.depots.append(Depot(depot[0], depot[1], depot[2], depot[3], depot[4]) )
        
        customers = DB.returnCustomerData(problem_index)
        for customer in customers:
            self.customers.append(Customer(customer[0], customer[1], customer[2], customer[3], customer[4]) )

        self.num_customers = len(customers)
        self.num_depots = len(depots)
        
        self.dist_matrix = self.calculate_dist_matrix()   
        self.tw_range = self.calculate_tw_range()