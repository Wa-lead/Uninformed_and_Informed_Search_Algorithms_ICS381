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
        self.wall_coords = wall_coords
        self.food_coords = food_coords
        self.goal_state = tuple((True for i in range(len(self.food_coords))))
        food_eaten = []

        for food in self.food_coords:
            food_eaten.append(False)

        food_eaten = tuple(food_eaten)
        self.initial_state = (initial_state, food_eaten)

    def actions(self, state):
        possibleActions = []
        if self.isSafe(state[0]):  # just an additional check
            [x, y] = state[0]
            theoriticalActions = {  # store all possible transitions from this state
                'up': (x, y+1),
                'down': (x, y-1),
                'right': (x+1, y),
                'left': (x-1, y),
            }
            for action in theoriticalActions.keys():  # check if the states resulted are actually possible transitions
                # if the transition is safe, store the action in possible actions
                if self.isSafe(theoriticalActions[action]):
                    possibleActions.append(action)
        return possibleActions

    def result(self, state, action):
        if self.isSafe(state[0]):  # additional check
            # check if the action can possible be done in the state's possible actions
            if action in self.actions(state):
                return self.nextState(state, action)
            else:
                return state

    def is_goal(self, state):
        return state[1] == self.goal_state

    def nextState(self, state, action):
        newState = []
        x, y = state[0]  # change format of state coords

        if action == 'up':
            stateCoords = (x, y+1)  # update state coords after action
            newState = [stateCoords, state[1]]  # create the format of state
            if stateCoords in self.food_coords:  # if new cords are the same as a food
                food_eaternList = list(newState[1])
                food_eaternList[self.food_coords.index(stateCoords)] = True
                newState[1] = tuple(food_eaternList)
        elif action == 'down':
            stateCoords = (x, y-1)  # update state coords after action
            newState = [stateCoords, state[1]]  # create the format of state
            if stateCoords in self.food_coords:  # if new cords are the same as a food
                food_eaternList = list(newState[1])
                food_eaternList[self.food_coords.index(stateCoords)] = True
                newState[1] = tuple(food_eaternList)
        elif action == 'left':
            stateCoords = (x-1, y)  # update state coords after action
            newState = [stateCoords, state[1]]  # create the format of state
            if stateCoords in self.food_coords:  # if new cords are the same as a food
                food_eaternList = list(newState[1])
                food_eaternList[self.food_coords.index(stateCoords)] = True
                newState[1] = tuple(food_eaternList)
        elif action == 'right':
            stateCoords = (x+1, y)  # update state coords after action
            newState = [stateCoords, state[1]]  # create the format of state
            if stateCoords in self.food_coords:  # if new cords are the same as a food
                food_eaternList = list(newState[1])
                food_eaternList[self.food_coords.index(stateCoords)] = True
                newState[1] = tuple(food_eaternList)

        return tuple(newState)

    def h(self, node):
        if self.is_goal(node.state):
            return 0
        x, y = node.state[0]
        distance = 100000
        for i in range(len(node.state[1])):
            if node.state[1][i] == False:
                x2, y2 = self.food_coords[i]
                mDis = abs(x - x2) + abs(y - y2)
                if mDis < distance:
                    distance = mDis
        return distance

    def isSafe(self, coords):
        if coords[0] > self.M or coords[0] < 1:
            return False
        elif coords[1] > self.N or coords[1] < 1:
            return False
        elif coords in self.wall_coords:
            return False
        else:
            return True
