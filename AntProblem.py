import time
import sys
import numpy as np
np.set_printoptions(threshold=sys.maxsize)

start_time = time.time()
# Class to represent world grid
class WorldGrid:
    def __init__(self, length, width, num_food, verbose=True):
        self.grid = np.zeros(length*width).reshape(length, width)
        self.food_pos = np.random.choice(length*width, num_food, replace=False)

        cols = self.food_pos % length
        rows = (self.food_pos - cols) / length

        self.grid[rows.astype(int), cols.astype(int)] = -1
        
        # if verbose:
            # print(self.grid)


# Class that represents each ant
class Ant:
    def __init__(self, length, width, id):
        self.id = id
        self.pos = np.random.choice(length*width)
    
    def move(self):
        move = np.random.choice([-1, 1, length, -length])
        
        if self.pos % length == 0 and move == -1: # Checking for left bound
            return
        elif self.pos % length == (length-1) and move == 1: # Checking for right bound
            return
        elif (self.pos+move) < 0 or (self.pos+move) >= (length*width): # Checking for upper and lower bound
            return
        else:
            self.pos += move


length = 100
width = length
food_droppings = 10

ants_total = 100
time_steps = 100
simulation_runs = 100

sim_food_eaten = np.zeros(simulation_runs)

for run in range(simulation_runs):
    food_eaten = 0
    World = WorldGrid(length, width, food_droppings)

    ants = list()
    id =1
    for i in range(ants_total):
        a = Ant(length, width, id)
        ants.append(a)

        if a.pos in World.food_pos:
            World.food_pos = np.delete(World.food_pos, np.where(World.food_pos == a.pos))
            food_eaten += 1
        
        col = a.pos % length
        row = int((a.pos - col) / length)
        World.grid[row, col] = a.id

        id += 1
    
    # print(World.grid)

    for t in range(time_steps):
        for ant in ants:
            ant.move()

            if ant.pos in World.food_pos:
                World.food_pos = np.delete(World.food_pos, np.where(World.food_pos == ant.pos))
                food_eaten += 1
            
            col = ant.pos % length
            row = int((ant.pos - col) / length)
            World.grid[row, col] = ant.id
    
            # print(World.grid, "\n\n")
    sim_food_eaten[run] = food_eaten
print(sim_food_eaten)
print(time.time()-start_time)