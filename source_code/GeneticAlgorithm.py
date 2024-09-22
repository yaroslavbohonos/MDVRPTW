from ReportsDB import DataBase
from Customer import Customer
from Depot import Depot
from Vehicle import Vehicle
from Solution import Solution

class GeneticAlgorithm():
    def __init__(self):
        self.problem_index = None
        self.num_generations = int
        self.selection_type = str
        self.mutation_prob = float
        self.crossover_prob = float
        self.init_pop_size = 0
        self.MAX_POP_SIZE = 100
        self.dist_matrix = None
        self.tw_range = None
        self.customers = []
        self.depots = []
        self.vehicles = []
        self.bestSolution = None
        self.fitness_values = []
        self.PENALTY = 1.4
        
    def record_problem_data(self, problemIndex:int):
        pass
    
    def record_parameters(self, problem_index, init_pop_size, generations, mutation_rate, crossover_rate, selection_type):
        
        # Set the parameters based on inputs
        self.problem_index = problem_index
        self.init_pop_size = init_pop_size
        self.num_generations = generations
        self.mutation_prob = mutation_rate
        self.crossover_prob = crossover_rate
        self.selection_type = selection_type
        
        # Store the parameters in a dictionary and return it
        params = {
            "Problem No": self.problem_index,
            "Initial Population Size": self.init_pop_size,
            "Generations": self.num_generations,
            "Mutation Rate": self.mutation_prob,
            "Crossover Rate": self.crossover_prob,
            "Selection Type": self.selection_type
        }
        return params