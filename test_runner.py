from problem import *
from search_algorithms import *
from node import Node
from collections import Counter

"""
    For those who are interested what this class does. Others can safely ignore.
    
    We want to implement a wrapper class that will count the 
    number of times a function is called. Particularly, we want to count the number of times
    a node: is popped from frontier and is generated. 
    To count the number of times a node is popped, notice that we call p.is_goal right after.
    So, we just need to count number of times is_goal is called for a Problem object.
    To counter number of times a node is generated, notice that we call p.result.
    So, we just need to count number of times result is called for a Problem object.
"""
class CallCounter:
    def __init__(self, obj):
        self.object = obj # the object being wrapped, for this assignment, it will be a Problem object
        self.counter = Counter() # the count dictionary for function calls
        
    def __getattr__(self, attr):
        self.counter[attr] += 1 # everytime function attr is called, increment the counter for it
        return getattr(self.object, attr) # then call the function 


"""
    Given a list of searchers and problems, prints the statistics report.
"""
def print_stat_report(searchers, problems, searcher_names=None):
    for i, searcher in enumerate(searchers):
        sname = searcher.__name__
        if searcher_names is not None:
            sname = searcher_names[i]
        print(sname)
        total_counts = Counter()
        for p in problems:
            prob   = CallCounter(p) # wrap the problem object in the counter
            soln   = searcher(prob) # run search algorithm
            counter = prob.counter;  # get the counter dict
            
            # get solution cost
            if soln is None:        
                counter.update(solndepth=0, solncost=0)
            else:
                counter.update(solndepth=soln.depth, solncost=soln.path_cost)
                
            # maintain total for the current search algorithm
            total_counts += counter
            print_counts_helper(counter, str(p)[:30])
        print_counts_helper(total_counts, 'TOTAL\n')
        print('----------------------------------------------------------------')
        
def print_counts_helper(counter, name):
    print('{:9,d} generated nodes |{:9,d} popped |{:5.0f} solution cost |{:8,d} solution depth | {}'.format(
          counter['result'], counter['is_goal'], counter['solncost'], counter['solndepth'], name))

if __name__ == "__main__":
    # route problem example
    example_map_graph = { 
    ('A', 'B'): 1,
    ('A', 'C'): 1,
    ('A', 'D'): 1,
    ('B', 'A'): 1,
    ('B', 'C'): 1,
    ('B', 'E'): 1,
    ('C', 'B'): 1
    }

    example_coords = {
    'A': (1,2),
    'B': (0,1), 
    'C': (1,1),
    'D': (2,1),
    'E': (0,0),
    }

    example_route_problem = RouteProblem(initial_state='A', goal_state='E', 
                                         map_graph=example_map_graph, 
                                         map_coords=example_coords)

    # grid problem example
    example_walls = [(4,3), (5,1), (5,2)] 

    example_food = [(3,1), (2,3), (4,5)]
                    
    example_grid_problem = GridProblem(initial_state=(7,4), 
                                       N=5, M=7, 
                                       wall_coords=example_walls,
                                       food_coords=example_food)
    
    # get some statistics on generated nodes, popped nodes, solution
    searchers1 = [breadth_first_search, depth_first_search, uniform_cost_search]
    problems = [example_route_problem, example_grid_problem]
    print_stat_report(searchers1, problems, searcher_names=['BFS', 'DFS', 'UCS'])
    
    # note: to use print_stat_report with search algorithms that take in more than the problem argument, 
    # you need to wrap the search algorithm in a wrapper.
    # for example, to use astar treelike version on a route problem p, you can define the following wrapper.
    def astar_treelike_wrapper(p):
        return astar_search(p, h=p.h, treelike=True)
        
    # Or a convenient alternative is to define lambda function (lambda p: greedy_search(p, h=p.h_euclidean, treelike=True))
    searchers2 = [astar_treelike_wrapper, (lambda p: astar_search(p, h=p.h)), (lambda p: greedy_search(p, h=p.h, treelike=False))]
    print_stat_report(searchers2, problems, searcher_names=['astar_treelike', 'astar', 'greedy'])
    
    # add your own problems and try printing report. try adding the route problems from the slides