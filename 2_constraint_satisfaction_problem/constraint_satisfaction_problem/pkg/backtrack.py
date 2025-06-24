from pkg.eightqueens import EightQueens


from copy import deepcopy, copy
import numpy as np


def inferences(row: int, col: int, domains: list, size: int, defined: list[int]) -> bool:
    for r in range(row + 1, size):
        to_remove = []
        for c in domains[r]:
            if c == col or abs(row - r) == abs(col - c):
                to_remove.append(c)

        for c in to_remove:
            domains[r].remove(c)

        # is column empty and there is no queen in that column
        if not domains[r] and defined[r] == -1:
            return True
        
    return False


def backtrack(csp: EightQueens, row: int,solutions: list, domains: list) -> list:
    
    columns: list = []
    for col in csp.domains[row]:
        columns.append(col)

    for col in columns:
        if csp.is_consistent(row, col):

            # add var = value to assignment
            csp.state[row] = col
            
            # maximum depth reached
            if row == 7 and csp.heuristic() == 0 and csp.cost(csp.state) == 8:
                # return current state, fingers crossed this is correct :D
                solutions[0] += 1
                print()
                print(f'Solution: {solutions}')
                print()
                csp.print_board()
                return csp.state

            # check inference, copy cps.domains as inferences applys changes to it
            domains = deepcopy(csp.domains)
            if not inferences(row, col, csp.domains, csp.size, csp.state):

                # recursive call
                result = backtrack(csp, row + 1, solutions, csp.domains)
        
            # remove var = value and inferences from assignment
            csp.state[row] = -1
            csp.domains = domains
    
    # no solution found on this depth, go up
    # failue would be [-1] * csp.size
    return csp.state
