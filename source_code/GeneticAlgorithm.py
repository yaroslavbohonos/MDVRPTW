from ReportsDB import DataBase
from Problem import Problem
from random import shuffle
from Solution import Solution
from Vehicle import Vehicle
import heapq, random

class GeneticAlgorithm(Problem):
    # Initialise GeneticAlgorithm object with its variables
    def __init__(self):
        super().__init__()
        self.currProblemIndex = None
        self.numGenerations = None
        self.selectionType = None
        self.mutationProb = None
        self.crossoverProb = None
        self.initPopSize = None
        self.MAX_POP_SIZE = 100
        self.vehicles = []
        self.bestSolution = None
        self.fitness_values = []
        self.PENALTY = 1.4
        self.population = []
     
    def record_parameters(self, problemIndex, initPopSize, generations, mutationProb, crossoverProb, selectionType):
        # Set parameters based on inputs
        self.currProblemIndex = problemIndex
        self.initPopSize = initPopSize
        self.numGenerations = generations
        self.mutationProb = mutationProb
        self.crossoverProb = crossoverProb
        self.selectionType = selectionType    

    def isFeasibleTW(self, stop1, stop2):  
        return stop1.TW[0] < stop2.TW[0] or stop1.TW[1] < stop2.TW[1]

    def isFeasible(self, sol):
        for route in sol.routes:
            depot = route[0]
            routeCapacity = 0
            for customer in route[1:-1]:
                if not self.isFeasibleTW(depot, customer):
                    return False
                routeCapacity += customer.DEMAND
                if routeCapacity > depot.CAPACITY:
                    return False
        return True

    def isFeasibleTwoRoutes(self, sol, route1, route2):
        # To do: implement later for efficient calculation
        pass
    
    # To do: apply caching for repeated distances
    def calculateFitness(self, sol):
        total_distance = 0
        for depotRoutes in sol.routes:
            for route in depotRoutes:
                distance = 0
                for i in range(0, len(route)):
                    totalDistance += super().distMatrix[route[i]][route[i + 1]]
                totalDistance += distance
        if not sol.isFeasible:
            totalDistance *= self.PENALTY
        return totalDistance
        
    # To do: think how I can get rid of removing customers 
    def createSolution(self):
        solutionRoutes = []
        customers = super().self.customers.copy()
        depots = super().self.depots.copy()
        shuffle(customers)
        
        while customers:
            depotRoutes=[]
            depot= depots[random.randint(0, super().numDepots-1)]
            vehicle = Vehicle(id=len(depotRoutes), CAPACITY=depot.CAPACITY)
            route = [depot]
            routeCapacity=0
            
            for customer in customers:
                if routeCapacity + customer.DEMAND <= vehicle.CAPACITY:
                    route.append(customer)
                    routeCapacity += customer.DEMAND
                    customers.remove(customer)

            route.append(depot)
            if len(route) > 2:  # Only add routes with customers
                depotRoutes.append(route)

            solutionRoutes.append(depotRoutes)
        sol = Solution(solutionRoutes, None, None)
        sol.fitness = self.calculateFitness(sol)
        sol.isFeasible = self.isFeasible(sol)
        return sol
        
                    
    def createPopulation(self, size):
        for _ in range(size):
            heapq.heappush(self.population, self.createSolution())
    

    def binaryTournament(self):
        sol1 = self.population[random.randint(0, len(self.population) // 4)]
        sol2 = self.population[random.randint(len(self.population) // 4, len(self.population)//2 - 1)]
        if sol1.fitness < sol2.fitness:
            return sol1
        else:
            return sol2    

    def crossover(self):
        sol = self.population[random.randint(0, len(self.population) - 1)]
        parent1, parent2 = random.sample(sol.routes[1:-1], 2) # Generates two non-repating routes
        sol1Size = len(parent1)
        sol2Size = len(parent2)
        # Avoid crossover if routes are too short. Assume size of population always > 1
        if sol1Size <= 3 or sol2Size <= 3:
            return
        point1 = random.randint(1, sol1Size - 2)
        point2 = random.randint(1, sol2Size - 2)
        child1 = parent1[:point1] + parent2[point2:-1] + [parent1[-1]]
        child2 = parent2[:point2] + parent1[point1:-1] + [parent2[-1]]
        sol.routes[sol.routes.index(parent1)] = child1
        sol.routes[sol.routes.index(parent2)] = child2
        sol.fitness = self.calculateFitness(sol)
        sol.isFeasible = self.isFeasible(sol)    
    
    def isGoodSwap(self, cust1, cust2, route1, route2, sol):
        # To do:  implement later for efficient calculation
        pass

    def localSearch(self, sol, totalNumAttempts, attemptsNumCustomer):
        bestSol=sol
        totalAttempts=0
        customers = super().self.customers.copy()
        routesToCheck = random.sample(sol.routes, super().self.numCustomers//6 - 1)     
        
        for cust1Route in routesToCheck:
            if totalAttempts > totalNumAttempts:
                break
            
            cust1 = random.choice(cust1Route[1:-1])
            for _ in range(attemptsNumCustomer):
                cust2 = random.choice(customers)
                if cust1 == cust2:
                    continue  
                cust2Route = None
                for route in sol.routes:
                    if cust2 in route:
                        cust2_route = route
                        break
                
                cust1Index = cust1Route.index(cust1)
                cust2Index = cust2Route.index(cust2)
                
                cust1Route[cust1Index]=cust2
                cust2Route[cust2Index]=cust1
                
                sol.isFeasible = self.isFeasible(sol)
                sol.fitness = self.calculateFitness(sol)

                if sol.isFeasible or sol.fitness < bestSol.fitness:
                    bestSol = sol
                else:
                    cust1Route[cust1Index]=cust1
                    cust2Route[cust2Index]=cust2
                totalAttempts += 1
                
        sol.routes = bestSol.routes
        sol.fitness = bestSol.fitness
        sol.isFeasible = bestSol.isFeasible


    def makeFeasible(self, sol):
        for route1 in sol.routes:
            depot = route1[0]
            tempRoute = route1.copy()
        
            while sum(c.DEMAND for c in route1[1:-1]) > depot.CAPACITY:
                customer = max(route1[1:-1], key=lambda c: c.DEMAND)
                route1.remove(customer)
                
                reassigned = False
                for route2 in sol.routes:
                    if route2[0] != depot and self.canFitInRoute(customer, route2):
                        route2.insert(-1, customer)
                        reassigned = True
                        break
                if not reassigned:
                    sol.routes.extend([depot, customer, depot])

            feasible_route = [depot]
            for i, customer in enumerate(route1[1:-1]):
                if self.isFeasibleCustomerTW(depot, customer) and (i == 0 or feasible_route[-1].TW[1] <= customer.TW[0]):
                    feasible_route.append(customer)
            feasible_route.append(depot)
            
            route1[:] = feasible_route if len(feasible_route) == len(route1) else tempRoute

        sol.isFeasible = self.isFeasible(sol)
        sol.fitness = self.calculateFitness(sol)
        
    def canFitInRoute(self, customer, route):
        depot = route[0]
        capacity = sum(c.DEMAND for c in route[1:-1])
        return ( capacity + customer.DEMAND <= depot.CAPACITY and self.isFeasibleTW(depot, customer) )
          

    def evolvePopulation(self):
        pass
    

"""
To do:
- Think how I can speed up generating random numbers 
  problem link -> https://eli.thegreenplace.net/2018/slow-and-fast-methods-for-generating-random-integers-in-python/
- 
"""
