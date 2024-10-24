from copy import deepcopy
import numpy as np
from utils import Problem

################################################## RANDOM GRID EXERCISES


def random_grid_problem(width, height, p_edge=0.5, cost=None, seed=0):
        '''
        Generate a random grid problem.

        '''
        
        states = []
        positions = {}
        s = 1        
        for y in range(height):
            for x in range(width):
                states.append(s)
                positions[s] = (x,y)
                s += 1

        initial = 1
        goals = {s-1}
        problem = Problem(states, initial, goals, positions=positions)        
        np.random.seed(seed)
        sxy = lambda x, y: 1 + x + width * y
        for y in range(height - 1):
            for x in range(width - 1):
                for x2,y2 in [(x+1, y), (x, y+1)]:
                    if np.random.random() < p_edge:
                        if cost is not None:
                            c = np.random.randint(cost[0], cost[1]+1)
                        else:
                            c = 1

                        problem.add_action(sxy(x,y), sxy(x2, y2),
                                           c=c, undir=True)

        y = (height - 1)
        for x in range(width - 1):
            print(f"(x,y) : ({x},{y}) -- s : {sxy(x,y)}")
            if np.random.random() < p_edge:
                if cost is not None:
                    c = np.random.randint(cost[0], cost[1]+1)
                else:
                    c = 1

                problem.add_action(sxy(x,y), sxy(x+1, y),
                                   c=c, undir=True)

        x = (width - 1)
        for y in range(height - 1):
            print(f"(x,y) : ({x},{y}) -- s : {sxy(x,y)}")
            if np.random.random() < p_edge:
                if cost is not None:
                    c = np.random.randint(cost[0], cost[1]+1)
                else:
                    c = 1

                problem.add_action(sxy(x,y), sxy(x, y+1),
                                   c=c, undir=True)
                

        return problem

def sg_sxy(x, y, graph_width):
    s = 1
    for y_p in range(y):
        s += graph_width if y_p % 2 == 0 else graph_width - 1
    s += x
    return s
    
def sg_find_long_line_neighbours(x, y, width, height):
    neighbours = []
    if y % 2 == 0:
        if(x == 0 or x == width - 1):
            for y_p in range(0, height, 2):
                if(y != y_p):
                    neighbours.append(sg_sxy(x, y_p, width))
        if(y == 0 or y == height - 1):
            for x_p in range(0, width, 1):
                if(x_p < x - 1 or x + 1 < x_p):
                    neighbours.append(sg_sxy(x_p, y, width))
    return neighbours
    
def sg_find_exa_neighbours(x, y, width, height):
    neighbours = []
    w_act = width if y % 2 == 0 else width - 1
    if(x - 1 >= 0): #LEFT
        neighbours.append(sg_sxy(x-1, y, width))
    if(x + 1 < w_act): #RIGHT
        neighbours.append(sg_sxy(x+1, y, width))
    if(y % 2 == 0):
        if(x < width - 1 and y + 1 < height): #Top-Right
            neighbours.append(sg_sxy(x, y+1, width))
        if(x < width - 1 and y - 1 >= 0): #Bottom-Right
            neighbours.append(sg_sxy(x, y-1, width))
        if(x - 1 >= 0 and y + 1 < height): #Top-Left
            neighbours.append(sg_sxy(x-1, y+1, width))
        if(x - 1 >= 0 and y - 1 >= 0): #Bottom-Left
            neighbours.append(sg_sxy(x-1, y-1, width))
    else:
        if(x + 1 < width and y + 1 < height): #Top-Right
            neighbours.append(sg_sxy(x+1, y+1, width))
        if(x + 1 < width and y - 1 >= 0): #Bottom-Right
            neighbours.append(sg_sxy(x+1, y-1, width))
        if(y + 1 < height): #Top-Left
            neighbours.append(sg_sxy(x, y+1, width))
        if(y - 1 >= 0): #Bottom-Left
            neighbours.append(sg_sxy(x, y-1, width))
    return neighbours

def strange_grid_problem(width, height, p_edge=0.3, cost=None, seed=0):
    states = []
    positions = {}
    s = 1        
    for y in range(height):
        if y % 2 == 0:
            for x in range(width):
                states.append(s)
                positions[s] = (x,y)
                s += 1
        else:
            for x in range(width - 1):
                states.append(s)
                positions[s] = (x+0.5,y)
                s += 1
     
    initial = 1
    goals = {s-1}
    problem = Problem(states, initial, goals, positions=positions)        
    np.random.seed(seed)
    
    for y in range(height):
        w_act = width if y % 2 == 0 else width - 1
        for x in range(w_act):
            s = sg_sxy(x, y, width)
            for neighbour in sg_find_exa_neighbours(x, y, width, height) + sg_find_long_line_neighbours(x, y, width, height):
                if np.random.random() < p_edge:
                    if cost is not None:
                        c = np.random.randint(cost[0], cost[1]+1)
                    else:
                        c = 1
                    problem.add_action(s, neighbour, c=c, undir=False)

    return problem    
    
