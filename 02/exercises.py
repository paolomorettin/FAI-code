from copy import deepcopy
import numpy as np
from utils import Problem


################################################## RANDOM GRID PROBLEMS

W, H = 4, 3
P_EDGE = 0.7
MAX_STEPS = H * W 
SEED = 666
GRIDPOS = {n : ((n-1) % W, (n-1) // W) for n in range(1, H*W+1)}

grid1 = Problem.grid(W, H, p_edge=P_EDGE, seed=SEED, initial=1, goals={H*W})
grid2 = Problem.grid(W, H, p_edge=P_EDGE, seed=SEED, initial=3, goals={H*W})
grid3 = Problem.grid(W, H, p_edge=P_EDGE, seed=SEED+1, initial=1, goals={H*W}, cost=[1,10])
grid4 = Problem.grid(W, H, p_edge=P_EDGE, seed=SEED+2, initial=1, goals={H*W}, cost=[1,10])

# more exercises
grid5 = Problem.grid(W, H, p_edge=1.0, seed=SEED, cost=[1,10])
grid6 = Problem.grid(W, H, p_edge=1.0, seed=SEED+1, cost=[1,10])
grid7 = Problem.grid(W, H, p_edge=1.0, seed=SEED+2, cost=[1,10])
grid8 = Problem.grid(W, H, p_edge=1.0, seed=SEED+3, cost=[1,10])


################################################## TREE EXAMPLES


states = list(range(7))
postree = {0 : (3, 2),
           1 : (1, 1),
           2 : (5, 1),
           3 : (0, 0),
           4 : (2, 0),
           5 : (4, 0),
           6 : (6, 0)}

initial = 0

goals1 = {6}
tree1 = Problem(states, initial, goals1)
tree1.add_action(0, 1); tree1.add_action(0, 2)
tree1.add_action(1, 3); tree1.add_action(1, 4)
tree1.add_action(2, 5); tree1.add_action(2, 6)


tree2 = deepcopy(tree1)
tree2.goals = {2}

tree3 = deepcopy(tree1)
tree3.goals = {3}

tree4 = deepcopy(tree1)
tree4.goals = {4, 2}



################################################## PATH EXAMPLES

N = 5
states = list(range(N))
pospath = {n : (n, 1) for n in states}
pospath[N-1] = (N-2, 0)

initial, goal = states[0], states[-1]

path1 = Problem(states, initial, {goal})
for i in range(len(states) - 1):
    path1.add_action(states[i], states[i+1])

path1.add_action(initial, goal)

path2 = Problem(states, initial, {goal})
for i in range(len(states) - 1):
    path2.add_action(states[i], states[i+1], c=1)

path2.add_action(initial, goal, c=N-2)

path3 = Problem(states, initial, {goal})
for i in range(len(states) - 1):
    path3.add_action(states[i], states[i+1], c=1)

path3.add_action(initial, goal, c=N)
