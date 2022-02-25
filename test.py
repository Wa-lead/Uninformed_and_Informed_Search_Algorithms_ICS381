from problem import *


example_walls = [(4,3), (5,1), (5,2)] 
example_food = [(3,1), (2,3), (4,5)]
example_grid_problem = GridProblem(initial_state=(7,4),
 N=5, M=7, 
 wall_coords=example_walls,
 food_coords=example_food)


print(example_grid_problem.result((1,1), 'up') )

