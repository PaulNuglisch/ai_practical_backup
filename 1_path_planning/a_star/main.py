import pygame
import math
from pkg.grid import Field, Grid
from pkg.config import BLACK, WHITE, BLUE, GREEN, RED, WIDTH, HEIGHT, MARGIN
from pkg.a_star import a_star, initialize
from pkg.myqueue import Queue
   
pygame.init()
size = (500, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My Game")
done = False
path = None
path_is_printed = False
clock = pygame.time.Clock()
grid = Grid(20, 20)

walls = [
    *[(y, 9) for y in range(0, 10)],      # vertical wall at column 10
    *[(9, x) for x in range(4, 10)],      # horizontal wall at row 10
    *[(y, 16) for y in range(9, 20)]      # vertical wall at column 18
]
grid.set_obstacles(walls)

# Start and goal
start = grid.grid[0][0]
goal = grid.grid[19][19]
grid.grid[0][0].color = GREEN     # S at (1,1)
grid.grid[19][19].color = RED     # G at (20,20)
grid.start = grid.grid[0][0]
grid.goal = grid.grid[19][19]

open = Queue('PRIO')
closed = Queue()
    
initialize(grid, open)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
        if path is None:    
            path = a_star(grid, open, closed)       
            
        screen.fill(BLACK)
        grid.draw(screen)

        pygame.display.flip()
        clock.tick(60)
        
        if path is not None and not path_is_printed:
            print("Path:")
            for node in path:
                print(f"({node.x}, {node.y})")
            path_is_printed = True
pygame.quit()




