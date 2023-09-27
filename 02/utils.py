
import networkx as nx
import numpy as np

class Node:
    '''
    Search node class.

    '''

    def __init__(self, state, parent=None, succ=None, path_cost=0, action=None):
        self.state = state
        self.parent = parent
        self.succ = succ
        self.path_cost = path_cost
        self.action = action

    def __str__(self):
        str_parent = self.parent.state if self.parent is not None else 'None'
        str_succ = self.succ.state if self.succ is not None else 'None'
        return f"<{self.state}, {str_parent}, {str_succ}, {self.path_cost}>"


class Solution:

    def __init__(self):
        self.path = []
        self.cost = []

    def __getitem__(self, index):
        return self.path[index]

    def __len__(self):
        return len(self.path)

    def __str__(self):
        return "[" + ", ".join(str(n.state) for n in self.path) + f"] ({self.cost})"

    @staticmethod
    def create(final_node):

        solution = Solution()
        solution.cost = final_node.path_cost
        x = final_node
        
        while x is not None:
            solution.path = [x] + solution.path
            x = x.parent

        return solution

    @staticmethod
    def join(is_forward, node1, node2):

        assert(node1.state == node2.state)
        solution = Solution()

        if is_forward:
            forward_node, backward_node = node1, node2
        else:
            forward_node, backward_node = node2, node1

        solution.cost = forward_node.path_cost + backward_node.path_cost
        x = forward_node
        
        while x is not None:
            solution.path = [x] + solution.path
            x = x.parent

        x = backward_node.succ
        while x is not None:
            solution.path.append(x)
            x = x.succ

        return solution



class PriorityQueue:
    '''
    Fake 'priority queue' used in best-first search algorithms.

    Complexity: push O(nlogn), pop O(1)
    instead of: push O(logn), pop O(logn)

    Lazily implemented as a list that gets sorted at each insertion.
    Makes no difference for our purposes.
.

    '''
    def __init__(self, func):
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
    '''
    Problem class.

    '''

    def __init__(self, states, initial, goals):
        '''
        Initialize the problem instance with:
        states - a set of states
        initial - an initial state in 'states'
        goals - a set of goals (subset of 'states')

        The state space is implemented as dict-of-dicts:
        ((s0) x action) -> (s1, cost)

        '''
        assert(initial in states)
        assert(all([g in states for g in goals]))
        self.state_graph = {s : dict() for s in states}
        self.initial = initial
        self.goals = goals

    def add_action(self, s0, s1, a=None, c=1, undir=False):
        '''
        Add an action to the state space given:
          s0 - the start state in S
          s1 - the destination state in S
          a - the action resulting in (s0 -> s1)
          c - the cost of a (default: 1)
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
            G.add_node(s0)
            for a in self.state_graph[s0]:
                s1, c = self.state_graph[s0][a]
                G.add_edge(s0, s1, action=a, cost=c)

        return G
        

    @staticmethod
    def grid(w, h, initial=None, goals=None, p_edge=0.5, cost=None, seed=0):
        '''
        Generate a grid problem.

        '''
        states = set(range(1, h * w + 1))

        np.random.seed(seed)        
        initial = np.random.choice(list(states)) if initial is None else initial
        goals = {np.random.choice(list(states - {initial}))} if goals is None else goals

        problem = Problem(states, initial, goals)


        sxy = lambda x, y: 1 + x + w * y
        for y in range(h - 1):
            for x in range(w - 1):

                
                c = np.random.randint(cost[0], cost[1]+1) if cost is not None else 1
                if np.random.random() < p_edge:
                    problem.add_action(sxy(x, y), sxy(x + 1, y), c=c)
                if np.random.random() < p_edge:
                    problem.add_action(sxy(x + 1, y), sxy(x, y), c=c)


                c = np.random.randint(cost[0], cost[1]+1) if cost is not None else 1
                if np.random.random() < p_edge:
                    problem.add_action(sxy(x, y), sxy(x, y + 1), c=c)
                if np.random.random() < p_edge:
                    problem.add_action(sxy(x, y + 1), sxy(x, y), c=c)

            c = np.random.randint(cost[0], cost[1]+1) if cost is not None else 1
            if np.random.random() < p_edge:
                problem.add_action(sxy(x + 1, y), sxy(x + 1, y + 1), c=c)
            if np.random.random() < p_edge:
                problem.add_action(sxy(x + 1, y + 1), sxy(x + 1, y), c=c)

        for x in range(w - 1):
            c = np.random.randint(cost[0], cost[1]+1) if cost is not None else 1
            if np.random.random() < p_edge:
                problem.add_action(sxy(x, y + 1), sxy(x + 1, y + 1), c=c)
            if np.random.random() < p_edge:
                problem.add_action(sxy(x + 1, y + 1), sxy(x, y + 1), c=c)

        return problem
    


def expand(problem, node, reverse=False):

    s0 = node.state
    expanded_states = []
    
    if not reverse:
        for action in problem.get_actions(s0):
            s_next, cost = problem.result(s0, action)
            expanded_states.append((s_next, cost, action))

        expanded_states.sort(key=lambda x : x[0])
        return [Node(s, parent = node, path_cost = (node.path_cost + c), action=a)
                for s, c, a in expanded_states]

    else:
        for s_candidate in problem.state_graph:
            for action in problem.get_actions(s_candidate):
                s_next, cost = problem.result(s_candidate, action)
                if s_next == s0:
                    expanded_states.append((s_candidate, cost, action))

        expanded_states.sort(key=lambda x : x[0])
        return [Node(s, succ = node, path_cost = (node.path_cost + c), action=a)
                for s, c, a in expanded_states]
                
    
