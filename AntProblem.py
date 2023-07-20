import time
import sys
import numpy as np
np.set_printoptions(threshold=sys.maxsize)
start_time = time.time()

# Class to represent world grid
class WorldGrid:
    def __init__(self, length, width, num_food, track_grid=False):
        # Place food in random locations
        self.food_pos = np.random.choice(length*width, num_food, replace=False)
        self.food_eaten = 0
        self.track_grid = track_grid

        # place -1 in food locations
        if self.track_grid:
            self.grid = np.zeros(length*width).reshape(length, width)
            cols = self.food_pos % length
            rows = (self.food_pos - cols) / length
            self.grid[rows.astype(int), cols.astype(int)] = -1

    def checkIfFoodPos(self, position):
        # Check if ant in food position, remove food from grid and update count if it is.
        if position in self.food_pos:
            self.food_pos = np.delete(self.food_pos, np.where(World.food_pos == position))
            self.food_eaten += 1

            # Update grid
            if self.track_grid:
                col = a.pos % length
                row = int((a.pos - col) / length)
                World.grid[row, col] = a.id

            return True
        
        else:
            return False


# Class that represents each ant
class Ant:
    def __init__(self, length, width, id, pos, num_moves):
        self.id = id # Identifier for ant
        self.pos = pos # Initializing ant position
        # self.moves = np.random.choice([-1, 1, length, -length], num_moves) # Generating a sequence of random moves for ant
        self.food_eaten = 0
    
    def move(self, move):
        col = self.pos % length # Column where ant is located
        
        if (col + move) < 0: # Checking for left bound
            return
        elif (col + move) > (length-1): # Checking for right bound
            return
        elif (self.pos+move) < 0 or (self.pos+move) >= (length*width): # Checking for upper and lower bound
            return
        else:
            self.pos += move # Updating ant position

# Initialize random food positions, random starting positions for ants, and random moves for ants
class RandomInitialization:
    def __init__(self, length, width, num_ants, num_moves, num_simulations):
        self.ant_starting_positions = np.random.choice(length*width, (num_simulations, num_ants)) # Initializing all random starting position for ants on all simulations
        self.moves = np.random.choice([-1, 1, length, -length], (num_simulations, num_moves)) # Generating a sequence of random moves for ant
        


grid_tracking = False

# Grid dimensions
length = 100
width = length

# Simulation parameters
food_droppings = 10
ants_total = 100
time_steps = 100
simulation_runs = 1000

sim_food_eaten = np.zeros(simulation_runs) # Array to track food eaten per simulation

x = RandomInitialization(length, width, ants_total, time_steps, simulation_runs)

# Iterate all simulations
for run in range(simulation_runs):
    food_eaten = 0
    World = WorldGrid(length, width, food_droppings, track_grid=grid_tracking)

    ants = list()
    id = 1
    # ant_starting_positions = np.random.choice(length*width, ants_total) # Initializing all random starting position for ants

    # Initialize all ant objects
    for i in range(ants_total):
        a = Ant(length, width, id, x.ant_starting_positions[run, i], time_steps)
        ants.append(a)

        # Check if ant in food position, increment food eaten in World and ant object if so
        if World.checkIfFoodPos(a.pos):
            a.food_eaten += 1

        id += 1

    # Iterate each time step for each ant
    for t in range(time_steps):
        for ant in ants:
            ant.move(x.moves[run, t]) # Make move from random move list sequence

            # Check if ant in food position, increment food eaten in World and ant object if so
            if World.checkIfFoodPos(ant.pos):
                ant.food_eaten += 1
                
    sim_food_eaten[run] = World.food_eaten

print(sim_food_eaten)

print("Mean of Total Food Eaten:", np.mean(sim_food_eaten))
print("Standard Deviation of Total Food Eaten:", np.std(sim_food_eaten))
print(time.time()-start_time)