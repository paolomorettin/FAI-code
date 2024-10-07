
import networkx as nx
import numpy as np

class Node:
    
    '''Search node class.'''

    def __init__(self, state, parent=None, path_cost=0, action=None):
        self.state = state
        self.parent = parent
        self.path_cost = path_cost
        self.action = action

    def __str__(self):
        str_parent = self.parent.state if self.parent is not None else 'None'
        nodestr = f"Node(state = {self.state},"
        nodestr += f" parent = {str_parent},"
        nodestr += f" cost = {self.path_cost})"
        return nodestr


class Solution:
    
    '''Solution helper class.  Not much to discuss here.'''

    def __init__(self, goal_node):
        self.path = []
        self.cost = goal_node.path_cost
        curr = goal_node
        while curr is not None: # bottom up visit until the root is reached
            self.path = [curr] + self.path
            curr = curr.parent

    def __getitem__(self, index):
        return self.path[index]

    def __len__(self):
        return len(self.path)

    def __str__(self):
        return "[" + ", ".join(str(n.state) for n in self.path) + f"] ({self.cost})"


class PriorityQueue:
    
    '''Fake 'priority queue' used in best-first search algorithms.

    Complexity: push O(nlogn), pop O(1)
    instead of: push O(logn), pop O(logn)

    Lazily implemented as a list of Nodes that gets sorted at each
    insertion.  Makes no difference for our purposes.'''
    
    def __init__(self, func):
        
        '''Default constructor. 'func' is the sorting criterion,
        i.e. a function mapping Nodes to numerical values.

        '''
        
        self.elements = []
        self.func = func

    def push(self, x):
        self.elements.append(x)
        self.elements.sort(key=self.func)

    def pop(self):
        return self.elements.pop(0)

    def top(self):
        if len(self) > 0:
            return self.elements[0]
        else:
            return None

    def __iter__(self):
        for x in self.elements:
            yield x

    def __len__(self):
        return len(self.elements)

    def __str__(self):
        return "[" + ", ".join(str(n) for n in self.elements) + "]"
        

class Problem:
    
    '''Problem class.'''

    def __init__(self, states, initial, goals, positions=None):
        '''
        Initialize the problem instance with:
        states - a set of states
        initial - an initial state in 'states'
        goals - a set of goals (subset of 'states')
        positions - map states -> 2d coordinates (optional)

        The state space is implemented as dict-of-dicts:
        ((s0) x action) -> (s1, cost)

        '''
        assert(initial in states)
        assert(all([g in states for g in goals]))
        self.state_graph = {s : dict() for s in states}
        self.initial = initial
        self.goals = goals
        self.positions = positions

    def add_action(self, s0, s1, a=None, c=1, undir=False):
        '''
        Add an action to the state space given:
          s0 - the start state in S
          s1 - the destination state in S
          a - action name (optional)
          c - action cost (default: 1)
          undir - undirected (default: false)        

        '''
        assert(s0 in self.state_graph)
        assert(s1 in self.state_graph)
        if a is None:
            action = f'to_{s1}'

        self.state_graph[s0][action] = (s1, c)
        if undir:
            if a is None:
                action = f'to_{s0}'
            self.state_graph[s1][action] = (s0, c)


    def get_actions(self, s):
        '''
        Get the possible actions from state 's'

        '''
        assert(s in self.state_graph)
        return set(self.state_graph[s].keys())

    def is_goal(self, s):
        '''
        Return true if 's' is a goal

        '''
        assert(s in self.state_graph)
        return (s in self.goals)

    def is_weighted(self):
        '''
        Return true if actions have different costs

        '''
        costs = set.union(*[set([self.state_graph[s][a][1]
                                for a in self.state_graph[s]])
                           for s in self.state_graph])
        return len(costs) > 1

    

    def result(self, s, a):
        '''
        Return the destination state and the cost
        of using action 'a' in state 's'.

        '''
        assert(s in self.state_graph)
        assert(a in self.state_graph[s])
        return self.state_graph[s][a]

    def to_graph(self):
        '''
        Convert the prolem instance to a
        networkx directed multigraph.

        '''
        G = nx.DiGraph()
        for s0 in self.state_graph:
            if self.positions is not None:
                pos = self.positions[s0]
            else:
                pos = None
            G.add_node(s0, pos=pos)
            for a in self.state_graph[s0]:
                s1, c = self.state_graph[s0][a]
                G.add_edge(s0, s1, action=a, cost=c)

        return G


def expand(problem, node):

    s0 = node.state
    expanded_states = []
    
    for action in problem.get_actions(s0):
        s_next, cost = problem.result(s0, action)
        expanded_states.append((s_next, cost, action))

    expanded_states.sort(key=lambda x : x[0])
    return [Node(s,
                 parent = node,
                 path_cost = (node.path_cost + c),
                 action=a)
            for s, c, a in expanded_states]

