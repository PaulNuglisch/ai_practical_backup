from pkg.eightqueens import EightQueens
from pkg.genetic_algorithm import genetic_algorithm, create_population
from pkg.backtrack import backtrack



# population = create_population(100)

# print('Length of list: ')
# print(len(population))


# for i in range(1, 101):
#     resulting_state = genetic_algorithm(population)

#     print(f"{i}.")
#     print('Length of list after Genetic Algorithm: ')
#     print(len(population))

#     resulting_state.print_board()
#     print()



csp = EightQueens()
solutions = [0]
result = backtrack(csp, 0, solutions, csp.domains)