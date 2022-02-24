class Problem():
    def __init__(self, initial_state,
                 goal_state=None):
        self.initial_state = initial_state
        self.goal_state = goal_state

    def actions(self, state):
        raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def is_goal(self, state):
        return state == self.goal_state

    def action_cost(self, state1, action, state2):
        return 1

    def h(self, node):
        return 0

#----------------------------------------------------------------------------------

class RouteProblem(Problem):
    
    def __init__(self, initial_state,
                 goal_state=None,
                 map_graph=None,
                 map_coords=None):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.map_graph = map_graph
        self.map_coords = map_coords
        self.neighbors = {}
  
        for pair in map_graph.keys():
            self.neighbors[pair[0]] = self.neighbors[pair[0]] + [pair[1]] if (pair[0] in self.neighbors.keys()) else [pair[1]]


    def actions(self, state):
        possibleDestinations = []
        if state:
            if state in self.neighbors.keys():
                for state in self.neighbors[state]:
                    possibleDestinations.append(state)
        return possibleDestinations


    def result(self, state, action):
        if action in self.neighbors[state]:
            return action
        else:
            return state

    def action_cost(self, state1, action, state2):
        return self.map_graph[(state1,action)]


    def h(self, node):
        nodeCoords = self.map_coords(node.state)
        goalCoords = self.map_coords(self.goal_state)
        distance = (
            (goalCoords[0]-nodeCoords[0])**2 +
                        (goalCoords[1]-nodeCoords[1])**2 ) **(1/2)
        return distance

