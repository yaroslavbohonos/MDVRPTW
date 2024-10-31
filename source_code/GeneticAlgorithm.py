
from ReportsDB import DataBase
from Problem import Problem

class GeneticAlgorithm(Problem):
    # Initialise GeneticAlgorithm object with its variables
    def __init__(self):
        super().__init__()
        self.curr_problem_index = None
        self.num_generations = int
        self.selection_type = str
        self.mutation_prob = float
        self.crossover_prob = float
        self.init_pop_size = 0
        self.MAX_POP_SIZE = 100
        self.vehicles = []
        self.bestSolution = None
        self.fitness_values = []
        self.PENALTY = 1.4
     
    def record_parameters(self, problem_index, init_pop_size, generations, mutation_rate, crossover_rate, selection_type):
        # Set the parameters based on inputs
        self.curr_problem_index = problem_index
        self.init_pop_size = init_pop_size
        self.num_generations = generations
        self.mutation_prob = mutation_rate
        self.crossover_prob = crossover_rate
        self.selection_type = selection_type

    
    def isFeasible():
        pass
    
    
    def calculateFitness():
        pass
    

    def generateSolution():
        pass
    

    def createPopulation():
        pass
    
    