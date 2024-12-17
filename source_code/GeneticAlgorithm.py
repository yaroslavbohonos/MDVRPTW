from Solution import Solution
from Customer import Customer
from Problem import Problem
from Depot import Depot
from random import shuffle
import random, copy


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
        self.PENALTY = 1.4
        self.bestSolution = None
        self.currentSol = None
        self.bestSolutions = {}
        self.population = []
        self.isdataRecorded = False


    def recordParameters(self, problemIndex, initPopSize, generations, mutationProb, crossoverProb, selectionType):
        # Set parameters based on inputs
        if problemIndex != self.currProblemIndex and self.currProblemIndex != None:
            self.isdataRecorded = False
        self.currProblemIndex = problemIndex
        self.initPopSize = initPopSize
        self.numGenerations = generations
        self.mutationProb = mutationProb
        self.crossoverProb = crossoverProb
        self.selectionType = selectionType
        """
        print(f"Problem index recorded {problemIndex}")
        print(f"Parameters recorded: problem no:{problemIndex}, initial population size: {initPopSize}, crossover probability:{crossoverProb}, ")
        print(f", numberof generations : {generations}, selection type:{selectionType}")
        """
        
    def recordProblemData(self, DB):
        if not self.isdataRecorded:
            self.customers=[]
            self.depots=[]
            self.bestSolutions = {}
            problemIndex = self.currProblemIndex
        
            depots = DB.returnDepotData(problemIndex)
            for depot in depots:
                self.depots.append(Depot(depot[0], depot[1], depot[2], depot[3], depot[4], depot[5]))

            customers = DB.returnCustomerData(problemIndex)
            for customer in customers:
                self.customers.append(Customer(len(depots) + customer[0], customer[1], customer[2], customer[3], customer[4], customer[5]) )

            self.numCustomers = len(customers)
            self.numDepots = len(depots)
        
            self.calculateDistMatrix()
            self.calculateTwRrange()
            self.dataRecorded = True


    def calculateArrivalTime(self, stop1, stop2):
        arrivesAt = max(stop1.TW[0], stop2.TW[0])
        if arrivesAt <= stop2.TW[1]:
            stop2.arrivesAt = arrivesAt

    def calculateRouteArrivalTimes(self, route):
        for i in range(1, len(route) - 1):
            stop1 = route[i - 1]
            stop2 = route[i]
            self.calculateArrivalTime(stop1, stop2)


    def isFeasibleTW(self, stop1, stop2):  
        #self.calculateArrivalTime(stop1, stop2)
        if stop2.arrivesAt == None:
            return False
        else:
            return stop2.TW[0] <= stop2.arrivesAt <= stop2.TW[1]


    def isFeasible(self, sol):        
        for route in sol.routes:
            self.calculateRouteArrivalTimes(route)
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
        totalDistance = 0
        for route in sol.routes:
            distance = 0
            for i in range(len(route)-1):
                #print(f"Accessing distMatrix at indices: {route[i]}, {route[i + 1]}")
                totalDistance += self.distMatrix[route[i].ID][route[i + 1].ID]
            totalDistance += distance
        if not sol.isFeasible:
            totalDistance *= self.PENALTY
        return round(totalDistance, 1)
        

    # To do: think how I can get rid of removing customers 
    def createSolution(self):
        solutionRoutes = []
        #print(f"createSolution, customers available: {self.customers}")
        customers = self.customers.copy()
        depots = self.depots.copy()
        shuffle(customers)
        
        while customers:
            depot= depots[random.randint(0, self.numDepots-1)]
            #vehicle = Vehicle(len(solutionRoutes), depot.CAPACITY)
            route = [depot]
            routeCapacity = 0
            
            for customer in customers:
                if (routeCapacity + customer.DEMAND) <= depot.CAPACITY:
                    route.append(customer)
                    routeCapacity += customer.DEMAND
                    customers.remove(customer)

            route.append(depot)
            if len(route) > 2:  # Add routes with customers
                solutionRoutes.append(route)

        sol = Solution(solutionRoutes, None, None)
        sol.fitness = self.calculateFitness(sol)
        sol.isFeasible = self.isFeasible(sol)
        
        #for route in sol.routes:
        #    print(f"Route of an initially generated solution", route)

        return sol 


    def addToPopulation(self, solution):
        self.population.append(solution)
        self.population.sort(key=lambda sol: sol.fitness)
            
        if len(self.population) > self.MAX_POP_SIZE:
            for _ in range(len(self.population) - self.initPopSize):
                self.population.pop()
            for _ in range(5):
                self.population.append(self.createSolution())        

        #print(f"Population size: {len(self.population)}")
        #print(f"Best fitness: {self.population[0].fitness}, Worst fitness: {self.population[-1].fitness}")
    

    def createPopulation(self):
        self.population = []  # Reset population
        for _ in range(self.initPopSize - 1):
            self.addToPopulation(self.createSolution())
    
    
    def binaryTournament(self):
        sol1 = self.population[0]
        sol2 = self.population[1]
        if sol1.fitness < sol2.fitness:
            self.currentSol = sol1
        else:
            self.currentSol = sol2


    def crossover(self):
        sol = self.currentSol
        if len(sol.routes) < 2: # Skip if only one route in a solution
            return
        parent1, parent2 = random.sample(sol.routes[1:-1], 2) # Generates two non-repating routes
        sol1Size = len(parent1)
        sol2Size = len(parent2)
        # Avoid crossover if routes are too short. Assume the size of population always > 1
        if sol1Size <= 3 or sol2Size <= 3:
            return
        # Swap two segments between 2 routes
        point1 = random.randint(1, sol1Size - 2)
        point2 = random.randint(1, sol2Size - 2)
        child1 = parent1[:point1] + parent2[point2:-1] + [parent1[-1]]
        child2 = parent2[:point2] + parent1[point1:-1] + [parent2[-1]]
        # Update current solution details
        sol.routes[sol.routes.index(parent1)] = child1
        sol.routes[sol.routes.index(parent2)] = child2
        """
        print("Solution after a crossover operation")
        for route in sol.routes:
            print(route)
        print()
        """
        self.currentSol = sol


    def isGoodSwap(self, cust1, cust2, route1, route2, sol):
        # To do:  implement later for efficient calculation
        pass


    def localSearch(self):
        totalNumAttempts = 15000
        attemptsNumCustomer = 15
        bestLocalSol = copy.deepcopy(self.currentSol)
        sol = self.currentSol
        totalAttempts = 0
        customers = self.customers.copy()
        for route in sol.routes:
            if len(route) <= 2:
                sol.routes.remove(route) 
        routesToCheck = random.sample(sol.routes, max(1, self.numCustomers // 6 - 1))

        for cust1Route in routesToCheck:
            if totalAttempts > totalNumAttempts:
                break
            
            cust1 = random.choice(cust1Route[1:-1])
            for _ in range(attemptsNumCustomer):
                cust2Route = random.choice(routesToCheck)
                cust2 = random.choice(cust2Route[1:-1])
                if cust1 == cust2:
                    continue  
                
                cust1Index = cust1Route.index(cust1)
                cust2Index = cust2Route.index(cust2)
                cust1Route[cust1Index] = cust2
                cust2Route[cust2Index] = cust1
            
                sol.fitness = self.calculateFitness(sol)
                #sol.isFeasible = self.isFeasible(sol)

                if sol.fitness < bestLocalSol.fitness:
                    bestLocalSol = copy.deepcopy(sol)        
                cust1Route[cust1Index] = cust1
                cust2Route[cust2Index] = cust2
                
                totalAttempts += 1
        """        
        print("Best solution after a local search operation")
        for route in sol.routes:
            print(route)
        print()
        """
        self.currentSol = bestLocalSol


    def makeFeasible(self):
        sol = copy.deepcopy(self.currentSol)
        for route in sol.routes:
            depot = route[0]
            currentDemand = sum(c.DEMAND for c in route[1:-1])
            if len(route) <= 2:
                    sol.routes.remove(route)

            while currentDemand > depot.CAPACITY:
                customerToRemove = max(route[1:-1], key=lambda c: c.DEMAND)
                route.remove(customerToRemove)
                
                currentDemand -= customerToRemove.DEMAND
            
                reassigned = False
                for otherRoute in sol.routes:
                    if otherRoute[0] != depot and self.canFitInRoute(customerToRemove, otherRoute):
                        otherRoute.insert(-1, customerToRemove)  # Add before the last depot
                        reassigned = True
                        break
            
                if not reassigned:
                    newRoute = [depot, customerToRemove, depot]
                    sol.routes.append(newRoute)
           
            # Check the t.w. feasibility for all arrivals in a route
            tempStop = depot # holds temporarily the current stop
            feasibleRoute = [depot]
            for customer in route[1:-1]:
                if self.isFeasibleTW(tempStop, customer):
                    feasibleRoute.append(customer)
                    tempStop = customer  # Update current stop to the last customer to check next time window
            feasibleRoute.append(depot)

            # Write its functionality comment
            route[:] = feasibleRoute if len(feasibleRoute) > 2 else [depot] 
        """
        print("Solution after make feasible operation")
        for route in sol.routes:
            print(route)
        print()

        self.currentSol.routes = sol.routes
        self.currentSol.isFeasible = self.isFeasible(sol)
        self.currentSol.fitness = self.calculateFitness(sol)
        """
        sol.fitness = self.calculateFitness(sol)
        sol.isFeasible = self.isFeasible(sol)
        self.currentSol = sol
        

    def canFitInRoute(self, customer, route):
        depot = route[0]
        capacity = sum(c.DEMAND for c in route[1:-1])
        return ( capacity + customer.DEMAND <= depot.CAPACITY and self.isFeasibleTW(depot, customer) )
          

    def evolvePopulation(self):
        self.createPopulation()
        self.currentSol = self.population[0]
        self.makeFeasible()
        self.bestSolution = self.currentSol
        self.bestSolutions[0] = self.bestSolution

        for generation in range(1, self.numGenerations + 1):
            self.binaryTournament()
            
            if random.random() < self.crossoverProb: # A number between 0.0 and 1.0
                self.crossover()
            
            self.localSearch()
            # every fifth generation the current sol. will be made feasible
            #if generation % 5 == 0: 
            self.makeFeasible()
            self.addToPopulation(self.currentSol)
            
            print(f"Current Sol fitness: {self.currentSol.fitness}")
            print(f"Bes Sol fitness: {self.bestSolution.fitness}")
            if self.currentSol.isFeasible and (self.currentSol.fitness < self.bestSolution.fitness):
                self.bestSolution = copy.deepcopy(self.currentSol)
                self.bestSolutions[generation] = copy.deepcopy(self.currentSol)
        self.bestSolutions[self.numGenerations] = self.bestSolution        
            #print(f"Generation {generation}: Best fitness {self.bestSolution.fitness}")
            
        #for generation in self.bestSolutions:
            #print(f"Generation: {generation}: Best fitness {self.bestSolutions[generation].fitness}")
        
        

"""
To do:
- Think how I can speed up generating random numbers 
  problem link -> https://eli.thegreenplace.net/2018/slow-and-fast-methods-for-generating-random-integers-in-python/
- 
"""