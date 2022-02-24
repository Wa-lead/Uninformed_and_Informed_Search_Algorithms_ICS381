from node import Node
import heapq

class PriorityQueue:
    def __init__(self, items=(), priority_function=(lambda x: x)):
        self.priority_function = priority_function
        self.pqueue = []
        # add the items to the PQ
        for item in items:
            self.add(item)

    def add(self, item):
        pair = (self.priority_function(item), item)
        heapq.heappush(self.pqueue, pair)

    def pop(self):
        return heapq.heappop(self.pqueue)[1]

    def __len__(self):
        return len(self. pqueue)
#-----------------------------------------------------------------------------------------------------------
def expand(problem, node):
    s = node.state
    yieldedChildren = []
    for action in problem.actions(s):
        sPrime = problem.result(s,action)
        cost = node.path_cost + problem.action_cost(s,action,sPrime)
        yieldedChildren.append(Node(state=sPrime, parent_node=node, action_from_parent=action, path_cost=cost))
    return yieldedChildren


def get_path_actions(node): #not sure about it
    actionsList = []
    while node != None:
        if node.parent_node != None:
            actionsList.append(node.action_from_parent)
        node = node.parent_node
    return actionsList[::-1]


def get_path_states(node):
    statesList = []
    while node != None:
        statesList.append(node.state)
        node = node.parent_node
    return statesList[::-1]
        

def best_first_search(problem,f):
    node = Node(state=problem.initial_state)
    frontier = PriorityQueue(items=[node], priority_function=f)
    reached = {problem.initial_state: node}
    while frontier:
        node = frontier.pop()
        if problem.is_goal(node.state):
            return node
        for child in expand(problem, node):
            s = child.state
            if (s not in reached.keys()) or child.path_cost < reached[s].path_cost:
                reached[s] = child
                frontier.add(child)
    return None



def best_first_search_treelike(problem,f):
    node = Node(state=problem.initial_state)
    frontier = PriorityQueue(items=[node], priority_function=f)
    while frontier.__len__() > 0:
        node = frontier.pop()
        if problem.is_goal(node.state):
            return node
        for child in expand(problem, node): ## deleted the s = child.state cause no need
            frontier.add(child)
    return None

#----------------------------------------------------------------
def breadth_first_search(problem, treelike = False):
    if treelike:
        goal = best_first_search_treelike(problem, f=lambda node: node.depth)
    else: 
        goal = best_first_search(problem, f=lambda node: node.depth)
    return goal

#----------------------------------------------------------------

def depth_first_search(problem,treelike = False):
    if treelike:
        goal = best_first_search_treelike(problem, f=lambda node: -1*node.depth)
    else: 
        goal = best_first_search(problem, f=lambda node: -1*node.depth)
    return goal

#----------------------------------------------------------------

def uniform_cost_search(problem, treelike = False):
    if treelike:
        goal = best_first_search_treelike(problem, f=lambda node: node.path_cost)
    else: 
        goal = best_first_search(problem, f=lambda node: node.path_cost)
    return goal
#----------------------------------------------------------------


def greedy_search(problem, h, treelike = False ):
    if treelike:
        goal = best_first_search_treelike(problem, f=lambda node: h(node))
    else: 
        goal = best_first_search(problem, f=lambda node: h(node))
    return goal

#----------------------------------------------------------------


def astar_search(problem, h, treelike = False ):
    if treelike:
        goal = best_first_search_treelike(problem, f=lambda node: h(node)+node.path_cost)
    else: 
        goal = best_first_search(problem, f=lambda node: h(node)+node.path_cost)
    return goal




