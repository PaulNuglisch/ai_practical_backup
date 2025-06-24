import random

class EightQueens:
    def __init__(self, initial_state=None, mode='empty'):
        self.size = 8
        if initial_state:
            self.state = initial_state #[-1,-1,-1,-1]
        elif mode == 'random':
            self.state = random.sample(range(self.size), self.size)
        else:
            self.state = [-1] * self.size  # -1 means no queen placed
        self.variables = list(range(self.size))  # one variable per row
        self.domains = [list(range(self.size)) for _ in range(self.size)]  # columns for each queen

    def is_consistent(self, row, col):
        """Check if placing a queen at (row, col) does not conflict with previous queens."""
        for r in range(row):
            c = self.state[r]
            if c == col or abs(row - r) == abs(col - c):
                return False
        return True

    def get_actions(self, row):
        """Return all valid columns for placing a queen in the given row."""
        return [col for col in self.domains[row] if self.is_consistent(row, col)]

    def apply_action(self, row, col):
        """Place a queen at the specified position."""
        self.state[row] = col

    def transition_model(self, row, col):
        """Return new state after placing a queen at (row, col)."""
        new_state = self.state[:]
        new_state[row] = col
        return new_state

    def heuristic(self, state = None):
        """Count the number of conflicting queen pairs."""
        conflicts = 0
        if state == None:
            state = self.state
            
        for i in range(self.size):
            for j in range(i + 1, self.size):
                if state[i] == -1 or state[j] == -1:
                    continue
                if state[i] == state[j] or abs(i - j) == abs(state[i] - state[j]):
                    conflicts += 1
        return conflicts
    
    def cost(self, state):
        return sum(1 for col in state if col != -1)

    def print_board(self):
        """Display the board as ASCII."""
        for r in range(self.size):
            row = ["Q" if self.state[r] == c else "." for c in range(self.size)]
            print(" ".join(row))
        print("Heuristic (conflicts):", self.heuristic(self.state))
        print("Cost:", self.cost(self.state))
        
