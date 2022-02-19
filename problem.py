class Problem(object):
    def __init__(self, initial_state, goal_state=None):
        self.initial_state = initial_state 
        self.goal_state = goal_state

    def actions(self,state):
        raise NotImplementedError
    
    def result(self,state, action):
        raise NotImplementedError

    def is_goal(self,state):
        return state == self.goal_state
    
    def action_cost(self,state1,action,state2):
        return 1
    
    def h(self,node):
        return 0