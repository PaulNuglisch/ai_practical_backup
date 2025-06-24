from pkg.myqueue import Queue
from pkg.grid import Field, Grid
from pkg.config import BLACK, WHITE, BLUE, GREEN, RED, WIDTH, HEIGHT, MARGIN

def initialize(grid, open):
    grid.start.g = 0
    grid.start.parent = grid.start
    grid.start.h = grid.calcH(grid.start)
    grid.start.f = grid.start.g + grid.start.h
    open.push(grid.start)
    
def upadateVertex(grid, current, neighbor, open):
    if current.g + 1 < neighbor.g:
        neighbor.g = current.g + 1
        neighbor.parent = current
        
        if open.contains(neighbor):
            open.remove(neighbor)
        
        neighbor.h = grid.calcH(neighbor)
        neighbor.f = neighbor.g + neighbor.h
        open.push(neighbor)
                
def a_star(grid, open, closed):
    
    if not open.is_empty():
        current = open.pop()
        if not current == grid.start and not current == grid.goal:
            current.color = BLUE
        if current == grid.goal:
            # Trace back the path
            path = []
            current_node = current.parent
            while current_node != grid.start:
                current_node.color = GREEN
                path.append(current_node)
                current_node = current_node.parent
            path.reverse()
            return path
        
        closed.push(current)
        current_neighbors = grid.get_neighbors(current)
        
        for neighbor in current_neighbors:
            if closed.contains(neighbor):
                continue
            upadateVertex(grid, current, neighbor, open)
            
    
    elif open.is_empty():
        print('NO PATH FOUND')
        return -1
                
        
        
        