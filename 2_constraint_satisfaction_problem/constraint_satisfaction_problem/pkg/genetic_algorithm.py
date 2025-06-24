import random
from pkg.eightqueens import EightQueens

def create_population(size=100):
    population = []
    for _ in range(size):
        state = EightQueens(mode='random')
        population.append(state)
        
    return population

def genetic_algorithm(population, mutation_probability:float = 0.05):
    new_population = []
    
    best_heuristic = float('inf')
    best_state = None
    
    for i in range(len(population)):
        parent1, parent2 = select_parents(population)
        
        merged = reproduce(parent1, parent2)
        
        if random.random() < mutation_probability:
            mutate(merged)
            
        new_population.append(merged)
        h = merged.heuristic()
        
        if h < best_heuristic:
            best_heuristic = h
            best_state = merged
    
    population = new_population        
    return best_state  

def reproduce(state1, state2):
    x = state1.state
    y = state2.state
    n = len(x)
    c = random.randint(1, n - 1)
    new_state = x[:c] + y[c:]
    return EightQueens(initial_state=new_state)


def mutate(state):
    row = random.randint(0, state.size - 1)
    new_col = random.randint(0, state.size - 1)
    state.state[row] = new_col
    
def select_parents(population):
    weights = [1 / (1 + individual.heuristic()) for individual in population]
    return random.choices(population, weights=weights, k=2)