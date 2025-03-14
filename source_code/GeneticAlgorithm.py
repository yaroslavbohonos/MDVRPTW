from Solution import Solution
from Customer import Customer
from Problem import Problem
from Depot import Depot
from random import shuffle
import random, copy
from itertools import permutations 


class GeneticAlgorithm(Problem):
    # Initialise GeneticAlgorithm object with its variables
    def __init__(self):
        super().__init__()
        # Hold current index of the problem used from database
        self.currProblemIndex = None
        # The number of total iterations(generations) in solving
        self.numGenerations = None
        # A type selection operation
        self.selectionType = None
        # A probability of executing mutation operation
        self.mutationProb = None
        # A probability of executing crossover operation
        self.crossoverProb = None
        # Initial size of population of solutions
        self.initPopSize = None
        # When the max size is reached, the population of solutions shrinks to intial size
        self.MAX_POP_SIZE = 100
        # Increases the distance of invalid solutions by the multiplying factor
        self.PENALTY = 1.4
        # Current best solution found
        self.bestSolution = None
        # Holds a solution taken to be improved at each iteration
        self.currentSol = None
        # Holds only solutions with decreased fitness(overall distance)
        self.bestSolutions = {}
        # Holds all current generated and improved solutions that could be valid and invalid
        self.population = []
        # Tracks if problem data for the current problem index has been successfully loaded from database
        # The flag ensures that data is not redundantly reloaded if it's already recorded for the current problem.
        # It is reset to False whenever a new problem index is set in `recordParameters` to signal that fresh data needs to be fetched.
        self.isdataRecorded = False


    # Public methods
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
            self.calculateTimeMatrix()
            self.calculateTwRrange()
            self.dataRecorded = True

    def evolvePopulation(self):
        self._createPopulation()
        self.currentSol = self.population[0]
        self._makeFeasible()
        self.bestSolution = self.currentSol
        self.bestSolutions[0] = self.bestSolution

        for generation in range(1, self.numGenerations + 1):
            self._binaryTournament()
            
            if random.random() < self.crossoverProb: # A number between 0.0 and 1.0
                self._crossover()
                
            self._localSearch()
            # every fifth generation the current sol. will be made feasible
            #if generation % 5 == 0: 
            self._makeFeasible()
            self._addToPopulation(self.currentSol)
            
            self.currentSol.isFeasible = self._isFeasible(self.currentSol)
            if self.currentSol.isFeasible and (self.currentSol.fitness < self.bestSolution.fitness):
                self.bestSolution = copy.deepcopy(self.currentSol)
                self.bestSolutions[generation] = copy.deepcopy(self.currentSol)
        self.bestSolutions[self.numGenerations] = self.bestSolution  


    # Private methods
    def _calculateRouteArrivalTimes(self, route):
        # Handle separately first customer in the route
        route[1].arrivesAt = max( route[1].TW[0], (self.timeMatrix[route[0].ID][route[1].ID] + route[0].TW[0]) )
        # A route has a single customer and its time is already handleded, so skip
        if len(route) == 3:
            return 
        
        for i in range(1, len(route) - 2):
            stop1 = route[i]
            stop2 = route[i + 1]
            travelTime = self.timeMatrix[stop1.ID][stop2.ID]
            arrivalTime = stop1.arrivesAt + travelTime
            stop2.arrivesAt = max(stop2.TW[0], arrivalTime)
        return

    def _calculateRoutesArrivalTimes(self, sol):
        for route in sol.routes:
            self._calculateRouteArrivalTimes(route)

    def _isFeasibleTW(self, stop1, stop2):  
        return stop2.TW[0] <= stop2.arrivesAt <= stop2.TW[1]

    def _isFeasibleRoute(self, route):
        if len(route) <= 3:
            return False
        
        self._calculateRouteArrivalTimes(route)
        depot = route[0]
        routeCapacity = route[1].DEMAND
        
        for i in range(1, len(route) - 2):
            stop1 = route[i]
            stop2 = route[i + 1]
            routeCapacity += stop2.DEMAND
            if not self._isFeasibleTW(stop1, stop2):
                return False
            if routeCapacity > depot.CAPACITY:
                return False
        return True

    def _isFeasible(self, sol):        
        self._calculateRoutesArrivalTimes(sol)
        """
        print("Arrival at customer times:")
        for cust in self.customers:
            print(f"Cust x:{cust.X}, y:{cust.Y}, arrives at:{cust.arrivesAt}") 
        """
        # Iterate over all routes and check feasibility
        for route in sol.routes:
            if not self._isFeasibleRoute(route):
                return False  # Solution is infeasible if any route is infeasible
        return True  # All routes are feasible

    def _calculateRouteFitness(self, route):
        totalDistance = 0
        for i in range(len(route)-1):
            totalDistance += self.distMatrix[route[i].ID][route[i + 1].ID]
        return totalDistance

    # To do: apply caching for repeated distances
    def _calculateFitness(self, sol):
        totalDistance = 0
        for route in sol.routes:
            totalDistance += self._calculateRouteFitness(route)
        if not sol.isFeasible:
            totalDistance *= self.PENALTY
        return round(totalDistance, 1)
        
    def _createSolution(self):
        solutionRoutes = []
        # Sort customers by the earliest time window start
        customers = sorted(self.customers.copy(), key=lambda c: c.TW[0])
        depots = self.depots.copy()
        shuffle(customers)

        while customers:
            depot= depots[random.randint(0, self.numDepots-1)]
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
        sol.fitness = self._calculateFitness(sol)
        sol.isFeasible = self._isFeasible(sol)
        return sol 

    def _addToPopulation(self, solution):
        self.population.append(solution)
        self.population.sort(key=lambda sol: sol.fitness)
            
        if len(self.population) > self.MAX_POP_SIZE:
            for _ in range(len(self.population) - self.initPopSize):
                self.population.pop()
            for _ in range(10):
                self.population.append(self._createSolution())        

        #print(f"Population size: {len(self.population)}")
        #print(f"Best fitness: {self.population[0].fitness}, Worst fitness: {self.population[-1].fitness}")
    

    def _createPopulation(self):
        self.population = []  # Reset population
        for _ in range(self.initPopSize - 1):
            self._addToPopulation(self._createSolution())
    
    def _binaryTournament(self):
        sol1 = self.population[0]
        sol2 = self.population[1]
        if sol1.fitness < sol2.fitness:
            self.currentSol = sol1
        else:
            self.currentSol = sol2

    def _crossover(self):
        sol = self.currentSol
        if len(sol.routes) <= 1: # Skip if only one route in a solution
            return
        parent1, parent2 = random.sample(sol.routes, 2) # Generates two non-repating routes
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
        self.currentSol = sol

    def _localSearch(self):
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
            
                sol.fitness = self._calculateFitness(sol)
                #sol.isFeasible = self._isFeasible(sol)

                if sol.fitness < bestLocalSol.fitness:
                    bestLocalSol = copy.deepcopy(sol)        
                cust1Route[cust1Index] = cust1
                cust2Route[cust2Index] = cust2
                
                totalAttempts += 1
        self.currentSol = bestLocalSol

    def _insertCustomer(self, customer):
        for route in self.currentSol.routes:
            for position in range(1, len(route)):  # Avoid depots at start and end
                tempRoute = route[:position] + [customer] + route[position:]
                if self._isFeasibleRoute(tempRoute):
                    route.insert(position, customer)
                    return
        # If no valid position found, create a new route with the depot and the customer
        depot = random.choice(self.depots)
        newRoute = [depot, customer, depot]
        self.currentSol.routes.append(newRoute)
    
    def _findInvalidCustomers(self,route):
        depot = route[0]
        invalidCustomers = []    
        tempValid = route[0]
        # Identify invalid customers
        for i in range(len(route)-2):
            stop1 = route[i]
            stop2 = route[i+1]
            currentDemand = sum(c.DEMAND for c in route[1:-1])    
            travelTime = self.timeMatrix[stop1.ID][stop2.ID]
            # Travel times and time windows violation
            if not self._isFeasibleTW(stop1, stop2) and tempValid.TW[1] > stop2.TW[0]:
                invalidCustomers.append(stop2)
            # Capacity violation
            elif currentDemand > depot.CAPACITY:
                invalidCustomers.append(stop2)
            else:
                tempValid = stop2
        return invalidCustomers        

    def _makeFeasible(self):
        sol = copy.deepcopy(self.currentSol)
        customersToReinsert = set()  # Use set to avoid duplicates
        
        self._calculateRoutesArrivalTimes(sol)             
        invalidRoutes = [] 
        # Identify invalid routes
        for route in sol.routes:
            if not self._isFeasibleRoute(route):
                invalidRoutes.append(route)    

        for route in invalidRoutes:
            if len(route) == 3:
                sol.routes.remove(route)
                customersToReinsert.add(route[1])
            else:
                route.reverse()
                # If the reverse repaired the route, skip reinsertion
                if self._isFeasibleRoute(route):
                    continue
            
                invalidCustomers = self._findInvalidCustomers(route)
                if len(invalidCustomers) == 1:
                    customer = invalidCustomers[0]
                    route.remove(customer)
                    customersToReinsert.add(customer)
                elif len(invalidCustomers) == 2:
                    customer1, customer2 = invalidCustomers
                    route.remove(customer1)
                    route.remove(customer2)
                    customersToReinsert.add(customer1)
                    customersToReinsert.add(customer2)
                elif len(invalidCustomers) >= 3:
                    bestFitness = float('inf')
                    bestRoute = None
                    # Try different combinations of customers in the route
                    for i in range(len(invalidCustomers)):
                        tempRoute = [route[0]] + invalidCustomers[:i] + invalidCustomers[i:] + [route[-1]]
                        if self._isFeasibleRoute(tempRoute):
                            tempFitness = self._calculateRouteFitness(tempRoute)
                            if tempFitness < bestFitness:
                                bestFitness = tempFitness
                                bestRoute = tempRoute.copy()

                    if bestRoute:
                        # Update the existing route
                        route = bestRoute
                        # Add remaining customers to reinsertion set
                        routeCustomers = set(bestRoute[1:-1])
                        for customer in invalidCustomers:
                            if customer not in routeCustomers:
                                customersToReinsert.add(customer)
                    else:
                        # If no feasible arrangement found, add all customers for reinsertion
                        for customer in invalidCustomers:
                            customersToReinsert.add(customer)
        
        # Reinsert all collected customers
        while customersToReinsert:
            customer = customersToReinsert.pop()
            self.currentSol = sol  # Temporarily update current solution for reinsertion
            self._insertCustomer(customer)
            sol = self.currentSol  # Retrieve the updated solution

        sol.isFeasible = self._isFeasible(sol)
        sol.fitness = self._calculateFitness(sol)
        self.currentSol = sol

    def _canFitInRoute(self, customer, route):
        depot = route[0]
        capacity = sum(c.DEMAND for c in route[1:-1])
        return ( capacity + customer.DEMAND <= depot.CAPACITY and self._isFeasibleTW(depot, customer) )
          

          
"""
To do:
- Think how I can speed up generating random numbers 
  problem link -> https://eli.thegreenplace.net/2018/slow-and-fast-methods-for-generating-random-integers-in-python/
- 
"""