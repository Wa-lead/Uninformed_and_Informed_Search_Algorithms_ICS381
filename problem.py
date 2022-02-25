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

# ----------------------------------------------------------------------------------


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

        # Create neigbour dict
        for pair in map_graph.keys():
            if pair[0] not in self.neighbors.keys():
                self.neighbors[pair[0]] = []
            if pair[1] not in self.neighbors.keys():
                self.neighbors[pair[1]] = []
            self.neighbors[pair[1]] += pair[0]
            self.neighbors[pair[0]] += pair[1]

    def actions(self, state):
        possibleDestinations = []
        if state:
            for (state1, state2) in self.map_graph:
                if state == state1:
                    possibleDestinations.append(state2)
        return possibleDestinations

    def result(self, state, action):
        if state and action:
            if (state, action) in self.map_graph.keys():
                return action
            else:
                return state

    def action_cost(self, state1, action, state2):
        return self.map_graph[(state1, action)]

    def h(self, node):
        if node.state == self.goal_state:
            return 0
        else:
            nodeCoords = self.map_coords[node.state]
            goalCoords = self.map_coords[self.goal_state]
            distance = (
                (goalCoords[0]-nodeCoords[0])**2 +
                (goalCoords[1]-nodeCoords[1])**2) ** (1/2)
            return distance

# ---------------------------------------------------------------


class GridProblem(Problem):
    def __init__(self, initial_state,
                 N,
                 M,
                 wall_coords,
                 food_coords
                 ):
        self.N = N
        self.M = M
        self.goal_state = None
        self.wall_coords = wall_coords
        self.food_coords = food_coords
        self.food_eaten = []

        for food in self.food_coords:
            self.food_eaten.append(False)

        self.food_eaten = tuple(self.food_eaten)
        self.initial_state = (initial_state, self.food_eaten)

    def actions(self, state):
        possibleActions = []
        if self.isSafe(state[0]):
            [x, y] = state[0]
            theoriticalActions = {
                'up': (x, y+1),
                'right': (x+1, y),
                'down': (x, y-1),
                'left': (x-1, y),
            }
            for action in theoriticalActions.keys():
                if self.isSafe(theoriticalActions[action]):
                    possibleActions.append(action)
        return possibleActions




    def result(self, state, action):
        if self.isSafe(state[0]):
            if action in self.actions(state):
                bro = tuple(self.nextState(state, action))
                return bro
            else:
                return state

    def nextState(self, state, action):
        newState = []
        [x, y] = list(state[0]) #change format of state coords

        if action == 'up':
            stateCoords = tuple([x, y+1]) #update state coords after action
            newState = [stateCoords, state[1]] #create the format of state
            if stateCoords in self.food_coords: #if new cords are the same as a food
                food_eaternList = list(newState[1])
                food_eaternList[self.food_coords.index(stateCoords)] = True
                newState[1] = tuple(food_eaternList)

        elif action == 'down':
            stateCoords = tuple([x, y-1]) #update state coords after action
            newState = [stateCoords, state[1]] #create the format of state
            if stateCoords in self.food_coords: #if new cords are the same as a food
                food_eaternList = list(newState[1])
                food_eaternList[self.food_coords.index(stateCoords)] = True
                newState[1] = tuple(food_eaternList)

        elif action == 'left':
            stateCoords = tuple([x - 1, y]) #update state coords after action
            newState = [stateCoords, state[1]] #create the format of state
            if stateCoords in self.food_coords: #if new cords are the same as a food
                food_eaternList = list(newState[1])
                food_eaternList[self.food_coords.index(stateCoords)] = True
                newState[1] = tuple(food_eaternList)

        elif action == 'right':
            stateCoords = tuple([x +1, y]) #update state coords after action
            newState = [stateCoords, state[1]] #create the format of state
            if stateCoords in self.food_coords: #if new cords are the same as a food
                food_eaternList = list(newState[1])
                food_eaternList[self.food_coords.index(stateCoords)] = True
                newState[1] = tuple(food_eaternList)

        return newState



    def isSafe (self, coords):
        if coords[0] > self.M:
            return False
        elif coords[1] > self.N:
            return False
        elif coords in self.wall_coords:
            return False
        else: 
            return True
