import unittest

from GeneticAlgorithm import GeneticAlgorithm
from Depot import Depot
from Customer import Customer
from Solution import Solution
from Problem import Problem

class TestGA(unittest.TestCase):
    
    def testFeasibilityInvalidTW(self):
        GA = GeneticAlgorithm()
        depots = []
        depots.append(Depot(1, 30, 30, 40, 8, 20))
        depots.append(Depot(2, 80, 80, 40, 8, 20))
        customers = []
        customers.append(Customer(1, 10, 10, 3, 8, 12))
        customers.append(Customer(2, 40, 10, 3, 10, 11))
        customers.append(Customer(3, 40, 40, 3, 8, 9))
        customers.append(Customer(4, 90, 90, 3, 8, 9))
        customers.append(Customer(5, 90, 30, 3, 10, 12))
        customers.append(Customer(6, 70, 40, 3, 12, 15))
        
        routes = [[depots[0], customers[0], customers[1], customers[2], depots[0] ],
                  [depots[1], customers[3], customers[4], customers[5], depots[1]] ]
        solution = Solution(routes, None, None)
        solution.isFeasible = GA.isFeasible(solution)
        print(f"Invalid #1 t.w. solution's feasibility {solution.isFeasible}")
        self.assertFalse(solution.isFeasible, "Determining feasibility of solution with invalid time windows is incorrect")
        
        customers[1]= Customer(2, 40, 10, 3, 9, 11) # Make feasible the first route to check on the second route below
        customers[4] = Customer(5, 90, 30, 3, 16, 17)
        solution.isFeasible = GA.isFeasible(solution)
        print(f"Invalid #2 t.w. solution's feasibility {solution.isFeasible}")
        self.assertFalse(solution.isFeasible, "Determining feasibility of solution with invalid time windows is incorrect")

    def testFeasibilityValidTW(self):
        GA = GeneticAlgorithm()
        depots = []
        depots.append(Depot(1, 30, 30, 40, 8, 20))
        depots.append(Depot(2, 80, 80, 40, 8, 20))
        customers = []
        customers.append(Customer(1, 10, 10, 3, 8, 12))
        customers.append(Customer(2, 40, 10, 3, 10, 11))
        customers.append(Customer(3, 40, 40, 3, 8, 10))
        customers.append(Customer(4, 90, 90, 3, 8, 9))
        customers.append(Customer(5, 90, 30, 3, 10, 12))
        customers.append(Customer(6, 70, 40, 3, 12, 15))
        
        routes = [[depots[0], customers[0], customers[1], customers[2], depots[0] ],
                  [depots[1], customers[3], customers[4], customers[5], depots[1]] ]
        solution = Solution(routes, None, None)
        solution.isFeasible = GA.isFeasible(solution)
        print(f"Valid t.w. solution's feasibility {solution.isFeasible}")
        self.assertTrue(solution.isFeasible, "Determining feasibility of solution with valid time windows is correct")    

    def testFeasibilityInvalidCapacity(self):
        GA = GeneticAlgorithm()
        depots = []
        depots.append(Depot(1, 30, 30, 40, 8, 20))
        depots.append(Depot(2, 80, 80, 40, 8, 20))
        customers = []
        customers.append(Customer(1, 10, 10, 10, 8, 12))
        customers.append(Customer(2, 40, 10, 20, 10, 11))
        customers.append(Customer(3, 40, 40, 50, 8, 10))
        customers.append(Customer(4, 90, 90, 10, 8, 9))
        customers.append(Customer(5, 90, 30, 30, 10, 12))
        customers.append(Customer(6, 70, 40, 30, 8, 9))
        
        routes = [[depots[0], customers[0], customers[1], customers[2], depots[0] ],
                  [depots[1], customers[3], customers[4], customers[5], depots[1]] ]
        solution = Solution(routes, None, None)
        solution.isFeasible = GA.isFeasible(solution)
        solution.isFeasible = GA.isFeasible(solution)
        print(f"Invalid capacity solution's feasibility {solution.isFeasible}")
        self.assertFalse(solution.isFeasible, "Determining feasibility of solution with capacity violation is incorrect")
    
    def testCalculateArrivalTimes(self):
        pass
    
    def testMakeFeasible(self):
        pass
  
    

if __name__ == '__main__':
    unittest.main()