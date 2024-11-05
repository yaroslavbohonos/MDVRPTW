from ReportsDB import DataBase
from Problem import Problem
from random import shuffle
from Solution import Solution
from Vehicle import Vehicle
import heapq, random, copy

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
        self.MAX_POP_SIZE = 50
        self.vehicles = []
        self.bestSolution = None
        self.currentSol = None
        self.fitness_values = []
        self.PENALTY = 1.4
        self.population = []
        self.minDistToIteration = [] 
        #self.minDistToIteration = {"1":"None"} # Min distance up to the iterationNo ["IterNo" : "min. dist."]
     
    def recordParameters(self, problemIndex, initPopSize, generations, mutationProb, crossoverProb, selectionType):
        # Set parameters based on inputs
        print(f"Recording parameters: problemIndex={problemIndex}, initPopSize={initPopSize}, generations={generations}, mutationProb={mutationProb}, crossoverProb={crossoverProb}, selectionType={selectionType}")
        self.currProblemIndex = problemIndex
        self.initPopSize = initPopSize
        self.numGenerations = generations
        self.mutationProb = mutationProb
        self.crossoverProb = crossoverProb
        self.selectionType = selectionType    

    def calculateArrivalTime(self, stop1, stop2):
        arrivesAt = max(stop1.TW[0], stop2.TW[0])
        if arrivesAt <= stop2.TW[1]:
            stop2.arrivesAt = arrivesAt
        else:
            stop2.arrives = None

    def calculateRouteArrivalTimes(self, route):
        for i in range(1, len(route) - 1):
            stop1 = route[i - 1]
            stop2 = route[i]
            self.calculateArrivalTime(stop1, stop2)

    def isFeasibleTW(self, stop1, stop2):  
        self.calculateArrivalTime(stop1, stop2)
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
        #if not sol.isFeasible:
        #    totalDistance *= self.PENALTY
        return totalDistance
        
    # To do: think how I can get rid of removing customers 
    def createSolution(self):
        solutionRoutes = []
        #print(f"createSolution, customers available: {self.customers}")
        customers = self.customers.copy()
        depots = self.depots.copy()
        shuffle(customers)
        
        while customers:
            depot= depots[random.randint(0, self.numDepots-1)]
            vehicle = Vehicle(len(solutionRoutes), depot.CAPACITY)
            route = [depot]
            routeCapacity=0
            
            for customer in customers:
                if routeCapacity + customer.DEMAND <= vehicle.CAPACITY:
                    route.append(customer)
                    routeCapacity += customer.DEMAND
                    customers.remove(customer)

            route.append(depot)
            if len(route) > 2:  # Only add routes with customers
                solutionRoutes.append(route)

        sol = Solution(solutionRoutes, None, None)
        sol.fitness = self.calculateFitness(sol)
        sol.isFeasible = self.isFeasible(sol)
        return sol 

    def addToPopulation(self, solution):
        if solution is not None:
            self.population.append(solution)
            self.population.sort(key=lambda sol: sol.fitness)
            
            if len(self.population) > self.MAX_POP_SIZE:
                for _ in range(len(self.population) - self.initPopSize):
                    self.population.pop()

        print(f"Population size: {len(self.population)}")
        #print(f"Best fitness: {self.population[0].fitness}, Worst fitness: {self.population[-1].fitness}")
    
    def createPopulation(self):
        self.population = []  # Reset population
        for _ in range(self.initPopSize):
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
        #sol = self.population[random.randint(0, len(self.population) - 1)]
        if len(sol.routes) <= 2: # 
            return
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
        self.currentSol = sol       

    def isGoodSwap(self, cust1, cust2, route1, route2, sol):
        # To do:  implement later for efficient calculation
        pass

    def localSearch(self):
        totalNumAttempts = 40
        attemptsNumCustomer = 5
        bestLocalSol = copy.deepcopy(self.currentSol)
        sol = self.currentSol
        totalAttempts = 0
        customers = self.customers.copy()

        routesToCheck = random.sample(sol.routes, min(len(sol.routes), max(1, self.numCustomers // 6 - 1)))

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
                        cust2Route = route
                        break

                cust1Index = cust1Route.index(cust1)
                cust2Index = cust2Route.index(cust2)
                cust1Route[cust1Index] = cust2
                cust2Route[cust2Index] = cust1
                sol.isFeasible = self.isFeasible(sol)
                sol.fitness = self.calculateFitness(sol)

                if sol.isFeasible and sol.fitness < bestLocalSol.fitness:
                    bestLocalSol = copy.deepcopy(sol)
                
                cust1Route[cust1Index] = cust1
                cust2Route[cust2Index] = cust2
                totalAttempts += 1

        return bestLocalSol

    def makeFeasible(self):
        sol = self.currentSol
        for route in sol.routes:
            depot = route[0]
            currentDemand = sum(c.DEMAND for c in route[1:-1])

            while currentDemand > depot.CAPACITY:
                customerToRemove = max(route[1:-1], key=lambda c: c.DEMAND)
                route.remove(customerToRemove)
                currentDemand -= customerToRemove.DEMAND
            
                reassigned = False
                for otherRoute in sol.routes:
                    if otherRoute[0] != depot and self.canFitInRoute(customerToRemove, otherRoute):
                        otherRoute.insert(-1, customerToRemove)  # Add to the end before the depot
                        reassigned = True
                        break
            
                if not reassigned:
                    newRoute = [depot, customerToRemove, depot]
                    sol.routes.append(newRoute)

            feasibleRoute = [depot]
            for customer in route[1:-1]:
                if self.isFeasibleTW(depot, customer):
                    feasibleRoute.append(customer)
                    depot = customer  # Update depot to the last customer to check time window
            feasibleRoute.append(depot)

            route[:] = feasibleRoute if len(feasibleRoute) > 1 else [depot]

        self.currentSol.routes = sol.routes
        self.currentSol.isFeasible = self.isFeasible(sol)
        self.currentSol.fitness = self.calculateFitness(sol)
        
    def canFitInRoute(self, customer, route):
        depot = route[0]
        capacity = sum(c.DEMAND for c in route[1:-1])
        return ( capacity + customer.DEMAND <= depot.CAPACITY and self.isFeasibleTW(depot, customer) )
          

    def evolvePopulation(self):
        self.createPopulation()
        
        if not self.population:
            raise ValueError("Population is empty. Ensure `createSolution` and `createPopulation` methods are functioning correctly.")

        self.currentSol = self.population[0]
        self.makeFeasible()
        self.bestSolution = self.currentSol

        for generation in range(self.numGenerations + 1):
            self.binaryTournament()
            
            if random.random() < self.crossoverProb: 
                self.crossover()
            
            improved_solution = self.localSearch()
        
            if improved_solution.isFeasible and improved_solution.fitness < self.bestSolution.fitness:
                self.bestSolution = copy.deepcopy(improved_solution) 
                
            #if generation % 10 == 0:
            self.makeFeasible()
            self.addToPopulation(self.currentSol)
            
            if improved_solution.isFeasible and improved_solution.fitness < self.bestSolution.fitness:
                self.bestSolution = improved_solution
            
            print(f"Generation {generation}: Best fitness {self.bestSolution.fitness}")
        
"""
To do:
- Think how I can speed up generating random numbers 
  problem link -> https://eli.thegreenplace.net/2018/slow-and-fast-methods-for-generating-random-integers-in-python/
- 
"""