named_exercises = {}

################################################## [SLIDES] TREE EXAMPLES


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
tree1 = Problem(states, initial, goals1, positions=postree)
tree1.add_action(0, 1); tree1.add_action(0, 2)
tree1.add_action(1, 3); tree1.add_action(1, 4)
tree1.add_action(2, 5); tree1.add_action(2, 6)


tree2 = deepcopy(tree1)
tree2.goals = {2}

tree3 = deepcopy(tree1)
tree3.goals = {3}

tree4 = deepcopy(tree1)
tree4.goals = {4, 2}

named_exercises.update({
        'tree1' : tree1,
        'tree2' : tree2,
        'tree3' : tree3,
        'tree4' : tree4
        })


################################################## [SLIDES] QUICK EXERCISES

N = 5
states = list(range(N))
pospath = {n : (n, 1) for n in states}
pospath[N-1] = (N-2, 0)

initial, goal = states[0], states[-1]

path1 = Problem(states, initial, {goal}, positions=pospath)
for i in range(len(states) - 1):
    path1.add_action(states[i], states[i+1])

path1.add_action(initial, goal)

path2 = Problem(states, initial, {goal}, positions=pospath)
for i in range(len(states) - 1):
    path2.add_action(states[i], states[i+1], c=1)

path2.add_action(initial, goal, c=N-2)

path3 = Problem(states, initial, {goal}, positions=pospath)
for i in range(len(states) - 1):
    path3.add_action(states[i], states[i+1], c=1)

path3.add_action(initial, goal, c=N)

named_exercises.update({
        'path1' : path1,
        'path2' : path2,
        'path3' : path3,
        })

################################################## WEIGHTED PROBLEMS

N = 10
states = list(range(N))
weightedpos = {0 : (0,2),
               1 : (0,1),
               2 : (0,0),
               3 : (1,1),
               4 : (2,2),
               5 : (2,1),
               6 : (2,0),
               7 : (3,2),
               8 : (3,1),
               9 : (3,0)}

initial, goal = 3, 8


weighted1 = Problem(states, initial, {goal}, positions=weightedpos)

weighted1.add_action(0, 1, c=1, undir=True)
weighted1.add_action(1, 2, c=2, undir=True)

weighted1.add_action(1, 3, c=1, undir=True)
weighted1.add_action(3, 5, c=3, undir=True)

weighted1.add_action(4, 5, c=1, undir=True)
weighted1.add_action(5, 6, c=2, undir=True)

weighted1.add_action(4, 7, c=2, undir=True)
weighted1.add_action(5, 8, c=666, undir=True)
weighted1.add_action(6, 9, c=1, undir=True)

weighted1.add_action(7, 8, c=5, undir=True)
weighted1.add_action(8, 9, c=2, undir=True)

N = 12
states = list(range(N))
weightedpos = {0 : (0,2),
               1 : (0,1),
               2 : (0,0),
               3 : (1,2),
               4 : (1,1),
               5 : (1,0),
               6 : (2,2),
               7 : (2,1),
               8 : (2,0),
               9 : (3,2),
               10 : (3,1),
               11 : (3,0),
               }

initial, goal = 4, 10
weighted2 = Problem(states, initial, {goal}, positions=weightedpos)

weighted2.add_action(0, 1, c=1, undir=True)
weighted2.add_action(1, 2, c=2, undir=True)

weighted2.add_action(1, 4, c=1, undir=True)
weighted2.add_action(4, 7, c=3, undir=True)

weighted2.add_action(6, 7, c=1, undir=True)
weighted2.add_action(7, 8, c=2, undir=True)

weighted2.add_action(6, 9, c=2, undir=True)
weighted2.add_action(7, 10, c=666, undir=True)
weighted2.add_action(8, 11, c=1, undir=True)

weighted2.add_action(9, 10, c=5, undir=True)
weighted2.add_action(10, 11, c=2, undir=True)


named_exercises.update({
        'weighted1' : weighted1,
        'weighted2' : weighted2,
        })
