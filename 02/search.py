
from utils import expand, Node, PriorityQueue, Solution


def best_first_search(problem, f, max_steps=100, printer=None):

    n = Node(problem.initial)
    frontier = PriorityQueue(f)
    reached = dict()
    solution = None
    
    if printer is not None:
        printer(0, problem, frontier, reached, None, solution)

    reached[n.state] = n.path_cost    
    frontier.push(n)
    
    if printer is not None:
        printer(1, problem, frontier, reached, None, solution)

    n_steps = 0
    while len(frontier) > 0 and n_steps < max_steps:

        n = frontier.pop()

        if problem.is_goal(n.state):
            
            solution = Solution.create(n)

            if printer is not None:
                printer(2 + n_steps, problem, frontier, reached, n, solution)

            return solution
        else:
            for child in expand(problem, n):
                if child.state not in reached or child.path_cost < reached[child.state]:
                    reached[child.state] = child.path_cost
                    frontier.push(child)

        if printer is not None:
            printer(2 + n_steps, problem, frontier, reached, n, solution)

        n_steps += 1

    return None


def bidirectional_path_cost_search(problem, max_steps=100, printer=None):

    def proceed(is_forward, problem, frontier, reached, reached2, solution):

        n = frontier.pop()

        for child in expand(problem, n, reverse=(not is_forward)):
            s = child.state
            if s not in reached or child.path_cost < reached[s].path_cost:
                reached[s] = child
                frontier.push(child)
                if s in reached2: 
                    solution2 = Solution.join(is_forward, child, reached2[s])
                    if not isinstance(solution, Solution) or solution2.cost < solution.cost:
                        solution = solution2

        return solution

    def terminated(solution, frontier1, frontier2):
        return solution == 'failure' or ((len(frontier1) == 0) and (len(frontier2) == 0))

    path_cost = lambda n : (n.path_cost, n.state)

    assert(len(problem.goals) == 1)

    frontier_f = PriorityQueue(path_cost)
    frontier_b = PriorityQueue(path_cost)

    reached_f = dict()
    reached_b = dict()

    solution = 'failure'

    if printer is not None:
        full_frontier = frontier_f.elements + frontier_b.elements
        full_reached = set(reached_f.keys()).union(set(reached_b.keys()))
        printer(0, problem, full_frontier, full_reached, None, solution)

    node_f = Node(problem.initial)
    node_b = Node(list(problem.goals)[0])

    frontier_f.push(node_f)
    frontier_b.push(node_b)

    reached_f[node_f.state] = node_f
    reached_b[node_b.state] = node_b

    it = 1
    while not terminated(solution, frontier_f, frontier_b):

        print('frontier_f', frontier_f)
        print('frontier_b', frontier_b)
        print('reached_f', reached_f.keys())
        print('reached_b', reached_b.keys())
        print('solution', solution)
        print('---')

        it += 1
        
        if len(frontier_f) == 0:
            backwards = False
            
        elif len(frontier_b) == 0 or frontier_f.top().path_cost >= frontier_b.top().path_cost:
            backwards = True

        else:
            backwards = False

        if printer is not None:
            full_frontier = frontier_f.elements + frontier_b.elements
            full_reached = set(reached_f.keys()).union(set(reached_b.keys()))
            current = frontier_b.top() if backwards else frontier_f.top()
            printer(it, problem, full_frontier, full_reached, current, solution)

        if backwards:
            solution = proceed(False, problem, frontier_b, reached_b, reached_f, solution)
            
        else:
            solution = proceed(True, problem, frontier_f, reached_f, reached_b, solution)
            


    if printer is not None:
        full_frontier = frontier_f.elements + frontier_b.elements
        full_reached = set(reached_f.keys()).union(set(reached_b.keys()))
        printer(it, problem, full_frontier, full_reached, None, solution)


    print('frontier_f', frontier_f)
    print('frontier_b', frontier_b)
    print('reached_f', reached_f.keys())
    print('reached_b', reached_b.keys())
    print('solution', solution)



    return solution



def breadth_first_search(problem, max_steps=100, printer=None):

    n = Node(problem.initial)
    frontier = list()
    reached = set()
    solution = None
    
    if printer is not None:
        printer(0, problem, frontier, reached, None, solution)

    reached.add(n.state)
    frontier.append(n)
    
    if printer is not None:
        printer(1, problem, frontier, reached, None, solution)

    n_steps = 0
    while len(frontier) > 0 and n_steps < max_steps:

        n = frontier.pop(0)
        for child in expand(problem, n):

            if problem.is_goal(child.state):

                solution = Solution.create(child)

                if printer is not None:
                    printer(2 + n_steps, problem, frontier, reached, n, solution)

                return solution
            
            if child.state not in reached:
                reached.add(child.state)
                frontier.append(child)

        if printer is not None:
            printer(2 + n_steps, problem, frontier, reached, n, solution)

        n_steps += 1

    return None



def depth_first_search(problem, max_steps=100, graph=False, printer=None, depth_limit=None, init_steps=0):

    depth = lambda n : 0 if n.parent is None else 1 + depth(n.parent)

    n = Node(problem.initial)
    frontier = list()
    reached = set()
    solution = 'failure'
    
    print("GO!\n")
    
    if printer is not None:
        printer(init_steps, problem, frontier, reached, None, solution)

    reached.add(n.state)
    frontier.append(n)
    
    if printer is not None:
        printer(init_steps + 1, problem, frontier, reached, None, solution)

    n_steps = init_steps + 2

    while len(frontier) > 0 and n_steps < max_steps:

        n = frontier.pop()
        if depth_limit is not None and depth(n) > depth_limit:
            solution = f'cutoff-{n_steps}'

        else:
            children = expand(problem, n)
            children.reverse()

            for child in children:
                if problem.is_goal(child.state):
                    solution = Solution.create(child)
                    if printer is not None:
                        print("frontier",  ", ".join(str(n) for n in frontier))
                        print("reached", reached)
                        print("n", n)
                        print("--------------------------------------------------")
                        print()
                        printer(n_steps, problem, frontier, reached, n, solution)
                        

                    return solution

                if not graph or (child.state not in reached):
                    frontier.append(child)

                reached.add(child.state)

            if printer is not None:
                print("frontier",  ", ".join(str(n) for n in frontier))
                print("reached", reached)
                print("n", n)
                print("--------------------------------------------------")
                print()

                printer(n_steps, problem, frontier, reached, n, solution)

        n_steps += 1

    return solution
            


def iterative_deepening_search(problem, max_steps=100, graph=True, printer=None):

    done = False
    depth = 0
    n_steps = 0
    while not done:

        res = depth_first_search(problem,
                                 max_steps=max_steps,
                                 graph=graph,
                                 printer=printer,
                                 depth_limit=depth,
                                 init_steps=n_steps)

        if not isinstance(res, str) or res == 'failure':
            done = True
        else:
            n_steps = int(res.partition('-')[-1])
            depth +=1



        
if __name__ == '__main__':
    import exercises
    from printers import pyplot_printer
    from utils import Problem
    
    f_cost = lambda x : (x.path_cost, x.state)

    problem = exercises.grid2
    pos = exercises.GRIDPOS

    interactive_printer = lambda i, p, f, r, c, s: pyplot_printer(i, p, f, r, c, s, pos=pos, interactive=True)
    #best_first_search(problem, f_cost, printer=interactive_printer, max_steps=100)
    #breadth_first_search(problem, printer=interactive_printer, max_steps=100)
    #depth_first_search(problem, printer=interactive_printer, max_steps=100)
    iterative_deepening_search(problem, printer=interactive_printer, max_steps=100)
    #bidirectional_path_cost_search(problem, printer=interactive_printer, max_steps=100)
